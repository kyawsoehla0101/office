from django.urls import path
from . import views

urlpatterns = [
    path('', views.dashboard, name='het.index'),
    path('members/', views.members, name='het.members'),
    path('requirements/', views.requirements, name='het.requirements'),
    path('requirements/add/', views.addRequirement, name='het.add-requirement'),
    path('report/', views.report, name='het.report'),
    path('report/add/', views.addReport, name='het.add-report'),
]
