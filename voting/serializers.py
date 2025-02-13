from rest_framework import serializers
from .models import Vote
from restaurants.models import Restaurant, Menu
from restaurants.serializers import RestaurantSerializer, MenuSerializer
from django.utils import timezone

class VoteSerializer(serializers.ModelSerializer):
    """
    Serializer for the Vote model.
    """
    class Meta:
        model = Vote
        fields = ['restaurant']

    def validate(self, data):
        user = data.get('user')
        date = data.get('date')
        if Vote.objects.filter(user=user, date=date).exists():
            raise serializers.ValidationError("You have already voted today.")
        return data
        

class RestaurantSerializer(serializers.ModelSerializer):
    """
    Serializer for the Restaurant model, including today's menu.
    """
    menu = serializers.SerializerMethodField()
    
    class Meta:
        model = Restaurant
        fields = ['id', 'name', 'address', 'phone_number', 'menu']
        
    def get_menu(self, obj):
        today = timezone.now().date()
        menu = Menu.objects.filter(restaurant=obj, date=today).first()
        if menu:
            return MenuSerializer(menu).data
        return None
