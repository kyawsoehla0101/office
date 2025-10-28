from django.shortcuts import render
from django.utils import timezone
from datetime import timedelta
# from django.contrib.auth import get_user_model

# User = get_user_model()
from django.contrib.auth.decorators import login_required
from accounts.decorators import admin_required
from accounts.models import CustomUser

@login_required(login_url="/")
@admin_required
def dashboard(request):
    context = {
        "active_menu": "admin_index",
        "today": timezone.now(),
        "software_count": 8,
        "hardware_count": 4,
        "training_count": 5,
        "software_last_updated": timezone.now(),
        "hardware_last_updated": timezone.now() - timedelta(days=2),
        "training_last_updated": timezone.now() - timedelta(days=1),
        "total_departments": 3,
        "total_members": 124,
        "total_projects": 19,
        "software_progress": 80,
        "hardware_progress": 65,
        "training_progress": 90,
        "notifications": [
            {"message": "New user registered for training program", "level": "info", "timestamp": timezone.now() - timedelta(hours=1)},
            {"message": "Hardware inventory needs review", "level": "warning", "timestamp": timezone.now() - timedelta(hours=3)},
        ],
        "recent_actions": [
            {"type": "add", "message": "Added new Software project 'Quick Chat'", "timestamp": timezone.now() - timedelta(hours=2)},
            {"type": "update", "message": "Updated team member roles", "timestamp": timezone.now() - timedelta(hours=5)},
        ],
    }
    return render(request, 'pages/admin/dashboard.html', context)

@login_required(login_url="/")
@admin_required
def users(request):
    users = CustomUser.objects.all().order_by('id')
    total_users = len(users)
    total_admins = sum(1 for user in users if user.role == "admin")
    
    total_active = sum(1 for user in users if user.is_active)
    total_inactive = total_users - total_active

    context = {
        "total_users": total_users, 
        "total_admins": total_admins,
        "total_active": total_active,   
        "total_inactive": total_inactive,
        "active_menu": "admin_users",
        "users": users,
    }
    # users = User.objects.all().order_by('id')
    # total_users = users.count()
    # total_admins = users.filter(is_superuser=True).count()
    # total_active = users.filter(is_active=True).count()
    # context = {
    #     "users": users,
    #     "total_users": total_users,
    #     "total_admins": total_admins,
    #     "total_active": total_active,
    # }
    return render(request, 'pages/admin/users.html', context)

# views.py
from django.shortcuts import render

def settings(request):
    if request.method == 'POST':
        # handle form save logic here
        pass

    context = {
        "active_menu": "admin_settings",
        'system_name': 'Engineering Management Dashboard',
        'organization': 'Software Engineering Team II',
        'theme': 'light',
        'email_notifications': True,
        'system_warnings': True,
        'weekly_reports': False,
        'min_password_length': 8,
        'session_timeout': 30,
    }
    return render(request, 'pages/admin/settings.html', context)
