from django.contrib import admin
from .models import PowerCenter, Pond, FeedingMotor, CheckTray, PondReading

# Inline for FeedingMotor under Pond
class FeedingMotorInline(admin.StackedInline):
    model = FeedingMotor
    extra = 0

# Inline for CheckTray under Pond
class CheckTrayInline(admin.TabularInline):
    model = CheckTray
    extra = 0

# Inline for PondReading (DO, PH, Temp, Salinity readings)
class PondReadingInline(admin.TabularInline):
    model = PondReading
    extra = 0

# Admin for Pond
class PondAdmin(admin.ModelAdmin):
    inlines = [FeedingMotorInline, CheckTrayInline, PondReadingInline]
    list_display = ("pond_id", "power_center", "status", "connected")
    search_fields = ("pond_id", "power_center__pc_id", "status")
    list_filter = ("status", "connected")

# Inline for Pond inside PowerCenter
class PondInline(admin.StackedInline):
    model = Pond
    extra = 0
    show_change_link = True

# Admin for PowerCenter
class PowerCenterAdmin(admin.ModelAdmin):
    inlines = [PondInline]
    list_display = ("pc_id", "status")
    search_fields = ("pc_id", "status")
    list_filter = ("status",)

# Register models
admin.site.register(PowerCenter, PowerCenterAdmin)
admin.site.register(Pond, PondAdmin)
admin.site.register(FeedingMotor)
admin.site.register(CheckTray)
admin.site.register(PondReading)
