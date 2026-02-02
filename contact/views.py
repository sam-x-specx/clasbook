# contact/views.py
from django.shortcuts import render, redirect
from django.contrib import messages
from django.views.decorators.http import require_http_methods
from django.core.exceptions import ValidationError
from django.core.validators import validate_email
from django.urls import reverse
from .models import ContactMessage


def contact_page(request):
    """Display the contact page"""
    return render(request, 'contact/contact.html')


@require_http_methods(["POST"])
def submit_contact(request):
    """Handle contact form submission"""
    
    try:
        # Get form data
        name = request.POST.get('name', '').strip()
        email = request.POST.get('email', '').strip()
        subject = request.POST.get('subject', '').strip()
        message_type = request.POST.get('message_type', '').strip()
        message = request.POST.get('message', '').strip()
        
        # Validation
        errors = []
        
        if not name:
            errors.append("Name is required.")
        elif len(name) < 2:
            errors.append("Name must be at least 2 characters long.")
        elif len(name) > 200:
            errors.append("Name must not exceed 200 characters.")
            
        if not email:
            errors.append("Email is required.")
        else:
            try:
                validate_email(email)
            except ValidationError:
                errors.append("Please enter a valid email address.")
        
        if not subject:
            errors.append("Subject is required.")
        elif len(subject) < 3:
            errors.append("Subject must be at least 3 characters long.")
        elif len(subject) > 300:
            errors.append("Subject must not exceed 300 characters.")
        
        if not message_type:
            errors.append("Please select a message type.")
        elif message_type not in dict(ContactMessage.MESSAGE_TYPES).keys():
            errors.append("Invalid message type selected.")
        
        if not message:
            errors.append("Message is required.")
        elif len(message) < 10:
            errors.append("Message must be at least 10 characters long.")
        elif len(message) > 5000:
            errors.append("Message must not exceed 5000 characters.")
        
        # If there are validation errors, show them and redirect back
        if errors:
            for error in errors:
                messages.error(request, error)
            # Use reverse to get the URL
            return redirect(reverse('contact:contact_page'))
        
        # Get additional metadata
        ip_address = get_client_ip(request)
        user_agent = request.META.get('HTTP_USER_AGENT', '')[:500]  # Limit length
        
        # Create and save the contact message
        contact_message = ContactMessage.objects.create(
            name=name,
            email=email,
            subject=subject,
            message_type=message_type,
            message=message,
            ip_address=ip_address,
            user_agent=user_agent,
        )
        
        # Success message
        messages.success(
            request, 
            "Thank you for contacting us! Your message has been received. "
            "We'll get back to you within 24 hours."
        )
        
        # Optional: Send email notification to admin
        # Uncomment and configure if you want email notifications
        # send_admin_notification(contact_message)
        # send_auto_reply(contact_message)
        
        # Use reverse to get the URL
        return redirect(reverse('contact:contact_page'))
        
    except Exception as e:
        # Log the error in production
        print(f"Error in contact form: {e}")
        messages.error(
            request, 
            "An error occurred while submitting your message. Please try again later."
        )
        # Use reverse to get the URL, with fallback to root
        try:
            return redirect(reverse('contact:contact_page'))
        except:
            return redirect('/')


def get_client_ip(request):
    """Get the client's IP address from the request"""
    x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
    if x_forwarded_for:
        ip = x_forwarded_for.split(',')[0]
    else:
        ip = request.META.get('REMOTE_ADDR')
    return ip


# Optional: Email notification function
# Uncomment and configure SMTP settings in settings.py to use this
"""
from django.core.mail import send_mail
from django.conf import settings

def send_admin_notification(contact_message):
    '''Send email notification to admin when new message is received'''
    try:
        subject = f'New Contact Message: {contact_message.subject}'
        message = f'''
New contact message received:

Name: {contact_message.name}
Email: {contact_message.email}
Subject: {contact_message.subject}
Type: {contact_message.get_message_type_display()}

Message:
{contact_message.message}

---
Submitted at: {contact_message.created_at.strftime('%Y-%m-%d %H:%M:%S')}
IP Address: {contact_message.ip_address}
        '''
        
        send_mail(
            subject=subject,
            message=message,
            from_email=settings.DEFAULT_FROM_EMAIL,
            recipient_list=[settings.EMAIL_HOST_USER],  # Send to the configured email
            fail_silently=True,
        )
    except Exception as e:
        # Log error but don't stop the process
        print(f"Failed to send admin notification: {e}")


def send_auto_reply(contact_message):
    '''Send automatic reply to the person who submitted the form'''
    try:
        subject = f'Re: {contact_message.subject}'
        message = f'''
Dear {contact_message.name},

Thank you for contacting us! We have received your message and will respond within 24 hours during business days.

Your inquiry details:
Subject: {contact_message.subject}
Type: {contact_message.get_message_type_display()}

If you have any urgent matters, please feel free to call us directly at +91 98765 43210.

Best regards,
The classBook Team

---
This is an automated message. Please do not reply to this email.
        '''
        
        send_mail(
            subject=subject,
            message=message,
            from_email=settings.DEFAULT_FROM_EMAIL,
            recipient_list=[contact_message.email],
            fail_silently=True,
        )
    except Exception as e:
        # Log error but don't stop the process
        print(f"Failed to send auto-reply: {e}")
"""