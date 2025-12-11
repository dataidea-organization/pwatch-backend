from rest_framework import serializers
from .models import ContactSubmission


class ContactSubmissionSerializer(serializers.ModelSerializer):
    """Serializer for contact form submissions"""

    class Meta:
        model = ContactSubmission
        fields = [
            'id',
            'name',
            'email',
            'subject',
            'message',
            'created_at',
        ]
        read_only_fields = ['id', 'created_at']

    def validate_email(self, value):
        """Validate email format"""
        if not value or '@' not in value:
            raise serializers.ValidationError("Please provide a valid email address")
        return value.lower()

    def validate_message(self, value):
        """Validate message length"""
        if len(value.strip()) < 10:
            raise serializers.ValidationError("Message must be at least 10 characters long")
        return value.strip()