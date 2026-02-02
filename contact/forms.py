# contact/forms.py
from django import forms
from .models import ContactMessage


class ContactForm(forms.ModelForm):
    """Form for contact submissions with validation"""
    
    class Meta:
        model = ContactMessage
        fields = ['name', 'email', 'subject', 'message_type', 'message']
        widgets = {
            'name': forms.TextInput(attrs={
                'class': 'w-full bg-gray-700 border border-gray-600 rounded-lg px-4 py-3 text-white placeholder-gray-400 focus:outline-none focus:border-blue-500 focus:ring-2 focus:ring-blue-500/20 transition-all',
                'placeholder': 'John Doe',
                'required': True,
            }),
            'email': forms.EmailInput(attrs={
                'class': 'w-full bg-gray-700 border border-gray-600 rounded-lg px-4 py-3 text-white placeholder-gray-400 focus:outline-none focus:border-blue-500 focus:ring-2 focus:ring-blue-500/20 transition-all',
                'placeholder': 'john@example.com',
                'required': True,
            }),
            'subject': forms.TextInput(attrs={
                'class': 'w-full bg-gray-700 border border-gray-600 rounded-lg px-4 py-3 text-white placeholder-gray-400 focus:outline-none focus:border-blue-500 focus:ring-2 focus:ring-blue-500/20 transition-all',
                'placeholder': 'How can we help you?',
                'required': True,
            }),
            'message_type': forms.Select(attrs={
                'class': 'w-full bg-gray-700 border border-gray-600 rounded-lg px-4 py-3 text-white focus:outline-none focus:border-blue-500 focus:ring-2 focus:ring-blue-500/20 transition-all',
                'required': True,
            }),
            'message': forms.Textarea(attrs={
                'class': 'w-full bg-gray-700 border border-gray-600 rounded-lg px-4 py-3 text-white placeholder-gray-400 focus:outline-none focus:border-blue-500 focus:ring-2 focus:ring-blue-500/20 transition-all resize-none',
                'placeholder': 'Tell us more about your inquiry...',
                'rows': 5,
                'required': True,
            }),
        }
        labels = {
            'name': 'Your Name',
            'email': 'Email Address',
            'subject': 'Subject',
            'message_type': 'Message Type',
            'message': 'Your Message',
        }
    
    def clean_name(self):
        """Validate name field"""
        name = self.cleaned_data.get('name', '').strip()
        if len(name) < 2:
            raise forms.ValidationError('Name must be at least 2 characters long.')
        if len(name) > 200:
            raise forms.ValidationError('Name must not exceed 200 characters.')
        return name
    
    def clean_subject(self):
        """Validate subject field"""
        subject = self.cleaned_data.get('subject', '').strip()
        if len(subject) < 3:
            raise forms.ValidationError('Subject must be at least 3 characters long.')
        if len(subject) > 300:
            raise forms.ValidationError('Subject must not exceed 300 characters.')
        return subject
    
    def clean_message(self):
        """Validate message field"""
        message = self.cleaned_data.get('message', '').strip()
        if len(message) < 10:
            raise forms.ValidationError('Message must be at least 10 characters long.')
        if len(message) > 5000:
            raise forms.ValidationError('Message must not exceed 5000 characters.')
        return message
