from rest_framework import viewsets, filters
from rest_framework.pagination import PageNumberPagination
from django_filters.rest_framework import DjangoFilterBackend
from .models import XSpace
from .serializers import XSpaceSerializer


class XSpacePagination(PageNumberPagination):
    page_size = 12
    page_size_query_param = 'page_size'
    max_page_size = 100


class XSpaceViewSet(viewsets.ModelViewSet):
    """
    ViewSet for X Spaces events
    
    Provides list, retrieve, create, update, and destroy actions
    Filters by status and scheduled_date
    Search by title, description, host, and topics
    """
    queryset = XSpace.objects.all()
    serializer_class = XSpaceSerializer
    pagination_class = XSpacePagination
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_fields = ['status']
    search_fields = ['title', 'description', 'host', 'topics', 'speakers']
    ordering_fields = ['scheduled_date', 'created_at', 'title']
    ordering = ['-scheduled_date', '-created_at']
