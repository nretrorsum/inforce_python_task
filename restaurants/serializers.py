from rest_framework import serializers
from .models import Restaurant, Menu

class RestaurantSerializer(serializers.ModelSerializer):
    """
    Serializer for the Restaurant model
    """
    class Meta:
        model = Restaurant
        fields = ['id', 'name', 'address', 'phone_number']
        
    def validate_phone_number(self, value):
        if len(value) < 10 or not value.isdigit():
            raise serializers.ValidationError("Phone number must be at least 10 digits long and contain only numbers.")
        return value
    
    def validate_address(self, value):

        if not value.strip():
            raise serializers.ValidationError("Address cannot be empty.")
        return value

class MenuSerializer(serializers.ModelSerializer):
    """
    Serializer for the Menu model with additional restaurant name field
    """
    restaurant_name = serializers.SerializerMethodField()

    class Meta:
        model = Menu
        fields = ['id', 'restaurant', 'restaurant_name', 'date', 'items']

    def get_restaurant_name(self, obj):
        return obj.restaurant.name

class MenuForVoteSerializer(serializers.ModelSerializer):
    """
    Serializer for the Menu model with restaurant name for voting
    """
    restaurant_name = serializers.SerializerMethodField()

    class Meta:
        model = Menu
        fields = ['id', 'restaurant', 'restaurant_name', 'date']

    def get_restaurant_name(self, obj):
        return obj.restaurant.name
