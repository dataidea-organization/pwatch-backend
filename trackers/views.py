from rest_framework import viewsets, filters
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.pagination import PageNumberPagination
from django_filters.rest_framework import DjangoFilterBackend
from .models import Bill, BillReading, MP
from .serializers import BillSerializer, BillListSerializer, BillReadingSerializer, MPListSerializer, MPDetailSerializer


class BillViewSet(viewsets.ModelViewSet):
    """
    ViewSet for viewing and editing bills.
    """
    queryset = Bill.objects.all()
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_fields = ['bill_type', 'status', 'year_introduced']
    search_fields = ['title', 'mover', 'assigned_to']
    ordering_fields = ['created_at', 'year_introduced', 'title']
    ordering = ['-created_at']

    def get_serializer_class(self):
        if self.action == 'list':
            return BillListSerializer
        return BillSerializer

    @action(detail=True, methods=['post'])
    def like(self, request, pk=None):
        """Increment the like count for a bill"""
        bill = self.get_object()
        bill.likes += 1
        bill.save()
        return Response({'likes': bill.likes})

    @action(detail=True, methods=['post'])
    def comment(self, request, pk=None):
        """Increment the comment count for a bill"""
        bill = self.get_object()
        bill.comments += 1
        bill.save()
        return Response({'comments': bill.comments})

    @action(detail=True, methods=['post'])
    def share(self, request, pk=None):
        """Increment the share count for a bill"""
        bill = self.get_object()
        bill.shares += 1
        bill.save()
        return Response({'shares': bill.shares})


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
    ordering_fields = ['name', 'last_name', 'district', 'created_at']
    ordering = ['last_name', 'first_name']

    def get_serializer_class(self):
        """Use different serializers for list and detail views"""
        if self.action == 'list':
            return MPListSerializer
        return MPDetailSerializer