# contact/urls.py
from django.urls import path
from . import views

app_name = 'contact'

urlpatterns = [
    path('', views.contact_page, name='contact_page'),  # This matches the redirect in views.py
    path('submit/', views.submit_contact, name='submit_contact'),
]