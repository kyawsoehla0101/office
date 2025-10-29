from django.shortcuts import render
from django.utils import timezone
from datetime import timedelta
from django.shortcuts import get_object_or_404, redirect
from django.contrib import messages
from set.decorators import set_required
from django.contrib.auth.decorators import login_required
from set.models import Member, Project
from accounts.utils.decorators import role_required

# SET Index View
@role_required("set")
def index(request):
    context = {
        "active_menu": "set_index",
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
@login_required(login_url="login")
@role_required("set", "admin")
def members(request):
    members = Member.objects.all().order_by("department", "position")
    total_active_members = members.filter(is_active=True).count()
    total_genders = members.values_list("gender", flat=True).distinct().count()
    total_male_members = members.filter(gender=Member.GENDER_CHOICES[0][0]).count()
    total_female_members = members.filter(gender=Member.GENDER_CHOICES[1][0]).count()  
    total_positions = members.values_list("position", flat=True).distinct().count()
    total_inactive_members = members.filter(is_active=False).count()    

    context = {
        "members": members,
        "total_members": len(members),
        "total_projects": 8,
        "total_departments": 2,
        "total_active_members": total_active_members,
        "total_genders": total_genders,
        "total_male_members": total_male_members,
        "total_female_members": total_female_members,
        "total_positions": total_positions,
        "total_inactive_members": total_inactive_members,
        "active_menu": "set_members",
    }
    return render(request, 'pages/set/members/members.html', context)

def addReport(request):
    return render(request, 'pages/set/add-report.html', {
        "active_menu": "set_report"
    })    

def projects(request):
    projects = Project.objects.all().order_by("status", "priority")
    total_projects = len(projects)
    total_active_projects = projects.filter(status=Project.STATUS_CHOICES[0][0]).count()
    total_inactive_projects = projects.filter(status=Project.STATUS_CHOICES[1][0]).count()
    total_planning_projects = projects.filter(status=Project.STATUS_CHOICES[0][0]).count()
    total_completed_projects = projects.filter(status=Project.STATUS_CHOICES[2][0]).count()
    total_ongoing_projects = projects.filter(status=Project.STATUS_CHOICES[1][0]).count()
    total_on_hold_projects = projects.filter(status=Project.STATUS_CHOICES[3][0]).count()
    total_cancelled_projects = projects.filter(status=Project.STATUS_CHOICES[4][0]).count()
    total_priorities = projects.values_list("priority", flat=True).distinct().count()
    total_low_priority_projects = projects.filter(priority=Project.PRIORITY_CHOICES[0][0]).count()
    total_medium_priority_projects = projects.filter(priority=Project.PRIORITY_CHOICES[1][0]).count()
    total_high_priority_projects = projects.filter(priority=Project.PRIORITY_CHOICES[2][0]).count()


    context = {
        "projects": projects,
        "total_projects": total_projects,
        "total_active_projects": total_active_projects,
        "total_inactive_projects": total_inactive_projects,
        "total_planning_projects": total_planning_projects,
        "total_completed_projects": total_completed_projects,
        "total_ongoing_projects": total_ongoing_projects,
        "total_priorities": total_priorities,
        "total_low_priority_projects": total_low_priority_projects,
        "total_medium_priority_projects": total_medium_priority_projects,
        "total_high_priority_projects": total_high_priority_projects,
        "total_on_hold_projects": total_on_hold_projects,
        "total_cancelled_projects": total_cancelled_projects,
        "active_menu": "set_projects",
    }
    return render(request, 'pages/set/projects/projects.html', context)

@role_required("set")
def addMember(request):
    positions = Member.POSITION_CHOICES
    ranks = Member.RANK_CHOICES
    genders = Member.GENDER_CHOICES
    context = {
        "active_menu": "set_members",
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
        # if not profile_photo:
        #     messages.error(request, "Profile photo is required.")
        #     return redirect("set.add_member")
            


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
        return redirect("set.members")

    return render(request, "pages/set/members/add-member.html", context)

@set_required
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

def memberDetail(request, id):
    member = get_object_or_404(Member, id=id)
    context = {
        "active_menu": "set_members",
        "member": member,
    }
    return render(request, 'pages/set/members/member-detail.html', context) 
@set_required
def deleteMember(request,id):
    member = get_object_or_404(Member, id=id)
    context = {
        "active_menu": "set_members",
        "member": member,
    }
    if request.method == "POST":
        member.delete()
        messages.success(request, f"Member '{member.full_name}' deleted successfully.")
        return redirect('set.members')
    return render(request, 'pages/set/members/member-delete.html', context)

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
    return render(request, "pages/set/requirements/requirements.html", {
        "requirements": requirements,
        "active_menu": "set_requirements"
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

    return render(request, "pages/set/requirements/add-requirement.html", {
        "active_menu": "set_requirements"
    })

def report(request):
    reports = [
        {"title": "Report 1", "department": "Software Engineering Team", "author": "Aung Kyaw", "created_at": timezone.now() - timedelta(days=1)},
        {"title": "Report 2", "department": "Software Engineering Team", "author": "Thandar Hlaing", "created_at": timezone.now() - timedelta(days=2)},
        {"title": "Report 3", "department": "Software Engineering Team", "author": "Ko Ko", "created_at": timezone.now() - timedelta(days=3)},
    ]
    context = {
        "reports": reports,
        "active_menu": "set_report",
    }
    return render(request, "pages/set/reports/report.html", context)

def addProject(request):
    members = Member.objects.all()
    statuses = Project.STATUS_CHOICES
    priorities = Project.PRIORITY_CHOICES   

    context = {
        "members": members,
        "statuses": statuses,   
        "active_menu": "set_projects",
        "priorities": priorities,
    }
    if request.method == "POST":
        title = request.POST.get("title")
        desc = request.POST.get("description")
        document = request.FILES.get("document")
        priority = request.POST.get("priority")
        start_date = request.POST.get("start_date")
        deadline = request.POST.get("deadline")
        team_lead_id = request.POST.get("lead")
        member_ids = request.POST.getlist("members")
        status = request.POST.get("status")
        document = request.FILES.get("document")

        project  = Project.objects.create(
            title=title,
            description=desc,
            created_by=request.user,
            status=status,
            project_document=document,
            priority=priority,
            start_date=start_date,
            deadline=deadline,
        )

        # ✅ team_lead assign
        if team_lead_id:
            try:
                project.team_lead = Member.objects.get(id=team_lead_id)
            except Member.DoesNotExist:
                pass
            project.save()

        # ✅ members assign (ManyToMany)
        if member_ids:
            project.members.set(member_ids)
        messages.success(request, "Project submitted successfully.")
        return redirect("set.projects")
    return render(request, 'pages/set/projects/add-project.html', context)


def editProject(request, id):
    context = {
        "active_menu": "set_projects",
        "priorities": Project.PRIORITY_CHOICES,
        "statuses": Project.STATUS_CHOICES,
        "members": Member.objects.all(),
    }
    project = get_object_or_404(Project, id=id)
    if request.method == "POST":
        project.title = request.POST.get("title")
        project.description = request.POST.get("description")
        project.lead = request.POST.get("lead")
        project.priority = request.POST.get("priority")
        project.start_date = request.POST.get("start_date")
        project.deadline = request.POST.get("deadline")
        project.members.set(request.POST.getlist("members"))
        project.status = request.POST.get("status")
        project_document = request.FILES.get("document")
        if project_document:
            project.project_document = project_document
        project.save()
        messages.success(request, f"Project '{project.title}' updated successfully.")
        return redirect("set.projects")
    context["project"] = project
    return render(request, "pages/set/projects/edit-project.html", context)

def detailProject(request, id):
    # project = get_object_or_404(Project, id=id)
    project = get_object_or_404(Project, id=id)
    return render(request, "pages/set/projects/project-detail.html", {
        "project": project,
        "active_menu": "set_projects"
    })

def deleteProject(request, id):
    project = get_object_or_404(Project, id=id)
    if request.method == "POST":
        project.delete()
        messages.success(request, f"Project '{project.title}' deleted successfully.")
        return redirect("set.projects")
    return render(request, "pages/set/projects/project-delete.html", {
        "project": project,
        "active_menu": "set_projects"
    })