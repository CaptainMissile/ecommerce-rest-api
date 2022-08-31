from django.urls import path

from .views import (RegisterAPI, VerifyEmailAPI, LoginAPI, ProfileAPI,
                    PasswordResetReqAPI, PasswordTokenCheckAPI,
                    SetNewPasswordAPIView, ProfileUpdateAPI)

app_name = 'accounts'

urlpatterns = [
    path('register/', RegisterAPI.as_view(), name='register'),
    path('verify-email/', VerifyEmailAPI.as_view(), name='verify_email'),
    path('login/', LoginAPI.as_view(), name="login"),
    path('password-reset-req/', PasswordResetReqAPI.as_view(), name="password-reset-req"),
    path('password-reset-confirm/<uidb64>/<token>/', PasswordTokenCheckAPI.as_view(), name='password-reset-confirm'),
    path('password-reset-complete/', SetNewPasswordAPIView.as_view(),name='password-reset-complete'),
    path('profile/<str:username>', ProfileAPI.as_view(), name="profile"),
    path('profile-update/<str:username>', ProfileUpdateAPI.as_view(), name="profile-update")
]
