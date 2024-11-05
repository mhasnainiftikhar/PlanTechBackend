from django.contrib.auth.models import AbstractUser
from django.db import models
from django.utils import timezone
from django.contrib.auth.models import AbstractUser, Group, Permission


class User(AbstractUser):
    email = models.EmailField(unique=True)
    role = models.CharField(max_length=20, default='user')

    # Use custom related_name to avoid clashes
    groups = models.ManyToManyField(
        Group,
        related_name="custom_user_set",
        blank=True,
        help_text="The groups this user belongs to.",
        verbose_name="groups",
    )
    user_permissions = models.ManyToManyField(
        Permission,
        related_name="custom_user_set",
        blank=True,
        help_text="Specific permissions for this user.",
        verbose_name="user permissions",
    )


class Plant(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="plants")
    name = models.CharField(max_length=100)
    planting_date = models.DateField()
    soil_type = models.CharField(max_length=50, blank=True, null=True)


class GrowthHistory(models.Model):
    plant = models.ForeignKey(Plant, on_delete=models.CASCADE, related_name="growth_history")
    date = models.DateField(default=timezone.now)
    growth_stage = models.CharField(max_length=50)


class Notification(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="notifications")
    message = models.CharField(max_length=255)
    timestamp = models.DateTimeField(default=timezone.now)
    is_read = models.BooleanField(default=False)
