from django.db import models

# Create your models here.
# contact/models.py
from django.db import models
from django.utils import timezone


class ContactMessage(models.Model):
    """Model to store contact form submissions"""
    
    MESSAGE_TYPES = (
        ('general', 'General Inquiry'),
        ('support', 'Technical Support'),
        ('feedback', 'Feedback'),
        ('bug', 'Bug Report'),
        ('feature', 'Feature Request'),
        ('other', 'Other'),
    )
    
    STATUS_CHOICES = (
        ('new', 'New'),
        ('in_progress', 'In Progress'),
        ('resolved', 'Resolved'),
        ('closed', 'Closed'),
    )
    
    # Contact Information
    name = models.CharField(max_length=200, help_text="Full name of the person contacting")
    email = models.EmailField(help_text="Email address for response")
    subject = models.CharField(max_length=300, help_text="Brief subject of the inquiry")
    
    # Message Details
    message_type = models.CharField(
        max_length=20, 
        choices=MESSAGE_TYPES, 
        default='general',
        help_text="Type of inquiry"
    )
    message = models.TextField(help_text="Detailed message content")
    
    # Metadata
    status = models.CharField(
        max_length=20,
        choices=STATUS_CHOICES,
        default='new',
        help_text="Current status of the inquiry"
    )
    created_at = models.DateTimeField(default=timezone.now, help_text="When the message was submitted")
    updated_at = models.DateTimeField(auto_now=True, help_text="Last update time")
    
    # Optional fields
    ip_address = models.GenericIPAddressField(null=True, blank=True, help_text="IP address of submitter")
    user_agent = models.TextField(blank=True, help_text="Browser user agent")
    is_read = models.BooleanField(default=False, help_text="Whether admin has read the message")
    admin_notes = models.TextField(blank=True, help_text="Internal notes from admin")
    
    class Meta:
        ordering = ['-created_at']
        verbose_name = 'Contact Message'
        verbose_name_plural = 'Contact Messages'
        indexes = [
            models.Index(fields=['-created_at']),
            models.Index(fields=['status']),
            models.Index(fields=['message_type']),
        ]
    
    def __str__(self):
        return f"{self.name} - {self.subject} ({self.created_at.strftime('%Y-%m-%d')})"
    
    def mark_as_read(self):
        """Mark the message as read"""
        self.is_read = True
        self.save(update_fields=['is_read', 'updated_at'])
    
    def get_status_color(self):
        """Return color class based on status"""
        colors = {
            'new': 'blue',
            'in_progress': 'yellow',
            'resolved': 'green',
            'closed': 'gray'
        }
        return colors.get(self.status, 'gray')
    
    def get_message_type_display_color(self):
        """Return color for message type display"""
        colors = {
            'general': 'blue',
            'support': 'purple',
            'feedback': 'green',
            'bug': 'red',
            'feature': 'pink',
            'other': 'gray'
        }
        return colors.get(self.message_type, 'gray')