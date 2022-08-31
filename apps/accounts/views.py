import os
import jwt

from django.http import HttpResponsePermanentRedirect
from django.contrib.sites.shortcuts import get_current_site
from django.contrib.auth import authenticate
from django.contrib.auth.tokens import PasswordResetTokenGenerator
from django.utils.http import urlsafe_base64_decode, urlsafe_base64_encode
from django.utils.encoding import (smart_str, force_str, smart_bytes,
                                    DjangoUnicodeDecodeError)
from django.urls import reverse
from django.conf import settings

from rest_framework.views import Response, APIView
from rest_framework import generics, status, views
from rest_framework.permissions import (IsAuthenticatedOrReadOnly,
                                        IsAuthenticated)
from rest_framework_simplejwt.tokens import RefreshToken
from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi


from apps.accounts.models import User, Profile
from apps.accounts.serializers import (RegisterSerializer, LoginSerializer,
                                       ResetPasswordReqSerializer,
                                       SetNewPasswordSerializer,
                                       ProfileSerializer, LogoutSerializer,
                                       EmailVerificationSerializer,
                                       SetNewPasswordSerializer)

from apps.accounts.permissions import IsVerified
from apps.accounts.utils import Util


class CustomRedirect(HttpResponsePermanentRedirect):
    allowed_schemes = [os.environ.get('APP_SCHEME'), 'http', 'https']

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
    serializer_class = EmailVerificationSerializer

    token_param_config = openapi.Parameter('token', in_=openapi.IN_QUERY,
                                            description='Description',
                                            type=openapi.TYPE_STRING)

    @swagger_auto_schema(manual_parameters=[token_param_config])
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
    permission_classes = [IsVerified]
    serializer_class = LoginSerializer

    def post(self, request):
        serializer = self.serializer_class(data=request.data)

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


class PasswordResetReqAPI(APIView):
    def post(self, request):
        serializer = ResetPasswordReqSerializer(data=request.data)

        email = request.data.get('email', '')

        if User.objects.filter(email=email).exists():
            user = User.objects.get(email=email)

            uidb64 = urlsafe_base64_encode(smart_bytes(user.id))
            token = PasswordResetTokenGenerator().make_token(user)
            current_site = get_current_site(request).domain
            relativeLink = reverse('accounts:password-reset-confirm', kwargs={'uidb64': uidb64, 'token': token})

            redirect_url = reverse('accounts:password-reset-complete')

            absurl = 'http://'+current_site + relativeLink
            email_body = f'Hello,\n Use link below to reset your password \n{absurl}?redirect_url={redirect_url}'

            data = {'body': email_body, 'to_email': user.email,
                    'subject': 'Reset your passsword'}
            Util.send_email(data)

        return Response({'success': 'We have sent you a link to reset your password'}, status=status.HTTP_200_OK)


class PasswordTokenCheckAPI(APIView):
    serializer_class = SetNewPasswordSerializer

    def get(self, request, uidb64, token):

        redirect_url = request.GET.get('redirect_url')
        print(redirect_url)
        try:
            id = smart_str(urlsafe_base64_decode(uidb64))
            user = User.objects.get(id=id)

            if not PasswordResetTokenGenerator().check_token(user, token):
                if len(redirect_url) > 3:
                    return CustomRedirect(redirect_url+'?token_valid=False')
                else:
                    return CustomRedirect(os.environ.get('FRONTEND_URL', '')+'?token_valid=False')

            if redirect_url and len(redirect_url) > 3:
                print('Hoep you are here')
                return CustomRedirect(redirect_url+'/?token_valid=True&message=Credentials Valid&uidb64='+uidb64+'&token='+token)
            else:
                return CustomRedirect(os.environ.get('FRONTEND_URL', '')+'?token_valid=False')

        except DjangoUnicodeDecodeError as identifier:
            try:
                if not PasswordResetTokenGenerator().check_token(user):
                    return CustomRedirect(redirect_url+'?token_valid=False')
                    
            except UnboundLocalError as e:
                return Response({'error': 'Token is not valid, please request a new one'}, status=status.HTTP_400_BAD_REQUEST)


class SetNewPasswordAPIView(generics.GenericAPIView):
    serializer_class = SetNewPasswordSerializer

    def patch(self, request):
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        return Response({'success': True, 'message': 'Password reset success'}, status=status.HTTP_200_OK)


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