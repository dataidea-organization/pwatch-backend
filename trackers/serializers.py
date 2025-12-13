from rest_framework import serializers
from .models import Bill, BillReading, MP, DebtData, Loan, Hansard, Budget, OrderPaper, Committee, CommitteeDocument


class BillReadingSerializer(serializers.ModelSerializer):
    stage_display = serializers.CharField(source='get_stage_display', read_only=True)

    class Meta:
        model = BillReading
        fields = [
            'id',
            'stage',
            'stage_display',
            'date',
            'details',
            'document',
            'committee_report',
            'analysis',
            'mp_photo',
            'created_at',
            'updated_at',
        ]


class BillSerializer(serializers.ModelSerializer):
    bill_type_display = serializers.CharField(source='get_bill_type_display', read_only=True)
    status_display = serializers.CharField(source='get_status_display', read_only=True)
    readings = BillReadingSerializer(many=True, read_only=True)

    class Meta:
        model = Bill
        fields = [
            'id',
            'title',
            'bill_type',
            'bill_type_display',
            'year_introduced',
            'mover',
            'assigned_to',
            'status',
            'status_display',
            'description',
            'video_url',
            'readings',
            'created_at',
            'updated_at',
        ]


class BillListSerializer(serializers.ModelSerializer):
    """Simplified serializer for bill listing"""
    bill_type_display = serializers.CharField(source='get_bill_type_display', read_only=True)
    status_display = serializers.CharField(source='get_status_display', read_only=True)

    class Meta:
        model = Bill
        fields = [
            'id',
            'title',
            'bill_type',
            'bill_type_display',
            'year_introduced',
            'mover',
            'status',
            'status_display',
            'created_at',
        ]


class MPListSerializer(serializers.ModelSerializer):
    """Simplified serializer for MP listing"""

    class Meta:
        model = MP
        fields = [
            'id',
            'name',
            'first_name',
            'middle_name',
            'last_name',
            'party',
            'phone_no',
            'constituency',
            'district',
            'photo',
            'email',
        ]


class MPDetailSerializer(serializers.ModelSerializer):
    """Full serializer for MP detail view"""

    class Meta:
        model = MP
        fields = [
            'id',
            'name',
            'first_name',
            'middle_name',
            'last_name',
            'party',
            'constituency',
            'district',
            'phone_no',
            'email',
            'photo',
            'bio',
            'created_at',
            'updated_at',
        ]
        read_only_fields = ['created_at', 'updated_at']


class DebtDataSerializer(serializers.ModelSerializer):
    """Serializer for Debt Data"""

    class Meta:
        model = DebtData
        fields = [
            'id',
            'year',
            'national_debt',
            'gdp',
            'interest',
            'total_expenditure',
            'debt_per_citizen',
            'gdp_per_capita',
            'per_capita_income',
            'population',
            'created_at',
            'updated_at',
        ]
        read_only_fields = ['created_at', 'updated_at']


class LoanSerializer(serializers.ModelSerializer):
    """Serializer for Loans"""
    sector_display = serializers.CharField(source='get_sector_display', read_only=True)
    currency_display = serializers.CharField(source='get_currency_display', read_only=True)
    source_display = serializers.CharField(source='get_source_display', read_only=True)

    class Meta:
        model = Loan
        fields = [
            'id',
            'sector',
            'sector_display',
            'label',
            'approved_amount',
            'currency',
            'currency_display',
            'source',
            'source_display',
            'approval_date',
            'description',
            'created_at',
            'updated_at',
        ]
        read_only_fields = ['created_at', 'updated_at']


class HansardSerializer(serializers.ModelSerializer):
    """Serializer for Hansards"""

    class Meta:
        model = Hansard
        fields = [
            'id',
            'name',
            'date',
            'file',
            'created_at',
            'updated_at',
        ]
        read_only_fields = ['created_at', 'updated_at']


class BudgetSerializer(serializers.ModelSerializer):
    """Serializer for Budgets"""

    class Meta:
        model = Budget
        fields = [
            'id',
            'name',
            'financial_year',
            'file',
            'budget_total_amount',
            'created_at',
            'updated_at',
        ]
        read_only_fields = ['created_at', 'updated_at']


class OrderPaperSerializer(serializers.ModelSerializer):
    """Serializer for Order Papers"""

    class Meta:
        model = OrderPaper
        fields = [
            'id',
            'name',
            'description',
            'file',
            'created_at',
            'updated_at',
        ]
        read_only_fields = ['created_at', 'updated_at']


class CommitteeDocumentSerializer(serializers.ModelSerializer):
    """Serializer for Committee Documents"""

    class Meta:
        model = CommitteeDocument
        fields = [
            'id',
            'title',
            'description',
            'file',
            'document_date',
            'created_at',
            'updated_at',
        ]
        read_only_fields = ['created_at', 'updated_at']


class CommitteeListSerializer(serializers.ModelSerializer):
    """Simplified serializer for Committee listing"""
    chairperson_name = serializers.CharField(source='chairperson.name', read_only=True)
    deputy_chairperson_name = serializers.CharField(source='deputy_chairperson.name', read_only=True)
    member_count = serializers.SerializerMethodField()

    class Meta:
        model = Committee
        fields = [
            'id',
            'title',
            'description',
            'chairperson_name',
            'deputy_chairperson_name',
            'member_count',
            'created_at',
            'updated_at',
        ]

    def get_member_count(self, obj):
        return obj.members.count()


class CommitteeDetailSerializer(serializers.ModelSerializer):
    """Full serializer for Committee detail view"""
    chairperson = MPListSerializer(read_only=True)
    deputy_chairperson = MPListSerializer(read_only=True)
    members = MPListSerializer(many=True, read_only=True)
    documents = CommitteeDocumentSerializer(many=True, read_only=True)

    class Meta:
        model = Committee
        fields = [
            'id',
            'title',
            'description',
            'chairperson',
            'deputy_chairperson',
            'members',
            'documents',
            'created_at',
            'updated_at',
        ]
        read_only_fields = ['created_at', 'updated_at']


# Lightweight serializers for home page summary
class HomeSummaryMPSerializer(serializers.ModelSerializer):
    """Minimal serializer for MP home summary"""
    class Meta:
        model = MP
        fields = ['id', 'name', 'party', 'constituency']


class HomeSummaryBillSerializer(serializers.ModelSerializer):
    """Minimal serializer for Bill home summary"""
    class Meta:
        model = Bill
        fields = ['id', 'title']


class HomeSummaryLoanSerializer(serializers.ModelSerializer):
    """Minimal serializer for Loan home summary"""
    sector_display = serializers.CharField(source='get_sector_display', read_only=True)
    source_display = serializers.CharField(source='get_source_display', read_only=True)
    
    class Meta:
        model = Loan
        fields = ['id', 'label', 'sector_display', 'source_display']


class HomeSummaryBudgetSerializer(serializers.ModelSerializer):
    """Minimal serializer for Budget home summary"""
    class Meta:
        model = Budget
        fields = ['id', 'name', 'financial_year', 'file']


class HomeSummaryHansardSerializer(serializers.ModelSerializer):
    """Minimal serializer for Hansard home summary"""
    class Meta:
        model = Hansard
        fields = ['id', 'name', 'date', 'file']


class HomeSummaryOrderPaperSerializer(serializers.ModelSerializer):
    """Minimal serializer for OrderPaper home summary"""
    class Meta:
        model = OrderPaper
        fields = ['id', 'name', 'file']