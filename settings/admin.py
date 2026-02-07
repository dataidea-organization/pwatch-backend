from django.contrib import admin
from django.utils.html import format_html
from .models import PageHeroImage, CitizensVoiceFeedbackLinks, FooterDocuments


@admin.register(CitizensVoiceFeedbackLinks)
class CitizensVoiceFeedbackLinksAdmin(admin.ModelAdmin):
    list_display = ['__str__', 'updated_at']
    readonly_fields = ['updated_at']

    def has_add_permission(self, request):
        # Allow only one instance (singleton)
        return not CitizensVoiceFeedbackLinks.objects.exists()

    def has_delete_permission(self, request, obj=None):
        return False


@admin.register(FooterDocuments)
class FooterDocumentsAdmin(admin.ModelAdmin):
    list_display = ['__str__', 'has_terms_of_service', 'has_privacy_policy', 'has_accessibility', 'updated_at']
    readonly_fields = ['updated_at', 'file_preview_terms', 'file_preview_privacy', 'file_preview_accessibility']

    fieldsets = (
        ('Terms of Service', {
            'fields': ('terms_of_service', 'file_preview_terms')
        }),
        ('Privacy Policy', {
            'fields': ('privacy_policy', 'file_preview_privacy')
        }),
        ('Accessibility', {
            'fields': ('accessibility', 'file_preview_accessibility')
        }),
        ('Timestamps', {
            'fields': ('updated_at',),
            'classes': ('collapse',)
        }),
    )

    def has_add_permission(self, request):
        # Allow only one instance (singleton)
        return not FooterDocuments.objects.exists()

    def has_delete_permission(self, request, obj=None):
        return False

    def has_terms_of_service(self, obj):
        return "Yes" if obj.terms_of_service else "No"
    has_terms_of_service.short_description = 'Terms of Service'

    def has_privacy_policy(self, obj):
        return "Yes" if obj.privacy_policy else "No"
    has_privacy_policy.short_description = 'Privacy Policy'

    def has_accessibility(self, obj):
        return "Yes" if obj.accessibility else "No"
    has_accessibility.short_description = 'Accessibility'

    def file_preview_terms(self, obj):
        if obj.terms_of_service:
            return format_html(
                '<a href="{}" target="_blank">View Terms of Service Document</a>',
                obj.terms_of_service.url
            )
        return "No file uploaded"
    file_preview_terms.short_description = 'Current Terms of Service'

    def file_preview_privacy(self, obj):
        if obj.privacy_policy:
            return format_html(
                '<a href="{}" target="_blank">View Privacy Policy Document</a>',
                obj.privacy_policy.url
            )
        return "No file uploaded"
    file_preview_privacy.short_description = 'Current Privacy Policy'

    def file_preview_accessibility(self, obj):
        if obj.accessibility:
            return format_html(
                '<a href="{}" target="_blank">View Accessibility Document</a>',
                obj.accessibility.url
            )
        return "No file uploaded"
    file_preview_accessibility.short_description = 'Current Accessibility'


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
