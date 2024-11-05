from rest_framework import serializers
from .models import User, Plant, GrowthHistory, Notification


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'username', 'email', 'role']


class PlantSerializer(serializers.ModelSerializer):
    class Meta:
        model = Plant
        fields = ['id', 'user', 'name', 'planting_date', 'soil_type']


class GrowthHistorySerializer(serializers.ModelSerializer):
    class Meta:
        model = GrowthHistory
        fields = ['id', 'plant', 'date', 'growth_stage']


class NotificationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Notification
        fields = ['id', 'user', 'message', 'timestamp', 'is_read']
