from rest_framework import serializers
from .models import News


class NewsListSerializer(serializers.ModelSerializer):
    """Simplified serializer for news list view"""
    category_display = serializers.CharField(read_only=True)

    class Meta:
        model = News
        fields = [
            'id',
            'title',
            'slug',
            'author',
            'category',
            'category_display',
            'excerpt',
            'image',
            'published_date',
        ]


class NewsDetailSerializer(serializers.ModelSerializer):
    """Full serializer for news detail view"""
    category_display = serializers.CharField(read_only=True)

    class Meta:
        model = News
        fields = [
            'id',
            'title',
            'slug',
            'author',
            'category',
            'category_display',
            'excerpt',
            'content',
            'image',
            'status',
            'published_date',
            'created_at',
            'updated_at',
        ]
        read_only_fields = ['slug', 'created_at', 'updated_at']