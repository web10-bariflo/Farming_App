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
        return Response(serializer.data, status=status.HTTP_200_OK)
    
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

            serializer = PowerCenterDeviceSerializer(pc)
            cluster_dict[cluster_id].append(serializer.data)

        clusters = [{"id": cid, "devices": devices} for cid, devices in cluster_dict.items()]
        return Response({"clusters": clusters})




