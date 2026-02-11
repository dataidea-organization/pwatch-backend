from rest_framework import serializers
from main.utils import get_full_media_url
from .models import Explainers, Report, PartnerPublication, Statement, Publication


class ExplainersSerializer(serializers.ModelSerializer):
    """Serializer for Explainers"""
    file = serializers.SerializerMethodField()

    class Meta:
        model = Explainers
        fields = [
            'id',
            'name',
            'description',
            'file',
            'created_at',
            'updated_at',
        ]
        read_only_fields = ['created_at', 'updated_at']

    def get_file(self, obj):
        if obj.file:
            return get_full_media_url(obj.file.url)
        return None


class ReportSerializer(serializers.ModelSerializer):
    """Serializer for Reports"""
    file = serializers.SerializerMethodField()

    class Meta:
        model = Report
        fields = [
            'id',
            'name',
            'description',
            'file',
            'date_received',
            'created_at',
            'updated_at',
        ]
        read_only_fields = ['created_at', 'updated_at']

    def get_file(self, obj):
        if obj.file:
            return get_full_media_url(obj.file.url)
        return None


class PartnerPublicationSerializer(serializers.ModelSerializer):
    """Serializer for Partner Publications"""
    file = serializers.SerializerMethodField()

    class Meta:
        model = PartnerPublication
        fields = [
            'id',
            'name',
            'description',
            'file',
            'date_received',
            'created_at',
            'updated_at',
        ]
        read_only_fields = ['created_at', 'updated_at']

    def get_file(self, obj):
        if obj.file:
            return get_full_media_url(obj.file.url)
        return None


class StatementSerializer(serializers.ModelSerializer):
    """Serializer for Statements"""
    file = serializers.SerializerMethodField()

    class Meta:
        model = Statement
        fields = [
            'id',
            'name',
            'description',
            'file',
            'date_received',
            'created_at',
            'updated_at',
        ]
        read_only_fields = ['created_at', 'updated_at']

    def get_file(self, obj):
        if obj.file:
            return get_full_media_url(obj.file.url)
        return None


# Lightweight serializers for home page summary
class HomeSummaryExplainerSerializer(serializers.ModelSerializer):
    """Minimal serializer for Explainer home summary"""
    file = serializers.SerializerMethodField()
    
    class Meta:
        model = Explainers
        fields = ['id', 'name', 'file']

    def get_file(self, obj):
        if obj.file:
            return get_full_media_url(obj.file.url)
        return None


class HomeSummaryReportSerializer(serializers.ModelSerializer):
    """Minimal serializer for Report home summary"""
    file = serializers.SerializerMethodField()
    
    class Meta:
        model = Report
        fields = ['id', 'name', 'file']

    def get_file(self, obj):
        if obj.file:
            return get_full_media_url(obj.file.url)
        return None


class HomeSummaryPartnerPublicationSerializer(serializers.ModelSerializer):
    """Minimal serializer for PartnerPublication home summary"""
    file = serializers.SerializerMethodField()
    
    class Meta:
        model = PartnerPublication
        fields = ['id', 'name', 'file']

    def get_file(self, obj):
        if obj.file:
            return get_full_media_url(obj.file.url)
        return None


class HomeSummaryStatementSerializer(serializers.ModelSerializer):
    """Minimal serializer for Statement home summary"""
    file = serializers.SerializerMethodField()
    
    class Meta:
        model = Statement
        fields = ['id', 'name', 'file']

    def get_file(self, obj):
        if obj.file:
            return get_full_media_url(obj.file.url)
        return None


class PublicationSerializer(serializers.ModelSerializer):
    """Serializer for Publications (research publications, policy briefs, reports)"""
    pdf = serializers.SerializerMethodField()
    image = serializers.SerializerMethodField()

    class Meta:
        model = Publication
        fields = [
            'id',
            'title',
            'type',
            'date',
            'description',
            'category',
            'url',
            'pdf',
            'image',
            'featured',
            'created_at',
            'updated_at',
        ]
        read_only_fields = ['created_at', 'updated_at']

    def get_pdf(self, obj):
        if obj.pdf:
            return get_full_media_url(obj.pdf.url)
        return None

    def get_image(self, obj):
        if obj.image:
            return get_full_media_url(obj.image.url)
        return None