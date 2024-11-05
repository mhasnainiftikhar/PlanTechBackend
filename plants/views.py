from rest_framework import status
from rest_framework.response import Response
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from .models import User, Plant, Notification
from .serializers import UserSerializer, PlantSerializer, NotificationSerializer
from django.contrib.auth import authenticate
from .utils import get_notifications_from_firestore, save_notification_to_firestore, save_notification_to_firestore, save_plant_to_firestore, save_user_to_firestore, send_firebase_notification

from django.shortcuts import render


def index(request):
    return render(request, 'index.html')

@api_view(['POST'])
def register(request):
    serializer = UserSerializer(data=request.data)
    if serializer.is_valid():
        user = serializer.save()
        save_user_to_firestore(user)  # Save user to Firestore
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)





@api_view(['POST'])
def login_view(request):
    email = request.data.get("email")
    password = request.data.get("password")
    user = authenticate(request, username=email, password=password)
    if user:
        return Response({"message": "Login successful"}, status=status.HTTP_200_OK)
    return Response({"error": "Invalid credentials"}, status=status.HTTP_401_UNAUTHORIZED)


@api_view(['GET', 'POST'])
@permission_classes([IsAuthenticated])
def manage_plants(request):
    if request.method == 'POST':
        serializer = PlantSerializer(data=request.data)
        if serializer.is_valid():
            plant = serializer.save(user=request.user)
            save_plant_to_firestore(plant)  # Save plant to Firestore
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    else:
        plants = Plant.objects.filter(user=request.user)
        serializer = PlantSerializer(plants, many=True)
        return Response(serializer.data)


@api_view(['POST'])
@permission_classes([IsAuthenticated])
def send_notification(request):
    user_token = request.data.get('user_token')
    title = request.data.get('title')
    body = request.data.get('body')

    if user_token and title and body:
        response = send_firebase_notification(user_token, title, body)
        save_notification_to_firestore(request.user.id, title, body)  # Save to Firestore
        return Response({"message": "Notification sent", "firebase_response": response}, status=status.HTTP_200_OK)
    return Response({"error": "Missing data"}, status=status.HTTP_400_BAD_REQUEST)

@api_view(['POST'])
@permission_classes([IsAuthenticated])
def send_notification(request):
    user_token = request.data.get('user_token')
    title = request.data.get('title')
    body = request.data.get('body')

    if user_token and title and body:
        response = send_firebase_notification(user_token, title, body)
        return Response({"message": "Notification sent", "firebase_response": response}, status=status.HTTP_200_OK)
    return Response({"error": "Missing data"}, status=status.HTTP_400_BAD_REQUEST)
@api_view(['GET'])
@permission_classes([IsAuthenticated])
def fetch_notifications(request):
    notifications = get_notifications_from_firestore(request.user.id)
    return Response(notifications, status=status.HTTP_200_OK)
