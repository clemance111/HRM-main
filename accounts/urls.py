from django.urls import path
from rest_framework.routers import DefaultRouter
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)

from accounts.views import (UserViewset,
CheckOTPView,ResendOTPView,ActivateAccountAPI,ForgotPasswordAPI,
ResetPasswordAPI,ResendPasswordResetOTP,
)
route=DefaultRouter()
route.register('users',UserViewset)
urlpatterns = [
    path('otp-validation/',CheckOTPView.as_view(),name="check-otp"),
    path('resend-otp/',ResendOTPView.as_view(),name='resendotp'),
    path('activate-account/',ActivateAccountAPI.as_view(),name="account-activate"),
    path('forgot-password/',ForgotPasswordAPI.as_view(),name="password-reset-request"),
    path('reset-password/<str:otp>/',ResetPasswordAPI.as_view(),name="passowrd-reset-comfirm"),
    path('resend-reset-password-otp/',ResendPasswordResetOTP.as_view(),name="resend-otp-reset-password"),
    path('token/create/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
]+route.urls
