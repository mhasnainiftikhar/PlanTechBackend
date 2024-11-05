from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('register/', views.register, name='register'),
    path('login/', views.login_view, name='login'),
    path('plants/', views.list_plants, name='list_plants'),  # Changed to list_plants
    path('plants/create/', views.create_plant, name='create_plant'),  # Added new URL for create_plant
]
