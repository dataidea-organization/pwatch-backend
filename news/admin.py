from django.contrib import admin
from .models import News, NewsComment, HotInParliament


@admin.register(News)
class NewsAdmin(admin.ModelAdmin):
    list_display = ['title', 'author', 'category', 'status', 'published_date']
    list_filter = ['status', 'category', 'published_date', 'author']
    search_fields = ['title', 'author__username', 'author__first_name', 'author__last_name', 'content']
    prepopulated_fields = {'slug': ('title',)}
    date_hierarchy = 'published_date'
    ordering = ['-published_date']

    fieldsets = (
        ('Content', {
            'fields': ('title', 'slug', 'author', 'category', 'content')
        }),
        ('Media', {
            'fields': ('image',)
        }),
        ('Publication', {
            'fields': ('status', 'published_date')
        }),
    )


@admin.register(NewsComment)
class NewsCommentAdmin(admin.ModelAdmin):
    list_display = ['author_name', 'news', 'created_at', 'is_approved']
    list_filter = ['is_approved', 'created_at']
    search_fields = ['author_name', 'author_email', 'body']
    list_editable = ['is_approved']
    raw_id_fields = ['news']


@admin.register(HotInParliament)
class HotInParliamentAdmin(admin.ModelAdmin):
    list_display = ['title', 'author', 'is_active', 'order', 'published_date']
    list_filter = ['is_active', 'published_date', 'author']
    search_fields = ['title', 'author__username', 'author__first_name', 'author__last_name', 'content']
    prepopulated_fields = {'slug': ('title',)}
    date_hierarchy = 'published_date'
    ordering = ['order', '-published_date']
    list_editable = ['is_active', 'order']

    fieldsets = (
        ('Content', {
            'fields': ('title', 'slug', 'author', 'content')
        }),
        ('Media', {
            'fields': ('image',)
        }),
        ('Settings', {
            'fields': ('is_active', 'order', 'link_url', 'published_date')
        }),
    )