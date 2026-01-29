from django.db import models
from ckeditor.fields import RichTextField


class Bill(models.Model):
    BILL_TYPE_CHOICES = [
        ('government', 'Government'),
        ('private_member', 'Private Member'),
    ]

    BILL_STATUS_CHOICES = [
        ('1st_reading', '1st Reading'),
        ('2nd_reading', '2nd Reading'),
        ('3rd_reading', '3rd Reading'),
        ('passed', 'Passed by Parliament'),
        ('assented', 'Assented to by the President'),
    ]

    title = models.CharField(max_length=500, db_index=True)
    bill_type = models.CharField(max_length=50, choices=BILL_TYPE_CHOICES)
    year_introduced = models.DateField()
    mover = models.CharField(max_length=200, db_index=True)
    assigned_to = models.CharField(max_length=200, help_text="Committee assigned to")
    status = models.CharField(max_length=50, choices=BILL_STATUS_CHOICES, default='1st_reading')
    description = models.TextField(blank=True)
    video_url = models.URLField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-created_at']
        verbose_name = 'Bill'
        verbose_name_plural = 'Bills'

    def __str__(self):
        return self.title


class BillReading(models.Model):
    READING_STAGE_CHOICES = [
        ('1st_reading', '1st Reading'),
        ('2nd_reading', '2nd Reading'),
        ('3rd_reading', '3rd Reading'),
        ('waiting_assent', 'Waiting for Assent'),
        ('assented', 'Assented to by the President'),
        ('withdrawn', 'Withdrawn'),
    ]

    bill = models.ForeignKey(Bill, on_delete=models.CASCADE, related_name='readings')
    stage = models.CharField(max_length=50, choices=READING_STAGE_CHOICES)
    date = models.DateField()
    details = models.TextField()
    document = models.FileField(upload_to='bill_documents/', blank=True, null=True)
    committee_report = models.FileField(upload_to='committee_reports/', blank=True, null=True)
    analysis = models.FileField(upload_to='bill_analysis/', blank=True, null=True)
    mp_photo = models.ImageField(upload_to='mp_photos/', blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['date']
        verbose_name = 'Bill Reading'
        verbose_name_plural = 'Bill Readings'
        unique_together = ['bill', 'stage']

    def __str__(self):
        return f"{self.bill.title} - {self.get_stage_display()}"


class MP(models.Model):
    """Model for Members of Parliament"""
    # Personal Information
    first_name = models.CharField(max_length=100)
    middle_name = models.CharField(max_length=100, blank=True)
    last_name = models.CharField(max_length=100)
    name = models.CharField(max_length=300, help_text="Full name of the MP", db_index=True)

    # Contact Information
    phone_no = models.CharField(max_length=20, blank=True)
    email = models.EmailField(blank=True)

    # Political Information
    party = models.CharField(max_length=100, help_text="Political party affiliation", db_index=True)
    constituency = models.CharField(max_length=200, db_index=True)
    district = models.CharField(max_length=100, db_index=True)

    # Additional Information
    photo = models.ImageField(upload_to='mps/', blank=True, null=True)
    bio = RichTextField(blank=True, null=True)

    # Timestamps
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['last_name', 'first_name']
        verbose_name = 'Member of Parliament'
        verbose_name_plural = 'Members of Parliament'

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        """Auto-generate full name if not provided"""
        if not self.name:
            name_parts = [self.first_name]
            if self.middle_name:
                name_parts.append(self.middle_name)
            name_parts.append(self.last_name)
            self.name = ' '.join(name_parts)
        super().save(*args, **kwargs)


class DebtData(models.Model):
    """Model for National Debt and Economic Data"""
    year = models.IntegerField(unique=True, help_text="Year of the data")

    # Debt metrics (in millions UGX)
    national_debt = models.DecimalField(
        max_digits=20,
        decimal_places=2,
        help_text="National debt in millions UGX"
    )
    gdp = models.DecimalField(
        max_digits=20,
        decimal_places=2,
        help_text="GDP in millions UGX"
    )
    interest = models.DecimalField(
        max_digits=20,
        decimal_places=2,
        default=0,
        help_text="Interest payments in millions UGX"
    )
    total_expenditure = models.DecimalField(
        max_digits=20,
        decimal_places=2,
        default=0,
        help_text="Total government expenditure in millions UGX"
    )

    # Per capita metrics
    debt_per_citizen = models.DecimalField(
        max_digits=15,
        decimal_places=2,
        default=0,
        help_text="Debt per citizen in UGX"
    )
    gdp_per_capita = models.DecimalField(
        max_digits=15,
        decimal_places=2,
        default=0,
        help_text="GDP per capita in UGX"
    )
    per_capita_income = models.DecimalField(
        max_digits=15,
        decimal_places=2,
        default=0,
        help_text="Per capita income in UGX"
    )

    # Metadata
    population = models.BigIntegerField(
        null=True,
        blank=True,
        help_text="Population for the year"
    )

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['year']
        verbose_name = 'Debt Data'
        verbose_name_plural = 'Debt Data'

    def __str__(self):
        return f"{self.year} - Debt: UGX {self.national_debt:,.0f}M, GDP: UGX {self.gdp:,.0f}M"


class Lender(models.Model):
    """Lender/source for loans. Admins can add new providers."""
    name = models.CharField(max_length=200, db_index=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['name']
        verbose_name = 'Lender'
        verbose_name_plural = 'Lenders'

    def __str__(self):
        return self.name


class Loan(models.Model):
    """Model for Government Loans and Projects"""
    SECTOR_CHOICES = [
        ('energy', 'Energy'),
        ('transport', 'Transport'),
        ('health', 'Health'),
        ('education', 'Education'),
        ('agriculture', 'Agriculture'),
        ('water', 'Water and Sanitation'),
        ('ict', 'ICT'),
        ('infrastructure', 'Infrastructure'),
        ('other', 'Other'),
    ]

    CURRENCY_CHOICES = [
        ('USD', 'US Dollar'),
        ('EUR', 'Euro'),
        ('GBP', 'British Pound'),
        ('CNY', 'Chinese Yuan'),
        ('UGX', 'Uganda Shilling'),
    ]

    SOURCE_CHOICES = [
        ('world_bank', 'World Bank'),
        ('imf', 'International Monetary Fund'),
        ('adb', 'African Development Bank'),
        ('china', 'China'),
        ('eu', 'European Union'),
        ('bilateral', 'Bilateral Agreement'),
        ('other', 'Other'),
    ]

    sector = models.CharField(max_length=50, choices=SECTOR_CHOICES)
    label = models.CharField(max_length=500, help_text="Project name or description", db_index=True)
    lender = models.ForeignKey(
        Lender,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='loans',
        help_text="Lender/provider. Add new in Lenders if not listed.",
    )
    source = models.CharField(
        max_length=50,
        choices=SOURCE_CHOICES,
        blank=True,
        help_text="Fallback if lender not set (legacy)",
        db_index=True
    )
    approved_amount = models.DecimalField(
        max_digits=20,
        decimal_places=2,
        help_text="Approved loan amount"
    )
    currency = models.CharField(max_length=3, choices=CURRENCY_CHOICES, default='USD')
    approval_date = models.DateField(null=True, blank=True)
    description = RichTextField(blank=True)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-approval_date', '-created_at']
        verbose_name = 'Loan'
        verbose_name_plural = 'Loans'

    def __str__(self):
        return f"{self.get_sector_display()}: {self.label[:50]}"

    @property
    def lender_display(self):
        if self.lender_id:
            return self.lender.name
        return self.get_source_display() if self.source else ""


class LoanDocument(models.Model):
    """Document attached to a loan (e.g. proposal, report)."""
    loan = models.ForeignKey(Loan, on_delete=models.CASCADE, related_name='documents', db_index=True)
    label = models.CharField(max_length=200, help_text="e.g. Proposal, Report, Agreement")
    file = models.FileField(upload_to='loans/documents/')
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['label']
        verbose_name = 'Loan document'
        verbose_name_plural = 'Loan documents'

    def __str__(self):
        return f"{self.label} – {self.loan.label}"

class Hansard(models.Model):
    """Model for Hansards"""
    name = models.CharField(
        max_length=50,
        help_text="Hansard name",
        db_index=True
    )
    date = models.DateField(null=True, blank=True, help_text="Date of the Hansard session")
    date_received = models.DateField(null=True, blank=True, help_text="Date the Hansard was received")
    file = models.FileField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-date', '-created_at']
        verbose_name = 'Hansard'
        verbose_name_plural = 'Hansards'

    def __str__(self):
        return self.name


class Budget(models.Model):
    """Model for National Budget Documents"""
    name = models.CharField(max_length=200, help_text="Budget document name", db_index=True)
    financial_year = models.CharField(max_length=20, help_text="Financial year (e.g., 2024/2025)")
    file = models.FileField(upload_to='budgets/', help_text="Budget PDF document")
    budget_total_amount = models.DecimalField(
        max_digits=20,
        decimal_places=2,
        null=True,
        blank=True,
        help_text="Total budget amount in UGX"
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-financial_year', '-created_at']
        verbose_name = 'Budget'
        verbose_name_plural = 'Budgets'

    def __str__(self):
        return f"{self.name} - {self.financial_year}"

class OrderPaper(models.Model):
    name = models.CharField(max_length=100, db_index=True)
    description = models.TextField(null=True, blank=True)
    file = models.FileField(null=True, blank=True)
    date_received = models.DateField(null=True, blank=True, help_text="Date the order paper was received")

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = 'Order Paper'
        ordering = ['-created_at']

        
class Committee(models.Model):
    """Model for Parliamentary Committees"""
    title = models.CharField(max_length=300, help_text="Committee name")
    description = models.TextField(blank=True, help_text="Committee description and mandate")

    # Term
    begin_date = models.DateField(null=True, blank=True, help_text="Committee term begin date")
    end_date = models.DateField(null=True, blank=True, help_text="Committee term end date")

    # Leadership
    chairperson = models.ForeignKey(
        MP,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='committees_chaired',
        help_text="Committee chairperson"
    )
    deputy_chairperson = models.ForeignKey(
        MP,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='committees_deputy_chaired',
        help_text="Committee deputy chairperson"
    )

    # Members
    members = models.ManyToManyField(
        MP,
        related_name='committee_memberships',
        blank=True,
        help_text="Committee members"
    )

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['title']
        verbose_name = 'Committee'
        verbose_name_plural = 'Committees'

    def __str__(self):
        return self.title


class CommitteeDocument(models.Model):
    """Model for Committee Documents"""
    committee = models.ForeignKey(
        Committee,
        on_delete=models.CASCADE,
        related_name='documents',
        help_text="Associated committee"
    )
    title = models.CharField(max_length=300, help_text="Document title")
    description = models.TextField(blank=True, help_text="Document description")
    file = models.FileField(upload_to='committee_documents/', help_text="Document file")
    document_date = models.DateField(null=True, blank=True, help_text="Document date")

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-document_date', '-created_at']
        verbose_name = 'Committee Document'
        verbose_name_plural = 'Committee Documents'

    def __str__(self):
        return f"{self.committee.title} - {self.title}"




