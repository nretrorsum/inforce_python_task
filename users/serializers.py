from django.core.validators import EmailValidator
from rest_framework import serializers
from rest_framework.exceptions import ValidationError
from rest_framework.validators import UniqueValidator

from .models import CustomUser
from .validators import CustomUserValidator

class BasePasswordSerializer(serializers.ModelSerializer):
    """
    Base serializer for handling password validation
    """
    def validate_passwords(self, password, password2):
        if password != password2:
            raise serializers.ValidationError({"password2": "Password fields didn't match."})
        try:
            CustomUserValidator.validate_password(password)
        except ValidationError as error:
            raise serializers.ValidationError({"password": error.detail})

class UserRegisterSerializer(BasePasswordSerializer):
    """
    Serializer for user registration
    """
    first_name = serializers.CharField(required=True, max_length=20)
    last_name = serializers.CharField(required=True, max_length=20)
    email = serializers.EmailField(required=True,
                                   validators=[UniqueValidator(queryset=CustomUser.objects.all())])
    password = serializers.CharField(write_only=True, required=True)
    password2 = serializers.CharField(write_only=True, required=True)
    phone_number = serializers.CharField(required=True)

    class Meta:
        model = CustomUser
        fields = ['id', 'first_name', 'last_name', 'email', 'password', 'password2', 'phone_number']

    def validate(self, attrs):
        self.validate_passwords(attrs.get('password'), attrs.get('password2'))
        try:
            CustomUserValidator.validate_phone_number(attrs.get('phone_number'))
        except ValidationError as error:
            raise serializers.ValidationError(error.detail)
        return attrs

    def create(self, validated_data):
        user = CustomUser.objects.create_user(
            first_name=validated_data['first_name'],
            last_name=validated_data['last_name'],
            email=validated_data['email'],
            phone_number=validated_data['phone_number'],
            password=validated_data['password']
        )
        return user
