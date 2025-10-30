import csv
from django.http import HttpResponse
from django.contrib import messages
from django.shortcuts import render,redirect,get_object_or_404
from django.utils import timezone
from datetime import timedelta
from .models import Member, HardwareRepair
from accounts.utils.decorators import role_required
from reportlab.lib.pagesizes import A4, landscape
from reportlab.pdfgen import canvas
from io import BytesIO
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle, Paragraph, Spacer
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.lib import colors
from datetime import datetime


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

def reports(request):
    q = request.GET.get("q", "")
    status = request.GET.get("status", "")
    repairs = HardwareRepair.objects.all().order_by("-completed_date")

    if q:
        repairs = repairs.filter(device_name__icontains=q) | repairs.filter(technician__full_name__icontains=q)
    if status:
        repairs = repairs.filter(status=status)

    return render(request, "pages/het/reports/reports.html", {
        "repairs": repairs,
        "status_choices": HardwareRepair.STATUS_CHOICES,
        "active_menu": "het_reports",
    })


def export_reports_csv(request):
    """Export repair reports to CSV"""
    response = HttpResponse(content_type="text/csv")
    response["Content-Disposition"] = 'attachment; filename="repair_reports.csv"'

    writer = csv.writer(response)
    writer.writerow(["Ticket ID", "Device Name", "Technician", "Status", "Completed Date", "Cost Estimate (MMK)"])

    repairs = HardwareRepair.objects.all()
    for r in repairs:
        writer.writerow([
            r.ticket_id,
            r.device_name,
            r.technician.full_name if r.technician else "-",
            r.get_status_display(),
            r.completed_date or "-",
            r.cost_estimate or "0",
        ])
    return response


# def export_reports_pdf(request):
#     """Export repair reports as table in PDF"""
#     buffer = BytesIO()
#     doc = SimpleDocTemplate(buffer, pagesize=landscape(A4))
#     elements = []
#     styles = getSampleStyleSheet()

#     header1 = Paragraph("<b>Arakan Army</b>", styles["Title"])
#     header = Paragraph("<b>Hardware Engineering Team</b>", styles["Title"])
#     title = Paragraph("<b>Hardware Repair Report Summary</b>", styles["Title"])
#     current_date = datetime.now().strftime("%Y-%m-%d %H:%M")
#     date_text = Paragraph(f"<para alignment='right'><b>Date:</b> {current_date}</para>", styles["Normal"])
#     # Make header as 2-column table (left title, right date)
    
#     head = Table([[date_text]], colWidths=[400, 200])
#     head.setStyle(TableStyle([
#         ("ALIGN", (0, 0), (0, 0), "LEFT"),
#         ("ALIGN", (1, 0), (1, 0), "RIGHT"),
#         ("VALIGN", (0, 0), (-1, -1), "MIDDLE"),
#         ("LEFTPADDING", (0, 0), (-1, -1), 100),
#         ("BOTTOMPADDING", (0, 0), (-1, -1), 8),
#     ]))
#     elements.append(header1)
#     elements.append(Spacer(1, 12))
#     elements.append(header)
#     elements.append(Spacer(1, 12))
#     elements.append(title)
#     elements.append(Spacer(1, 12))
#     elements.append(head)
#     elements.append(Spacer(1, 12))

#     # Table header
#     data = [
#         [
#             "Ticket ID",
#             "Device Name",
#             "Technician",
#             "Status",
#             "Start Date",
#             "Completed Date",
#             "Cost (MMK)",
#         ]
#     ]

#     # Query data
#     repairs = HardwareRepair.objects.all().order_by("-completed_date")
#     for r in repairs:
#         data.append([
#             r.ticket_id,
#             r.device_name,
#             r.technician.full_name if r.technician else "-",
#             r.get_status_display(),
#             r.start_date.strftime("%Y-%m-%d") if r.start_date else "-",
#             r.completed_date.strftime("%Y-%m-%d") if r.completed_date else "-",
#             f"{r.cost_estimate or 0:.2f}",
#         ])

#     # Create table
#     table = Table(data, colWidths=[90, 140, 120, 90, 100, 90])
#     table.setStyle(TableStyle([
#         ("BACKGROUND", (0, 0), (-1, 0), colors.HexColor("#1e293b")),  # dark header
#         ("TEXTCOLOR", (0, 0), (-1, 0), colors.white),
#         ("ALIGN", (0, 0), (-1, -1), "CENTER"),
#         ("FONTNAME", (0, 0), (-1, 0), "Helvetica-Bold"),
#         ("FONTSIZE", (0, 0), (-1, 0), 11),
#         ("BOTTOMPADDING", (0, 0), (-1, 0), 8),
#         ("BACKGROUND", (0, 1), (-1, -1), colors.whitesmoke),
#         ("GRID", (0, 0), (-1, -1), 0.25, colors.gray),
#     ]))

#     elements.append(table)
#     doc.build(elements)

#     pdf = buffer.getvalue()
#     buffer.close()

#     response = HttpResponse(content_type="application/pdf")
#     response["Content-Disposition"] = 'attachment; filename="repair_reports_table.pdf"'
#     response.write(pdf)
#     return response
def export_reports_pdf(request):
    buffer = BytesIO()
    doc = SimpleDocTemplate(buffer, pagesize=landscape(A4),topMargin=5,       # အပေါ် margin ကို လျှော့
    bottomMargin=5,
    leftMargin=30,
    rightMargin=30,)
    elements = []
    styles = getSampleStyleSheet()

    header = Paragraph("<b>Arakan Army</b>", styles["Title"])
    header2 = Paragraph("<b>Hardware Engineering Team</b>", styles["Title"])
    title = Paragraph("<b>Hardware Repair Report Summary</b>", styles["Title"])
    elements.append(header)
    elements.append(Spacer(1, 12))
    elements.append(header2)
    elements.append(Spacer(1, 12))
    elements.append(title)
    elements.append(Spacer(1, 12))

    # ---------- Table Data ----------
    data = [["Ticket ID", "Device Name", "Technician", "Status", "Start Date", "Completed Date", "Cost (MMK)"]]
    repairs = HardwareRepair.objects.all().order_by("-completed_date")

    for r in repairs:
        data.append([
            r.ticket_id,
            r.device_name,
            r.technician.full_name if r.technician else "-",
            r.get_status_display(),
            r.start_date.strftime("%Y-%m-%d") if r.start_date else "-",
            r.completed_date.strftime("%Y-%m-%d") if r.completed_date else "-",
            f"{r.cost_estimate or 0:.2f}",
        ])

    # ---------- Date Header Row (aligned with table) ----------
    current_date = datetime.now().strftime("%d, %B %Y")
    date_data = [["", "", "", "", "", "Date:", current_date]]  # same 6 columns as main table
    date_table = Table(date_data, colWidths=[90, 140, 120, 90, 100, 120])
    date_table.setStyle(TableStyle([
        ("SPAN", (0, 0), (3, 0)),  # merge first 4 columns
        ("ALIGN", (4, 0), (5, 0), "RIGHT"),
        ("FONTNAME", (4, 0), (5, 0), "Helvetica-Oblique"),
        ("TEXTCOLOR", (4, 0), (5, 0), colors.HexColor("#1e293b")),
        ("BACKGROUND", (0, 0), (-1, 0), colors.HexColor("#ffffff")),
        ("BOTTOMPADDING", (0, 0), (-1, 0), 6),
        ("TOPPADDING", (0, 0), (-1, 0), 6),
        ("LEFTPADDING", (0, 0), (-1, 0), 40),
    ]))

    # ---------- Main Table ----------
    main_table = Table(data, colWidths=[90, 140, 120, 90, 100, 120])
    main_table.setStyle(TableStyle([
        ("BACKGROUND", (0, 0), (-1, 0), colors.HexColor("#1e293b")),
        ("TEXTCOLOR", (0, 0), (-1, 0), colors.white),
        ("ALIGN", (0, 0), (-1, -1), "CENTER"),
        ("FONTNAME", (0, 0), (-1, 0), "Helvetica-Bold"),
        ("FONTSIZE", (0, 0), (-1, 0), 11),
        ("BOTTOMPADDING", (0, 0), (-1, 0), 8),
        ("GRID", (0, 0), (-1, -1), 0.25, colors.gray),
        ("BACKGROUND", (0, 1), (-1, -1), colors.whitesmoke),
    ]))

    # ---------- Combine ----------
    elements.append(date_table)
    elements.append(Spacer(1, 6))
    elements.append(main_table)

    doc.build(elements)
    pdf = buffer.getvalue()
    buffer.close()

    response = HttpResponse(content_type="application/pdf")
    response["Content-Disposition"] = 'attachment; filename="repair_reports_table.pdf"'
    response.write(pdf)
    return response

def addReport(request):
    return render(request, 'pages/het/reports/add-report.html', {
        "active_menu": "het_reports"
    })



def repairs(request):
    repairs = HardwareRepair.objects.select_related("technician").prefetch_related("support_team").all()

    context = {
        "active_menu": "het_repairs",
        "repairs": repairs,
        "total_repairs": repairs.count(),
        "pending_repairs": repairs.filter(status="pending").count(),
        "progress_repairs": repairs.filter(status="in_progress").count(),
        "completed_repairs": repairs.filter(status="completed").count(),
    }
    return render(request, "pages/het/repairs/repairs.html", context)

def addRepair(request):
    

    if request.method == "POST":
        data = request.POST
        repair = HardwareRepair.objects.create(
            device_name=data.get("device_name"),
            device_type=data.get("device_type"),
            issue_description=data.get("issue_description"),
            technician_id=data.get("technician") or None,
            priority=data.get("priority"),
            cost_estimate=data.get("cost_estimate") or None,
            created_by=request.user,
        )
        repair.support_team.set(request.POST.getlist("support_team"))
        if request.FILES.get("photo_before"):
            repair.photo_before = request.FILES["photo_before"]
        if request.FILES.get("report_document"):
            repair.report_document = request.FILES["report_document"]
        repair.save()
        messages.success(request, "Repair record added successfully!")
        return redirect("het.repairs")

    context = {
        "members": Member.objects.all(),
        "device_types": HardwareRepair.DEVICE_TYPE_CHOICES,
        "priorities": HardwareRepair.PRIORITY_CHOICES,
    }
    return render(request, "pages/het/repairs/add-repair.html", context)


def editRepair(request, id):

    repair = get_object_or_404(HardwareRepair, id=id)

    if request.method == "POST":
        data = request.POST
        repair.device_name = data.get("device_name")
        repair.device_type = data.get("device_type")
        repair.technician_id = data.get("technician") or None
        repair.priority = data.get("priority")
        repair.status = data.get("status")
        repair.repair_notes = data.get("repair_notes")
        repair.cost_estimate = data.get("cost_estimate") or None
        repair.start_date = data.get("start_date") or None
        repair.completed_date = data.get("completed_date") or None
        repair.support_team.set(request.POST.getlist("support_team"))

        if request.FILES.get("photo_after"):
            repair.photo_after = request.FILES["photo_after"]
        if request.FILES.get("report_document"):
            repair.report_document = request.FILES["report_document"]

        repair.save()
        messages.success(request, "Repair updated successfully!")
        return redirect("het.repairs")

    context = {
        "repair": repair,
        "members": Member.objects.all(),
        "device_types": HardwareRepair.DEVICE_TYPE_CHOICES,
        "status_choices": HardwareRepair.STATUS_CHOICES,
        "priorities": HardwareRepair.PRIORITY_CHOICES,
    }
    return render(request, "pages/het/repairs/edit-repair.html", context)

def view_repair(request, id):
    repair = get_object_or_404(HardwareRepair, id=id)
    context = {"repair": repair}
    return render(request, "pages/het/repairs/view-repair.html", context)
