from django.shortcuts import render
from rest_framework import generics, viewsets, status
from rest_framework.response import Response
from .models import Restaurant, Menu
from .serializers import RestaurantSerializer, MenuSerializer
from rest_framework.permissions import IsAuthenticated, AllowAny
from django.utils import timezone
from rest_framework.exceptions import ValidationError
from django.http import JsonResponse


class RestaurantCreateView(generics.CreateAPIView):
    """
    API view for creating a new restaurant
    """
    queryset = Restaurant.objects.all()
    serializer_class = RestaurantSerializer
    permission_classes = [AllowAny]  # Change to a custom permission in the future
    
    def post(self, request, *args, **kwargs):
        return super().post(request, *args, **kwargs)

class RestaurantViewSet(viewsets.ModelViewSet):
    """
    API viewset for retrieving, updating, and deleting restaurants
    """
    queryset = Restaurant.objects.all()
    serializer_class = RestaurantSerializer
    permission_classes = [IsAuthenticated]

class MenuCreateView(generics.CreateAPIView):
    """
    API view for creating a new menu
    """
    queryset = Menu.objects.all()
    serializer_class = MenuSerializer
    permission_classes = [AllowAny]  # Change to a custom permission in the future
    
    def perform_create(self, serializer):
        date = serializer.validated_data.get('date')
        if date < timezone.now().date():
            raise ValidationError({'date': 'Cannot set a menu for a past date. Please select today or a future date.'})
        super().perform_create(serializer)

class TodayMenuView(generics.ListAPIView):
    """
    API view for listing today's menu items
    """
    serializer_class = MenuSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        date = timezone.now().date()
        return Menu.objects.filter(date=date)