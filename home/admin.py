from django.contrib import admin
from .models import HeroImage


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

