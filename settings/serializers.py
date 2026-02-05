from rest_framework import serializers
from .models import PageHeroImage, CitizensVoiceFeedbackLinks
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
