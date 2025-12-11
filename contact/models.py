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