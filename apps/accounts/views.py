import jwt

from django.contrib.sites.shortcuts import get_current_site
from django.contrib.auth import authenticate
from django.urls import reverse
from django.conf import settings

from rest_framework.response import Response
from rest_framework import generics, status, views
from rest_framework.permissions import (IsAuthenticatedOrReadOnly,
                                        IsAuthenticated)
from rest_framework_simplejwt.tokens import RefreshToken

from .models import User, Profile
from apps.accounts.serializers import (RegisterSerializer, LoginSerializer,
                                       ProfileSerializer, LogoutSerializer)
from apps.accounts.utils import Util


# Create your views here.
class RegisterAPI(views.APIView):
    def post(self, request):
        user = request.data
        serializer = RegisterSerializer(data = user)

        if serializer.is_valid():
            serializer.save()
            user_data = serializer.data

            user = User.objects.get(email= user_data['email'])
            token = RefreshToken.for_user(user).access_token

            current_site = get_current_site(request).domain
            relative_link = reverse('accounts:verify_email')
            abs_url = 'http://' + str(current_site) + relative_link+'?token='+str(token)

            email_body = f'''HI! {user.username},\n
                            Use Link Below to Verify Your Email:\n\t{abs_url}'''

            email_data = {'subject': 'Email Verificaton', 'body': email_body}

            Util.send_email(email_data)
            return Response({'msg': 'Email Verification Sent.'}, status = status.HTTP_201_CREATED)
        else:
            return Response(status = status.HTTP_400_BAD_REQUEST)


class VerifyEmailAPI(generics.GenericAPIView):
    def get(self, request):
        token = request.GET.get('token')

        try:
            payload = jwt.decode(token, settings.SECRET_KEY,algorithms=['HS256'])
            user = User.objects.get(id=payload['user_id'])

            resp = ''
            if not user.is_verified:
                user.is_verified = True
                user.save()
                resp = 'Email Successfully Verified'
            else:
                resp = 'Already Verified'
            
            return Response({'msg': resp}, status= status.HTTP_200_OK)
        except jwt.ExpiredSignatureError:
            return Response({'error': 'Activation Expired'}, status=status.HTTP_400_BAD_REQUEST)
        except jwt.exceptions.DecodeError:
            return Response({'error': 'Invalid Token'}, status=status.HTTP_400_BAD_REQUEST)



class LoginAPI(views.APIView):
    def post(self, request):
        serializer = LoginSerializer(data=request.data)

        serializer.is_valid(raise_exception=True)
        email = serializer.data.get('email')
        password = serializer.data.get('password')
        user = authenticate(email=email, password=password)

        if user is not None:
            token = self.get_tokens_for_user(user)
            return Response(token, status=status.HTTP_200_OK)
        else:
            return Response({'error':'Email or Password is not valid'}, status=status.HTTP_404_NOT_FOUND)

    def get_tokens_for_user(self, user):
        refresh = RefreshToken.for_user(user)

        return {
            'refresh': str(refresh),
            'access': str(refresh.access_token),
            }


class LogoutAPI(views.APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        serializer = LogoutSerializer(data=request.data)

        if serializer.is_valid(raise_exception=True):
            serializer.save()

        return Response(status=status.HTTP_204_NO_CONTENT)



class ProfileAPI(views.APIView):
  permission_classes = [IsAuthenticatedOrReadOnly]

  def get(self, request, username, format=None):
    profile = Profile.objects.filter(user__username = username)

    serializer = ProfileSerializer(profile[0])
    return Response(serializer.data, status=status.HTTP_200_OK)

  def put(self, request, username, format=None):
    if request.user.username == username:
        profile_instance = Profile.objects.get(user__username = username)

        serializer = ProfileSerializer(
                            instance= profile_instance,
                            data = request.data,
                            partial=True)

        if serializer.is_valid(raise_exception=True):
            serializer.save()
            return Response({'msg': 'Profile Updated'}, status = status.HTTP_200_OK)
    
    return Response({'error':'You are not authorized to make this change'}, status = status.HTTP_400_BAD_REQUEST)