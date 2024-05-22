from django.urls import path
from .views import (
    AdminRegisterAPIView, ClientRegisterAPIView, MyTokenObtainPairView, RequestOTPView, ResetPasswordView, StylistRegisterAPIView,  VerifyOTPView,
)
from rest_framework_simplejwt.views import TokenRefreshView

urlpatterns = [

    # Register URLs
    path('admin/register/', AdminRegisterAPIView.as_view(), name='admin_register'),
    path('client/register/', ClientRegisterAPIView.as_view(), name='client_register'),
    path('stylist/register/', StylistRegisterAPIView.as_view(),
         name='stylist_register'),
    # Login URLs
    path('token/', MyTokenObtainPairView.as_view(), name='token_obtain_pair'),
    # password recovery
    path('password-recovery/request-otp/',
         RequestOTPView.as_view(), name='request_otp'),
    path('password-recovery/verify-otp/',
         VerifyOTPView.as_view(), name='verify_otp'),
    path('password-recovery/reset-password/',
         ResetPasswordView.as_view(), name='reset_password'),
]
