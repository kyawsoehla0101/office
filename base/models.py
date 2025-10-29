# adminpanel/models.py
from django.db import models

class SystemSettings(models.Model):
    system_name = models.CharField(max_length=100, default="Engineering Management Dashboard")
    organization = models.CharField(max_length=100, default="Software Engineering Team II")


    email_notifications = models.BooleanField(default=True)
    system_warnings = models.BooleanField(default=True)
    weekly_reports = models.BooleanField(default=False)

    session_timeout = models.PositiveIntegerField(default=30)

    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.system_name} Settings"
