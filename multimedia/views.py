from rest_framework import viewsets, filters, status
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.pagination import PageNumberPagination
from django_filters.rest_framework import DjangoFilterBackend
from django.utils import timezone
from .models import XSpace, Podcast, Gallery, Poll, PollOption, PollVote, XPollEmbed
from .serializers import (
    XSpaceSerializer, PodcastSerializer, GallerySerializer,
    PollSerializer, PollOptionSerializer, PollVoteSerializer,
    XPollEmbedSerializer,
)


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


class PodcastPagination(PageNumberPagination):
    page_size = 12
    page_size_query_param = 'page_size'
    max_page_size = 100


class PodcastViewSet(viewsets.ModelViewSet):
    """
    ViewSet for Podcasts
    
    Provides list, retrieve, create, update, and destroy actions
    Filters by category
    Search by title, description, host, guest, and tags
    """
    queryset = Podcast.objects.all()
    serializer_class = PodcastSerializer
    pagination_class = PodcastPagination
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_fields = ['category']
    search_fields = ['title', 'description', 'host', 'guest', 'tags']
    ordering_fields = ['published_date', 'created_at', 'title']
    ordering = ['-published_date', '-created_at']


class GalleryPagination(PageNumberPagination):
    page_size = 20
    page_size_query_param = 'page_size'
    max_page_size = 100


class GalleryViewSet(viewsets.ModelViewSet):
    """
    ViewSet for Gallery Images
    
    Provides list, retrieve, create, update, and destroy actions
    Filters by category and featured status
    Search by title, description, photographer, and tags
    """
    queryset = Gallery.objects.all().order_by('-featured', '-event_date', '-created_at')
    serializer_class = GallerySerializer
    pagination_class = GalleryPagination
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_fields = ['category', 'featured']
    search_fields = ['title', 'description', 'photographer', 'tags']
    ordering_fields = ['event_date', 'created_at', 'title', 'featured']
    ordering = ['-featured', '-created_at']


class PollPagination(PageNumberPagination):
    page_size = 10
    page_size_query_param = 'page_size'
    max_page_size = 50


class PollViewSet(viewsets.ModelViewSet):
    """
    ViewSet for Polls
    
    Provides list, retrieve, create, update, and destroy actions
    Filters by status, category, and featured
    Search by title and description
    """
    queryset = Poll.objects.all().prefetch_related('x_poll_link').order_by('-featured', '-created_at')
    serializer_class = PollSerializer
    pagination_class = PollPagination
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_fields = ['status', 'category', 'featured']
    search_fields = ['title', 'description', 'category']
    ordering_fields = ['created_at', 'start_date', 'end_date', 'title']
    ordering = ['-featured', '-created_at']

    @action(detail=True, methods=['post'], url_path='vote')
    def vote(self, request, pk=None):
        """
        Submit a vote for a poll option
        """
        poll = self.get_object()
        
        # Check if poll is active
        if not poll.is_active:
            return Response(
                {'error': 'This poll is not currently active.'},
                status=status.HTTP_400_BAD_REQUEST
            )

        option_id = request.data.get('option_id')
        if not option_id:
            return Response(
                {'error': 'option_id is required.'},
                status=status.HTTP_400_BAD_REQUEST
            )

        try:
            option = PollOption.objects.get(id=option_id, poll=poll)
        except PollOption.DoesNotExist:
            return Response(
                {'error': 'Invalid option selected.'},
                status=status.HTTP_400_BAD_REQUEST
            )

        # Get IP address and session ID
        ip_address = self.get_client_ip(request)
        session_id = request.session.session_key or request.data.get('session_id', '')

        # Check for existing vote (if multiple votes not allowed)
        if not poll.allow_multiple_votes:
            existing_vote = PollVote.objects.filter(
                poll=poll,
                ip_address=ip_address,
                session_id=session_id
            ).first()

            if existing_vote:
                return Response(
                    {'error': 'You have already voted on this poll.'},
                    status=status.HTTP_400_BAD_REQUEST
                )

        # Create vote
        vote = PollVote.objects.create(
            poll=poll,
            option=option,
            ip_address=ip_address,
            session_id=session_id
        )

        serializer = PollVoteSerializer(vote)
        return Response(serializer.data, status=status.HTTP_201_CREATED)

    @action(detail=True, methods=['get'], url_path='results')
    def results(self, request, pk=None):
        """
        Get poll results with vote counts and percentages
        """
        poll = self.get_object()
        options = PollOption.objects.filter(poll=poll).order_by('order', 'created_at')
        
        results = []
        total_votes = poll.total_votes
        
        for option in options:
            vote_count = option.vote_count
            percentage = option.vote_percentage
            
            results.append({
                'option_id': option.id,
                'text': option.text,
                'vote_count': vote_count,
                'percentage': percentage,
            })

        return Response({
            'poll_id': poll.id,
            'poll_title': poll.title,
            'total_votes': total_votes,
            'results': results,
        })

    def get_client_ip(self, request):
        """Get client IP address from request"""
        x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
        if x_forwarded_for:
            ip = x_forwarded_for.split(',')[0]
        else:
            ip = request.META.get('REMOTE_ADDR')
        return ip


class XPollEmbedViewSet(viewsets.ReadOnlyModelViewSet):
    """List and retrieve X (Twitter) poll embeds. Standalone, not linked to Poll."""
    queryset = XPollEmbed.objects.all()
    serializer_class = XPollEmbedSerializer
    pagination_class = None
