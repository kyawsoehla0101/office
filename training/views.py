from django.shortcuts import render
from django.utils import timezone
from datetime import timedelta

def index(request):
    context = {
        "active_students": 256,
        "new_students_this_month": 14,
        "ongoing_courses": 12,
        "certificates_issued": 480,
        "new_certificates_today": 5,
        "active_instructors": 8,
        "courses_per_instructor": 3,
        "last_course_update": timezone.now() - timedelta(days=1),
        "top_courses": [
            {"name": "Python for Beginners", "instructor": "Mr. Hla Win", "students": 48, "completion_rate": 92},
            {"name": "Advanced Django", "instructor": "Ms. Thandar", "students": 36, "completion_rate": 85},
            {"name": "AI & Machine Learning", "instructor": "Dr. Kyaw Soe", "students": 40, "completion_rate": 78},
        ],
        "recent_activities": [
            {"type": "enroll", "message": "👨‍🎓 New student enrolled in 'Python for Beginners'", "timestamp": timezone.now() - timedelta(hours=2)},
            {"type": "complete", "message": "🎉 3 students completed 'Advanced Django'", "timestamp": timezone.now() - timedelta(hours=4)},
            {"type": "enroll", "message": "📚 New batch started for 'AI & ML Basics'", "timestamp": timezone.now() - timedelta(hours=7)},
        ],
    }
    return render(request, "pages/training/index.html", context)
