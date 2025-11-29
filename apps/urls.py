from django.urls import path
from .views import FeedingDataAPI, WaterQualityAPI, PowerMonitoringAPI, PondViewAPI, PondDetailAPI

urlpatterns = [
    path('feeding-data/', FeedingDataAPI.as_view(), name="feeding-data-api"),                   # GET
    path('water-quality/', WaterQualityAPI.as_view(), name="water-quality-api"),                # GET
    path('power-monitoring/', PowerMonitoringAPI.as_view(), name="power-monitoring-api"),       # GET

    # Add Pond APIs.

    path('ponds/', PondViewAPI.as_view(), name="pond-list-api"),                                # GET all ponds
    path('ponds/<str:pond_id>/', PondDetailAPI.as_view(), name="pond-detail-api")                # GET single pond
]
