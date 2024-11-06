from rest_framework import viewsets, status
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from django.contrib.auth.hashers import check_password, make_password
from .firebase import db  # Import the Firestore client
from .serializers import (
    UserSerializer, UserPlantSerializer, PlantDiagnosisSerializer,
    PlantDiseaseSerializer, GrowthTrackerSerializer, SoilAnalysisSerializer,
    PlantTypeSerializer, GrowthStageSerializer, NotificationSerializer, WeatherDataSerializer
)
from django.shortcuts import render

def index(request):
    return render(request, 'index.html')

# User viewset
class UserViewSet(viewsets.ViewSet):
    
    def list(self, request):
        # Retrieve email and password from query parameters
        email = request.query_params.get('email')
        password = request.query_params.get('password')

        # Debugging: Log the received email and password
        print(f"Received email: {email}")
        print(f"Password: {password}")

        if not email or not password:
            return Response({"error": "Email and password are required"}, status=status.HTTP_400_BAD_REQUEST)

        # Query the users collection for the document with the specified email
        users_ref = db.collection('users').where('email', '==', email)
        users = users_ref.stream()

        # Create a list of users that match the email query
        user_list = [user.to_dict() for user in users]
        print(f"Users found: {user_list}")

        if user_list:
            user_data = user_list[0]
            # Check if the password is correct and return user info if it matches
            if check_password(password, user_data['password']):
                print(f"User info: ")
                user_info = {
                    "email": user_data['email'],
                    "username": user_data['username']
                }
                print(f"Returning user: {user_info}")
                return Response(user_info, status=status.HTTP_200_OK)
            else:
                # Return a response indicating invalid credentials if password doesn't match
                return Response({"error": "Invalid credentials"}, status=status.HTTP_401_UNAUTHORIZED)
        
        # Return a response indicating that no user was found with the provided email
        return Response({"error": "User not found"}, status=status.HTTP_404_NOT_FOUND)


    def retrieve(self, request):
        print(f"Received email:")

        # Retrieve email from query parameters
        email = request.query_params.get('email')
        
        # Debugging: Log the received email
        print(f"Received email: {email}")

        if not email:
            return Response({"error": "Email is required"}, status=status.HTTP_400_BAD_REQUEST)

        # Query the users collection for the document with the specified email
        users_ref = db.collection('users').where('email', '==', email)
        users = users_ref.stream()

        # Debugging: Log the number of users found
        user_list = [user.to_dict() for user in users]
        print(f"Users found: {user_list}")  # Log the entire user list found

        if user_list:
            # Debugging: Log the first user being returned
            print(f"Returning user: {user_list[0]}")
            return Response(user_list[0], status=status.HTTP_200_OK)

        # Debugging: Log that no user was found
        print("No user found with the provided email.")
        return Response({"error": "User not found"}, status=status.HTTP_404_NOT_FOUND)

    def create(self, request):
        data = request.data
        if 'password' in data:
            data['password'] = make_password(data['password'])
        user_ref = db.collection('users').document()  # Create a new document
        user_ref.set(data)
        return Response({"id": user_ref.id, **data}, status=status.HTTP_201_CREATED)

    def update(self, request, pk=None):
        data = request.data
        user_ref = db.collection('users').document(pk)
        user_ref.update(data)
        return Response({"id": pk, **data}, status=status.HTTP_200_OK)

    def destroy(self, request, pk=None):
        user_ref = db.collection('users').document(pk)
        user_ref.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


# UserPlant viewset
class UserPlantViewSet(viewsets.ViewSet):
    
    
    def list(self, request):
        plants = [doc.to_dict() for doc in db.collection('userplants').stream()]
        return Response(plants, status=status.HTTP_200_OK)

    def retrieve(self, request, pk=None):
        plant_ref = db.collection('userplants').document(pk)
        plant = plant_ref.get()
        if plant.exists:
            return Response(plant.to_dict(), status=status.HTTP_200_OK)
        return Response({"error": "UserPlant not found"}, status=status.HTTP_404_NOT_FOUND)

    def create(self, request):
        data = request.data
        plant_ref = db.collection('userplants').document()
        plant_ref.set(data)
        return Response({"id": plant_ref.id, **data}, status=status.HTTP_201_CREATED)

    def update(self, request, pk=None):
        data = request.data
        plant_ref = db.collection('userplants').document(pk)
        plant_ref.update(data)
        return Response({"id": pk, **data}, status=status.HTTP_200_OK)

    def destroy(self, request, pk=None):
        plant_ref = db.collection('userplants').document(pk)
        plant_ref.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


# GrowthTracker viewset
class GrowthTrackerViewSet(viewsets.ViewSet):
    

    def list(self, request):
        trackers = [doc.to_dict() for doc in db.collection('growthtracker').stream()]
        return Response(trackers, status=status.HTTP_200_OK)

    def retrieve(self, request, pk=None):
        tracker_ref = db.collection('growthtracker').document(pk)
        tracker = tracker_ref.get()
        if tracker.exists:
            return Response(tracker.to_dict(), status=status.HTTP_200_OK)
        return Response({"error": "GrowthTracker not found"}, status=status.HTTP_404_NOT_FOUND)

    def create(self, request):
        data = request.data
        tracker_ref = db.collection('growthtracker').document()
        tracker_ref.set(data)
        return Response({"id": tracker_ref.id, **data}, status=status.HTTP_201_CREATED)

    def update(self, request, pk=None):
        data = request.data
        tracker_ref = db.collection('growthtracker').document(pk)
        tracker_ref.update(data)
        return Response({"id": pk, **data}, status=status.HTTP_200_OK)

    def destroy(self, request, pk=None):
        tracker_ref = db.collection('growthtracker').document(pk)
        tracker_ref.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


# SoilAnalysis viewset
class SoilAnalysisViewSet(viewsets.ViewSet):
    

    def list(self, request):
        analyses = [doc.to_dict() for doc in db.collection('soilanalysis').stream()]
        return Response(analyses, status=status.HTTP_200_OK)

    def retrieve(self, request, pk=None):
        analysis_ref = db.collection('soilanalysis').document(pk)
        analysis = analysis_ref.get()
        if analysis.exists:
            return Response(analysis.to_dict(), status=status.HTTP_200_OK)
        return Response({"error": "SoilAnalysis not found"}, status=status.HTTP_404_NOT_FOUND)

    def create(self, request):
        data = request.data
        analysis_ref = db.collection('soilanalysis').document()
        analysis_ref.set(data)
        return Response({"id": analysis_ref.id, **data}, status=status.HTTP_201_CREATED)

    def update(self, request, pk=None):
        data = request.data
        analysis_ref = db.collection('soilanalysis').document(pk)
        analysis_ref.update(data)
        return Response({"id": pk, **data}, status=status.HTTP_200_OK)

    def destroy(self, request, pk=None):
        analysis_ref = db.collection('soilanalysis').document(pk)
        analysis_ref.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


# PlantType viewset
class PlantTypeViewSet(viewsets.ViewSet):
    

    def list(self, request):
        plant_types = [doc.to_dict() for doc in db.collection('planttypes').stream()]
        return Response(plant_types, status=status.HTTP_200_OK)

    def retrieve(self, request, pk=None):
        plant_type_ref = db.collection('planttypes').document(pk)
        plant_type = plant_type_ref.get()
        if plant_type.exists:
            return Response(plant_type.to_dict(), status=status.HTTP_200_OK)
        return Response({"error": "PlantType not found"}, status=status.HTTP_404_NOT_FOUND)

    def create(self, request):
        data = request.data
        plant_type_ref = db.collection('planttypes').document()
        plant_type_ref.set(data)
        return Response({"id": plant_type_ref.id, **data}, status=status.HTTP_201_CREATED)

    def update(self, request, pk=None):
        data = request.data
        plant_type_ref = db.collection('planttypes').document(pk)
        plant_type_ref.update(data)
        return Response({"id": pk, **data}, status=status.HTTP_200_OK)

    def destroy(self, request, pk=None):
        plant_type_ref = db.collection('planttypes').document(pk)
        plant_type_ref.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


# GrowthStage viewset
class GrowthStageViewSet(viewsets.ViewSet):
    

    def list(self, request):
        stages = [doc.to_dict() for doc in db.collection('growthstages').stream()]
        return Response(stages, status=status.HTTP_200_OK)

    def retrieve(self, request, pk=None):
        stage_ref = db.collection('growthstages').document(pk)
        stage = stage_ref.get()
        if stage.exists:
            return Response(stage.to_dict(), status=status.HTTP_200_OK)
        return Response({"error": "GrowthStage not found"}, status=status.HTTP_404_NOT_FOUND)

    def create(self, request):
        data = request.data
        stage_ref = db.collection('growthstages').document()
        stage_ref.set(data)
        return Response({"id": stage_ref.id, **data}, status=status.HTTP_201_CREATED)

    def update(self, request, pk=None):
        data = request.data
        stage_ref = db.collection('growthstages').document(pk)
        stage_ref.update(data)
        return Response({"id": pk, **data}, status=status.HTTP_200_OK)

    def destroy(self, request, pk=None):
        stage_ref = db.collection('growthstages').document(pk)
        stage_ref.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


# PlantDisease viewset
class PlantDiseaseViewSet(viewsets.ViewSet):
    

    def list(self, request):
        diseases = [doc.to_dict() for doc in db.collection('plantdiseases').stream()]
        return Response(diseases, status=status.HTTP_200_OK)

    def retrieve(self, request, pk=None):
        disease_ref = db.collection('plantdiseases').document(pk)
        disease = disease_ref.get()
        if disease.exists:
            return Response(disease.to_dict(), status=status.HTTP_200_OK)
        return Response({"error": "PlantDisease not found"}, status=status.HTTP_404_NOT_FOUND)

    def create(self, request):
        data = request.data
        disease_ref = db.collection('plantdiseases').document()
        disease_ref.set(data)
        return Response({"id": disease_ref.id, **data}, status=status.HTTP_201_CREATED)

    def update(self, request, pk=None):
        data = request.data
        disease_ref = db.collection('plantdiseases').document(pk)
        disease_ref.update(data)
        return Response({"id": pk, **data}, status=status.HTTP_200_OK)

    def destroy(self, request, pk=None):
        disease_ref = db.collection('plantdiseases').document(pk)
        disease_ref.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


# PlantDiagnosis viewset
class PlantDiagnosisViewSet(viewsets.ViewSet):
    # 

    def list(self, request):
        diagnoses = [doc.to_dict() for doc in db.collection('plantdiagnoses').stream()]
        return Response(diagnoses, status=status.HTTP_200_OK)

    def retrieve(self, request, pk=None):
        diagnosis_ref = db.collection('plantdiagnoses').document(pk)
        diagnosis = diagnosis_ref.get()
        if diagnosis.exists:
            return Response(diagnosis.to_dict(), status=status.HTTP_200_OK)
        return Response({"error": "PlantDiagnosis not found"}, status=status.HTTP_404_NOT_FOUND)

    def create(self, request):
        data = request.data
        diagnosis_ref = db.collection('plantdiagnoses').document()
        diagnosis_ref.set(data)
        return Response({"id": diagnosis_ref.id, **data}, status=status.HTTP_201_CREATED)

    def update(self, request, pk=None):
        data = request.data
        diagnosis_ref = db.collection('plantdiagnoses').document(pk)
        diagnosis_ref.update(data)
        return Response({"id": pk, **data}, status=status.HTTP_200_OK)

    def destroy(self, request, pk=None):
        diagnosis_ref = db.collection('plantdiagnoses').document(pk)
        diagnosis_ref.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

# Notification viewset
class NotificationViewSet(viewsets.ViewSet):
    

    def list(self, request):
        notifications = [doc.to_dict() for doc in db.collection('notifications').stream()]
        return Response(notifications, status=status.HTTP_200_OK)

    def retrieve(self, request, pk=None):
        notification_ref = db.collection('notifications').document(pk)
        notification = notification_ref.get()
        if notification.exists:
            return Response(notification.to_dict(), status=status.HTTP_200_OK)
        return Response({"error": "Notification not found"}, status=status.HTTP_404_NOT_FOUND)

    def create(self, request):
        data = request.data
        notification_ref = db.collection('notifications').document()
        notification_ref.set(data)
        return Response({"id": notification_ref.id, **data}, status=status.HTTP_201_CREATED)

    def update(self, request, pk=None):
        data = request.data
        notification_ref = db.collection('notifications').document(pk)
        notification_ref.update(data)
        return Response({"id": pk, **data}, status=status.HTTP_200_OK)

    def destroy(self, request, pk=None):
        notification_ref = db.collection('notifications').document(pk)
        notification_ref.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


# WeatherData viewset
class WeatherDataViewSet(viewsets.ViewSet):
    

    def list(self, request):
        weather_data = [doc.to_dict() for doc in db.collection('weatherdata').stream()]
        return Response(weather_data, status=status.HTTP_200_OK)

    def retrieve(self, request, pk=None):
        weather_data_ref = db.collection('weatherdata').document(pk)
        weather_data = weather_data_ref.get()
        if weather_data.exists:
            return Response(weather_data.to_dict(), status=status.HTTP_200_OK)
        return Response({"error": "WeatherData not found"}, status=status.HTTP_404_NOT_FOUND)

    def create(self, request):
        data = request.data
        weather_data_ref = db.collection('weatherdata').document()
        weather_data_ref.set(data)
        return Response({"id": weather_data_ref.id, **data}, status=status.HTTP_201_CREATED)

    def update(self, request, pk=None):
        data = request.data
        weather_data_ref = db.collection('weatherdata').document(pk)
        weather_data_ref.update(data)
        return Response({"id": pk, **data}, status=status.HTTP_200_OK)

    def destroy(self, request, pk=None):
        weather_data_ref = db.collection('weatherdata').document(pk)
        weather_data_ref.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)