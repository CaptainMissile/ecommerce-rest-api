from django.urls import path

from .views import RegisterAPI, VerifyEmailAPI, LoginAPI

app_name = 'accounts'

urlpatterns = [
    path('register/', RegisterAPI.as_view(), name='register'),
    path('verify-email/', VerifyEmailAPI.as_view(), name='verify_email'),
    path('login/', LoginAPI.as_view(), name="login")
]
