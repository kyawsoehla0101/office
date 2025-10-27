from django.shortcuts import render
from django.utils import timezone
from datetime import timedelta
from django.shortcuts import get_object_or_404, redirect
from django.contrib import messages

# Create your views here.
def index(request):
    context = {
        "active_developers": 42,
        "new_devs_this_month": 3,
        "ongoing_projects": 9,
        "commits_today": 158,
        "commits_growth": 12,
        "open_issues": 14,
        "critical_bugs": 2,
        "last_project_update": timezone.now() - timedelta(days=1),
        "projects": [
            {"name": "JobSeeker Portal", "lead": "Aung Kyaw", "progress": 85, "last_commit": timezone.now()},
            {"name": "Quick Chat App", "lead": "May Thazin", "progress": 70, "last_commit": timezone.now() - timedelta(hours=2)},
            {"name": "Resume Builder", "lead": "Min Htet", "progress": 95, "last_commit": timezone.now() - timedelta(hours=5)},
        ],
        "recent_activities": [
            {"type": "commit", "message": "🚀 Deployed new version of Resume Builder", "timestamp": timezone.now() - timedelta(hours=1)},
            {"type": "issue", "message": "❗ Fixed critical bug in authentication", "timestamp": timezone.now() - timedelta(hours=3)},
            {"type": "merge", "message": "✅ Merged new chat module (Socket.io)", "timestamp": timezone.now() - timedelta(hours=5)},
        ]
    }
    return render(request, 'pages/set/index.html', context)

def members(request):
    members = [
        {"emp_no": "SE-1001", "name": "Aung Kyaw", "rank": "Backend Developer", "is_active": True},
        {"emp_no": "SE-1002", "name": "Thandar Hlaing", "rank": "Frontend Developer", "is_active": True},
        {"emp_no": "SE-1003", "name": "Ko Ko", "rank": "UI/UX Designer", "is_active": False},
    ]
    context = {
        "members": members,
        "total_members": len(members),
        "total_projects": 8,
        "total_departments": 2,
        "active_menu": "set_members",
    }
    return render(request, 'pages/set/members.html', context)

def addReport(request):
    return render(request, 'pages/set/add-report.html')

def projects(request):
    projects = [
        {"name": "JobSeeker Portal", "lead": "Aung Kyaw", "progress": 85, "last_commit": timezone.now()},
        {"name": "Quick Chat App", "lead": "May Thazin", "progress": 70, "last_commit": timezone.now() - timedelta(hours=2)},
        {"name": "Resume Builder", "lead": "Min Htet", "progress": 95, "last_commit": timezone.now() - timedelta(hours=5)},
    ]
    context = {
        "projects": projects,
        "total_projects": len(projects),
        "active_menu": "set_projects",
    }
    return render(request, 'pages/set/projects.html', context)

def addMember(request):
    return render(request, 'pages/set/add-member.html')

def editMember(request):
    return render(request, 'pages/set/edit-member.html')

def memberDetail(request):
    return render(request, 'pages/set/member-detail.html')

def deleteMember(request):
    # member = get_object_or_404(Member, id=id)
    # if request.method == "POST":
    #     member.delete()
    #     messages.success(request, f"Member '{member.name}' deleted successfully.")
    #     return redirect('set.members')
    return render(request, 'pages/set/member-delete.html')

def requirements(request):
    requirements = [
        {
            "title": "Requirement 1",
            "description": "Description for Requirement 1",
            "submitted_by": "Aung Kyaw",
            "number" : "REQ-001",
            "team" : "Software Engineering Team",
            "created_at": timezone.now() - timedelta(days=1),
        },
        {
            "title": "Requirement 2",
            "description": "Description for Requirement 2",
            "submitted_by": "Thandar Hlaing",
            "number" : "REQ-002",   
            "team" : "Software Engineering Team",
            "created_at": timezone.now() - timedelta(days=2),
        },
        {
            "title": "Requirement 3",
            "description": "Description for Requirement 3",
            "submitted_by": "Ko Ko",
            "number" : "REQ-003",
            "team" : "Software Engineering Team",
            "created_at": timezone.now() - timedelta(days=3),
        },
        {
            "title": "Requirement 4",
            "description": "Description for Requirement 4",
            "submitted_by": "Ko Ko",
            "number" : "REQ-004",
            "team" : "Software Engineering Team",
            "created_at": timezone.now() - timedelta(days=4),
        },
    ]
    return render(request, "pages/set/requirements.html", {
        "requirements": requirements,
        # "active_menu": "set_requirements"
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
        return redirect("set.requirements")

    return render(request, "pages/set/add-requirement.html", {
        "active_menu": "set_requirements"
    })
