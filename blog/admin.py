from django.contrib import admin
from .models import Blog, BlogComment


@admin.register(Blog)
class BlogAdmin(admin.ModelAdmin):
    list_display = ['title', 'author', 'category', 'status', 'published_date', 'created_at']
    list_filter = ['status', 'category', 'published_date', 'created_at', 'author']
    search_fields = ['title', 'author__username', 'author__first_name', 'author__last_name', 'content']
    prepopulated_fields = {'slug': ('title',)}
    readonly_fields = ['created_at', 'updated_at']
    date_hierarchy = 'published_date'
    ordering = ['-published_date', '-created_at']

    fieldsets = (
        ('Content', {
            'fields': ('title', 'slug', 'author', 'category', 'content', 'image')
        }),
        ('Publishing', {
            'fields': ('status', 'published_date')
        }),
        ('Metadata', {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )


@admin.register(BlogComment)
class BlogCommentAdmin(admin.ModelAdmin):
    list_display = ['author_name', 'blog', 'created_at', 'is_approved']
    list_filter = ['is_approved', 'created_at']
    search_fields = ['author_name', 'author_email', 'body']
    list_editable = ['is_approved']
    raw_id_fields = ['blog']
