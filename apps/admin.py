from django.contrib import admin
from .models import PowerCenter, Pond, FeedingMotor, CheckTray

# Inline for FeedingMotor under Pond
class FeedingMotorInline(admin.StackedInline):
    model = FeedingMotor
    extra = 0  # do not show extra empty forms

# Inline for CheckTray under Pond
class CheckTrayInline(admin.TabularInline):
    model = CheckTray
    extra = 0

# Admin for Pond, showing FeedingMotor and CheckTray
class PondAdmin(admin.ModelAdmin):
    inlines = [FeedingMotorInline, CheckTrayInline]
    list_display = ('pond_id', 'power_center', 'status')
    search_fields = ('pond_id', 'power_center__pc_id', 'status')
    list_filter = ('status',)

# Inline for Pond under PowerCenter
class PondInline(admin.StackedInline):
    model = Pond
    extra = 0
    show_change_link = True  # click to edit Pond and see FeedingMotor / CheckTray

# Admin for PowerCenter, showing Ponds inline
class PowerCenterAdmin(admin.ModelAdmin):
    inlines = [PondInline]
    list_display = ('pc_id', 'status')
    search_fields = ('pc_id', 'status')
    list_filter = ('status',)

# Register models
admin.site.register(PowerCenter, PowerCenterAdmin)
admin.site.register(Pond, PondAdmin)
admin.site.register(FeedingMotor)
admin.site.register(CheckTray)
