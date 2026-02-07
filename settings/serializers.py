from rest_framework import serializers
from .models import PageHeroImage, CitizensVoiceFeedbackLinks, FooterDocuments
from main.utils import get_full_media_url


class CitizensVoiceFeedbackLinksSerializer(serializers.ModelSerializer):
    class Meta:
        model = CitizensVoiceFeedbackLinks
        fields = ['ask_mp_form_url', 'comment_bill_form_url', 'feedback_law_form_url']


class PageHeroImageSerializer(serializers.ModelSerializer):
    image = serializers.SerializerMethodField()

    class Meta:
        model = PageHeroImage
        fields = ['id', 'page_slug', 'page_name', 'image', 'alt_text', 'is_active', 'created_at', 'updated_at']

    def get_image(self, obj):
        if obj.image:
            return get_full_media_url(obj.image.url)
        return None


class FooterDocumentsSerializer(serializers.ModelSerializer):
    terms_of_service = serializers.SerializerMethodField()
    privacy_policy = serializers.SerializerMethodField()
    accessibility = serializers.SerializerMethodField()

    class Meta:
        model = FooterDocuments
        fields = ['terms_of_service', 'privacy_policy', 'accessibility', 'updated_at']
        read_only_fields = ['updated_at']

    def get_terms_of_service(self, obj):
        if obj.terms_of_service:
            return get_full_media_url(obj.terms_of_service.url)
        return None

    def get_privacy_policy(self, obj):
        if obj.privacy_policy:
            return get_full_media_url(obj.privacy_policy.url)
        return None

    def get_accessibility(self, obj):
        if obj.accessibility:
            return get_full_media_url(obj.accessibility.url)
        return None
