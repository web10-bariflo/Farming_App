from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response
from .models import PowerCenter, PondReading
from .serializers import FeedingDataSerializer, PondSerializer

# Create your views here.
# [Rashmi Ranjan Pradhan]
class FeedingDataAPI(APIView):
    def get(self, request):

        # Fetch all PowerCenters with related ponds, feeding motors, and check trays
        power_centers = PowerCenter.objects.prefetch_related("ponds").all()

        # Group by cluster 
        cluster_dict = {}
        for pc in power_centers:
            cluster_id = pc.pc_id.split("-")[0]         # e.g., (C1, C2, etc.) based on pc_id prefix
            if cluster_id not in cluster_dict:
                cluster_dict[cluster_id] = []
            cluster_dict[cluster_id].append(pc)
        
        # Serialize each device and build cluster structure
        clusters = []
        for cluster_id, devices in cluster_dict.items():
            serializer = FeedingDataSerializer(devices, many=True)
            clusters.append(
                {
                    "id": cluster_id,
                    "devices": serializer.data
                }
            )
        return Response({"clusters": clusters})

        # return Response({"powerCenters": serializer.data})

class WaterQualityAPI(APIView):
    #  API to fetch all pond readings with connected status. Returns pond readings grouped by pond.
    def get(self, request):
        # Fetch all ponds with their readings
        ponds = PondReading.objects.select_related('pond').all()

        pond_data = []
        for pond_reading in ponds:
            # Collect readings by type (DO, PH, Salinity, Temp)
            readings_dict = {pond_reading.type: pond_reading.values}

            # Check if pond already added
            existing = next((p for p in pond_data if p["id"] == pond_reading.pond.pond_id), None)
            if existing:
                existing["readings"].update(readings_dict)
            else:
                pond_data.append({
                    "id": pond_reading.pond.pond_id,
                    "name": pond_reading.pond.pond_id,
                    "connected": pond_reading.pond.connected,
                    "readings": readings_dict
                })
        return Response(pond_data)
    
class PowerMonitoringAPI(APIView):
    # Returns clusters with devices and ponds' power status

    def get(self, request):
        power_centers = PowerCenter.objects.prefetch_related("ponds").all()

        cluster_dict = {}
        for pc in power_centers:
            cluster_id = pc.pc_id.split("-")[0]
            if cluster_id not in cluster_dict:
                cluster_dict[cluster_id] = []

            device_data = {
                "id": pc.pc_id,
                "device": pc.pc_id,
                "status": "online" if pc.status == "active" else "offline",
                "ponds": [
                    {"id": p.pond_id, "name": p.pond_id, "power": p.status=="active"}
                    for p in pc.ponds.all()
                ]
            }
            cluster_dict[cluster_id].append(device_data)

        clusters = [{"id": cid, "devices": devices} for cid, devices in cluster_dict.items()]
        return Response({"clusters": clusters})

