from rest_framework import serializers
from main.utils import get_full_media_url
from .models import News, HotInParliament


class NewsListSerializer(serializers.ModelSerializer):
    """Simplified serializer for news list view"""
    category_display = serializers.CharField(read_only=True)
    author = serializers.SerializerMethodField()
    image = serializers.SerializerMethodField()

    class Meta:
        model = News
        fields = [
            'id',
            'title',
            'slug',
            'author',
            'category',
            'category_display',
            'image',
            'published_date',
        ]

    def get_author(self, obj):
        if obj.author:
            return obj.author.get_full_name() or obj.author.username
        return 'Unknown'

    def get_image(self, obj):
        if obj.image:
            return get_full_media_url(obj.image.url)
        return None


class NewsDetailSerializer(serializers.ModelSerializer):
    """Full serializer for news detail view"""
    category_display = serializers.CharField(read_only=True)
    author = serializers.SerializerMethodField()
    image = serializers.SerializerMethodField()

    class Meta:
        model = News
        fields = [
            'id',
            'title',
            'slug',
            'author',
            'category',
            'category_display',
            'content',
            'image',
            'status',
            'published_date',
            'created_at',
            'updated_at',
        ]
        read_only_fields = ['slug', 'created_at', 'updated_at']

    def get_author(self, obj):
        if obj.author:
            return obj.author.get_full_name() or obj.author.username
        return 'Unknown'

    def get_image(self, obj):
        if obj.image:
            return get_full_media_url(obj.image.url)
        return None


class HomeNewsSummarySerializer(serializers.ModelSerializer):
    """Minimal serializer for home page news summary"""
    category_display = serializers.CharField(read_only=True)
    author = serializers.SerializerMethodField()
    image = serializers.SerializerMethodField()
    
    class Meta:
        model = News
        fields = ['id', 'title', 'slug', 'author', 'category', 'category_display', 'image', 'published_date']

    def get_author(self, obj):
        if obj.author:
            return obj.author.get_full_name() or obj.author.username
        return 'Unknown'

    def get_image(self, obj):
        if obj.image:
            return get_full_media_url(obj.image.url)
        return None


class HotInParliamentSerializer(serializers.ModelSerializer):
    """Serializer for Hot in Parliament items"""
    author = serializers.SerializerMethodField()
    image = serializers.SerializerMethodField()

    class Meta:
        model = HotInParliament
        fields = [
            'id',
            'title',
            'slug',
            'author',
            'content',
            'image',
            'link_url',
            'published_date',
        ]

    def get_author(self, obj):
        if obj.author:
            return obj.author.get_full_name() or obj.author.username
        return 'Unknown'

    def get_image(self, obj):
        if obj.image:
            return get_full_media_url(obj.image.url)
        return None