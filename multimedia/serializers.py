from rest_framework import serializers
from .models import XSpace


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

