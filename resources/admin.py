from django.contrib import admin
from .models import Explainers, Report, PartnerPublication, Statement, Publication


@admin.register(Explainers)
class ExplainersAdmin(admin.ModelAdmin):
    list_display = ['name', 'description', 'file', 'created_at']
    search_fields = ['name', 'description']
    ordering = ['-created_at']

    fieldsets = (
        ('Explainer Information', {
            'fields': ('name', 'description', 'file')
        }),
    )


@admin.register(Report)
class ReportAdmin(admin.ModelAdmin):
    list_display = ['name', 'date_received', 'file', 'created_at']
    search_fields = ['name', 'description']
    list_filter = ['date_received', 'created_at']
    ordering = ['-date_received', '-created_at']
    date_hierarchy = 'date_received'

    fieldsets = (
        ('Report Information', {
            'fields': ('name', 'description', 'file', 'date_received')
        }),
    )


@admin.register(PartnerPublication)
class PartnerPublicationAdmin(admin.ModelAdmin):
    list_display = ['name', 'date_received', 'file', 'created_at']
    search_fields = ['name', 'description']
    list_filter = ['date_received', 'created_at']
    ordering = ['-date_received', '-created_at']
    date_hierarchy = 'date_received'

    fieldsets = (
        ('Partner Publication Information', {
            'fields': ('name', 'description', 'file', 'date_received')
        }),
    )


@admin.register(Statement)
class StatementAdmin(admin.ModelAdmin):
    list_display = ['name', 'date_received', 'file', 'created_at']
    search_fields = ['name', 'description']
    list_filter = ['date_received', 'created_at']
    ordering = ['-date_received', '-created_at']
    date_hierarchy = 'date_received'

    fieldsets = (
        ('Statement Information', {
            'fields': ('name', 'description', 'file', 'date_received')
        }),
    )


@admin.register(Publication)
class PublicationAdmin(admin.ModelAdmin):
    list_display = ['title', 'type', 'category', 'date', 'featured', 'created_at']
    search_fields = ['title', 'description', 'category']
    list_filter = ['type', 'category', 'featured', 'created_at']
    ordering = ['-created_at']
    date_hierarchy = 'date'

    fieldsets = (
        ('Publication Information', {
            'fields': ('title', 'type', 'date', 'description', 'category', 'url', 'pdf', 'image', 'featured')
        }),
    )