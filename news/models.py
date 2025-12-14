from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone
from django.utils.text import slugify
from ckeditor.fields import RichTextField


def default_published_date():
    return timezone.now().date()


class News(models.Model):
    STATUS_CHOICES = [
        ('draft', 'Draft'),
        ('published', 'Published'),
    ]

    CATEGORY_CHOICES = [
        ('latest_blogs', 'Latest on Blogs'),
        ('news_updates', 'News and Updates'),
        ('parliament', 'Parliament News'),
        ('governance', 'Governance'),
        ('accountability', 'Accountability'),
    ]

    title = models.CharField(max_length=500, db_index=True)
    slug = models.SlugField(max_length=550, unique=True, blank=True, db_index=True)
    author = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True, related_name='news_articles', db_index=True)
    category = models.CharField(max_length=50, choices=CATEGORY_CHOICES, default='news_updates')
    content = RichTextField()
    image = models.ImageField(upload_to='news/', blank=True, null=True)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='draft')
    published_date = models.DateField(default=default_published_date)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name_plural = 'News'
        ordering = ['-published_date', '-created_at']

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.title)
        super().save(*args, **kwargs)

    def __str__(self):
        return self.title

    @property
    def category_display(self):
        return dict(self.CATEGORY_CHOICES).get(self.category, self.category)