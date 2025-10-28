from django.shortcuts import render
from django.utils import timezone
from datetime import timedelta



# Create your views here.
def dashboard(request):
    context = {
        "active_menu": "het_index",
        "active_machines": 23,
        "new_devices_this_week": 4,
        "under_maintenance": 5,
        "repairs_completed": 17,
        "system_uptime": 99.2,
        "last_repair_update": timezone.now() - timedelta(days=1),
        "maintenance_logs": [
            {"device_name": "3D Printer 01", "technician": "Aung Ko", "status": "Completed", "last_checked": timezone.now() - timedelta(hours=3)},
            {"device_name": "Laser Cutter", "technician": "Thazin Win", "status": "Pending", "last_checked": timezone.now() - timedelta(hours=5)},
            {"device_name": "Microcontroller Batch #12", "technician": "Myo Min", "status": "In Progress", "last_checked": timezone.now() - timedelta(hours=6)},
        ],
        "recent_activities": [
            {"type": "repair", "message": "✅ Power supply of CNC machine replaced successfully", "timestamp": timezone.now() - timedelta(hours=1)},
            {"type": "issue", "message": "⚠️ Temperature sensor malfunction detected", "timestamp": timezone.now() - timedelta(hours=3)},
            {"type": "repair", "message": "🛠️ 3D printer nozzle cleaned and recalibrated", "timestamp": timezone.now() - timedelta(hours=5)},
        ],
    }
    return render(request, 'pages/het/index.html', context)

def members(request):
    members = [
        {"emp_no": "HW-1001", "name": "Myo Myo", "rank": "Engineer", "is_active": True},
        {"emp_no": "HW-1002", "name": "Aung Aung", "rank": "Technician", "is_active": False},
        {"emp_no": "HW-1003", "name": "Nyein Nyein", "rank": "Supervisor", "is_active": True},
    ]
    context = {
        "members": members,
        "total_members": len(members),
        "total_projects": 5,
        "total_departments": 2,
        "active_menu": "het_members",
    }
    return render(request, "pages/het/members/members.html", context)
def requirements(request):
    requirements = [
        {
            "title": "Requirement 1",
            "description": "Description for Requirement 1",
            "submitted_by": "Aung Kyaw",
            "number" : "REQ-001",
            "team" : "Hardware Engineering Team",
            "created_at": timezone.now() - timedelta(days=1),
        },
        {
            "title": "Requirement 2",
            "description": "Description for Requirement 2",
            "submitted_by": "Thandar Hlaing",
            "number" : "REQ-002",   
            "team" : "Hardware Engineering Team",
            "created_at": timezone.now() - timedelta(days=2),
        },
        {
            "title": "Requirement 3",
            "description": "Description for Requirement 3",
            "submitted_by": "Ko Ko",
            "number" : "REQ-003",
            "team" : "Hardware Engineering Team",
            "created_at": timezone.now() - timedelta(days=3),
        },
        {
            "title": "Requirement 4",
            "description": "Description for Requirement 4",
            "submitted_by": "Ko Ko",
            "number" : "REQ-004",
            "team" : "Hardware Engineering Team",
            "created_at": timezone.now() - timedelta(days=4),
        },
    ]
    return render(request, "pages/het/requirements/requirements.html", {
        "requirements": requirements,
        "active_menu": "het_requirements"   
    })

def addRequirement(request):
    if request.method == "POST":
        title = request.POST.get("title")
        desc = request.POST.get("description")
        file = request.FILES.get("attachment")
        Requirement.objects.create(
            title=title,
            description=desc,
            submitted_by=request.user,
            attachment=file,
            status="pending",
        )
        messages.success(request, "Requirement submitted successfully.")
        return redirect("het.requirements")

    return render(request, "pages/het/requirements/add-requirement.html", {
        "active_menu": "het_requirements"
    })

def report(request):
    reports = [
        {"title": "Report 1", "department": "Software Engineering Team", "author": "Aung Kyaw", "created_at": timezone.now() - timedelta(days=1)},
        {"title": "Report 2", "department": "Software Engineering Team", "author": "Thandar Hlaing", "created_at": timezone.now() - timedelta(days=2)},
        {"title": "Report 3", "department": "Software Engineering Team", "author": "Ko Ko", "created_at": timezone.now() - timedelta(days=3)},
    ]
    context = {
        "reports": reports,
        "active_menu": "het_reports",
    }
    return render(request, "pages/het/reports/report.html", context)
def addReport(request):
    return render(request, 'pages/het/reports/add-report.html', {
        "active_menu": "het_reports"
    })
