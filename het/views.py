from django.contrib import messages
from django.shortcuts import render,redirect,get_object_or_404
from django.utils import timezone
from datetime import timedelta
from .models import Member
from accounts.utils.decorators import role_required



# Dashboard View
@role_required("het")
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

# Members View
@role_required("het", "admin")
def members(request):
    members = Member.objects.all()
    context = {
        "active_menu": "het_members",
        "members": members,
    }
    return render(request, 'pages/het/members/members.html', context)

# Add Member View
@role_required("het", "admin")
def addMember(request):
    positions = Member.POSITION_CHOICES
    ranks = Member.RANK_CHOICES
    genders = Member.GENDER_CHOICES
    context = {
        "active_menu": "het_members",
        "positions": positions,
        "ranks": ranks, 
        "genders": genders,
    } 
    if request.method == "POST":
        reg_no = request.POST.get("reg_no")
        full_name = request.POST.get("full_name")
        position = request.POST.get("position")
        joined_date = request.POST.get("joined_date")
        position = request.POST.get("position")
        bio = request.POST.get("bio")
        profile_photo = request.FILES.get("profile_photo")
        rank = request.POST.get("rank")
        gender = request.POST.get("gender")
        birth_date = request.POST.get("birth_date")     
        # Auto assign department from user role
        department = request.user.role.upper()  # e.g. "set" → "SET"

        Member.objects.create(
            reg_no=reg_no,
            full_name=full_name,
            position=position,
            joined_date=joined_date,
            department=department,
            user=request.user,
            bio=bio,
            profile_photo=profile_photo,
            rank=rank,
            gender=gender,
            birth_date=birth_date,
        )
        
        messages.success(request, f"Member '{full_name}' added to {department} team.")
        return redirect("het.members")

    return render(request, "pages/het/members/add-member.html", context)

# Edit Member View
@role_required("het")
def editMember(request, id):
    member = get_object_or_404(Member, id=id)
    if request.method == "POST":
        member.full_name = request.POST.get("full_name")
        member.reg_no = request.POST.get("reg_no")
        member.rank = request.POST.get("rank")
        member.position = request.POST.get("position")
        member.joined_date = request.POST.get("joined_date")
        member.bio = request.POST.get("bio")
        member.gender = request.POST.get("gender")
        member.birth_date = request.POST.get("birth_date")
        member.is_active = bool(request.POST.get("is_active"))

        if request.FILES.get("profile_photo"):
            member.profile_photo = request.FILES["profile_photo"]

        member.save()
        messages.success(request, f"Member '{member.full_name}' updated successfully!")
        return redirect("set.members")

    context = {
        "active_menu": "set_members",
        "member": member,
        "ranks": Member.RANK_CHOICES,
        "positions": Member.POSITION_CHOICES,
        "genders": Member.GENDER_CHOICES,
    }
    return render(request, "pages/set/members/edit-member.html", context)

# Member Detail View
@role_required("het", "admin")
def memberDetail(request, id):
    member = get_object_or_404(Member, id=id)
    context = {
        "active_menu": "het_members",
        "member": member,
    }
    return render(request, 'pages/het/members/member-detail.html', context) 

# Delete Member View
@role_required("het")   
def deleteMember(request,id):
    member = get_object_or_404(Member, id=id)
    context = {
        "active_menu": "het_members",
        "member": member,
    }
    if request.method == "POST":
        member.delete()
        messages.success(request, f"Member '{member.full_name}' deleted successfully.")
        return redirect('het.members')
    return render(request, 'pages/het/members/member-delete.html', context)


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
