from django.contrib import admin
from django.utils.html import format_html
from .models import PageHeroImage


@admin.register(PageHeroImage)
class PageHeroImageAdmin(admin.ModelAdmin):
    list_display = ['page_name', 'page_slug', 'image_preview', 'is_active', 'updated_at']
    list_filter = ['is_active', 'page_slug']
    search_fields = ['page_slug', 'page_name', 'alt_text']
    ordering = ['page_slug']
    list_editable = ['is_active']
    readonly_fields = ['image_preview_large', 'created_at', 'updated_at']

    fieldsets = (
        ('Page Information', {
            'fields': ('page_slug', 'page_name')
        }),
        ('Image', {
            'fields': ('image', 'image_preview_large', 'alt_text')
        }),
        ('Settings', {
            'fields': ('is_active',)
        }),
        ('Timestamps', {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )

    def image_preview(self, obj):
        if obj.image:
            return format_html(
                '<img src="{}" style="max-height: 50px; max-width: 100px; object-fit: cover;" />',
                obj.image.url
            )
        return "-"
    image_preview.short_description = 'Preview'

    def image_preview_large(self, obj):
        if obj.image:
            return format_html(
                '<img src="{}" style="max-height: 200px; max-width: 400px; object-fit: cover;" />',
                obj.image.url
            )
        return "No image uploaded"
    image_preview_large.short_description = 'Current Image'
