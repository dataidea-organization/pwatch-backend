from django.db import models


class ContactSubmission(models.Model):
    """Model to store contact form submissions"""

    STATUS_CHOICES = [
        ('new', 'New'),
        ('in_progress', 'In Progress'),
        ('resolved', 'Resolved'),
    ]

    name = models.CharField(max_length=200)
    email = models.EmailField()
    subject = models.CharField(max_length=500)
    message = models.TextField()
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='new')

    # Metadata
    ip_address = models.GenericIPAddressField(null=True, blank=True)
    user_agent = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-created_at']
        verbose_name = 'Contact Submission'
        verbose_name_plural = 'Contact Submissions'

    def __str__(self):
        return f"{self.name} - {self.subject[:50]}"


class DonationSubmission(models.Model):
    """Model to store donation form submissions"""

    STATUS_CHOICES = [
        ('new', 'New'),
        ('acknowledged', 'Acknowledged'),
        ('processed', 'Processed'),
        ('completed', 'Completed'),
    ]

    DONATION_METHOD_CHOICES = [
        ('mobile-money', 'Mobile Money'),
        ('bank-transfer', 'Bank Transfer'),
        ('other', 'Other'),
    ]

    name = models.CharField(max_length=200)
    email = models.EmailField()
    country = models.CharField(max_length=100, default='Uganda')
    address = models.TextField(blank=True)
    donation_method = models.CharField(
        max_length=50,
        choices=DONATION_METHOD_CHOICES,
        blank=True,
        help_text="Preferred donation method"
    )
    message = models.TextField(blank=True)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='new')

    # Metadata
    ip_address = models.GenericIPAddressField(null=True, blank=True)
    user_agent = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-created_at']
        verbose_name = 'Donation Submission'
        verbose_name_plural = 'Donation Submissions'

    def __str__(self):
        return f"{self.name} - {self.country} ({self.created_at.strftime('%Y-%m-%d')})"


class Feedback(models.Model):
    """Model to store user feedback from Citizens Voice page"""

    STATUS_CHOICES = [
        ('new', 'New'),
        ('reviewed', 'Reviewed'),
        ('archived', 'Archived'),
    ]

    name = models.CharField(max_length=200)
    email = models.EmailField()
    message = models.TextField()
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='new')

    # Metadata
    ip_address = models.GenericIPAddressField(null=True, blank=True)
    user_agent = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-created_at']
        verbose_name = 'Feedback'
        verbose_name_plural = 'Feedback'

    def __str__(self):
        return f"{self.name} - {self.created_at.strftime('%Y-%m-%d')}"