from django.db import models
from ckeditor.fields import RichTextField


class Objective(models.Model):
    """
    Model for CEPA Objectives
    """
    title = models.CharField(max_length=200, help_text="Objective title or number")
    description = models.TextField(help_text="Detailed description of the objective")
    order = models.IntegerField(default=0, help_text="Display order")
    icon = models.CharField(
        max_length=100,
        blank=True,
        help_text="Icon name or identifier (optional)"
    )
    is_active = models.BooleanField(default=True, help_text="Whether this objective is active")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['order', 'created_at']
        verbose_name = 'Objective'
        verbose_name_plural = 'Objectives'

    def __str__(self):
        return self.title


class TeamMember(models.Model):
    """
    Model for Team Members
    """
    name = models.CharField(max_length=200, help_text="Full name of the team member")
    title = models.CharField(max_length=200, help_text="Job title or position")
    bio = models.TextField(blank=True, help_text="Short biography")
    photo = models.ImageField(upload_to='team/', blank=True, null=True, help_text="Team member photo")
    email = models.EmailField(blank=True, help_text="Email address")
    phone = models.CharField(max_length=20, blank=True, help_text="Phone number")
    linkedin_url = models.URLField(blank=True, help_text="LinkedIn profile URL")
    twitter_url = models.URLField(blank=True, help_text="Twitter profile URL")
    facebook_url = models.URLField(blank=True, help_text="Facebook profile URL")
    order = models.IntegerField(default=0, help_text="Display order")
    is_active = models.BooleanField(default=True, help_text="Whether this team member is active")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['order', 'name']
        verbose_name = 'Team Member'
        verbose_name_plural = 'Team Members'

    def __str__(self):
        return f"{self.name} - {self.title}"


class WhoWeAre(models.Model):
    """
    Model for "Who We Are" section content
    """
    title = models.CharField(max_length=200, default="Who We Are")
    content = RichTextField(help_text="Content for the Who We Are section")
    image = models.ImageField(upload_to='about/', blank=True, null=True, help_text="Optional image for the section")
    youtube_video_url = models.URLField(
        blank=True,
        null=True,
        help_text="Optional YouTube video URL. If set, the video is shown instead of the image on the About page."
    )
    is_active = models.BooleanField(default=True, help_text="Whether this section is active")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = 'Who We Are'
        verbose_name_plural = 'Who We Are'
        ordering = ['-updated_at']

    def __str__(self):
        return self.title

    def save(self, *args, **kwargs):
        # Ensure only one active instance
        if self.is_active:
            WhoWeAre.objects.filter(is_active=True).exclude(pk=self.pk).update(is_active=False)
        super().save(*args, **kwargs)


class OurStory(models.Model):
    """
    Model for "Our Story" section content
    """
    title = models.CharField(max_length=200, default="Our Story")
    content = RichTextField(help_text="Content for the Our Story section")
    image = models.ImageField(upload_to='about/', blank=True, null=True, help_text="Optional image for the section")
    youtube_video_url = models.URLField(
        blank=True,
        null=True,
        help_text="Optional YouTube video URL. If set, the video is shown instead of the image on the About page."
    )
    is_active = models.BooleanField(default=True, help_text="Whether this section is active")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = 'Our Story'
        verbose_name_plural = 'Our Story'
        ordering = ['-updated_at']

    def __str__(self):
        return self.title

    def save(self, *args, **kwargs):
        # Ensure only one active instance
        if self.is_active:
            OurStory.objects.filter(is_active=True).exclude(pk=self.pk).update(is_active=False)
        super().save(*args, **kwargs)


class WhatSetsUsApart(models.Model):
    """
    Model for "What Sets Us Apart" items (features/advantages)
    """
    title = models.CharField(max_length=200, help_text="Feature title")
    description = models.TextField(help_text="Description of the feature")
    icon = models.CharField(
        max_length=100,
        blank=True,
        help_text="Icon name or identifier (optional)"
    )
    order = models.IntegerField(default=0, help_text="Display order")
    is_active = models.BooleanField(default=True, help_text="Whether this item is active")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['order', 'created_at']
        verbose_name = 'What Sets Us Apart'
        verbose_name_plural = 'What Sets Us Apart'

    def __str__(self):
        return self.title


class Partner(models.Model):
    """
    Model for Partners
    """
    name = models.CharField(max_length=200, help_text="Partner organization name")
    description = models.TextField(blank=True, help_text="Description of the partner")
    logo = models.ImageField(upload_to='partners/', blank=True, null=True, help_text="Partner logo")
    website_url = models.URLField(blank=True, help_text="Partner website URL")
    order = models.IntegerField(default=0, help_text="Display order")
    is_active = models.BooleanField(default=True, help_text="Whether this partner is active")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['order', 'name']
        verbose_name = 'Partner'
        verbose_name_plural = 'Partners'

    def __str__(self):
        return self.name
