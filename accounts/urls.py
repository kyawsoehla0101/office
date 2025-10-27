from django.urls import path
from . import views

urlpatterns = [
    path('', views.login, name='login'),
    path('add-user/', views.add_user, name='admin.add_user'),
]
