from django.db import models
from django.conf import settings
import os


class Document(models.Model):
    """Model to track documents available for the chatbot"""
    name = models.CharField(max_length=255, db_index=True, help_text="Display name for the document")
    file = models.FileField(upload_to='chatbot/documents/', help_text="Upload PDF document")
    description = models.TextField(blank=True, null=True, help_text="Optional description of the document")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-created_at']
        verbose_name = 'Document'
        verbose_name_plural = 'Documents'

    def __str__(self):
        return self.name

    @property
    def full_path(self):
        """Get the full file path"""
        if self.file:
            return self.file.path
        return None

    @property
    def file_url(self):
        """Get the URL to access the file"""
        if self.file:
            return self.file.url
        return None

    @property
    def file_type(self):
        """Get file type from extension"""
        if self.file:
            return os.path.splitext(self.file.name)[1].lower().replace('.', '')
        return 'pdf'
