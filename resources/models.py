from django.db import models
from django.utils import timezone
from django.core.validators import URLValidator

# Create your models here.
class Explainers(models.Model):
    name = models.CharField(max_length=100, db_index=True)
    description = models.TextField(null=True, blank=True)
    file = models.FileField(null=True, blank=True)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = 'Explainer'
        ordering = ['-created_at']


class Report(models.Model):
    name = models.CharField(max_length=100, db_index=True)
    description = models.TextField(null=True, blank=True)
    file = models.FileField(null=True, blank=True)
    date_received = models.DateField(null=True, blank=True, help_text="Date the report was received")

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = 'Report'
        ordering = ['-created_at']


class PartnerPublication(models.Model):
    name = models.CharField(max_length=100, db_index=True)
    description = models.TextField(null=True, blank=True)
    file = models.FileField(null=True, blank=True)
    date_received = models.DateField(null=True, blank=True, help_text="Date the publication was received")

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = 'PartnerPublication'
        ordering = ['-created_at']


class Statement(models.Model):
    name = models.CharField(max_length=100, db_index=True)
    description = models.TextField(null=True, blank=True)
    file = models.FileField(null=True, blank=True)
    date_received = models.DateField(null=True, blank=True, help_text="Date the statement was received")

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = 'Statement'
        ordering = ['-created_at']


class Publication(models.Model):
    """Model for research publications, policy briefs, and reports"""
    PUBLICATION_TYPES = [
        ('Policy Brief', 'Policy Brief'),
        ('Policy Paper', 'Policy Paper'),
        ('Research Report', 'Research Report'),
        ('Analysis', 'Analysis'),
    ]

    title = models.TextField()
    type = models.CharField(max_length=100, choices=PUBLICATION_TYPES)
    date = models.DateField(default=timezone.now)
    description = models.TextField()
    category = models.CharField(max_length=100)
    url = models.URLField(blank=True, null=True, validators=[URLValidator()])
    pdf = models.FileField(upload_to="publications/documents", blank=True, null=True)
    image = models.ImageField(upload_to="publications/images", blank=True, null=True)
    featured = models.BooleanField(default=False)
    created_at = models.DateTimeField(default=timezone.now)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-created_at']
        verbose_name = 'Publication'
        verbose_name_plural = 'Publications'

    def __str__(self):
        return self.title

