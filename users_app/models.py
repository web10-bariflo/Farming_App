from django.db import models
from django.utils import timezone
# Create your models here.

# -------------------------------
# User
# -------------------------------

class User(models.Model):
    uid = models.CharField(max_length=50, primary_key=True)                     # Primary key
    email = models.EmailField(unique=True)                                      # Unique email
    name = models.CharField(max_length=255)                                     # User name
    mobile_no = models.CharField(max_length=20, blank=True, null=True)
    state = models.CharField(max_length=100, blank=True, null=True)
    district = models.CharField(max_length=100, blank=True, null=True)         
    city_village = models.CharField(max_length=100, blank=True, null=True)
    pin_code = models.CharField(max_length=20, blank=True, null=True)
    photo_url = models.TextField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)                        # Set timestamp on creation
    updated_at = models.DateTimeField(auto_now=True)                            # Update timestamp on save

    def __str__(self):
        return self.name
    
