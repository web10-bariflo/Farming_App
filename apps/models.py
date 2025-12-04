from django.db import models
from django.utils import timezone
from users_app.models import User

# Create your models here.

#      [Rashmi Rnjan Pradhan]

# ---------------------------------------------------------------
#                       Power Center
# ---------------------------------------------------------------
class PowerCenter(models.Model):
    pc_id = models.CharField(max_length=50, unique=True)
    status = models.CharField(max_length=20)

    def __str__(self):
        return self.pc_id

# ------------------------------------------------------------------
#                           Pond
# ------------------------------------------------------------------
class Pond(models.Model):
    pond_id = models.CharField(max_length=50, primary_key=True)
    user = models.ForeignKey(
        User,
        to_field='uid',              # refers to uid field in User model
        db_column='user_uid',        # custom column name
        related_name='ponds',
        null=True,
        blank=True,
        on_delete=models.SET_NULL  
    )
    farm_name = models.CharField(max_length=255, default="Unknown Farm")
    section = models.CharField(max_length=100, blank=True, null=True)
    pond_name = models.CharField(max_length=255)
    pond_type = models.CharField(max_length=100, blank=True, null=True)
    pond_use = models.CharField(max_length=100, blank=True, null=True)
    pond_depth = models.DecimalField(max_digits=5, decimal_places=2, default=0.0)
    pond_depth_type = models.CharField(max_length=50, blank=True, null=True)
    pond_size = models.DecimalField(max_digits=10, decimal_places=2, default="0")
    area_type = models.CharField(max_length=50, blank=True, null=True)
    species_type = models.CharField(max_length=100, blank=True, null=True)
    species_value = models.CharField(max_length=100, blank=True, null=True)
    stocking_time = models.TimeField(blank=True, null=True)
    stocking_date = models.DateField(blank=True, null=True)
    aerator = models.CharField(max_length=100, blank=True, null=True)
    pond_shape = models.CharField(max_length=100, blank=True, null=True)
    pond_status = models.CharField(max_length=50, default='active')
    city_village = models.CharField(max_length=100, blank=True, null=True)
    doc = models.IntegerField(blank=True, null=True)                            # Day of Culture

    status = models.CharField(max_length=20, default='active')                  # For API "status"
    connected = models.BooleanField(default=True)                               # For API "connected" field

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)


    power_center = models.ForeignKey(
        PowerCenter, related_name="ponds", on_delete=models.CASCADE
    )

    def __str__(self):
        return self.pond_id
    
    @property
    def power(self):
        # pond power is True if any feeding motor is online
        if hasattr(self, 'feeding_motor') and self.feeding_motor:
            return self.feeding_motor.status.lower() == "active"
        return False
    
# ---------------------------------------------------------------------------
#                       Feeding Motor (1 per pond)
# ---------------------------------------------------------------------------
class FeedingMotor(models.Model):
    pond = models.OneToOneField(
        Pond, related_name="feeding_motor", on_delete=models.CASCADE
    )
    motor_id = models.CharField(max_length=50, unique=True)
    status = models.CharField(max_length=20)

    def __str__(self):
        return self.motor_id
    
# ----------------------------------------------------------------------------------
#                       Check Tray (multiple per pond)
# ----------------------------------------------------------------------------------
class CheckTray(models.Model):
    pond = models.ForeignKey(
        Pond, related_name="check_trays", on_delete=models.CASCADE
    )
    tray_id = models.CharField(max_length=50, unique=True)
    status = models.CharField(max_length=20)

    def __str__(self):
        return self.tray_id
    
# ------------------------------------------------------------------------------------
#                         Pond Sensor water_quality
# ------------------------------------------------------------------------------------
class WaterQuality(models.Model):
    pond = models.OneToOneField(
        Pond, related_name="water_quality", on_delete=models.CASCADE
    )
    alkalinity = models.DecimalField(max_digits=8, decimal_places=2, null=True, blank=True)
    ammonia = models.DecimalField(max_digits=8, decimal_places=2, null=True, blank=True)
    calcium = models.DecimalField(max_digits=8, decimal_places=2, null=True, blank=True)
    carbonate = models.DecimalField(max_digits=8, decimal_places=2, null=True, blank=True)
    dissolved_oxygen = models.DecimalField(max_digits=8, decimal_places=2, null=True, blank=True)
    doc = models.IntegerField()
    measurement_date = models.DateField()
    hardness = models.DecimalField(max_digits=8, decimal_places=2, null=True, blank=True)
    bicarbonate = models.DecimalField(max_digits=8, decimal_places=2, null=True, blank=True)
    iron = models.DecimalField(max_digits=8, decimal_places=2, null=True, blank=True)
    magnesium = models.DecimalField(max_digits=8, decimal_places=2, null=True, blank=True)
    nitrite = models.DecimalField(max_digits=8, decimal_places=2, null=True, blank=True)
    ph = models.DecimalField(max_digits=4, decimal_places=2, null=True, blank=True)
    do = models.DecimalField(max_digits=4, decimal_places=2, null=True, blank=True)
    salinity = models.DecimalField(max_digits=8, decimal_places=2, null=True, blank=True)
    temperature = models.DecimalField(max_digits=5, decimal_places=2, null=True, blank=True)
    tds = models.DecimalField(max_digits=8, decimal_places=2, null=True, blank=True)
    turbidity = models.DecimalField(max_digits=8, decimal_places=2, null=True, blank=True)
    water_color = models.CharField(max_length=100, null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)


    def __str__(self):
        return f"Water Quality of {self.pond.pond_id}"
