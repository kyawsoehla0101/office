from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='set.index'),
    path('members/', views.members, name='set.members'),
    path('add-report/', views.addReport, name='set.add-report'),
    path('projects/', views.projects, name='set.projects'),
    path('add-member/', views.addMember, name='set.add-member'),
    path('edit-member/<uuid:id>/', views.editMember, name='set.edit-member'),
    path('member-detail/<uuid:id>/', views.memberDetail, name='set.member-detail'),
    path('delete-member/<uuid:id>/', views.deleteMember, name='set.delete-member'),
    path('requirements/', views.requirements, name='set.requirements'),
    path('add-requirement/', views.addRequirement, name='set.add-requirement'),
    path('report/', views.report, name='set.report'),
    path('add-project/', views.addProject, name='set.add-project'),
    path('edit-project/<uuid:id>/', views.editProject, name='set.edit-project'),
    path('project-detail/<uuid:id>/', views.detailProject, name='set.project-detail'),
    path('delete-project/<uuid:id>/', views.deleteProject, name='set.delete-project'),
]
