from rest_framework import viewsets, filters
from rest_framework.pagination import PageNumberPagination
from django_filters.rest_framework import DjangoFilterBackend
from .models import News
from .serializers import NewsListSerializer, NewsDetailSerializer


class NewsPagination(PageNumberPagination):
    page_size = 12
    page_size_query_param = 'page_size'
    max_page_size = 100


class NewsViewSet(viewsets.ModelViewSet):
    """
    ViewSet for News model

    Provides list, retrieve, create, update, and destroy actions
    Filters by category and status
    Search by title, author, and content
    """
    queryset = News.objects.all().order_by('-published_date')
    pagination_class = NewsPagination
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_fields = ['category', 'status', 'author']
    search_fields = ['title', 'author', 'content', 'excerpt']
    ordering_fields = ['published_date', 'created_at', 'title']
    lookup_field = 'slug'

    def get_serializer_class(self):
        """Use different serializers for list and detail views"""
        if self.action == 'list':
            return NewsListSerializer
        return NewsDetailSerializer

    def get_queryset(self):
        """
        Filter to show only published news in list view for non-admin users
        """
        queryset = super().get_queryset()

        # If retrieving a single item, return all statuses
        if self.action == 'retrieve':
            return queryset

        # For list view, only show published news unless user is staff
        if not self.request.user.is_staff:
            queryset = queryset.filter(status='published')

        return queryset