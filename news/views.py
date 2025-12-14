from rest_framework import viewsets, filters
from rest_framework.pagination import PageNumberPagination
from rest_framework.views import APIView
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from django_filters.rest_framework import DjangoFilterBackend
from django.views.decorators.cache import cache_page
from django.utils.decorators import method_decorator
from django.core.cache import cache
from .models import News
from .serializers import NewsListSerializer, NewsDetailSerializer, HomeNewsSummarySerializer


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
    search_fields = ['title', 'author__username', 'author__first_name', 'author__last_name', 'content']
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


# Home page news summary endpoint - optimized and cached
class HomeNewsSummaryView(APIView):
    """
    Optimized endpoint for home page news summary.
    Returns latest 3 published news articles in a single response.
    Cached for 10 minutes to improve performance.
    """
    permission_classes = [AllowAny]

    @method_decorator(cache_page(600))  # Cache for 10 minutes
    def get(self, request):
        cache_key = 'home_news_summary'
        cached_data = cache.get(cache_key)
        
        if cached_data is not None:
            return Response(cached_data)
        
        # Fetch latest 3 published news articles with optimized query
        # Using only() to fetch only needed fields
        news_articles = News.objects.filter(
            status='published'
        ).select_related('author').only(
            'id', 'title', 'slug', 'author', 'category', 'image', 'published_date'
        ).order_by('-published_date', '-created_at')[:3]
        
        # Serialize data
        data = {
            'results': HomeNewsSummarySerializer(news_articles, many=True).data
        }
        
        # Cache the response
        cache.set(cache_key, data, 600)  # Cache for 10 minutes
        
        return Response(data)