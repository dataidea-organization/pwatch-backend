from rest_framework import serializers
from .models import Blog


class BlogListSerializer(serializers.ModelSerializer):
    """Simplified serializer for blog list view"""
    category_display = serializers.CharField(read_only=True)
    author = serializers.SerializerMethodField()

    class Meta:
        model = Blog
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


class BlogDetailSerializer(serializers.ModelSerializer):
    """Full serializer for blog detail view"""
    category_display = serializers.CharField(read_only=True)
    author = serializers.SerializerMethodField()

    class Meta:
        model = Blog
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


class HomeBlogSummarySerializer(serializers.ModelSerializer):
    """Minimal serializer for home page blog summary"""
    category_display = serializers.CharField(read_only=True)
    author = serializers.SerializerMethodField()
    
    class Meta:
        model = Blog
        fields = ['id', 'title', 'slug', 'author', 'category', 'category_display', 'image', 'published_date']

    def get_author(self, obj):
        if obj.author:
            return obj.author.get_full_name() or obj.author.username
        return 'Unknown'

