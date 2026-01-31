from rest_framework import viewsets, status
from rest_framework.response import Response
from rest_framework.decorators import action
from django.shortcuts import get_object_or_404
from .models import PageHeroImage
from .serializers import PageHeroImageSerializer


class PageHeroImageViewSet(viewsets.ReadOnlyModelViewSet):
    """
    ViewSet for Page Hero Images
    
    Provides list and retrieve actions.
    Use /api/settings/page-hero-images/{page_slug}/ to get hero image for a specific page.
    """
    queryset = PageHeroImage.objects.filter(is_active=True)
    serializer_class = PageHeroImageSerializer
    lookup_field = 'page_slug'
    
    def retrieve(self, request, page_slug=None):
        """
        Get the hero image for a specific page by its slug.
        Returns 404 if no active hero image exists for the page.
        """
        try:
            hero_image = PageHeroImage.objects.get(page_slug=page_slug, is_active=True)
            serializer = self.get_serializer(hero_image)
            return Response(serializer.data)
        except PageHeroImage.DoesNotExist:
            return Response(
                {"detail": "No hero image found for this page."},
                status=status.HTTP_404_NOT_FOUND
            )
