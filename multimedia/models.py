from django.db import models
from django.utils import timezone


class XSpace(models.Model):
    """
    Model for X (Twitter) Spaces events
    """
    title = models.CharField(max_length=200, help_text="Title of the X Space event", db_index=True)
    description = models.TextField(blank=True, help_text="Description of the event")
    host = models.CharField(max_length=200, help_text="Host or organizer of the X Space", db_index=True)
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


class Podcast(models.Model):
    """
    Model for YouTube Podcasts
    """
    title = models.CharField(max_length=200, help_text="Title of the podcast episode", db_index=True)
    description = models.TextField(blank=True, help_text="Description of the podcast episode")
    host = models.CharField(max_length=200, help_text="Host or presenter of the podcast", db_index=True)
    guest = models.CharField(max_length=200, blank=True, help_text="Guest speaker(s) if any")
    youtube_url = models.URLField(help_text="URL to the YouTube video")
    thumbnail = models.ImageField(upload_to='podcasts/', blank=True, null=True, help_text="Thumbnail image for the podcast")
    duration = models.IntegerField(null=True, blank=True, help_text="Duration in minutes")
    published_date = models.DateTimeField(help_text="Date when the podcast was published")
    episode_number = models.IntegerField(null=True, blank=True, help_text="Episode number if applicable")
    category = models.CharField(
        max_length=100,
        blank=True,
        help_text="Category or topic of the podcast"
    )
    tags = models.CharField(
        max_length=500,
        blank=True,
        help_text="Comma-separated list of tags"
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-published_date', '-created_at']
        verbose_name = 'Podcast'
        verbose_name_plural = 'Podcasts'

    def __str__(self):
        return self.title


class Gallery(models.Model):
    """
    Model for Gallery Images
    """
    title = models.CharField(max_length=200, help_text="Title of the gallery image", db_index=True)
    description = models.TextField(blank=True, help_text="Description of the image")
    image = models.ImageField(upload_to='gallery/', help_text="Gallery image")
    category = models.CharField(
        max_length=100,
        blank=True,
        help_text="Category of the image (e.g., Events, Parliament, Activities)"
    )
    event_date = models.DateField(null=True, blank=True, help_text="Date when the event/photograph was taken")
    photographer = models.CharField(max_length=200, blank=True, help_text="Photographer or source")
    tags = models.CharField(
        max_length=500,
        blank=True,
        help_text="Comma-separated list of tags"
    )
    featured = models.BooleanField(default=False, help_text="Whether this image should be featured")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-featured', '-event_date', '-created_at']
        verbose_name = 'Gallery Image'
        verbose_name_plural = 'Gallery Images'

    def __str__(self):
        return self.title


class Poll(models.Model):
    """
    Model for Citizen Voice Polls
    """
    STATUS_CHOICES = [
        ('draft', 'Draft'),
        ('active', 'Active'),
        ('closed', 'Closed'),
    ]

    title = models.CharField(max_length=300, help_text="Poll question or title", db_index=True)
    description = models.TextField(blank=True, help_text="Detailed description of the poll")
    category = models.CharField(
        max_length=100,
        blank=True,
        help_text="Category or topic (e.g., Legislation, Budget, Governance)"
    )
    status = models.CharField(
        max_length=20,
        choices=STATUS_CHOICES,
        default='draft',
        help_text="Current status of the poll"
    )
    start_date = models.DateTimeField(null=True, blank=True, help_text="When the poll becomes active")
    end_date = models.DateTimeField(null=True, blank=True, help_text="When the poll closes")
    allow_multiple_votes = models.BooleanField(default=False, help_text="Allow users to vote multiple times")
    show_results_before_voting = models.BooleanField(default=False, help_text="Show results before user votes")
    featured = models.BooleanField(default=False, help_text="Feature this poll on the homepage")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-featured', '-created_at']
        verbose_name = 'Poll'
        verbose_name_plural = 'Polls'

    def __str__(self):
        return self.title

    @property
    def total_votes(self):
        """Calculate total number of votes for this poll"""
        return PollVote.objects.filter(poll=self).count()

    @property
    def is_active(self):
        """Check if poll is currently active"""
        if self.status != 'active':
            return False
        now = timezone.now()
        if self.start_date and now < self.start_date:
            return False
        if self.end_date and now > self.end_date:
            return False
        return True


class PollOption(models.Model):
    """
    Model for Poll Options/Choices
    """
    poll = models.ForeignKey(Poll, on_delete=models.CASCADE, related_name='options')
    text = models.CharField(max_length=500, help_text="Option text")
    order = models.IntegerField(default=0, help_text="Display order")
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['order', 'created_at']
        verbose_name = 'Poll Option'
        verbose_name_plural = 'Poll Options'

    def __str__(self):
        return f"{self.poll.title} - {self.text}"

    @property
    def vote_count(self):
        """Get the number of votes for this option"""
        return PollVote.objects.filter(poll=self.poll, option=self).count()

    @property
    def vote_percentage(self):
        """Calculate percentage of votes for this option"""
        total = self.poll.total_votes
        if total == 0:
            return 0
        return round((self.vote_count / total) * 100, 1)


class PollVote(models.Model):
    """
    Model to track individual votes
    """
    poll = models.ForeignKey(Poll, on_delete=models.CASCADE, related_name='votes')
    option = models.ForeignKey(PollOption, on_delete=models.CASCADE, related_name='votes')
    ip_address = models.GenericIPAddressField(null=True, blank=True, help_text="Voter's IP address")
    session_id = models.CharField(max_length=100, blank=True, help_text="Session identifier")
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-created_at']
        verbose_name = 'Poll Vote'
        verbose_name_plural = 'Poll Votes'

    def __str__(self):
        return f"Vote for {self.option.text} in {self.poll.title}"


class XPoll(models.Model):
    """
    Links a Poll to an X (Twitter) poll. Create the poll on X first, then create
    a Poll here with the same question/options and add an XPoll with the X post URL.
    Voting is allowed on both X and here; results here are independent.
    """
    poll = models.OneToOneField(
        Poll,
        on_delete=models.CASCADE,
        related_name='x_poll_link',
        help_text="The poll on this site that mirrors the X poll"
    )
    x_poll_url = models.URLField(
        help_text="URL to the X (Twitter) post where this poll was created. Users can view or vote on X too."
    )
    embed_html = models.TextField(
        blank=True,
        help_text="Paste the full blockquote HTML from Twitter's 'Embed Tweet' (the <blockquote class=\"twitter-tweet\">...</blockquote> part). Required for the poll and vote options to show."
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-created_at']
        verbose_name = 'X Poll'
        verbose_name_plural = 'X Polls'

    def __str__(self):
        return f"X poll: {self.poll.title}"


class XPollEmbed(models.Model):
    """
    Standalone X (Twitter) poll embed. Paste the full embed code from Twitter
    (blockquote + script); we store and display the blockquote part. Not related to Poll.
    """
    title = models.CharField(
        max_length=200,
        blank=True,
        help_text="Optional label for admin (e.g. poll topic)"
    )
    embed_html = models.TextField(
        help_text="Paste the full embed from Twitter: the <blockquote class=\"twitter-tweet\">...</blockquote> part (script is loaded on the page)."
    )
    order = models.PositiveIntegerField(default=0, help_text="Display order (lower first)")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['order', '-created_at']
        verbose_name = 'X Poll Embed'
        verbose_name_plural = 'X Poll Embeds'

    def __str__(self):
        return self.title or f"X Poll Embed #{self.id}"
