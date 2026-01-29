from django.db import models
from django.db.models.signals import post_save, post_delete
from django.dispatch import receiver
from django.contrib.auth.models import User
from django.utils import timezone
from django.utils.text import slugify
from django.core.cache import cache
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


class NewsComment(models.Model):
    """Anonymous comment on a news article. No login required."""
    news = models.ForeignKey(News, on_delete=models.CASCADE, related_name='comments', db_index=True)
    author_name = models.CharField(max_length=255)
    author_email = models.EmailField()
    body = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    is_approved = models.BooleanField(default=True, help_text='Approved comments are shown publicly')

    class Meta:
        ordering = ['-created_at']
        verbose_name = 'News comment'
        verbose_name_plural = 'News comments'

    def __str__(self):
        return f'Comment by {self.author_name} on {self.news.title}'


class HotInParliament(models.Model):
    """Model for 'Hot in Parliament' items displayed on the home page"""
    title = models.CharField(max_length=500, db_index=True)
    slug = models.SlugField(max_length=550, unique=True, blank=True, db_index=True)
    author = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True, related_name='hot_in_parliament', db_index=True)
    content = RichTextField()
    image = models.ImageField(upload_to='hot_in_parliament/', blank=True, null=True)
    link_url = models.URLField(blank=True, null=True, help_text="Optional link to related article or external resource")
    is_active = models.BooleanField(default=True, help_text="Whether this item should be displayed")
    order = models.PositiveIntegerField(default=0, help_text="Order for display (lower numbers appear first)")
    published_date = models.DateField(default=default_published_date)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = 'Hot in Parliament'
        verbose_name_plural = 'Hot in Parliament'
        ordering = ['order', '-published_date', '-created_at']

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.title)
        super().save(*args, **kwargs)

    def __str__(self):
        return self.title


# Signal to clear cache when HotInParliament items are saved or deleted
@receiver(post_save, sender=HotInParliament)
@receiver(post_delete, sender=HotInParliament)
def clear_hot_in_parliament_cache(sender, instance, **kwargs):
    """Clear the cache when Hot in Parliament items are modified"""
    cache.delete('hot_in_parliament')