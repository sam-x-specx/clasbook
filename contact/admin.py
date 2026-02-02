# contact/admin.py
from django.contrib import admin
from django.utils.html import format_html
from django.urls import reverse
from django.utils.safestring import mark_safe
from .models import ContactMessage


@admin.register(ContactMessage)
class ContactMessageAdmin(admin.ModelAdmin):
    """Admin interface for managing contact messages"""
    
    list_display = [
        'name', 
        'email', 
        'subject', 
        'message_type_badge',
        'status_badge',
        'is_read',
        'created_at',
    ]
    
    list_filter = [
        'status',
        'message_type',
        'is_read',
        'created_at',
    ]
    
    search_fields = [
        'name',
        'email',
        'subject',
        'message',
    ]
    
    readonly_fields = [
        'name',
        'email',
        'subject',
        'message_type',
        'message',
        'created_at',
        'updated_at',
        'ip_address',
        'user_agent',
    ]
    
    fieldsets = (
        ('Contact Information', {
            'fields': ('name', 'email', 'subject')
        }),
        ('Message Details', {
            'fields': ('message_type', 'message')
        }),
        ('Status & Management', {
            'fields': ('status', 'is_read', 'admin_notes')
        }),
        ('Metadata', {
            'fields': ('created_at', 'updated_at', 'ip_address', 'user_agent'),
            'classes': ('collapse',)
        }),
    )
    
    date_hierarchy = 'created_at'
    
    ordering = ['-created_at']
    
    actions = [
        'mark_as_read',
        'mark_as_unread',
        'mark_as_in_progress',
        'mark_as_resolved',
        'mark_as_closed',
    ]
    
    def message_type_badge(self, obj):
        """Display message type as a colored badge"""
        color = obj.get_message_type_display_color()
        colors_map = {
            'blue': '#3B82F6',
            'purple': '#A855F7',
            'green': '#10B981',
            'red': '#EF4444',
            'pink': '#EC4899',
            'gray': '#6B7280'
        }
        bg_color = colors_map.get(color, '#6B7280')
        
        return format_html(
            '<span style="background-color: {}; color: white; padding: 4px 12px; '
            'border-radius: 12px; font-size: 11px; font-weight: 600;">{}</span>',
            bg_color,
            obj.get_message_type_display()
        )
    message_type_badge.short_description = 'Type'
    
    def status_badge(self, obj):
        """Display status as a colored badge"""
        color = obj.get_status_color()
        colors_map = {
            'blue': '#3B82F6',
            'yellow': '#F59E0B',
            'green': '#10B981',
            'gray': '#6B7280'
        }
        bg_color = colors_map.get(color, '#6B7280')
        
        return format_html(
            '<span style="background-color: {}; color: white; padding: 4px 12px; '
            'border-radius: 12px; font-size: 11px; font-weight: 600;">{}</span>',
            bg_color,
            obj.get_status_display()
        )
    status_badge.short_description = 'Status'
    
    def mark_as_read(self, request, queryset):
        """Mark selected messages as read"""
        updated = queryset.update(is_read=True)
        self.message_user(request, f'{updated} message(s) marked as read.')
    mark_as_read.short_description = 'Mark as read'
    
    def mark_as_unread(self, request, queryset):
        """Mark selected messages as unread"""
        updated = queryset.update(is_read=False)
        self.message_user(request, f'{updated} message(s) marked as unread.')
    mark_as_unread.short_description = 'Mark as unread'
    
    def mark_as_in_progress(self, request, queryset):
        """Mark selected messages as in progress"""
        updated = queryset.update(status='in_progress')
        self.message_user(request, f'{updated} message(s) marked as in progress.')
    mark_as_in_progress.short_description = 'Mark as in progress'
    
    def mark_as_resolved(self, request, queryset):
        """Mark selected messages as resolved"""
        updated = queryset.update(status='resolved')
        self.message_user(request, f'{updated} message(s) marked as resolved.')
    mark_as_resolved.short_description = 'Mark as resolved'
    
    def mark_as_closed(self, request, queryset):
        """Mark selected messages as closed"""
        updated = queryset.update(status='closed')
        self.message_user(request, f'{updated} message(s) marked as closed.')
    mark_as_closed.short_description = 'Mark as closed'
    
    def has_add_permission(self, request):
        """Disable adding messages from admin (they should come from the form)"""
        return False
    
    class Media:
        css = {
            'all': ('admin/css/custom_admin.css',)
        }