from django.contrib import admin
from .models import News


@admin.register(News)
class NewsAdmin(admin.ModelAdmin):
    list_display = ['title', 'author', 'category', 'status', 'published_date']
    list_filter = ['status', 'category', 'published_date']
    search_fields = ['title', 'author', 'content', 'excerpt']
    prepopulated_fields = {'slug': ('title',)}
    date_hierarchy = 'published_date'
    ordering = ['-published_date']

    fieldsets = (
        ('Content', {
            'fields': ('title', 'slug', 'author', 'category', 'excerpt', 'content')
        }),
        ('Media', {
            'fields': ('image',)
        }),
        ('Publication', {
            'fields': ('status', 'published_date')
        }),
    )