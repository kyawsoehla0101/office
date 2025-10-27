from django.urls import path
from . import views

urlpatterns = [
    path('', views.dashboard, name='het.index'),
    path('members/', views.members, name='het.members'),
]
