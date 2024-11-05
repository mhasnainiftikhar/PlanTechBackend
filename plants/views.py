from rest_framework import status
from rest_framework.response import Response
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from .models import User, Plant, Notification
from .serializers import UserSerializer, PlantSerializer, NotificationSerializer
from django.contrib.auth import authenticate
from .utils import send_firebase_notification
from django.shortcuts import render
from rest_framework.pagination import PageNumberPagination
import logging

logger = logging.getLogger(__name__)  # Set up logger


def index(request):
    return render(request, 'index.html')


@api_view(['POST'])
def register(request):
    serializer = UserSerializer(data=request.data)
    email = request.data.get("email")
    username = request.data.get("username")
    
    if User.objects.filter(email=email).exists():
        return Response({"error": "Email is already taken."}, status=status.HTTP_400_BAD_REQUEST)
    
    if User.objects.filter(username=username).exists():
        return Response({"error": "Username is already taken."}, status=status.HTTP_400_BAD_REQUEST)
    
    if serializer.is_valid():
        serializer.save()  # Django handles password hashing
        logger.info("New user registered: %s", email)
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    
    logger.error("Registration failed: %s", serializer.errors)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['POST'])
def login_view(request):
    serializer = UserSerializer(data=request.data)
    if serializer.is_valid(raise_exception=True):
        user = authenticate(username=serializer.validated_data["username"], 
                            password=serializer.validated_data["password"])
        if user:
            # Serialize user data
            user_data = UserSerializer(user).data
            return Response({"message": "Login successful", "user": user_data}, status=status.HTTP_200_OK)
    
    return Response({"error": "Invalid credentials"}, status=status.HTTP_401_UNAUTHORIZED)


# Custom Pagination for Plants
class PlantPagination(PageNumberPagination):
    page_size = 10


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def list_plants(request):
    plants = Plant.objects.filter(user=request.user).select_related('user')
    paginator = PlantPagination()
    result_page = paginator.paginate_queryset(plants, request)
    serializer = PlantSerializer(result_page, many=True)
    return paginator.get_paginated_response(serializer.data)


@api_view(['POST'])
@permission_classes([IsAuthenticated])
def create_plant(request):
    serializer = PlantSerializer(data=request.data)
    if serializer.is_valid():
        serializer.save(user=request.user)
        logger.info("New plant created by user: %s", request.user.email)
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    
    logger.error("Plant creation failed: %s", serializer.errors)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['POST'])
@permission_classes([IsAuthenticated])
def send_notification(request):
    user_token = request.data.get('user_token')
    title = request.data.get('title')
    body = request.data.get('body')
    
    if user_token and title and body:
        # Store notification in the database
        Notification.objects.create(user=request.user, title=title, body=body)
        
        # Send notification (asynchronously)
        try:
            response = send_firebase_notification.delay(user_token, title, body)  # `.delay()` for Celery task
            logger.info("Notification sent to %s with title %s", user_token, title)
            return Response({"message": "Notification sent", "firebase_response": response}, status=status.HTTP_200_OK)
        except Exception as e:
            logger.error("Failed to send notification: %s", e)
            return Response({"error": "Failed to send notification"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
    
    return Response({"error": "Missing data"}, status=status.HTTP_400_BAD_REQUEST)
