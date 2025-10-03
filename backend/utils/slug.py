"""
Slug Generation Utility
"""
import re
from datetime import datetime
from typing import Optional


def slugify(text: str, max_length: int = 200) -> str:
    """
    Convert text to URL-friendly slug

    Args:
        text: Text to convert
        max_length: Maximum length of slug

    Returns:
        URL-friendly slug

    Example:
        "Hello World! 123" -> "hello-world-123"
    """
    # Convert to lowercase
    slug = text.lower()

    # Replace spaces and special characters with hyphens
    slug = re.sub(r'[^\w\s-]', '', slug)
    slug = re.sub(r'[\s_-]+', '-', slug)
    slug = re.sub(r'^-+|-+$', '', slug)

    # Truncate to max length
    if len(slug) > max_length:
        slug = slug[:max_length].rsplit('-', 1)[0]

    return slug


def generate_unique_slug(title: str, timestamp: Optional[datetime] = None) -> str:
    """
    Generate a unique slug from title with optional timestamp

    Args:
        title: Blog post title
        timestamp: Optional timestamp to append

    Returns:
        Unique slug

    Example:
        "My Blog Post" -> "my-blog-post-20251003"
    """
    slug = slugify(title)

    # Append timestamp for uniqueness
    if timestamp:
        date_str = timestamp.strftime("%Y%m%d")
        slug = f"{slug}-{date_str}"

    return slug
