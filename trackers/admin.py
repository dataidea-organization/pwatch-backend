from django.contrib import admin
from .models import Bill, BillReading, MP, ParliamentTerm, DebtData, Lender, Loan, LoanDocument, Hansard, Budget, OrderPaper, Committee, CommitteeDocument


@admin.register(ParliamentTerm)
class ParliamentTermAdmin(admin.ModelAdmin):
    list_display = ['name', 'start_year', 'end_year', 'is_current']
    list_filter = ['is_current']
    search_fields = ['name']
    ordering = ['-start_year']


class LoanDocumentInline(admin.TabularInline):
    model = LoanDocument
    extra = 0
    fields = ['label', 'file']


class BillReadingInline(admin.TabularInline):
    model = BillReading
    extra = 1
    fields = ['stage', 'date', 'details', 'document', 'committee_report', 'analysis', 'mp_photo']


@admin.register(Bill)
class BillAdmin(admin.ModelAdmin):
    list_display = ['title', 'bill_type', 'status', 'year_introduced', 'mover', 'created_at']
    list_filter = ['bill_type', 'status', 'year_introduced']
    search_fields = ['title', 'mover', 'assigned_to']
    date_hierarchy = 'created_at'
    ordering = ['-created_at']
    inlines = [BillReadingInline]

    fieldsets = (
        ('Basic Information', {
            'fields': ('title', 'bill_type', 'year_introduced', 'mover', 'assigned_to', 'status')
        }),
        ('Description', {
            'fields': ('description',)
        }),
        ('Video', {
            'fields': ('video_url',)
        }),
    )


@admin.register(BillReading)
class BillReadingAdmin(admin.ModelAdmin):
    list_display = ['bill', 'stage', 'date', 'created_at']
    list_filter = ['stage', 'date']
    search_fields = ['bill__title', 'details']
    date_hierarchy = 'date'
    ordering = ['-date']

    fieldsets = (
        ('Reading Information', {
            'fields': ('bill', 'stage', 'date', 'details')
        }),
        ('Documents', {
            'fields': ('document', 'committee_report', 'analysis', 'mp_photo')
        }),
    )


@admin.register(MP)
class MPAdmin(admin.ModelAdmin):
    list_display = ['name', 'parliament_term', 'party', 'constituency', 'district', 'email', 'phone_no']
    list_filter = ['party', 'district', 'parliament_term']
    search_fields = ['name', 'first_name', 'last_name', 'constituency', 'district', 'email']
    ordering = ['last_name', 'first_name']

    fieldsets = (
        ('Parliament Term', {
            'fields': ('parliament_term',)
        }),
        ('Personal Information', {
            'fields': ('first_name', 'middle_name', 'last_name', 'name', 'photo')
        }),
        ('Political Information', {
            'fields': ('party', 'constituency', 'district')
        }),
        ('Contact Information', {
            'fields': ('phone_no', 'email')
        }),
        ('Biography', {
            'fields': ('bio',)
        }),
    )


@admin.register(DebtData)
class DebtDataAdmin(admin.ModelAdmin):
    list_display = ['year', 'national_debt', 'gdp', 'interest', 'total_expenditure']
    list_filter = ['year']
    search_fields = ['year']
    ordering = ['-year']

    fieldsets = (
        ('Year', {
            'fields': ('year',)
        }),
        ('Debt Metrics (Millions UGX)', {
            'fields': ('national_debt', 'gdp', 'interest', 'total_expenditure')
        }),
        ('Per Capita Metrics (UGX)', {
            'fields': ('debt_per_citizen', 'gdp_per_capita', 'per_capita_income')
        }),
        ('Population', {
            'fields': ('population',)
        }),
    )


@admin.register(Lender)
class LenderAdmin(admin.ModelAdmin):
    list_display = ['name', 'created_at']
    search_fields = ['name']
    ordering = ['name']


@admin.register(Loan)
class LoanAdmin(admin.ModelAdmin):
    list_display = ['sector', 'label', 'approved_amount', 'currency', 'lender', 'source', 'approval_date']
    list_filter = ['sector', 'currency', 'source', 'approval_date']
    search_fields = ['label', 'description', 'sector']
    ordering = ['-approval_date', '-created_at']
    date_hierarchy = 'approval_date'
    inlines = [LoanDocumentInline]

    fieldsets = (
        ('Loan Information', {
            'fields': ('sector', 'label', 'description')
        }),
        ('Financial Details', {
            'fields': ('approved_amount', 'currency')
        }),
        ('Source / Lender', {
            'fields': ('lender', 'source', 'approval_date'),
            'description': 'Use Lender for custom providers, or Source for preset. Lender takes precedence if set.'
        }),
    )


@admin.register(Hansard)
class HansardAdmin(admin.ModelAdmin):
    list_display = ['name', 'date', 'date_received', 'file', 'created_at']
    list_filter = ['date', 'date_received']
    search_fields = ['name']
    ordering = ['-date', '-created_at']
    date_hierarchy = 'date'

    fieldsets = (
        ('Hansard Information', {
            'fields': ('name', 'date', 'date_received', 'file')
        }),
    )


@admin.register(Budget)
class BudgetAdmin(admin.ModelAdmin):
    list_display = ['name', 'financial_year', 'budget_total_amount', 'file', 'created_at']
    list_filter = ['financial_year']
    search_fields = ['name', 'financial_year']
    ordering = ['-financial_year', '-created_at']

    fieldsets = (
        ('Budget Information', {
            'fields': ('name', 'financial_year', 'budget_total_amount')
        }),
        ('Document', {
            'fields': ('file',)
        }),
    )


@admin.register(OrderPaper)
class OrderPaperAdmin(admin.ModelAdmin):
    list_display = ['name', 'date_received', 'file', 'created_at']
    search_fields = ['name', 'description']
    list_filter = ['date_received', 'created_at']
    ordering = ['-date_received', '-created_at']
    date_hierarchy = 'date_received'

    fieldsets = (
        ('Order Paper Information', {
            'fields': ('name', 'description', 'file', 'date_received')
        }),
    )


class CommitteeDocumentInline(admin.TabularInline):
    model = CommitteeDocument
    extra = 1
    fields = ['title', 'description', 'file', 'document_date']


@admin.register(Committee)
class CommitteeAdmin(admin.ModelAdmin):
    list_display = ['title', 'chairperson', 'deputy_chairperson', 'begin_date', 'end_date', 'created_at']
    list_filter = ['begin_date', 'end_date', 'created_at']
    search_fields = ['title', 'description', 'chairperson__name', 'deputy_chairperson__name']
    date_hierarchy = 'created_at'
    ordering = ['title']
    filter_horizontal = ['members']
    inlines = [CommitteeDocumentInline]

    fieldsets = (
        ('Basic Information', {
            'fields': ('title', 'description')
        }),
        ('Term', {
            'fields': ('begin_date', 'end_date')
        }),
        ('Leadership', {
            'fields': ('chairperson', 'deputy_chairperson')
        }),
        ('Members', {
            'fields': ('members',)
        }),
    )


@admin.register(CommitteeDocument)
class CommitteeDocumentAdmin(admin.ModelAdmin):
    list_display = ['title', 'committee', 'document_date', 'created_at']
    list_filter = ['document_date', 'created_at', 'committee']
    search_fields = ['title', 'description', 'committee__title']
    date_hierarchy = 'document_date'
    ordering = ['-document_date', '-created_at']

    fieldsets = (
        ('Document Information', {
            'fields': ('committee', 'title', 'description', 'file', 'document_date')
        }),
    )