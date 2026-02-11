from rest_framework import viewsets, filters
from rest_framework.pagination import PageNumberPagination
from rest_framework.views import APIView
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from django_filters.rest_framework import DjangoFilterBackend
from django.views.decorators.cache import cache_page
from django.utils.decorators import method_decorator
from django.core.cache import cache
from .models import Explainers, Report, PartnerPublication, Statement, Publication
from .serializers import (
    ExplainersSerializer, ReportSerializer, PartnerPublicationSerializer, StatementSerializer,
    PublicationSerializer,
    HomeSummaryExplainerSerializer, HomeSummaryReportSerializer,
    HomeSummaryPartnerPublicationSerializer, HomeSummaryStatementSerializer
)


class ResourcePagination(PageNumberPagination):
    page_size = 15
    page_size_query_param = 'page_size'
    max_page_size = 100


class ExplainersViewSet(viewsets.ModelViewSet):
    """
    ViewSet for Explainers

    Provides educational explainer documents
    """
    queryset = Explainers.objects.all()
    serializer_class = ExplainersSerializer
    pagination_class = ResourcePagination
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    search_fields = ['name', 'description']
    ordering_fields = ['created_at', 'name']
    ordering = ['-created_at']


class ReportViewSet(viewsets.ModelViewSet):
    """
    ViewSet for Reports & Briefs

    Provides reports and brief documents
    """
    queryset = Report.objects.all()
    serializer_class = ReportSerializer
    pagination_class = ResourcePagination
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    search_fields = ['name', 'description']
    ordering_fields = ['created_at', 'name']
    ordering = ['-created_at']


class PartnerPublicationViewSet(viewsets.ModelViewSet):
    """
    ViewSet for Partner Publications

    Provides partner publication documents
    """
    queryset = PartnerPublication.objects.all()
    serializer_class = PartnerPublicationSerializer
    pagination_class = ResourcePagination
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    search_fields = ['name', 'description']
    ordering_fields = ['created_at', 'name']
    ordering = ['-created_at']


class StatementViewSet(viewsets.ModelViewSet):
    """
    ViewSet for Statements

    Provides official statement documents
    """
    queryset = Statement.objects.all()
    serializer_class = StatementSerializer
    pagination_class = ResourcePagination
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    search_fields = ['name', 'description']
    ordering_fields = ['created_at', 'name']
    ordering = ['-created_at']


class PublicationViewSet(viewsets.ModelViewSet):
    """
    ViewSet for Publications

    Provides research publications, policy briefs, and reports
    """
    queryset = Publication.objects.all()
    serializer_class = PublicationSerializer
    pagination_class = ResourcePagination
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    search_fields = ['title', 'description', 'category']
    ordering_fields = ['created_at', 'date', 'title']
    ordering = ['-created_at']
    filterset_fields = ['type', 'category', 'featured']


# Home page resources summary endpoint - optimized and cached
class HomeResourcesSummaryView(APIView):
    """
    Optimized endpoint for home page resources summary.
    Returns latest 5 items from each resource type in a single response.
    Cached for 10 minutes to improve performance.
    """
    permission_classes = [AllowAny]

    @method_decorator(cache_page(600))  # Cache for 10 minutes
    def get(self, request):
        cache_key = 'home_resources_summary'
        cached_data = cache.get(cache_key)
        
        if cached_data is not None:
            return Response(cached_data)
        
        # Fetch latest 5 items from each resource type with optimized queries
        # Using only() to fetch only needed fields
        explainers = Explainers.objects.only('id', 'name', 'file').order_by('-created_at')[:5]
        reports = Report.objects.only('id', 'name', 'file').order_by('-created_at')[:5]
        partner_publications = PartnerPublication.objects.only('id', 'name', 'file').order_by('-created_at')[:5]
        statements = Statement.objects.only('id', 'name', 'file').order_by('-created_at')[:5]
        
        # Serialize data
        data = {
            'explainers': HomeSummaryExplainerSerializer(explainers, many=True).data,
            'reports': HomeSummaryReportSerializer(reports, many=True).data,
            'partner_publications': HomeSummaryPartnerPublicationSerializer(partner_publications, many=True).data,
            'statements': HomeSummaryStatementSerializer(statements, many=True).data,
        }
        
        # Cache the response
        cache.set(cache_key, data, 600)  # Cache for 10 minutes
        
        return Response(data)