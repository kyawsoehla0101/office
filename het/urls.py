from django.urls import path
from . import views

urlpatterns = [
    path('', views.dashboard, name='het.index'),
    path('members/', views.members, name='het.members'),
    path('add-member/', views.addMember, name='het.add-member'),
    path('edit-member/<uuid:id>/', views.editMember, name='het.edit-member'),
    path('member-detail/<uuid:id>/', views.memberDetail, name='het.member-detail'),
    path('delete-member/<uuid:id>/', views.deleteMember, name='het.delete-member'),
    path('requirements/', views.requirements, name='het.requirements'),
    path('requirements/add/', views.addRequirement, name='het.add-requirement'),
    path('report/', views.report, name='het.report'),
    path('report/add/', views.addReport, name='het.add-report'),
]
