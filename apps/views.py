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
         # Get all PowerCenter objects from the database
        power_centers = PowerCenter.objects.all()
        # Initialize the response structure
        response_data = {"powerCenters": []}

        # Loop through each PowerCenter
        for pc in power_centers:
            # Create a dictionary for each power center
            pc_data = {
                "id": pc.pc_id,
                "status": pc.status.lower(),
                "ponds": []         # Initialize list to hold pond data
            }

            # Loop through all ponds associated with this power center
            for pond in pc.ponds.all():
                # Get the feeding motor associated with this pond (if exists)
                feeding_motor = getattr(pond, "feeding_motor", None)

                # Build pond data dictionary
                pond_data = {
                    "id": pond.pond_id,
                    "status": pond.status.lower(),
                    "feedingMotor": {
                        "id": feeding_motor.motor_id if feeding_motor else None,
                        "status": feeding_motor.status.lower() if feeding_motor else "inactive"
                    },
                    "checktrays": [          # List of all check trays for this pond
                        {
                            "id": ct.tray_id,
                            "status": ct.status.lower(),
                        }
                        for ct in pond.check_trays.all()        # Loop through all check trays
                    ]
                }
                # Append pond data to the current power center's pond list
                pc_data["ponds"].append(pond_data)

             # Append this power center's data to the final response
            response_data["powerCenters"].append(pc_data)

        # Return the final structured response as JSON
        return Response(response_data)

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
