# PoweCenter, Pond, FeedingMotor, CheckTray                             [Rashmi Ranjan Pradhan]

from rest_framework import serializers
from .models import PowerCenter, Pond, FeedingMotor, CheckTray

# -----------------------------------------------------------
# Serializer for CheckTray model
# Converts CheckTray instances to JSON with 'id' and 'status'
# -----------------------------------------------------------
class CheckTraySerializer(serializers.ModelSerializer):
    id = serializers.CharField(source="tray_id")

    class Meta:
        model = CheckTray
        fields = ["id", "status"]
# --------------------------------------------------------------
# Serializer for FeedingMotor model
# Converts FeedingMotor instances to JSON with 'id' and 'status'
# --------------------------------------------------------------
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
    name = serializers.CharField(source="pond_id")
    connected = serializers.BooleanField()
    power = serializers.ReadOnlyField()                                              # calculated from @property
    feedingMotor = FeedingMotorSerializer(source="feeding_motor")                    # One-To-One
    checktrays = CheckTraySerializer(source="check_trays", many=True)                # Many checktrays

    class Meta:
        model = Pond
        fields = ["id", "name", "status", "connected", "power", "feedingMotor", "checktrays"]
# --------------------------------------------------------------
# Serializer for PowerCenter model
# Includes nested Pond serializer
# --------------------------------------------------------------
class FeedingDataSerializer(serializers.ModelSerializer):
    id = serializers.CharField(source="pc_id")
    device = serializers.CharField(source="pc_id")              # device name same as pc_id
    ponds = PondSerializer(many=True)

    class Meta:
        model = PowerCenter
        fields = ["id", "device", "status", "ponds"]

