from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='set.index'),
    path('members/', views.members, name='set.members'),
    path('add-report/', views.addReport, name='set.add-report'),
    path('projects/', views.projects, name='set.projects'),
    path('add-member/', views.addMember, name='set.add-member'),
    path('edit-member/', views.editMember, name='set.edit-member'),
    path('member-detail/', views.memberDetail, name='set.member-detail'),
    path('delete-member/', views.deleteMember, name='set.delete-member'),
    path('requirements/', views.requirements, name='set.requirements'),
    path('add-requirement/', views.addRequirement, name='set.add-requirement'),
]
