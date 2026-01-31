from django.core.exceptions import ObjectDoesNotExist
from rest_framework import serializers
from main.utils import get_full_media_url
from .models import XSpace, Podcast, Gallery, Poll, PollOption, PollVote, XPollEmbed


class XSpaceSerializer(serializers.ModelSerializer):
    status_display = serializers.CharField(source='get_status_display', read_only=True)
    thumbnail = serializers.SerializerMethodField()

    class Meta:
        model = XSpace
        fields = [
            'id',
            'title',
            'description',
            'host',
            'scheduled_date',
            'duration',
            'x_space_url',
            'recording_url',
            'thumbnail',
            'status',
            'status_display',
            'topics',
            'speakers',
            'created_at',
            'updated_at',
        ]

    def get_thumbnail(self, obj):
        if obj.thumbnail:
            return get_full_media_url(obj.thumbnail.url)
        return None


class PodcastSerializer(serializers.ModelSerializer):
    thumbnail = serializers.SerializerMethodField()

    class Meta:
        model = Podcast
        fields = [
            'id',
            'title',
            'description',
            'host',
            'guest',
            'youtube_url',
            'thumbnail',
            'duration',
            'published_date',
            'episode_number',
            'category',
            'tags',
            'created_at',
            'updated_at',
        ]

    def get_thumbnail(self, obj):
        if obj.thumbnail:
            return get_full_media_url(obj.thumbnail.url)
        return None


class GallerySerializer(serializers.ModelSerializer):
    image = serializers.SerializerMethodField()

    class Meta:
        model = Gallery
        fields = [
            'id',
            'title',
            'description',
            'image',
            'category',
            'event_date',
            'photographer',
            'tags',
            'featured',
            'created_at',
            'updated_at',
        ]

    def get_image(self, obj):
        if obj.image:
            return get_full_media_url(obj.image.url)
        return None


class PollOptionSerializer(serializers.ModelSerializer):
    vote_count = serializers.IntegerField(read_only=True)
    vote_percentage = serializers.FloatField(read_only=True)

    class Meta:
        model = PollOption
        fields = [
            'id',
            'text',
            'order',
            'vote_count',
            'vote_percentage',
            'created_at',
        ]


class PollSerializer(serializers.ModelSerializer):
    options = PollOptionSerializer(many=True, read_only=True)
    total_votes = serializers.IntegerField(read_only=True)
    is_active = serializers.BooleanField(read_only=True)
    status_display = serializers.CharField(source='get_status_display', read_only=True)
    is_x_poll = serializers.SerializerMethodField()
    x_poll_url = serializers.SerializerMethodField()
    x_poll_embed_html = serializers.SerializerMethodField()

    class Meta:
        model = Poll
        fields = [
            'id',
            'title',
            'description',
            'category',
            'status',
            'status_display',
            'start_date',
            'end_date',
            'allow_multiple_votes',
            'show_results_before_voting',
            'featured',
            'is_x_poll',
            'x_poll_url',
            'x_poll_embed_html',
            'options',
            'total_votes',
            'is_active',
            'created_at',
            'updated_at',
        ]

    def _get_x_poll_link(self, obj):
        """Return XPoll for this poll or None. Safe when no XPoll exists (reverse OneToOne raises)."""
        try:
            return obj.x_poll_link
        except ObjectDoesNotExist:
            return None

    def get_is_x_poll(self, obj):
        return self._get_x_poll_link(obj) is not None

    def get_x_poll_url(self, obj):
        link = self._get_x_poll_link(obj)
        return link.x_poll_url if link else None

    def get_x_poll_embed_html(self, obj):
        link = self._get_x_poll_link(obj)
        if link and link.embed_html:
            return link.embed_html
        return None


class PollVoteSerializer(serializers.ModelSerializer):
    class Meta:
        model = PollVote
        fields = [
            'id',
            'poll',
            'option',
            'created_at',
        ]
        read_only_fields = ['created_at']


class XPollEmbedSerializer(serializers.ModelSerializer):
    class Meta:
        model = XPollEmbed
        fields = ['id', 'title', 'embed_html', 'order', 'created_at', 'updated_at']

