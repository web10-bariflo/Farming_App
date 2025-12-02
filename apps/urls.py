from django.urls import path
from .views import (FeedingDataAPI, 
                    WaterQualityAPI, 
                    PowerMonitoringAPI, 
                    PondViewAPI, 
                    PondDetailAPI, 
                    PondCreateAPI,
                    PondDeleteAPI,
                    PondUpdateAPI)

urlpatterns = [
    path('feeding-data/', FeedingDataAPI.as_view(), name="feeding-data-api"),                   # GET
    path('water-quality/', WaterQualityAPI.as_view(), name="water-quality-api"),                # GET
    path('power-monitoring/', PowerMonitoringAPI.as_view(), name="power-monitoring-api"),       # GET

    # Pond APIs.
    path('pond/create/', PondCreateAPI.as_view(), name = 'pond-create-api'),                    # POST API FOR CREATE POND
    path('ponds/', PondViewAPI.as_view(), name="pond-list-api"),                                # GET all ponds
    path('ponds/<str:pond_id>/', PondDetailAPI.as_view(), name="pond-detail-api"),              # GET single pond
    path('pond/update/<str:pond_id>/', PondUpdateAPI.as_view(), name='pond-update-api'),        # PUT - Update Pond
    path('pond/delete/<str:pond_id>/', PondDeleteAPI.as_view(), name='pond-delete-api'),        # DELETE - Delete Pond
]
