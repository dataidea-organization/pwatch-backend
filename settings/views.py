from rest_framework import viewsets, status
from rest_framework.response import Response
from rest_framework.views import APIView
from django.shortcuts import get_object_or_404
from .models import PageHeroImage, CitizensVoiceFeedbackLinks, FooterDocuments
from .serializers import PageHeroImageSerializer, CitizensVoiceFeedbackLinksSerializer, FooterDocumentsSerializer


class CitizensVoiceFeedbackLinksView(APIView):
    """
    GET /api/settings/citizens-voice-feedback/
    Returns the three Google form URLs for the Citizens Voice feedback cards.
    If no config exists, returns empty strings for each URL.
    """
    def get(self, request):
        instance = CitizensVoiceFeedbackLinks.objects.first()
        if not instance:
            return Response({
                'ask_mp_form_url': '',
                'comment_bill_form_url': '',
                'feedback_law_form_url': '',
            })
        serializer = CitizensVoiceFeedbackLinksSerializer(instance)
        return Response(serializer.data)


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


class FooterDocumentsView(APIView):
    """
    GET /api/settings/footer-documents/
    Returns the file URLs for Terms of Service, Privacy Policy, and Accessibility documents.
    If no config exists, returns null for each document URL.
    """
    def get(self, request):
        instance = FooterDocuments.objects.first()
        if not instance:
            return Response({
                'terms_of_service': None,
                'privacy_policy': None,
                'accessibility': None,
            })
        serializer = FooterDocumentsSerializer(instance)
        return Response(serializer.data)
