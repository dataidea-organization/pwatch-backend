"""
Utility functions for the main app
"""
import re
from django.conf import settings
from decouple import config


def get_full_media_url(relative_url):
    """
    Convert a relative media URL to a full backend URL.
    
    Args:
        relative_url: Relative URL from media folder (e.g., '/media/news/image.jpg' or 'news/image.jpg')
    
    Returns:
        Full backend URL (e.g., 'https://backend.example.com/media/news/image.jpg')
    """
    if not relative_url:
        return None
    
    # Remove leading /media/ if present
    if relative_url.startswith('/media/'):
        relative_url = relative_url[7:]  # Remove '/media/'
    elif relative_url.startswith('media/'):
        relative_url = relative_url[6:]  # Remove 'media/'
    
    # Get full media URL from settings
    full_media_url = getattr(settings, 'FULL_MEDIA_URL', None)
    if full_media_url:
        # Remove trailing slash if present
        full_media_url = full_media_url.rstrip('/')
        return f"{full_media_url}/{relative_url}"
    
    # Fallback: construct from MEDIA_URL
    if settings.DEBUG:
        return f"http://localhost:8000{settings.MEDIA_URL}{relative_url}"
    else:
        # In production, try to get from environment or use default
        backend_domain = config('BACKEND_DOMAIN', default='https://pwatch-backend-production.up.railway.app')
        return f"{backend_domain}{settings.MEDIA_URL}{relative_url}"


def process_content_images(html_content):
    """
    Process HTML content and convert relative image URLs to absolute URLs.
    
    Args:
        html_content: HTML string that may contain image tags with relative URLs
    
    Returns:
        HTML string with absolute image URLs
    """
    if not html_content:
        return html_content
    
    # Get full media URL base
    full_media_url = getattr(settings, 'FULL_MEDIA_URL', None)
    if not full_media_url:
        if settings.DEBUG:
            full_media_url = f"http://localhost:8000{settings.MEDIA_URL}"
        else:
            backend_domain = config('BACKEND_DOMAIN', default='https://pwatch-backend-production.up.railway.app')
            full_media_url = f"{backend_domain}{settings.MEDIA_URL}"
    
    full_media_url = full_media_url.rstrip('/')
    
    # Pattern to match img tags with src attributes
    # Matches: <img src="/media/..." or <img src="media/..." or <img src="ckeditor/..."
    def replace_image_url(match):
        before_src = match.group(1)  # Everything before src value
        src_value = match.group(2)  # The src URL value
        after_src = match.group(3)  # Quote and everything after
        
        # Skip if already absolute URL (starts with http:// or https://)
        if src_value.startswith('http://') or src_value.startswith('https://'):
            return match.group(0)
        
        # Remove leading slash and /media/ prefix if present
        if src_value.startswith('/media/'):
            relative_path = src_value[7:]  # Remove '/media/'
        elif src_value.startswith('media/'):
            relative_path = src_value[6:]  # Remove 'media/'
        elif src_value.startswith('/'):
            relative_path = src_value[1:]  # Remove leading '/'
        else:
            relative_path = src_value
        
        # Construct absolute URL
        absolute_url = f"{full_media_url}/{relative_path}"
        
        # Reconstruct the img tag with absolute URL
        return f"{before_src}{absolute_url}{after_src}"
    
    # Replace img src attributes
    # Match img tags with src="/media/...", src="media/...", or src="ckeditor/..."
    # Pattern: <img ... src="..." ...> or <img ... src='...' ...>
    # Group 1: before src value, Group 2: src value, Group 3: quote and after
    pattern = r'(<img[^>]*\ssrc=["\'])([^"\']+)(["\'][^>]*>)'
    html_content = re.sub(pattern, replace_image_url, html_content, flags=re.IGNORECASE)
    
    return html_content

