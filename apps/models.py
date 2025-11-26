from django.db import models

# Create your models here.

#      [Rashmi Rnjan Pradhan]

# -------------------------------
# Power Center
# -------------------------------
class PowerCenter(models.Model):
    pc_id = models.CharField(max_length=50, unique=True)
    status = models.CharField(max_length=20)

    def __str__(self):
        return self.pc_id
    
# -------------------------------
# Pond
# -------------------------------
class Pond(models.Model):
    power_center = models.ForeignKey(
        PowerCenter, related_name="ponds", on_delete=models.CASCADE
    )
    pond_id = models.CharField(max_length=50, unique=True)
    status = models.CharField(max_length=20)
    connected = models.BooleanField(default=True)            # For API "connected" field

    def __str__(self):
        return self.pond_id
    
    @property
    def power(self):
        # pond power is True if any feeding motor is online
        if hasattr(self, 'feeding_motor') and self.feeding_motor:
            return self.feeding_motor.status.lower() == "online"
        return False
    
# -------------------------------
# Feeding Motor (1 per pond)
# -------------------------------
class FeedingMotor(models.Model):
    pond = models.OneToOneField(
        Pond, related_name="feeding_motor", on_delete=models.CASCADE
    )
    motor_id = models.CharField(max_length=50, unique=True)
    status = models.CharField(max_length=20)

    def __str__(self):
        return self.motor_id
    
# -------------------------------
# Check Tray (multiple per pond)
# -------------------------------
class CheckTray(models.Model):
    pond = models.ForeignKey(
        Pond, related_name="check_trays", on_delete=models.CASCADE
    )
    tray_id = models.CharField(max_length=50, unique=True)
    status = models.CharField(max_length=20)

    def __str__(self):
        return self.tray_id
    
# -------------------------------
# Pond Sensor Readings
# -------------------------------
class PondReading(models.Model):
    pond = models.ForeignKey(Pond, related_name="sensor_readings", on_delete=models.CASCADE)
    sensor_type = models.CharField(max_length=20)      # "DO", "PH", "Salinity", "Temp"
    reading_values = models.JSONField(default=list)     # store multiple readings as a list

    def __str__(self):
        return f"{self.pond.pond_id} - {self.sensor_type}"


