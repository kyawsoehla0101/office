from django.shortcuts import render, redirect
from django.contrib import messages
from django.utils import timezone
from datetime import timedelta
from django.contrib.auth.decorators import login_required
from accounts.utils.decorators import role_required
from accounts.models import CustomUser
from base.models import SystemSettings



@login_required(login_url="/")
@role_required("admin")
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
@role_required("admin")
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

@login_required(login_url="/")
@role_required("admin")
def admin_settings(request):
    # Settings record တစ်ခုမရှိရင် auto create
    settings_obj, created = SystemSettings.objects.get_or_create(id=1)

    if request.method == "POST":
        # POST data ထဲက values ကို update
        settings_obj.system_name = request.POST.get("system_name", settings_obj.system_name)
        settings_obj.organization = request.POST.get("organization", settings_obj.organization)

        settings_obj.email_notifications = "email_notifications" in request.POST
        settings_obj.system_warnings = "system_warnings" in request.POST
        settings_obj.weekly_reports = "weekly_reports" in request.POST

        settings_obj.session_timeout = int(request.POST.get("session_timeout", 30))

        settings_obj.save()

        messages.success(request, "✅ Settings saved successfully!")
        return redirect("admin.settings")

    # GET request → form values show
    context = {
        "system_name": settings_obj.system_name,
        "organization": settings_obj.organization,
        "email_notifications": settings_obj.email_notifications,
        "system_warnings": settings_obj.system_warnings,
        "weekly_reports": settings_obj.weekly_reports,
        "session_timeout": settings_obj.session_timeout,
        "active_menu": "admin_settings",
    }
    return render(request, "pages/admin/settings.html", context)