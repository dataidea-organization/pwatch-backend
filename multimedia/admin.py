from django.contrib import admin
from django.utils.html import mark_safe
from .models import XSpace, Podcast, Gallery, Poll, PollOption, PollVote, XPollEmbed, Trivia, TriviaQuestion, TriviaOption


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
    list_display = ['title', 'category', 'status', 'total_votes_display', 'voting_open_display', 'featured', 'created_at']
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

    def voting_open_display(self, obj):
        """Whether voting is open right now (considers status and start/end dates)."""
        if obj.is_active:
            return mark_safe('<span style="color: green;">Yes</span>')
        return mark_safe('<span style="color: red;">No</span>')
    voting_open_display.short_description = 'Voting open'


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


@admin.register(XPollEmbed)
class XPollEmbedAdmin(admin.ModelAdmin):
    list_display = ['id', 'title', 'order', 'created_at']
    list_editable = ['order']
    search_fields = ['title', 'embed_html']
    ordering = ['order', '-created_at']
    fields = ('title', 'embed_html', 'order')


class TriviaOptionInline(admin.TabularInline):
    model = TriviaOption
    extra = 2
    ordering = ['order']
    fields = ['order', 'text', 'is_correct']


class TriviaQuestionInline(admin.TabularInline):
    model = TriviaQuestion
    extra = 1
    ordering = ['order']
    fields = ['order', 'question_text', 'answer_text']


@admin.register(Trivia)
class TriviaAdmin(admin.ModelAdmin):
    list_display = ['title', 'order', 'is_active', 'question_count_display', 'created_at']
    list_filter = ['is_active', 'created_at']
    search_fields = ['title', 'description']
    list_editable = ['order', 'is_active']
    ordering = ['order', '-created_at']
    inlines = [TriviaQuestionInline]
    fieldsets = (
        ('Basic Information', {
            'fields': ('title', 'description', 'image')
        }),
        ('Display', {
            'fields': ('order', 'is_active')
        }),
    )

    def question_count_display(self, obj):
        return obj.questions.count()
    question_count_display.short_description = 'Questions'


@admin.register(TriviaQuestion)
class TriviaQuestionAdmin(admin.ModelAdmin):
    list_display = ['trivia', 'order', 'question_preview', 'option_count', 'created_at']
    list_filter = ['trivia', 'created_at']
    search_fields = ['question_text', 'answer_text', 'trivia__title']
    ordering = ['trivia', 'order']
    inlines = [TriviaOptionInline]

    def question_preview(self, obj):
        return obj.question_text[:60] + ('...' if len(obj.question_text) > 60 else '')
    question_preview.short_description = 'Question'

    def option_count(self, obj):
        return obj.options.count()
    option_count.short_description = 'Options'


@admin.register(TriviaOption)
class TriviaOptionAdmin(admin.ModelAdmin):
    list_display = ['question', 'text_preview', 'is_correct', 'order', 'created_at']
    list_filter = ['is_correct', 'question__trivia', 'created_at']
    search_fields = ['text', 'question__question_text', 'question__trivia__title']
    ordering = ['question', 'order']
    list_editable = ['is_correct', 'order']

    def text_preview(self, obj):
        return obj.text[:50] + ('...' if len(obj.text) > 50 else '')
    text_preview.short_description = 'Option'

