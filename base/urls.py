from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('member/', views.member, name='member'),
    path('add-report/', views.addReport, name='add-report'),
]
