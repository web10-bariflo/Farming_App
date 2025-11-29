from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response
from .models import PowerCenter, Pond
from .serializers import PondSerializer, CheckTraySerializer, FeedingMotorSerializer, FeedingDataSerializer,PondWaterQualitySerializer, PowerCenterDeviceSerializer
from rest_framework import status


# [Rashmi Ranjan Pradhan]
# -------------------------------
# Pond View API
# -------------------------------
class PondViewAPI(APIView):
    def get(self, request):
        ponds = Pond.objects.all()
        serializer = PondSerializer(ponds, many=True)
        return Response(serializer.data, status=status.HTTP_200_ok)
    
# -------------------------------
# Pond Details API
# -------------------------------
class PondDetailAPI(APIView):
    def get(self, request, pond_id):
        try:
            pond = Pond.objects.get(pond_id=pond_id)
        except Pond.DoesNotExist:
            return Response({"error": "Pond not found"}, status=status.HTTP_404_NOT_FOUND)
        serializer = PondSerializer(pond)
        return Response(serializer.data, status=status.HTTP_200_OK)
        
# -------------------------------
# Feeding Data API
# -------------------------------
# class FeedingDataAPI(APIView):
#     def get(self, request):
#          # Get all PowerCenter objects from the database
#         power_centers = PowerCenter.objects.all()
#         # Initialize the response structure
#         response_data = {"powerCenters": []}

#         # Loop through each PowerCenter
#         for pc in power_centers:
#             # Create a dictionary for each power center
#             pc_data = {
#                 "id": pc.pc_id,
#                 "status": pc.status.lower(),
#                 "ponds": []         # Initialize list to hold pond data
#             }

#             # Loop through all ponds associated with this power center
#             for pond in pc.ponds.all():
#                 # Get the feeding motor associated with this pond (if exists)
#                 feeding_motor = getattr(pond, "feeding_motor", None)

#                 # Build pond data dictionary
#                 pond_data = {
#                     "id": pond.pond_id,
#                     "status": pond.status.lower(),
#                     "feedingMotor": {
#                         "id": feeding_motor.motor_id if feeding_motor else None,
#                         "status": feeding_motor.status.lower() if feeding_motor else "inactive"
#                     },
#                     "checktrays": [          # List of all check trays for this pond
#                         {
#                             "id": ct.tray_id,
#                             "status": ct.status.lower(),
#                         }
#                         for ct in pond.check_trays.all()        # Loop through all check trays
#                     ]
#                 }
#                 # Append pond data to the current power center's pond list
#                 pc_data["ponds"].append(pond_data)

#              # Append this power center's data to the final response
#             response_data["powerCenters"].append(pc_data)

#         # Return the final structured response as JSON
#         return Response(response_data)
class FeedingDataAPI(APIView):
    def get(self, request):
        pcs = PowerCenter.objects.prefetch_related(
            "ponds__feeding_motor",
            "ponds__check_trays",
        ).all()

        serializer = FeedingDataSerializer(pcs, many=True)

        return Response({"powerCenters": serializer.data}, status=status.HTTP_200_OK)

# -------------------------------
# Water Quality API
# -------------------------------
# class WaterQualityAPI(APIView):
#     def get(self, request):
#         pond_data = []

#         # Use select_related for OneToOneField
#         ponds = Pond.objects.select_related('water_quality').all()

#         for p in ponds:
#             water_quality = getattr(p, 'water_quality', None)  
#             pond_data.append({
#                 "id": p.pond_id,
#                 "name": p.pond_id,
#                 "connected": p.connected,
#                 "readings": {
#                     "DO": water_quality.DO if water_quality else [],
#                     "PH": water_quality.PH if water_quality else [],
#                     "Salinity": water_quality.Salinity if water_quality else [],
#                     "Temp": water_quality.Temp if water_quality else [],
#                 }
#             })

#         return Response(pond_data)
class WaterQualityAPI(APIView):
    def get(self, request):
        ponds = Pond.objects.select_related("water_quality").all()
        serializer = PondWaterQualitySerializer(ponds, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)


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

            # device_data = {
            #     "id": pc.pc_id,
            #     "device": pc.pc_id,
            #     "status": "online" if pc.status.lower() == "active" else "offline",
            #     "ponds": [
            #         {"id": p.pond_id, "name": p.pond_id, "power": p.status.lower() == "active"}
            #         for p in pc.ponds.all()
            #     ]
            # }
            serializer = PowerCenterDeviceSerializer(pc)
            cluster_dict[cluster_id].append(serializer.data)

        clusters = [{"id": cid, "devices": devices} for cid, devices in cluster_dict.items()]
        return Response({"clusters": clusters})




