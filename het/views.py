from django.shortcuts import render
from django.utils import timezone
from datetime import timedelta



# Create your views here.
def dashboard(request):
    context = {
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
    return render(request, "pages/het/members.html", context)
