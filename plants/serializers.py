from rest_framework import serializers
from .models import User, UserPlant, PlantDiagnosis, PlantDisease, GrowthTracker, SoilAnalysis, PlantType, GrowthStage, Notification, WeatherData

# User serializer
class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'email', 'password_hash', 'create_date']
        read_only_fields = ['create_date']

# PlantDisease serializer
class PlantDiseaseSerializer(serializers.ModelSerializer):
    class Meta:
        model = PlantDisease
        fields = ['id', 'disease_name', 'description', 'symptoms', 'treatment_instructions']

# PlantDiagnosis serializer
class PlantDiagnosisSerializer(serializers.ModelSerializer):
    user_plant = serializers.PrimaryKeyRelatedField(queryset=UserPlant.objects.all())
    disease = PlantDiseaseSerializer()

    class Meta:
        model = PlantDiagnosis
        fields = ['id', 'user_plant', 'disease', 'diagnosis_date', 'treatments']

# PlantType serializer
class PlantTypeSerializer(serializers.ModelSerializer):
    class Meta:
        model = PlantType
        fields = ['id', 'growth_maintain_oid', 'plant_type_name', 'plant_description', 'seed_depth', 'plant_spacing', 'plant_orientation', 'care_instructions']

# GrowthStage serializer
class GrowthStageSerializer(serializers.ModelSerializer):
    plant_type = PlantTypeSerializer()

    class Meta:
        model = GrowthStage
        fields = ['id', 'plant_type', 'growth_stage_name', 'growth_description', 'animation_path']

# UserPlant serializer
class UserPlantSerializer(serializers.ModelSerializer):
    user = serializers.PrimaryKeyRelatedField(queryset=User.objects.all())
    plant_type_id = PlantTypeSerializer()

    class Meta:
        model = UserPlant
        fields = ['id', 'user', 'plant_name', 'planting_date', 'plant_type_id']

# GrowthTracker serializer
class GrowthTrackerSerializer(serializers.ModelSerializer):
    user_plant = UserPlantSerializer()
    growth_stage_id = GrowthStageSerializer()

    class Meta:
        model = GrowthTracker
        fields = ['id', 'user_plant', 'image_path', 'date_tracked', 'growth_stage_id']

# SoilAnalysis serializer
class SoilAnalysisSerializer(serializers.ModelSerializer):
    user = serializers.PrimaryKeyRelatedField(queryset=User.objects.all())

    class Meta:
        model = SoilAnalysis
        fields = ['id', 'user', 'image_path', 'analysis_date', 'texture', 'color', 'contaminants', 'moisture_level', 'pH_level', 'recommendations']

# Notification serializer
class NotificationSerializer(serializers.ModelSerializer):
    user = serializers.PrimaryKeyRelatedField(queryset=User.objects.all())

    class Meta:
        model = Notification
        fields = ['id', 'user', 'notification_type', 'notification_message', 'send_date', 'read_status']

# WeatherData serializer
class WeatherDataSerializer(serializers.ModelSerializer):
    user = serializers.PrimaryKeyRelatedField(queryset=User.objects.all())

    class Meta:
        model = WeatherData
        fields = ['id', 'user', 'date', 'temperature', 'precipitation', 'humidity', 'wind_speed']