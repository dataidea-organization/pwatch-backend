from rest_framework import serializers
from .models import ContactSubmission, DonationSubmission, Feedback


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


class DonationSubmissionSerializer(serializers.ModelSerializer):
    """Serializer for donation form submissions"""

    class Meta:
        model = DonationSubmission
        fields = [
            'id',
            'name',
            'email',
            'country',
            'address',
            'donation_method',
            'message',
            'created_at',
        ]
        read_only_fields = ['id', 'created_at']

    def validate_email(self, value):
        """Validate email format"""
        if not value or '@' not in value:
            raise serializers.ValidationError("Please provide a valid email address")
        return value.lower()


class FeedbackSerializer(serializers.ModelSerializer):
    """Serializer for feedback submissions"""

    class Meta:
        model = Feedback
        fields = [
            'id',
            'name',
            'email',
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