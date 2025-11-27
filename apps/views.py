from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response
from .models import PowerCenter, Pond
from .serializers import FeedingDataSerializer, PondSerializer

# -------------------------------
# Feeding Data API
# -------------------------------
class FeedingDataAPI(APIView):
    def get(self, request):
        pond_data = []

        ponds = Pond.objects.all().prefetch_related('readings')

        for p in ponds:
            readings = getattr(p, 'readings', None)  # safely get readings
            pond_data.append({
                "id": p.pond_id,
                "name": p.pond_id,
                "connected": p.connected,
                "readings": {
                    "DO": readings.DO if readings else [],
                    "PH": readings.PH if readings else [],
                    "Salinity": readings.Salinity if readings else [],
                    "Temp": readings.Temp if readings else [],
                }
            })

        return Response(pond_data)

# -------------------------------
# Water Quality API
# -------------------------------
class WaterQualityAPI(APIView):
    def get(self, request):
        pond_data = []

        # Use the Pond model, not 'pond' variable
        ponds = Pond.objects.all().prefetch_related('readings')

        for p in ponds:
            readings = getattr(p, 'readings', None)  # safely get readings
            pond_data.append({
                "id": p.pond_id,
                "name": p.pond_id,
                "connected": p.connected,
                "readings": {
                    "DO": readings.DO if readings else [],
                    "PH": readings.PH if readings else [],
                    "Salinity": readings.Salinity if readings else [],
                    "Temp": readings.Temp if readings else [],
                }
            })

        return Response(pond_data)

# -------------------------------
# Power Monitoring API
# -------------------------------
class PowerMonitoringAPI(APIView):
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
                "status": "online" if pc.status.lower() == "active" else "offline",
                "ponds": [
                    {"id": p.pond_id, "name": p.pond_id, "power": p.status.lower() == "active"}
                    for p in pc.ponds.all()
                ]
            }
            cluster_dict[cluster_id].append(device_data)

        clusters = [{"id": cid, "devices": devices} for cid, devices in cluster_dict.items()]
        return Response({"clusters": clusters})
