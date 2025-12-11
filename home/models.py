from django.db import models


class HeroImage(models.Model):
    """
    Model for Home Page Hero Images
    """
    title = models.CharField(max_length=200, blank=True, help_text="Optional title for the image")
    image = models.ImageField(upload_to='hero/', help_text="Hero image for the carousel")
    order = models.IntegerField(default=0, help_text="Display order (lower numbers appear first)")
    is_active = models.BooleanField(default=True, help_text="Whether this image is active in the carousel")
    alt_text = models.CharField(
        max_length=200,
        blank=True,
        help_text="Alternative text for accessibility"
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['order', 'created_at']
        verbose_name = 'Hero Image'
        verbose_name_plural = 'Hero Images'

    def __str__(self):
        return self.title or f"Hero Image {self.id}"
