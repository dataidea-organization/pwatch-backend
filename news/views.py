from rest_framework import viewsets, filters
from rest_framework.pagination import PageNumberPagination
from rest_framework.views import APIView
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework import status
from django.db.models import F
from django_filters.rest_framework import DjangoFilterBackend
from django.views.decorators.cache import cache_page
from django.utils.decorators import method_decorator
from django.core.cache import cache
from django.db.models import F
from .models import News, NewsComment, HotInParliament, HotInParliamentComment
from .serializers import (
    NewsListSerializer,
    NewsDetailSerializer,
    HomeNewsSummarySerializer,
    HotInParliamentSerializer,
    NewsCommentSerializer,
    NewsCommentCreateSerializer,
    HotInParliamentCommentSerializer,
    HotInParliamentCommentCreateSerializer,
)


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

    def retrieve(self, request, *args, **kwargs):
        instance = self.get_object()
        News.objects.filter(pk=instance.pk).update(view_count=F('view_count') + 1)
        instance.refresh_from_db()
        serializer = self.get_serializer(instance)
        return Response(serializer.data)


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


# Hot in Parliament endpoint - optimized and cached
class HotInParliamentView(APIView):
    """
    Optimized endpoint for Hot in Parliament items.
    Returns active items ordered by order and published_date.
    Cached for 10 minutes to improve performance.
    Use ?nocache=1 to bypass cache for debugging.
    """
    permission_classes = [AllowAny]

    def get(self, request):
        # Allow bypassing cache with ?nocache=1 parameter
        bypass_cache = request.query_params.get('nocache') == '1'
        
        if not bypass_cache:
            cache_key = 'hot_in_parliament'
            cached_data = cache.get(cache_key)
            
            if cached_data is not None:
                return Response(cached_data)
        
        # Fetch active hot in parliament items with optimized query
        hot_items = HotInParliament.objects.filter(
            is_active=True
        ).select_related('author').only(
            'id', 'title', 'slug', 'author', 'content', 'image', 'link_url', 'published_date', 'view_count'
        ).order_by('order', '-published_date', '-created_at')
        
        # Serialize data
        data = {
            'results': HotInParliamentSerializer(hot_items, many=True).data
        }
        
        # Cache the response (unless bypassing)
        if not bypass_cache:
            cache.set(cache_key, data, 600)  # Cache for 10 minutes
        
        return Response(data)


# Hot in Parliament detail endpoint - increments view_count
class HotInParliamentDetailView(APIView):
    """
    Endpoint to retrieve a single Hot in Parliament item by slug.
    Increments view_count on each request.
    """
    permission_classes = [AllowAny]

    def get(self, request, slug):
        try:
            hot_item = HotInParliament.objects.get(slug=slug)
            HotInParliament.objects.filter(pk=hot_item.pk).update(view_count=F('view_count') + 1)
            hot_item.refresh_from_db()
            serializer = HotInParliamentSerializer(hot_item)
            return Response(serializer.data)
        except HotInParliament.DoesNotExist:
            return Response(
                {'error': 'Hot in Parliament item not found'},
                status=404
            )


# Hot in Parliament comments - no login required
class HotInParliamentCommentListCreateView(APIView):
    """
    List comments for a Latest in Parliament item (GET) or create a comment (POST).
    No authentication required.
    """
    permission_classes = [AllowAny]

    def get(self, request, slug):
        try:
            hot_item = HotInParliament.objects.get(slug=slug)
        except HotInParliament.DoesNotExist:
            return Response({'error': 'Item not found'}, status=status.HTTP_404_NOT_FOUND)
        comments = HotInParliamentComment.objects.filter(hot_item=hot_item, is_approved=True).order_by('-created_at')
        serializer = HotInParliamentCommentSerializer(comments, many=True)
        return Response(serializer.data)

    def post(self, request, slug):
        try:
            hot_item = HotInParliament.objects.get(slug=slug)
        except HotInParliament.DoesNotExist:
            return Response({'error': 'Item not found'}, status=status.HTTP_404_NOT_FOUND)
        data = {**request.data, 'hot_item': hot_item.id}
        serializer = HotInParliamentCommentCreateSerializer(data=data)
        if serializer.is_valid():
            serializer.save()
            output = HotInParliamentCommentSerializer(serializer.instance)
            return Response(output.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


# News comments - no login required
class NewsCommentListCreateView(APIView):
    """
    List comments for a news article (GET) or create a comment (POST).
    No authentication required.
    """
    permission_classes = [AllowAny]

    def get(self, request, slug):
        try:
            news = News.objects.get(slug=slug)
        except News.DoesNotExist:
            return Response({'error': 'News article not found'}, status=status.HTTP_404_NOT_FOUND)
        comments = NewsComment.objects.filter(news=news, is_approved=True).order_by('-created_at')
        serializer = NewsCommentSerializer(comments, many=True)
        return Response(serializer.data)

    def post(self, request, slug):
        try:
            news = News.objects.get(slug=slug)
        except News.DoesNotExist:
            return Response({'error': 'News article not found'}, status=status.HTTP_404_NOT_FOUND)
        data = {**request.data, 'news': news.id}
        serializer = NewsCommentCreateSerializer(data=data)
        if serializer.is_valid():
            serializer.save()
            # Return the comment in list format (no email)
            output = NewsCommentSerializer(serializer.instance)
            return Response(output.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)