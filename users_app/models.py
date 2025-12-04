from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager
#-------------------------------------------------------------
# Custom user manager to handle user creation
#-------------------------------------------------------------
class UserManager(BaseUserManager):
    def create_user(self, email, phone, password=None, **extra_fields):
        """
        Creates and saves a User with the given email, phone, and password.
        """
        if not email:
            raise ValueError("Email is required")
        if not phone:
            raise ValueError("Phone number is required")
        
        # Normalize email (convert domain part to lowercase)
        email = self.normalize_email(email)
        
        # Create a new user instance with provided details
        user = self.model(email=email, phone=phone, **extra_fields)
        
        # Set the password (hashing it properly)
        user.set_password(password)
        
        # Save the user to the database
        user.save(using=self._db)
        return user

#------------------------------------
# Custom User model
#------------------------------------
class User(AbstractBaseUser):
    uid = models.AutoField(primary_key=True)
    username = models.CharField(max_length=100)
    email = models.EmailField(unique=True)
    phone = models.CharField(max_length=15, unique=True)
    aadhar = models.CharField(max_length=12, unique=True, null=True, blank=True)
    address = models.TextField(blank=True, null=True)
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    # Assign the custom user manager
    objects = UserManager()

    # Field used for login authentication
    USERNAME_FIELD = "phone"
    
    # Fields required when creating a user via createsuperuser
    REQUIRED_FIELDS = ["email", "username"]

    @property
    def display_uid(self):
        """
        Returns the UID in a formatted way: U-1 
        """
        return f"U-{self.uid}"  # Uses the uid field

    def __str__(self):
        """
        Returns a human-readable representation of the user.
        """
        return f"{self.username} ({self.phone})"
