from rest_framework import serializers
from .models import XSpace, Podcast, Gallery, Poll, PollOption, PollVote


class XSpaceSerializer(serializers.ModelSerializer):
    status_display = serializers.CharField(source='get_status_display', read_only=True)

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


class PodcastSerializer(serializers.ModelSerializer):
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


class GallerySerializer(serializers.ModelSerializer):
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
            'options',
            'total_votes',
            'is_active',
            'created_at',
            'updated_at',
        ]


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

