from django.shortcuts import render
from django.http import HttpResponse
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import AllowAny
from django.core.cache import cache
from django.db.models import Q
from concurrent.futures import ThreadPoolExecutor, as_completed

# Import models
from news.models import News
from blog.models import Blog
from trackers.models import MP, Bill, Loan, Budget, Hansard, OrderPaper
from resources.models import Explainers, Report, PartnerPublication, Statement
from multimedia.models import Podcast, XSpace, Gallery, Poll

# Import serializers
from news.serializers import NewsListSerializer
from blog.serializers import BlogListSerializer
from trackers.serializers import (
    MPListSerializer, BillListSerializer, LoanSerializer,
    BudgetSerializer, HansardSerializer, OrderPaperSerializer
)
from resources.serializers import ExplainersSerializer, ReportSerializer, PartnerPublicationSerializer, StatementSerializer
from multimedia.serializers import PodcastSerializer, XSpaceSerializer, GallerySerializer, PollSerializer


def home(request):
    """
    Simple landing page for the backend root route
    """
    return render(request, 'main/home.html')


class GlobalSearchView(APIView):
    """
    Optimized global search endpoint that searches across all content types.
    Uses parallel queries, query optimization, and caching for sub-second performance.
    """
    permission_classes = [AllowAny]

    def get(self, request):
        query = request.query_params.get('q', '').strip()
        limit = int(request.query_params.get('limit', 5))  # Default 5 for dropdown, 20 for full page

        if not query:
            return Response({
                'query': '',
                'total_results': 0,
                'results': {},
                'counts': {}
            })

        # Check cache first
        cache_key = f'search:{query.lower()}:{limit}'
        cached_result = cache.get(cache_key)
        if cached_result:
            return Response(cached_result)

        # Perform parallel searches
        results = {}
        counts = {}
        
        with ThreadPoolExecutor(max_workers=10) as executor:
            # Submit all search tasks
            futures = {
                executor.submit(self._search_news, query, limit): 'news',
                executor.submit(self._search_blogs, query, limit): 'blogs',
                executor.submit(self._search_mps, query, limit): 'mps',
                executor.submit(self._search_bills, query, limit): 'bills',
                executor.submit(self._search_loans, query, limit): 'loans',
                executor.submit(self._search_budgets, query, limit): 'budgets',
                executor.submit(self._search_hansards, query, limit): 'hansards',
                executor.submit(self._search_order_papers, query, limit): 'order_papers',
                executor.submit(self._search_explainers, query, limit): 'explainers',
                executor.submit(self._search_reports, query, limit): 'reports',
                executor.submit(self._search_partner_publications, query, limit): 'partner_publications',
                executor.submit(self._search_statements, query, limit): 'statements',
                executor.submit(self._search_podcasts, query, limit): 'podcasts',
                executor.submit(self._search_xspaces, query, limit): 'xspaces',
                executor.submit(self._search_gallery, query, limit): 'gallery',
                executor.submit(self._search_polls, query, limit): 'polls',
            }

            # Collect results as they complete
            for future in as_completed(futures):
                category = futures[future]
                try:
                    category_results, category_count = future.result()
                    results[category] = category_results
                    counts[category] = category_count
                except Exception as e:
                    # Log error but don't fail entire search
                    print(f"Error searching {category}: {e}")
                    results[category] = []
                    counts[category] = 0

        # Calculate total results
        total_results = sum(counts.values())

        # Prepare response
        response_data = {
            'query': query,
            'total_results': total_results,
            'results': results,
            'counts': counts
        }

        # Cache for 10 minutes
        cache.set(cache_key, response_data, 600)

        return Response(response_data)

    def _search_news(self, query, limit):
        """Search news articles"""
        q = Q(title__icontains=query) | Q(author__icontains=query) | Q(excerpt__icontains=query) | Q(content__icontains=query)
        queryset = News.objects.filter(q, status='published').only(
            'id', 'title', 'slug', 'author', 'category', 'excerpt', 'image', 'published_date'
        ).order_by('-published_date')[:limit]
        
        serializer = NewsListSerializer(queryset, many=True)
        count = News.objects.filter(q, status='published').count()
        return serializer.data, count

    def _search_blogs(self, query, limit):
        """Search blog posts"""
        q = Q(title__icontains=query) | Q(author__icontains=query) | Q(excerpt__icontains=query) | Q(content__icontains=query)
        queryset = Blog.objects.filter(q, status='published').only(
            'id', 'title', 'slug', 'author', 'category', 'excerpt', 'image', 'published_date'
        ).order_by('-published_date')[:limit]
        
        serializer = BlogListSerializer(queryset, many=True)
        count = Blog.objects.filter(q, status='published').count()
        return serializer.data, count

    def _search_mps(self, query, limit):
        """Search Members of Parliament"""
        q = Q(name__icontains=query) | Q(party__icontains=query) | Q(constituency__icontains=query) | Q(district__icontains=query)
        queryset = MP.objects.filter(q).only(
            'id', 'name', 'party', 'constituency', 'district', 'photo'
        ).order_by('name')[:limit]
        
        serializer = MPListSerializer(queryset, many=True)
        count = MP.objects.filter(q).count()
        return serializer.data, count

    def _search_bills(self, query, limit):
        """Search bills"""
        q = Q(title__icontains=query) | Q(mover__icontains=query) | Q(description__icontains=query)
        queryset = Bill.objects.filter(q).only(
            'id', 'title', 'bill_type', 'mover', 'status', 'year_introduced', 'created_at'
        ).order_by('-created_at')[:limit]
        
        serializer = BillListSerializer(queryset, many=True)
        count = Bill.objects.filter(q).count()
        return serializer.data, count

    def _search_loans(self, query, limit):
        """Search loans"""
        q = Q(label__icontains=query) | Q(description__icontains=query) | Q(source__icontains=query)
        queryset = Loan.objects.filter(q).only(
            'id', 'sector', 'label', 'approved_amount', 'currency', 'source', 'approval_date'
        ).order_by('-approval_date')[:limit]
        
        serializer = LoanSerializer(queryset, many=True)
        count = Loan.objects.filter(q).count()
        return serializer.data, count

    def _search_budgets(self, query, limit):
        """Search budgets"""
        q = Q(name__icontains=query) | Q(financial_year__icontains=query)
        queryset = Budget.objects.filter(q).only(
            'id', 'name', 'financial_year', 'file', 'created_at'
        ).order_by('-financial_year')[:limit]
        
        serializer = BudgetSerializer(queryset, many=True)
        count = Budget.objects.filter(q).count()
        return serializer.data, count

    def _search_hansards(self, query, limit):
        """Search hansards"""
        q = Q(name__icontains=query)
        queryset = Hansard.objects.filter(q).only(
            'id', 'name', 'date', 'file', 'created_at'
        ).order_by('-date')[:limit]
        
        serializer = HansardSerializer(queryset, many=True)
        count = Hansard.objects.filter(q).count()
        return serializer.data, count

    def _search_order_papers(self, query, limit):
        """Search order papers"""
        q = Q(name__icontains=query) | Q(description__icontains=query)
        queryset = OrderPaper.objects.filter(q).only(
            'id', 'name', 'description', 'file', 'created_at'
        ).order_by('-created_at')[:limit]
        
        serializer = OrderPaperSerializer(queryset, many=True)
        count = OrderPaper.objects.filter(q).count()
        return serializer.data, count

    def _search_explainers(self, query, limit):
        """Search explainers"""
        q = Q(name__icontains=query) | Q(description__icontains=query)
        queryset = Explainers.objects.filter(q).only(
            'id', 'name', 'description', 'file', 'created_at'
        ).order_by('-created_at')[:limit]
        
        serializer = ExplainersSerializer(queryset, many=True)
        count = Explainers.objects.filter(q).count()
        return serializer.data, count

    def _search_reports(self, query, limit):
        """Search reports"""
        q = Q(name__icontains=query) | Q(description__icontains=query)
        queryset = Report.objects.filter(q).only(
            'id', 'name', 'description', 'file', 'created_at'
        ).order_by('-created_at')[:limit]
        
        serializer = ReportSerializer(queryset, many=True)
        count = Report.objects.filter(q).count()
        return serializer.data, count

    def _search_partner_publications(self, query, limit):
        """Search partner publications"""
        q = Q(name__icontains=query) | Q(description__icontains=query)
        queryset = PartnerPublication.objects.filter(q).only(
            'id', 'name', 'description', 'file', 'created_at'
        ).order_by('-created_at')[:limit]
        
        serializer = PartnerPublicationSerializer(queryset, many=True)
        count = PartnerPublication.objects.filter(q).count()
        return serializer.data, count

    def _search_statements(self, query, limit):
        """Search statements"""
        q = Q(name__icontains=query) | Q(description__icontains=query)
        queryset = Statement.objects.filter(q).only(
            'id', 'name', 'description', 'file', 'created_at'
        ).order_by('-created_at')[:limit]
        
        serializer = StatementSerializer(queryset, many=True)
        count = Statement.objects.filter(q).count()
        return serializer.data, count

    def _search_podcasts(self, query, limit):
        """Search podcasts"""
        q = Q(title__icontains=query) | Q(host__icontains=query) | Q(description__icontains=query) | Q(guest__icontains=query) | Q(tags__icontains=query)
        queryset = Podcast.objects.filter(q).only(
            'id', 'title', 'host', 'guest', 'youtube_url', 'thumbnail', 'published_date', 'category'
        ).order_by('-published_date')[:limit]
        
        serializer = PodcastSerializer(queryset, many=True)
        count = Podcast.objects.filter(q).count()
        return serializer.data, count

    def _search_xspaces(self, query, limit):
        """Search X Spaces"""
        q = Q(title__icontains=query) | Q(host__icontains=query) | Q(description__icontains=query) | Q(topics__icontains=query) | Q(speakers__icontains=query)
        queryset = XSpace.objects.filter(q).only(
            'id', 'title', 'host', 'scheduled_date', 'x_space_url', 'thumbnail', 'status'
        ).order_by('-scheduled_date')[:limit]
        
        serializer = XSpaceSerializer(queryset, many=True)
        count = XSpace.objects.filter(q).count()
        return serializer.data, count

    def _search_gallery(self, query, limit):
        """Search gallery images"""
        q = Q(title__icontains=query) | Q(description__icontains=query) | Q(photographer__icontains=query) | Q(tags__icontains=query)
        queryset = Gallery.objects.filter(q).only(
            'id', 'title', 'description', 'image', 'category', 'event_date', 'photographer'
        ).order_by('-featured', '-event_date')[:limit]
        
        serializer = GallerySerializer(queryset, many=True)
        count = Gallery.objects.filter(q).count()
        return serializer.data, count

    def _search_polls(self, query, limit):
        """Search polls"""
        q = Q(title__icontains=query) | Q(description__icontains=query) | Q(category__icontains=query)
        queryset = Poll.objects.filter(q, status='active').only(
            'id', 'title', 'description', 'category', 'status', 'start_date', 'end_date', 'featured'
        ).order_by('-featured', '-created_at')[:limit]
        
        serializer = PollSerializer(queryset, many=True)
        count = Poll.objects.filter(q, status='active').count()
        return serializer.data, count


