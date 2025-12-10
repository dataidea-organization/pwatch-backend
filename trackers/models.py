from django.db import models


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

    title = models.CharField(max_length=500)
    bill_type = models.CharField(max_length=50, choices=BILL_TYPE_CHOICES)
    year_introduced = models.DateField()
    mover = models.CharField(max_length=200)
    assigned_to = models.CharField(max_length=200, help_text="Committee assigned to")
    status = models.CharField(max_length=50, choices=BILL_STATUS_CHOICES, default='1st_reading')
    description = models.TextField(blank=True)
    video_url = models.URLField(blank=True, null=True)
    likes = models.IntegerField(default=0)
    comments = models.IntegerField(default=0)
    shares = models.IntegerField(default=0)
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
    name = models.CharField(max_length=300, help_text="Full name of the MP")

    # Contact Information
    phone_no = models.CharField(max_length=20, blank=True)
    email = models.EmailField(blank=True)

    # Political Information
    party = models.CharField(max_length=100, help_text="Political party affiliation")
    constituency = models.CharField(max_length=200)
    district = models.CharField(max_length=100)

    # Additional Information
    photo = models.ImageField(upload_to='mps/', blank=True, null=True)
    bio = models.TextField(blank=True, null=True)

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