from django.contrib import admin
from .models import XSpace


@admin.register(XSpace)
class XSpaceAdmin(admin.ModelAdmin):
    list_display = ['title', 'host', 'scheduled_date', 'status', 'created_at']
    list_filter = ['status', 'scheduled_date']
    search_fields = ['title', 'description', 'host', 'topics', 'speakers']
    date_hierarchy = 'scheduled_date'
    ordering = ['-scheduled_date', '-created_at']
    
    fieldsets = (
        ('Basic Information', {
            'fields': ('title', 'description', 'host', 'status')
        }),
        ('Schedule', {
            'fields': ('scheduled_date', 'duration')
        }),
        ('Links', {
            'fields': ('x_space_url', 'recording_url')
        }),
        ('Media', {
            'fields': ('thumbnail',)
        }),
        ('Details', {
            'fields': ('topics', 'speakers')
        }),
    )

