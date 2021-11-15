from django.contrib import admin
from django.urls import path
from django.views.generic.base import TemplateView
from . import views

urlpatterns = [
    path('', TemplateView.as_view(template_name='home.html')),
    path('login/', views.scrape),
    path('test/', views.testing)
]
