from django.urls import path
from . import views

urlpatterns = [
    path('', views.dashboard, name='dashboard'),
    path('users/', views.users, name='admin.users'),
    path('settings/', views.settings, name='admin.settings'),
]
