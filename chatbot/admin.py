from django.contrib import admin
from .models import Document


@admin.register(Document)
class DocumentAdmin(admin.ModelAdmin):
    list_display = ['name', 'file', 'file_type', 'created_at']
    list_filter = ['created_at']
    search_fields = ['name', 'description']
    readonly_fields = ['created_at', 'updated_at', 'file_type']
    
    fieldsets = (
        ('Document Information', {
            'fields': ('name', 'file', 'description')
        }),
        ('Metadata', {
            'fields': ('file_type', 'created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )
