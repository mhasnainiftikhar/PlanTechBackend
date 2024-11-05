from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import (
    UserViewSet, UserPlantViewSet, PlantDiagnosisViewSet, PlantDiseaseViewSet,
    GrowthTrackerViewSet, SoilAnalysisViewSet, PlantTypeViewSet,
    GrowthStageViewSet, NotificationViewSet, WeatherDataViewSet
)

router = DefaultRouter()
router.register(r'users', UserViewSet, basename='user')
router.register(r'userplants', UserPlantViewSet, basename='userplant')
router.register(r'plantdiagnoses', PlantDiagnosisViewSet, basename='plantdiagnoses')
router.register(r'plantdiseases', PlantDiseaseViewSet, basename='plantdisease')
router.register(r'growthtrackers', GrowthTrackerViewSet, basename='growthtrack')
router.register(r'soilanalyses', SoilAnalysisViewSet, basename='soilanalysis' )
router.register(r'planttypes', PlantTypeViewSet, basename='planttype' )
router.register(r'growthstages', GrowthStageViewSet, basename='growthstage' )
router.register(r'notifications', NotificationViewSet,'notification')
router.register(r'weatherdata', WeatherDataViewSet,'weatherdata')

urlpatterns = [
    path('', include(router.urls)),
    
]
