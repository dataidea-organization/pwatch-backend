from django.contrib import admin
from django.utils.html import mark_safe
from .models import XSpace, Podcast, Gallery, Poll, PollOption, PollVote, XPoll


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


@admin.register(Podcast)
class PodcastAdmin(admin.ModelAdmin):
    list_display = ['title', 'host', 'guest', 'published_date', 'episode_number']
    list_filter = ['category', 'published_date']
    search_fields = ['title', 'description', 'host', 'guest', 'tags']
    date_hierarchy = 'published_date'
    ordering = ['-published_date', '-created_at']
    
    fieldsets = (
        ('Basic Information', {
            'fields': ('title', 'description', 'host', 'guest')
        }),
        ('Episode Details', {
            'fields': ('episode_number', 'published_date', 'duration')
        }),
        ('YouTube', {
            'fields': ('youtube_url', 'thumbnail')
        }),
        ('Categorization', {
            'fields': ('category', 'tags')
        }),
    )


@admin.register(Gallery)
class GalleryAdmin(admin.ModelAdmin):
    list_display = ['title', 'category', 'event_date', 'photographer', 'featured', 'created_at']
    list_filter = ['category', 'featured', 'event_date']
    search_fields = ['title', 'description', 'photographer', 'tags']
    date_hierarchy = 'event_date'
    ordering = ['-featured', '-event_date', '-created_at']
    list_editable = ['featured']
    
    fieldsets = (
        ('Basic Information', {
            'fields': ('title', 'description', 'image')
        }),
        ('Details', {
            'fields': ('category', 'event_date', 'photographer')
        }),
        ('Organization', {
            'fields': ('tags', 'featured')
        }),
    )


class PollOptionInline(admin.TabularInline):
    model = PollOption
    extra = 2
    ordering = ['order']


@admin.register(Poll)
class PollAdmin(admin.ModelAdmin):
    list_display = ['title', 'category', 'status', 'total_votes_display', 'is_active_display', 'featured', 'created_at']
    list_filter = ['status', 'category', 'featured', 'created_at']
    search_fields = ['title', 'description', 'category']
    date_hierarchy = 'created_at'
    ordering = ['-featured', '-created_at']
    list_editable = ['featured', 'status']
    inlines = [PollOptionInline]
    
    fieldsets = (
        ('Basic Information', {
            'fields': ('title', 'description', 'category')
        }),
        ('Settings', {
            'fields': ('status', 'start_date', 'end_date', 'featured')
        }),
        ('Voting Options', {
            'fields': ('allow_multiple_votes', 'show_results_before_voting')
        }),
    )

    def total_votes_display(self, obj):
        return obj.total_votes
    total_votes_display.short_description = 'Total Votes'

    def is_active_display(self, obj):
        if obj.is_active:
            return mark_safe('<span style="color: green;">●</span> Active')
        return mark_safe('<span style="color: red;">●</span> Inactive')
    is_active_display.short_description = 'Status'


@admin.register(PollOption)
class PollOptionAdmin(admin.ModelAdmin):
    list_display = ['text', 'poll', 'order', 'vote_count_display', 'vote_percentage_display']
    list_filter = ['poll', 'created_at']
    search_fields = ['text', 'poll__title']
    ordering = ['poll', 'order']

    def vote_count_display(self, obj):
        return obj.vote_count
    vote_count_display.short_description = 'Votes'

    def vote_percentage_display(self, obj):
        return f"{obj.vote_percentage}%"
    vote_percentage_display.short_description = 'Percentage'


@admin.register(PollVote)
class PollVoteAdmin(admin.ModelAdmin):
    list_display = ['poll', 'option', 'ip_address', 'created_at']
    list_filter = ['poll', 'created_at']
    search_fields = ['poll__title', 'option__text', 'ip_address']
    date_hierarchy = 'created_at'
    ordering = ['-created_at']
    readonly_fields = ['created_at']


@admin.register(XPoll)
class XPollAdmin(admin.ModelAdmin):
    list_display = ['poll', 'x_poll_url', 'created_at']
    list_filter = ['created_at']
    search_fields = ['poll__title', 'x_poll_url']
    raw_id_fields = ['poll']
    readonly_fields = ['created_at', 'updated_at']

