from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='training.index'),
    path('students/', views.students, name='training.students'),
]
