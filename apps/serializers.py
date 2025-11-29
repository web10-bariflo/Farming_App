# PoweCenter, Pond, FeedingMotor, CheckTray, WaterQuality                                       [Rashmi Ranjan Pradhan]

from rest_framework import serializers
from .models import PowerCenter, Pond, FeedingMotor, CheckTray, WaterQuality

# ---------------------------------------------------------------
# Serializer for CheckTray model
# Converts CheckTray instances to JSON with 'id' and 'status'
# ---------------------------------------------------------------
class CheckTraySerializer(serializers.ModelSerializer):
    id = serializers.CharField(source="tray_id")

    class Meta:
        model = CheckTray
        fields = ["id", "status"]

# -----------------------------------------------------------------
# Serializer for FeedingMotor model
# Converts FeedingMotor instances to JSON with 'id' and 'status'
# -----------------------------------------------------------------
class FeedingMotorSerializer(serializers.ModelSerializer):
    id = serializers.CharField(source="motor_id")

    class Meta:
        model = FeedingMotor
        fields = ["id", "status"]

# --------------------------------------------------------------
# Serializer for Pond model
# Includes nested FeedingMotor and CheckTray serializers
# --------------------------------------------------------------
class PondSerializer(serializers.ModelSerializer):
    id = serializers.CharField(source="pond_id")
    feedingMotor = FeedingMotorSerializer(source="feeding_motor")
    checktrays = CheckTraySerializer(source="check_trays", many=True)

    class Meta:
        model = Pond
        fields = ["id", "status", "feedingMotor", "checktrays"]

    def to_representation(self, instance):
        rep = super().to_representation(instance)
        # Convert status to active/inactive
        rep["status"] = "active" if rep["status"].lower() == "active" else "inactive"
        # Convert feedingMotor status
        if rep.get("feedingMotor"):
            rep["feedingMotor"]["status"] = (
                "active" if rep["feedingMotor"]["status"].lower() == "active" else "inactive"
            )
        # Convert checktrays status
        if rep.get("checktrays"):
            for ct in rep["checktrays"]:
                ct["status"] = "active" if ct["status"].lower() == "active" else "inactive"
        return rep

# --------------------------------------------------------------
# Serializer for PowerCenter model
# Includes nested Pond serializer
# --------------------------------------------------------------
class FeedingDataSerializer(serializers.ModelSerializer):
    id = serializers.CharField(source="pc_id")
    device = serializers.CharField(source="pc_id")  # device name same as pc_id
    ponds = PondSerializer(many=True)

    class Meta:
        model = PowerCenter
        fields = ["id", "device", "status", "ponds"]


# --------------------------------------------------------------
# Water Quality Reading Serializer
# Serializes only the water quality parameters (DO, PH, Salinity, Temp)
# Used as a nested serializer inside the PondWaterQualitySerializer
# --------------------------------------------------------------
class WaterQualityReadingSerializer(serializers.ModelSerializer):
    class Meta:
        model = WaterQuality
        fields = ["DO", "PH", "Salinity", "Temp"]


# --------------------------------------------------------------
# Pond Water Quality Serializer
# Returns pond basic details along with nested water quality readings
# Uses WaterQualityReadingSerializer to serialize One-to-One water_quality data
# --------------------------------------------------------------
class PondWaterQualitySerializer(serializers.ModelSerializer):
    id = serializers.CharField(source="pond_id")
    name = serializers.CharField(source="pond_id")
    readings = WaterQualityReadingSerializer(source="water_quality", read_only=True)

    class Meta:
        model = Pond
        fields = ["id", "name", "connected", "readings"]


# --------------------------------------------------------------
# Serializer for Pond's Power Status
# Used for Power Monitoring API
# --------------------------------------------------------------
class PondPowerSerializer(serializers.ModelSerializer):
    id = serializers.CharField(source="pond_id")
    name = serializers.CharField(source="pond_id")
    power = serializers.SerializerMethodField()

    class Meta:
        model = Pond
        fields = ["id", "name", "power"]

    def get_power(self, obj):
        return obj.status.lower() == "active"


# --------------------------------------------------------------
# Serializer for PowerCenter Device
# Includes nested ponds with their power status
# --------------------------------------------------------------
class PowerCenterDeviceSerializer(serializers.ModelSerializer):
    id = serializers.CharField(source="pc_id")
    device = serializers.CharField(source="pc_id")
    status = serializers.SerializerMethodField()
    ponds = PondPowerSerializer(many=True, read_only=True)

    class Meta:
        model = PowerCenter
        fields = ["id", "device", "status", "ponds"]

    def get_status(self, obj):
        return "online" if obj.status.lower() == "active" else "offline"


# --------------------------------------------------------------
# Serializer for Cluster
# Groups devices by cluster id (calculated in view)
# --------------------------------------------------------------
class ClusterSerializer(serializers.Serializer):
    id = serializers.CharField()
    devices = PowerCenterDeviceSerializer(many=True)
