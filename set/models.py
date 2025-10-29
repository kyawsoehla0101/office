from hashlib import blake2b
from django.db import models
import uuid
from accounts.models import CustomUser   # link with your user table

class Member(models.Model):
    GENDER_CHOICES = [
        ('male', 'Male'),
        ('female', 'Female'),
    ]
    RANK_CHOICES = [
        ('private', 'Private'),
        ('lance_corporal', 'Lance Corporal'),
        ('coporal', 'Coporal'),
        ('sergeant', 'Sergeant'),
        ('warrant_officer_class-1', 'Warrant Officer Class - I'),
        ('warrant_officer_class-2', 'Warrant Officer Class - II'),
        ('second Lieutenant', 'Second Lieutenant'),
        ('lieutenant', 'Lieutenant'),
        ('captain', 'Captain'),
        ('major', 'Major'),
        ('colonel', 'Colonel'),
        ('general', 'General'),

    ]
    DEPARTMENT_CHOICES = [
        ("SET", "Software Engineering Team"),
        ("HET", "Hardware Engineering Team"),
        ("TRAINING", "Training & Learning"),
    ]
    POSITION_CHOICES = [
        ("developer", "Developer"),
        ("designer", "UI/UX Designer"),
        ("mobile_developer", "Mobile Developer"),
        ("server_admin", "Server Administrator"),
        ("tester", "Tester"),
        ("manager", "Project Manager"),
        ("intern", "Intern"),
    ]

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    user = models.ForeignKey(
        CustomUser, on_delete=models.CASCADE,
        related_name="set_members", null=True, blank=True,
        help_text="If this member is linked to a user account"
    )
    department = models.CharField(max_length=30, choices=DEPARTMENT_CHOICES, editable=False, blank=True, null=True)
    gender = models.CharField(max_length=10, choices=GENDER_CHOICES, blank=True, null=True)
    birth_date = models.DateField(blank=True, null=True)
    rank = models.CharField(max_length=50, choices=RANK_CHOICES, blank=True, null=True)
    full_name = models.CharField(max_length=150)
    reg_no = models.CharField(max_length=10, unique=True)
    position = models.CharField(max_length=50, choices=POSITION_CHOICES)
    joined_date = models.DateField(auto_now_add=True)
    is_active = models.BooleanField(default=True)
    bio = models.TextField(blank=True, null=True)

    # Optional: project link (if SET has Projects model)
    # project = models.ForeignKey(
    #     "set.Project", on_delete=models.SET_NULL,
    #     null=True, blank=True, related_name="members"
    # )

    profile_photo = models.ImageField(
        upload_to="members/photos/", blank=True, null=True,
        help_text="Optional profile picture"
    )

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    def save(self, *args, **kwargs):
        """Auto set department if not manually specified"""
        if not self.department and self.user:
            self.department = self.user.role.upper()
        super().save(*args, **kwargs)
    class Meta:
        verbose_name = "SET Member"
        verbose_name_plural = "SET Members"
        ordering = ["-created_at"]
    def get_profile_photo_url(self):
        """Return actual file or fallback default"""
        if self.profile_photo and hasattr(self.profile_photo, "url"):
            return self.profile_photo.url
        from django.templatetags.static import static
        return static("profile/default-profile.png")


class Project(models.Model):
    STATUS_CHOICES = [
        ("PLANNING", "Planning"),
        ("ONGOING", "Ongoing"),
        ("COMPLETED", "Completed"),
        ("ONHOLD", "On Hold"),
        ("CANCELLED", "Cancelled"),
    ]

    PRIORITY_CHOICES = [
        ("LOW", "Low"),
        ("MEDIUM", "Medium"),
        ("HIGH", "High"),
    ]

    # Basic info
    title = models.CharField(max_length=200)
    description = models.TextField(blank=True, null=True)

    # Relationships
    team_lead = models.ForeignKey(
        Member,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="led_projects"
    )
    members = models.ManyToManyField(
        Member,
        blank=True,
        related_name="member_projects",
        help_text="Select members working on this project"
    )

    # Status & Dates
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default="PLANNING")
    priority = models.CharField(max_length=10, choices=PRIORITY_CHOICES, default="MEDIUM")
    start_date = models.DateField()
    deadline = models.DateField(blank=True, null=True)
    # progress = models.IntegerField(default=0, help_text="Project progress percentage (0-100)")
    project_document = models.FileField(
        upload_to="set/projects/docs/", blank=True, null=True,
        help_text="Optional project document"
    )
    # Meta info
    created_by = models.ForeignKey(
        CustomUser, on_delete=models.CASCADE, related_name="created_projects"
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ["-created_at"]
        verbose_name = "Project"
        verbose_name_plural = "Projects"

    def __str__(self):
        return f"{self.title} ({self.status})"

    @property
    def total_members(self):
        return self.members.count()
    members_list = property(lambda self: self.members.all())
    full_members_list = property(lambda self: [member.full_name for member in self.members_list])
    @property
    def duration_days(self):
        if self.start_date and self.end_date:
            return (self.end_date - self.start_date).days
        return None
    def get_status_display(self):
        return dict([(value, key) for key, value in self.STATUS_CHOICES]).get(self.status, self.status.title())
