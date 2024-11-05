from django.db import models

from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin
from django.db import models

class UserManager(BaseUserManager):
    def create_user(self, email, password=None, **extra_fields):
        """Create and return a 'User' with an email and password."""
        if not email:
            raise ValueError('The Email field must be set')
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, password=None, **extra_fields):
        """Create and return a superuser with an email and password."""
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)

        return self.create_user(email, password, **extra_fields)

class User(AbstractBaseUser, PermissionsMixin):
    email = models.EmailField(unique=True)
    username = models.CharField(max_length=150, unique=True)  # Username field
    password_hash = models.CharField(max_length=255)
    create_date = models.DateTimeField(auto_now_add=True)

    # Required fields for user model
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username']  # Username is now a required field

    objects = UserManager()

    def __str__(self):
        return self.email
    
# UserPlant model
class UserPlant(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    plant_name = models.CharField(max_length=255)
    planting_date = models.DateField()
    plant_type_id = models.ForeignKey('PlantType', on_delete=models.SET_NULL, null=True)

    def _str_(self):
        return self.plant_name

# PlantDiagnosis model
class PlantDiagnosis(models.Model):
    user_plant = models.ForeignKey(UserPlant, on_delete=models.CASCADE)
    disease = models.ForeignKey('PlantDisease', on_delete=models.CASCADE)
    diagnosis_date = models.DateField()
    treatments = models.TextField()

    def _str_(self):
        return f"Diagnosis for {self.user_plant.plant_name}"

# PlantDisease model
class PlantDisease(models.Model):
    disease_name = models.CharField(max_length=255)
    description = models.TextField()
    symptoms = models.TextField()
    treatment_instructions = models.TextField()

    def _str_(self):
        return self.disease_name

# GrowthTracker model
class GrowthTracker(models.Model):
    user_plant = models.ForeignKey(UserPlant, on_delete=models.CASCADE)
    image_path = models.CharField(max_length=255)
    date_tracked = models.DateField()
    growth_stage_id = models.ForeignKey('GrowthStage', on_delete=models.SET_NULL, null=True)

    def _str_(self):
        return f"Growth Tracker for {self.user_plant.plant_name}"

# SoilAnalysis model
class SoilAnalysis(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    image_path = models.CharField(max_length=255)
    analysis_date = models.DateField()
    texture = models.CharField(max_length=255)
    color = models.CharField(max_length=255)
    contaminants = models.CharField(max_length=255)
    moisture_level = models.CharField(max_length=255)
    pH_level = models.CharField(max_length=255)
    recommendations = models.TextField()

    def _str_(self):
        return f"Soil Analysis for {self.user.email}"

# PlantType model
class PlantType(models.Model):
    growth_maintain_oid = models.IntegerField()
    plant_type_name = models.CharField(max_length=255)
    plant_description = models.TextField()
    seed_depth = models.CharField(max_length=255)
    plant_spacing = models.CharField(max_length=255)
    plant_orientation = models.CharField(max_length=255)
    care_instructions = models.TextField()

    def _str_(self):
        return self.plant_type_name

# GrowthStage model
class GrowthStage(models.Model):
    plant_type = models.ForeignKey(PlantType, on_delete=models.CASCADE)
    growth_stage_name = models.CharField(max_length=255)
    growth_description = models.TextField()
    animation_path = models.CharField(max_length=255)

    def _str_(self):
        return self.growth_stage_name

# Notification model
class Notification(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    notification_type = models.CharField(max_length=255)
    notification_message = models.TextField()
    send_date = models.DateField()
    read_status = models.BooleanField(default=False)

    def _str_(self):
        return f"Notification for {self.user.email}"

# WeatherData model
class WeatherData(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    date = models.DateField()
    temperature = models.CharField(max_length=255)
    precipitation = models.CharField(max_length=255)
    humidity = models.CharField(max_length=255)
    wind_speed = models.CharField(max_length=255)

    def _str_(self):
        return f"Weather data for {self.user.email} on {self.date}"