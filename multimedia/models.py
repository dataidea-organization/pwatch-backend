from django.db import models


class XSpace(models.Model):
    """
    Model for X (Twitter) Spaces events
    """
    title = models.CharField(max_length=200, help_text="Title of the X Space event")
    description = models.TextField(blank=True, help_text="Description of the event")
    host = models.CharField(max_length=200, help_text="Host or organizer of the X Space")
    scheduled_date = models.DateTimeField(help_text="Scheduled date and time for the X Space")
    duration = models.IntegerField(null=True, blank=True, help_text="Duration in minutes")
    x_space_url = models.URLField(help_text="URL to the X Space event")
    recording_url = models.URLField(blank=True, null=True, help_text="URL to recording if available")
    thumbnail = models.ImageField(upload_to='x_spaces/', blank=True, null=True, help_text="Thumbnail image for the event")
    status = models.CharField(
        max_length=20,
        choices=[
            ('upcoming', 'Upcoming'),
            ('live', 'Live'),
            ('completed', 'Completed'),
            ('cancelled', 'Cancelled'),
        ],
        default='upcoming',
        help_text="Current status of the X Space"
    )
    topics = models.CharField(
        max_length=500,
        blank=True,
        help_text="Comma-separated list of topics to be discussed"
    )
    speakers = models.TextField(
        blank=True,
        help_text="List of speakers/participants (one per line or comma-separated)"
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-scheduled_date', '-created_at']
        verbose_name = 'X Space'
        verbose_name_plural = 'X Spaces'

    def __str__(self):
        return self.title
