from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone
from django.utils.text import slugify
from ckeditor.fields import RichTextField


def default_published_date():
    return timezone.now().date()


class Blog(models.Model):
    STATUS_CHOICES = [
        ('draft', 'Draft'),
        ('published', 'Published'),
    ]

    CATEGORY_CHOICES = [
        ('governance', 'Governance'),
        ('leadership', 'Leadership'),
        ('youth_powered', 'Youth Powered'),
        ('accountability', 'Accountability'),
    ]

    title = models.CharField(max_length=500, db_index=True)
    slug = models.SlugField(max_length=550, unique=True, blank=True, db_index=True)
    author = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True, related_name='blog_posts', db_index=True)
    category = models.CharField(max_length=50, choices=CATEGORY_CHOICES, default='governance')
    content = RichTextField()
    image = models.ImageField(upload_to='blogs/', blank=True, null=True)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='draft')
    published_date = models.DateField(default=default_published_date)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-published_date', '-created_at']
        verbose_name = 'Blog'
        verbose_name_plural = 'Blogs'

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.title)
        super().save(*args, **kwargs)

    def __str__(self):
        return self.title

    @property
    def category_display(self):
        return dict(self.CATEGORY_CHOICES).get(self.category, self.category)


class BlogComment(models.Model):
    """Anonymous comment on a blog post. No login required."""
    blog = models.ForeignKey(Blog, on_delete=models.CASCADE, related_name='comments', db_index=True)
    author_name = models.CharField(max_length=255)
    author_email = models.EmailField()
    body = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    is_approved = models.BooleanField(default=True, help_text='Approved comments are shown publicly')

    class Meta:
        ordering = ['-created_at']
        verbose_name = 'Blog comment'
        verbose_name_plural = 'Blog comments'

    def __str__(self):
        return f'Comment by {self.author_name} on {self.blog.title}'
