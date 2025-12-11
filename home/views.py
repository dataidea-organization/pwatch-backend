from rest_framework import viewsets, filters
from rest_framework.pagination import PageNumberPagination
from django_filters.rest_framework import DjangoFilterBackend
from .models import HeroImage
from .serializers import HeroImageSerializer


class HeroImageViewSet(viewsets.ModelViewSet):
    """
    ViewSet for Hero Images
    
    Provides list, retrieve, create, update, and destroy actions
    Filters by is_active
    """
    queryset = HeroImage.objects.filter(is_active=True).order_by('order', 'created_at')
    serializer_class = HeroImageSerializer
    filter_backends = [DjangoFilterBackend, filters.OrderingFilter]
    filterset_fields = ['is_active']
    ordering_fields = ['order', 'created_at']
    ordering = ['order', 'created_at']
    http_method_names = ['get', 'head', 'options']  # Read-only for public
