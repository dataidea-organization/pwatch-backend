from rest_framework import serializers
from main.utils import get_full_media_url
from .models import Explainers, Report, PartnerPublication, Statement


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