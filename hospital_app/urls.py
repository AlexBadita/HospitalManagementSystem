from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='hospital-home'),
    path('contact/', views.contact, name='hospital-contact'),
]