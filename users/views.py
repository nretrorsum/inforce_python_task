from django.shortcuts import render
from django.contrib.auth import authenticate, login
from rest_framework.permissions import AllowAny
from rest_framework_simplejwt.views import (
    TokenObtainPairView as BaseTokenObtainPairView,
    TokenRefreshView as BaseTokenRefreshView,
)
from rest_framework import generics
from rest_framework.response import Response
from rest_framework import status
from users.serializers import UserRegisterSerializer
from users.models import CustomUser

class UserRegisterView(generics.CreateAPIView):
    """
    Handles user registration.
    """
    queryset = CustomUser.objects.all()
    serializer_class = UserRegisterSerializer
    permission_classes = [AllowAny]

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        headers = self.get_success_headers(serializer.data)
        return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)

class TokenObtainPairView(BaseTokenObtainPairView):
    """
    Handles JWT token creation and sets tokens in cookies.
    """
    permission_classes = [AllowAny]

    def post(self, request, *args, **kwargs):
        response = super().post(request, *args, **kwargs)
        user = authenticate(request, email=request.data.get('email'), password=request.data.get('password'))
        if user:
            login(request, user)
        token = response.data.get('access')
        refresh_token = response.data.get('refresh')

        if token:
            # Set the access token in a cookie
            response.set_cookie(
                'jwt_token',
                token,
                max_age=300,  # Token lifetime (5 minutes)
                httponly=True,  # To prevent JavaScript access
                secure=True,  # If using HTTPS
                samesite='Strict',
            )
        if refresh_token:
            # Set the refresh token in a separate cookie
            response.set_cookie(
                'refresh_token',
                refresh_token,
                max_age=400,
                httponly=True,
                secure=True,
                samesite='Strict',
            )
        return response

class TokenRefreshView(BaseTokenRefreshView):
    """
    Handles JWT token refreshing and sets the refreshed token in a cookie.
    """
    permission_classes = [AllowAny]
    throttle_scope = 'token_refresh'
    
    def post(self, request, *args, **kwargs):
        response = super().post(request, *args, **kwargs)
        # Get the refreshed token from the response data
        token = response.data.get('access')
        if token:
            response.set_cookie(
                'jwt_token',
                token,
                max_age=300,
                httponly=True,
                secure=True,
                samesite='Strict',
            )
        return response
