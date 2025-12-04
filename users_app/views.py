from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .serializers import UserSignUpSerializer
from .models import User

# -----------------------------
# API for User Signup
# -----------------------------
class SignupAPI(APIView):
    """
    Handles user registration (signup).
    Accepts POST requests with user details and creates a new user.
    """
    def post(self, request):
        serializer = UserSignUpSerializer(data=request.data)
        
        if serializer.is_valid():
            serializer.save()
            return Response({"message": "Signup successful"}, status=201)
        
        return Response(serializer.errors, status=400)


# -----------------------------
# API for User Signin
# -----------------------------
class SigninAPI(APIView):
    """
    Handles user login (signin).
    Accepts POST requests with username (phone/email) and password.
    Authenticates the user and returns basic user info on success.
    """
    def post(self, request):
        data = request.data or {}
        phone_or_email = data.get("username") or data.get("phone") or data.get("email")
        password = data.get("password")

        if not phone_or_email or not password:
            return Response(
                {"error": "Username (phone/email) and password are required"},
                status=status.HTTP_400_BAD_REQUEST
            )

        # Find user
        try:
            if "@" in phone_or_email:
                user = User.objects.get(email=phone_or_email)
            else:
                user = User.objects.get(phone=phone_or_email)
        except User.DoesNotExist:
            return Response({"error": "User not found"}, status=404)

        # Check password
        if not user.check_password(password):
            return Response({"error": "Incorrect password"}, status=400)

        return Response({
            "message": "Signin successful",
            "user_id": str(user.uid),
            "username": user.username,
            "email": user.email,
            "phone": user.phone
        }, status=200)

# -----------------------------
# API for Forgot Password
# -----------------------------
class ForgotPasswordAPI(APIView):
    """
    User enters email or phone.
    System checks if user exists and returns a success response.
    Next step: Reset password.
    """
    def post(self, request):
        identifier = request.data.get("email") or request.data.get("phone")

        if not identifier:
            return Response({"error": "Email or Phone is required"}, status=400)

        # Find user
        try:
            if "@" in identifier:
                user = User.objects.get(email=identifier)
            else:
                user = User.objects.get(phone=identifier)
        except User.DoesNotExist:
            return Response({"error": "User not found"}, status=404)

        return Response({
            "message": "User verified. You can reset your password now.",
            "user_id": str(user.uid)
        }, status=200)

# -----------------------------
# API for Reset Password
# -----------------------------
class ResetPasswordAPI(APIView):
    """
    User enters email/phone + new password + confirm password.
    System updates password if both match and new password is not same as previous.
    """
    def post(self, request):
        identifier = request.data.get("email") or request.data.get("phone")
        new_password = request.data.get("new_password")
        confirm_password = request.data.get("confirm_password")

        # Required fields check
        if not identifier:
            return Response({"error": "Email or Phone is required"}, status=400)

        if not new_password or not confirm_password:
            return Response({"error": "Both password fields are required"}, status=400)

        if new_password != confirm_password:
            return Response({"error": "Passwords do not match"}, status=400)

        # Find user
        try:
            if "@" in identifier:
                user = User.objects.get(email=identifier)
            else:
                user = User.objects.get(phone=identifier)
        except User.DoesNotExist:
            return Response({"error": "User not found"}, status=404)

        # Check if new password is same as previous
        if user.check_password(new_password):
            return Response(
                {"error": "New password cannot be the same as the old password"},
                status=400
            )

        # Update password
        user.set_password(new_password)
        user.save()

        return Response({"message": "Password reset successful"}, status=200)
