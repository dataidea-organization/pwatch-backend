from rest_framework import viewsets, filters
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.pagination import PageNumberPagination
from rest_framework.views import APIView
from rest_framework.permissions import AllowAny
from django_filters.rest_framework import DjangoFilterBackend
from django.db.models import Count, Q
from django.views.decorators.cache import cache_page
from django.utils.decorators import method_decorator
from django.core.cache import cache
from .models import Bill, BillReading, MP, DebtData, Loan, Hansard, Budget, OrderPaper, Committee, CommitteeDocument
from .serializers import (
    BillSerializer, BillListSerializer, BillReadingSerializer, MPListSerializer, MPDetailSerializer,
    DebtDataSerializer, LoanSerializer, LoanDetailSerializer, HansardSerializer, BudgetSerializer, OrderPaperSerializer,
    CommitteeListSerializer, CommitteeDetailSerializer,
    HomeSummaryMPSerializer, HomeSummaryBillSerializer, HomeSummaryLoanSerializer,
    HomeSummaryBudgetSerializer, HomeSummaryHansardSerializer, HomeSummaryOrderPaperSerializer
)


class BillViewSet(viewsets.ModelViewSet):
    """
    ViewSet for viewing and editing bills.
    """
    queryset = Bill.objects.all()
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_fields = ['bill_type', 'status', 'year_introduced']
    search_fields = ['title', 'mover', 'assigned_to']
    ordering_fields = ['created_at', 'year_introduced', 'title', 'bill_type', 'status', 'mover']
    ordering = ['-created_at']

    def get_serializer_class(self):
        if self.action == 'list':
            return BillListSerializer
        return BillSerializer

    @action(detail=False, methods=['get'])
    def summary(self, request):
        """Get summary statistics for bills by status"""
        queryset = self.get_queryset()
        
        # Count bills by status
        status_counts = queryset.values('status').annotate(count=Count('id'))
        
        # Create a dictionary with all statuses, defaulting to 0
        summary = {
            '1st_reading': 0,
            '2nd_reading': 0,
            '3rd_reading': 0,
            'passed': 0,
            'assented': 0,
            'withdrawn': 0,  # Not in model, but included for frontend
        }
        
        # Update with actual counts
        for item in status_counts:
            status = item['status']
            if status in summary:
                summary[status] = item['count']
        
        # Also include total count
        summary['total'] = queryset.count()
        
        return Response(summary)


class BillReadingViewSet(viewsets.ModelViewSet):
    """
    ViewSet for viewing and editing bill readings.
    """
    queryset = BillReading.objects.all()
    serializer_class = BillReadingSerializer
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['bill', 'stage']


class MPPagination(PageNumberPagination):
    page_size = 20
    page_size_query_param = 'page_size'
    max_page_size = 100


class MPViewSet(viewsets.ModelViewSet):
    """
    ViewSet for Members of Parliament

    Provides list, retrieve, create, update, and destroy actions
    Filters by party, district, and constituency
    Search by name, constituency, and district
    """
    queryset = MP.objects.all()
    pagination_class = MPPagination
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_fields = ['party', 'district', 'constituency']
    search_fields = ['name', 'first_name', 'last_name', 'constituency', 'district']
    ordering_fields = ['name', 'last_name', 'first_name', 'party', 'district', 'constituency', 'created_at']
    ordering = ['last_name', 'first_name']

    def get_queryset(self):
        """Support multi-select party/district filters via comma-separated values."""
        qs = super().get_queryset()
        party_param = self.request.query_params.get('party')
        district_param = self.request.query_params.get('district')

        if party_param:
            parties = [p.strip() for p in party_param.split(',') if p.strip()]
            if parties:
                # Use case-insensitive matching for parties
                party_q = Q()
                for party in parties:
                    party_q |= Q(party__iexact=party)
                qs = qs.filter(party_q)

        if district_param:
            districts = [d.strip() for d in district_param.split(',') if d.strip()]
            if districts:
                # Use case-insensitive matching for districts
                district_q = Q()
                for district in districts:
                    district_q |= Q(district__iexact=district)
                qs = qs.filter(district_q)

        return qs

    def get_serializer_class(self):
        """Use different serializers for list and detail views"""
        if self.action == 'list':
            return MPListSerializer
        return MPDetailSerializer

    @action(detail=False, methods=['get'])
    def summary(self, request):
        """Get summary statistics for MPs"""
        queryset = self.filter_queryset(self.get_queryset())

        total_mps = queryset.count()
        total_parties = queryset.values('party').distinct().count()
        total_districts = queryset.values('district').distinct().count()

        # Get party distribution
        parties = queryset.values('party').annotate(
            count=Count('id')
        ).order_by('-count')

        # Calculate percentages
        party_distribution = []
        for item in parties:
            party_distribution.append({
                'party': item['party'],
                'count': item['count'],
                'percentage': round((item['count'] / total_mps * 100), 1) if total_mps > 0 else 0
            })

        return Response({
            'total_mps': total_mps,
            'total_parties': total_parties,
            'total_districts': total_districts,
            'party_distribution': party_distribution
        })


class DebtDataViewSet(viewsets.ModelViewSet):
    """
    ViewSet for National Debt and Economic Data

    Provides historical debt and economic metrics
    """
    queryset = DebtData.objects.all().order_by('year')
    serializer_class = DebtDataSerializer
    filter_backends = [DjangoFilterBackend, filters.OrderingFilter]
    filterset_fields = ['year']
    ordering_fields = ['year']
    ordering = ['year']

    @action(detail=False, methods=['get'])
    def latest(self, request):
        """Get the latest debt data"""
        latest_data = DebtData.objects.order_by('-year').first()
        if latest_data:
            serializer = self.get_serializer(latest_data)
            return Response(serializer.data)
        return Response({})


class LoanPagination(PageNumberPagination):
    page_size = 10
    page_size_query_param = 'page_size'
    max_page_size = 100


class LoanViewSet(viewsets.ModelViewSet):
    """
    ViewSet for Government Loans

    Provides loan data with filtering by sector and source
    """
    queryset = Loan.objects.all().select_related('lender').prefetch_related('documents')
    serializer_class = LoanSerializer
    pagination_class = LoanPagination

    def get_serializer_class(self):
        if self.action == 'retrieve':
            return LoanDetailSerializer
        return LoanSerializer
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_fields = ['sector', 'currency', 'source']
    search_fields = ['label', 'description', 'sector']
    ordering_fields = ['approved_amount', 'approval_date', 'created_at']
    ordering = ['-approval_date', '-created_at']

    @action(detail=False, methods=['get'])
    def sources_summary(self, request):
        """Get loan sources summary for pie chart"""
        # Use the same filtering as the main queryset to respect search/filters
        queryset = self.filter_queryset(self.get_queryset())
        
        sources = queryset.values('source').annotate(
            count=Count('id')
        ).order_by('-count')

        # Calculate percentages
        total = sum(item['count'] for item in sources)
        summary = []
        for item in sources:
            source_obj = queryset.filter(source=item['source']).first()
            summary.append({
                'source': item['source'],
                'name': source_obj.get_source_display() if source_obj else item['source'],
                'count': item['count'],
                'percentage': round((item['count'] / total * 100), 1) if total > 0 else 0
            })

        return Response(summary)


class HansardPagination(PageNumberPagination):
    page_size = 15
    page_size_query_param = 'page_size'
    max_page_size = 100


class HansardViewSet(viewsets.ModelViewSet):
    """
    ViewSet for Hansards

    Provides parliamentary hansard records with file downloads
    """
    queryset = Hansard.objects.all()
    serializer_class = HansardSerializer
    pagination_class = HansardPagination
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_fields = ['date']
    search_fields = ['name']
    ordering_fields = ['date', 'created_at', 'name']
    ordering = ['-date', '-created_at']


class BudgetPagination(PageNumberPagination):
    page_size = 15
    page_size_query_param = 'page_size'
    max_page_size = 100


class BudgetViewSet(viewsets.ModelViewSet):
    """
    ViewSet for Budgets

    Provides national budget documents with file downloads
    Note: Filtering and searching are handled client-side
    """
    queryset = Budget.objects.all()
    serializer_class = BudgetSerializer
    pagination_class = BudgetPagination
    ordering_fields = ['financial_year', 'created_at', 'name']
    ordering = ['-financial_year', '-created_at']


class OrderPaperPagination(PageNumberPagination):
    page_size = 15
    page_size_query_param = 'page_size'
    max_page_size = 100


class OrderPaperViewSet(viewsets.ModelViewSet):
    """
    ViewSet for Order Papers

    Provides parliamentary order papers with file downloads
    """
    queryset = OrderPaper.objects.all()
    serializer_class = OrderPaperSerializer
    pagination_class = OrderPaperPagination
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    search_fields = ['name', 'description']
    ordering_fields = ['created_at', 'name']
    ordering = ['-created_at']


class CommitteePagination(PageNumberPagination):
    page_size = 20
    page_size_query_param = 'page_size'
    max_page_size = 100


class CommitteeViewSet(viewsets.ModelViewSet):
    """
    ViewSet for Parliamentary Committees

    Provides committee information including chairperson, deputy, members, and documents
    """
    queryset = Committee.objects.select_related('chairperson', 'deputy_chairperson').prefetch_related('members', 'documents')
    pagination_class = CommitteePagination
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    search_fields = ['title', 'description', 'chairperson__name', 'deputy_chairperson__name']
    ordering_fields = ['title', 'created_at']
    ordering = ['title']

    def get_serializer_class(self):
        """Use different serializers for list and detail views"""
        if self.action == 'list':
            return CommitteeListSerializer
        return CommitteeDetailSerializer


# Home page summary endpoint - optimized and cached
class HomeSummaryView(APIView):
    """
    Optimized endpoint for home page trackers summary.
    Returns latest 5 items from each tracker in a single response.
    Cached for 10 minutes to improve performance.
    """
    permission_classes = [AllowAny]

    @method_decorator(cache_page(600))  # Cache for 10 minutes
    def get(self, request):
        cache_key = 'home_trackers_summary'
        cached_data = cache.get(cache_key)
        
        if cached_data is not None:
            return Response(cached_data)
        
        # Fetch latest 5 items from each tracker with optimized queries
        # Using only() to fetch only needed fields
        mps = MP.objects.only('id', 'name', 'party', 'constituency').order_by('-created_at')[:5]
        bills = Bill.objects.only('id', 'title').order_by('-created_at')[:5]
        loans = Loan.objects.only('id', 'label', 'sector', 'source').order_by('-created_at')[:5]
        budgets = Budget.objects.only('id', 'name', 'financial_year', 'file').order_by('-created_at')[:5]
        hansards = Hansard.objects.only('id', 'name', 'date', 'file').order_by('-created_at')[:5]
        order_papers = OrderPaper.objects.only('id', 'name', 'file').order_by('-created_at')[:5]
        
        # Serialize data
        data = {
            'mps': HomeSummaryMPSerializer(mps, many=True).data,
            'bills': HomeSummaryBillSerializer(bills, many=True).data,
            'loans': HomeSummaryLoanSerializer(loans, many=True).data,
            'budgets': HomeSummaryBudgetSerializer(budgets, many=True).data,
            'hansards': HomeSummaryHansardSerializer(hansards, many=True).data,
            'order_papers': HomeSummaryOrderPaperSerializer(order_papers, many=True).data,
        }
        
        # Cache the response
        cache.set(cache_key, data, 600)  # Cache for 10 minutes
        
        return Response(data)