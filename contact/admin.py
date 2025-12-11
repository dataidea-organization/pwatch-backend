from django.contrib import admin
from .models import ContactSubmission


@admin.register(ContactSubmission)
class ContactSubmissionAdmin(admin.ModelAdmin):
    list_display = ['name', 'email', 'subject', 'status', 'created_at']
    list_filter = ['status', 'created_at']
    search_fields = ['name', 'email', 'subject', 'message']
    readonly_fields = ['ip_address', 'user_agent', 'created_at', 'updated_at']
    ordering = ['-created_at']
    date_hierarchy = 'created_at'

    fieldsets = (
        ('Contact Information', {
            'fields': ('name', 'email', 'subject', 'message')
        }),
        ('Status', {
            'fields': ('status',)
        }),
        ('Metadata', {
            'fields': ('ip_address', 'user_agent', 'created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )

    def has_add_permission(self, request):
        """Disable adding submissions through admin (only via API)"""
        return False