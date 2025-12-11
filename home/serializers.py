from rest_framework import serializers
from .models import HeroImage


class HeroImageSerializer(serializers.ModelSerializer):
    class Meta:
        model = HeroImage
        fields = [
            'id',
            'title',
            'image',
            'order',
            'is_active',
            'alt_text',
            'created_at',
            'updated_at',
        ]
        read_only_fields = ['created_at', 'updated_at']

