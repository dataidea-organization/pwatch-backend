from django.contrib import admin
from .models import Objective, TeamMember, WhoWeAre, OurStory, WhatSetsUsApart, Partner


@admin.register(Objective)
class ObjectiveAdmin(admin.ModelAdmin):
    list_display = ['title', 'order', 'is_active', 'created_at']
    list_filter = ['is_active', 'created_at']
    search_fields = ['title', 'description']
    ordering = ['order', 'created_at']
    list_editable = ['order', 'is_active']
    
    fieldsets = (
        ('Basic Information', {
            'fields': ('title', 'description', 'icon')
        }),
        ('Display', {
            'fields': ('order', 'is_active')
        }),
    )


@admin.register(TeamMember)
class TeamMemberAdmin(admin.ModelAdmin):
    list_display = ['name', 'title', 'order', 'is_active', 'created_at']
    list_filter = ['is_active', 'created_at']
    search_fields = ['name', 'title', 'bio']
    ordering = ['order', 'name']
    list_editable = ['order', 'is_active']
    
    fieldsets = (
        ('Basic Information', {
            'fields': ('name', 'title', 'bio', 'photo')
        }),
        ('Contact Information', {
            'fields': ('email', 'phone')
        }),
        ('Social Media', {
            'fields': ('linkedin_url', 'twitter_url', 'facebook_url')
        }),
        ('Display', {
            'fields': ('order', 'is_active')
        }),
    )


@admin.register(WhoWeAre)
class WhoWeAreAdmin(admin.ModelAdmin):
    list_display = ['title', 'is_active', 'updated_at']
    list_filter = ['is_active', 'created_at', 'updated_at']
    search_fields = ['title', 'content']
    ordering = ['-updated_at']
    list_editable = ['is_active']
    
    fieldsets = (
        ('Content', {
            'fields': ('title', 'content', 'image', 'youtube_video_url')
        }),
        ('Display', {
            'fields': ('is_active',)
        }),
    )


@admin.register(OurStory)
class OurStoryAdmin(admin.ModelAdmin):
    list_display = ['title', 'is_active', 'updated_at']
    list_filter = ['is_active', 'created_at', 'updated_at']
    search_fields = ['title', 'content']
    ordering = ['-updated_at']
    list_editable = ['is_active']
    
    fieldsets = (
        ('Content', {
            'fields': ('title', 'content', 'image', 'youtube_video_url')
        }),
        ('Display', {
            'fields': ('is_active',)
        }),
    )


@admin.register(WhatSetsUsApart)
class WhatSetsUsApartAdmin(admin.ModelAdmin):
    list_display = ['title', 'order', 'is_active', 'created_at']
    list_filter = ['is_active', 'created_at']
    search_fields = ['title', 'description']
    ordering = ['order', 'created_at']
    list_editable = ['order', 'is_active']
    
    fieldsets = (
        ('Basic Information', {
            'fields': ('title', 'description', 'icon')
        }),
        ('Display', {
            'fields': ('order', 'is_active')
        }),
    )


@admin.register(Partner)
class PartnerAdmin(admin.ModelAdmin):
    list_display = ['name', 'order', 'is_active', 'created_at']
    list_filter = ['is_active', 'created_at']
    search_fields = ['name', 'description']
    ordering = ['order', 'name']
    list_editable = ['order', 'is_active']
    
    fieldsets = (
        ('Basic Information', {
            'fields': ('name', 'description', 'logo', 'website_url')
        }),
        ('Display', {
            'fields': ('order', 'is_active')
        }),
    )

