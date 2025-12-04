from django.urls import path
from .views import SignupAPI, SigninAPI, ForgotPasswordAPI, ResetPasswordAPI

urlpatterns = [
    path("signup/", SignupAPI.as_view(), name="user-signup"),                           # POST
    path("signin/", SigninAPI.as_view(), name="user-signin"),                           # POST
    path("forgot-password/", ForgotPasswordAPI.as_view(), name="forgot-password"),      # POST
    path("reset-password/", ResetPasswordAPI.as_view(), name="reset-password"),         # POST
]
