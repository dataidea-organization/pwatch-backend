from django.db import models


class PageHeroImage(models.Model):
    """
    Model for Page-specific Hero Images
    Allows admin to set custom hero images for different pages
    """
    PAGE_CHOICES = [
        ('bills', 'Bills Tracker'),
        ('mps', 'MPs Tracker'),
        ('loans', 'Loans Tracker'),
        ('budgets', 'Budgets Tracker'),
        ('hansards', 'Hansards Tracker'),
        ('order-paper', 'Order Paper Tracker'),
        ('committees', 'Committees'),
        ('statements', 'Statements'),
        ('reports-briefs', 'Reports & Briefs'),
        ('podcast', 'Podcast'),
        ('gallery', 'Gallery'),
        ('x-spaces', 'X Spaces'),
        ('citizens-voice', 'Citizens Voice'),
    ]

    page_slug = models.CharField(
        max_length=50,
        choices=PAGE_CHOICES,
        unique=True,
        help_text="The page this hero image is for"
    )
    page_name = models.CharField(
        max_length=100,
        blank=True,
        help_text="Display name for the page (auto-filled from slug if empty)"
    )
    image = models.ImageField(
        upload_to='page_heroes/',
        help_text="Hero image for this page"
    )
    alt_text = models.CharField(
        max_length=200,
        blank=True,
        help_text="Alternative text for accessibility"
    )
    is_active = models.BooleanField(
        default=True,
        help_text="Whether this hero image is active"
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['page_slug']
        verbose_name = 'Page Hero Image'
        verbose_name_plural = 'Page Hero Images'

    def save(self, *args, **kwargs):
        # Auto-fill page_name from PAGE_CHOICES if empty
        if not self.page_name:
            for slug, name in self.PAGE_CHOICES:
                if slug == self.page_slug:
                    self.page_name = name
                    break
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.page_name or self.page_slug} Hero Image"
