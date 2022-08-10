import email
from django.shortcuts import render,
from django.contrib.sites.shortcuts import get_current_site

from rest_framework.response import Response
from rest_framework import generics, status
from rest_framework_simplejwt.tokens import RefreshToken

from apps.accounts.serializers import RegisterSerializer
from apps.accounts.utils import Util
from .models import User

# Create your views here.
class RegisterView(generics.GenericAPIView):
    serializer_class = RegisterSerializer

    def post(self, request):
        user = request.data
        serializer = self.serializer_class(data = user)

        if serializer.is_valid():
            serializer.save()
            user_data = serializer.data

            user = User.objects.get(email= user_data['email'])
            token = RefreshToken.for_user(user).access_token

            current_site = get_current_site(request)
            relative_link = 'verify_email'

            abs_url = 'http://' + current_site + relative_link+'?token='+token.access

            email_body = 'HI!' + user.username+',\n Use Link Below to Verify your email:\n' + abs_url
            data = {'email_subject': 'Email Verificaton', 'email_body':email_body}

            Util.send_email(data)

            return Response(user_data, status = status.HTTP_201_CREATED)
        else:
            return Response(status = status.HTTP_400_BAD_REQUEST)


class VerifyEmail(generics.GenericAPIView):
    def get(self):
        pass