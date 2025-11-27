from django.contrib import admin
from .models import User

# Register your models here.
@admin.register(User)
# Admin for User
class UserAdmin(admin.ModelAdmin):
    list_display = ("uid", "name", "email", "mobile_no", "city_village", "district", "state")
    search_fields = ("uid", "name", "email", "mobile_no")
    list_filter = ("state", "district", "city_village")
