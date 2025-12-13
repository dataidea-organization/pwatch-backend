from django.contrib import admin
from .models import HeroImage, Headline

admin.site.site_header = "Parliament Watch Uganda"
admin.site.site_title = "Parliament Watch Uganda Admin"
admin.site.index_title = "Welcome to Parliament Watch Uganda Admin Panel"


@admin.register(HeroImage)
class HeroImageAdmin(admin.ModelAdmin):
    list_display = ['title', 'order', 'is_active', 'created_at']
    list_filter = ['is_active', 'created_at']
    search_fields = ['title', 'alt_text']
    ordering = ['order', 'created_at']
    list_editable = ['order', 'is_active']
    
    fieldsets = (
        ('Image Information', {
            'fields': ('title', 'image', 'alt_text')
        }),
        ('Display Settings', {
            'fields': ('order', 'is_active')
        }),
    )


@admin.register(Headline)
class HeadlineAdmin(admin.ModelAdmin):
    list_display = ['text_preview', 'is_bold', 'order', 'is_active', 'created_at']
    list_filter = ['is_active', 'is_bold', 'created_at']
    search_fields = ['text']
    ordering = ['order', 'created_at']
    list_editable = ['order', 'is_active', 'is_bold']
    
    fieldsets = (
        ('Headline Information', {
            'fields': ('text', 'is_bold')
        }),
        ('Display Settings', {
            'fields': ('order', 'is_active')
        }),
    )

    def text_preview(self, obj):
        return obj.text[:60] + ('...' if len(obj.text) > 60 else '')
    text_preview.short_description = 'Text'

