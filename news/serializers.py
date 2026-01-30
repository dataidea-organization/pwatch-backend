from rest_framework import serializers
from main.utils import get_full_media_url, process_content_images
from .models import News, NewsComment, HotInParliament, HotInParliamentComment


class NewsCommentSerializer(serializers.ModelSerializer):
    """Serializer for news comments (list/read)."""
    class Meta:
        model = NewsComment
        fields = ['id', 'author_name', 'body', 'created_at']
        read_only_fields = ['id', 'created_at']


class NewsCommentCreateSerializer(serializers.ModelSerializer):
    """Serializer for creating a news comment. No auth required."""
    class Meta:
        model = NewsComment
        fields = ['news', 'author_name', 'author_email', 'body']

    def create(self, validated_data):
        return NewsComment.objects.create(**validated_data)


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
    content = serializers.SerializerMethodField()

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
            'view_count',
            'created_at',
            'updated_at',
        ]
        read_only_fields = ['slug', 'view_count', 'created_at', 'updated_at']

    def get_author(self, obj):
        if obj.author:
            return obj.author.get_full_name() or obj.author.username
        return 'Unknown'

    def get_image(self, obj):
        if obj.image:
            return get_full_media_url(obj.image.url)
        return None
    
    def get_content(self, obj):
        """Process content HTML to convert relative image URLs to absolute URLs"""
        if obj.content:
            return process_content_images(obj.content)
        return obj.content


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


class HotInParliamentCommentSerializer(serializers.ModelSerializer):
    """Serializer for Hot in Parliament comments (list/read)."""
    class Meta:
        model = HotInParliamentComment
        fields = ['id', 'author_name', 'body', 'created_at']
        read_only_fields = ['id', 'created_at']


class HotInParliamentCommentCreateSerializer(serializers.ModelSerializer):
    """Serializer for creating a Hot in Parliament comment. No auth required."""
    class Meta:
        model = HotInParliamentComment
        fields = ['hot_item', 'author_name', 'author_email', 'body']

    def create(self, validated_data):
        return HotInParliamentComment.objects.create(**validated_data)


class HotInParliamentSerializer(serializers.ModelSerializer):
    """Serializer for Hot in Parliament items"""
    author = serializers.SerializerMethodField()
    image = serializers.SerializerMethodField()
    content = serializers.SerializerMethodField()

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
            'view_count',
        ]

    def get_author(self, obj):
        if obj.author:
            return obj.author.get_full_name() or obj.author.username
        return 'Unknown'

    def get_image(self, obj):
        if obj.image:
            return get_full_media_url(obj.image.url)
        return None
    
    def get_content(self, obj):
        """Process content HTML to convert relative image URLs to absolute URLs"""
        if obj.content:
            return process_content_images(obj.content)
        return obj.content