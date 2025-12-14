from rest_framework import serializers
from .models import Document


class DocumentSerializer(serializers.ModelSerializer):
    file_url = serializers.CharField(read_only=True)
    file_type = serializers.CharField(read_only=True)

    class Meta:
        model = Document
        fields = ['id', 'name', 'file', 'file_type', 'description', 'file_url', 'created_at']


class ChatbotQuerySerializer(serializers.Serializer):
    query = serializers.CharField(required=True, help_text="User's question")


class ChatbotResponseSerializer(serializers.Serializer):
    answer = serializers.CharField(help_text="AI-generated answer")
    document_name = serializers.CharField(help_text="Name of the relevant document")
    document_url = serializers.CharField(help_text="URL to access the document")
    confidence = serializers.FloatField(help_text="Confidence score (0-1)", required=False)

