from django.db import models
from django.contrib.auth.models import User


class UserProfile(models.Model):
    ROLE_STUDENT = "student"
    ROLE_ADMIN = "admin"
    ROLE_PLACEMENT_OFFICER = "placement_officer"
    ROLE_EMPLOYER = "employer"

    ROLE_CHOICES = [
        (ROLE_STUDENT, "Student"),
        (ROLE_ADMIN, "Admin"),
        (ROLE_PLACEMENT_OFFICER, "Placement Officer"),
        (ROLE_EMPLOYER, "Employer"),
    ]

    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name="profile")
    role = models.CharField(max_length=30, choices=ROLE_CHOICES, default=ROLE_STUDENT)

    def __str__(self):
        return f"{self.user.username} ({self.role})"
