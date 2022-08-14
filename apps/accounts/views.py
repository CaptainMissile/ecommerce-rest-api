from django.contrib.sites.shortcuts import get_current_site
from django.urls import reverse
from django.conf import settings

import jwt
from rest_framework.response import Response
from rest_framework import generics, status
from rest_framework_simplejwt.tokens import RefreshToken

from apps.accounts.serializers import RegisterSerializer
from apps.accounts.utils import Util
from .models import User

# Create your views here.
class RegisterAPI(generics.GenericAPIView):
    serializer_class = RegisterSerializer

    def post(self, request):
        user = request.data
        serializer = self.serializer_class(data = user)

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


class LoginAPI(generics.GenericAPIView):
    def get(self, request):
        pass