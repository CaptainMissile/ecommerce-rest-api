from django.shortcuts import render
from rest_framework.response import Response
from rest_framework import generics, status

from apps.accounts.serializers import RegisterSerializer

# Create your views here.
class RegisterView(generics.GenericAPIView):
    serializer_class = RegisterSerializer

    def post(self, request):
        user = request.data
        serializer = self.serializer_class(data = user)

        if serializer.is_valid():
            serializer.save()
            user_data = serializer.data
            return Response(user_data, status = status.HTTP_201_CREATED)
        else:
            return Response(status = status.HTTP_400_BAD_REQUEST)


