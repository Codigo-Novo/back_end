from rest_framework.serializers import ModelSerializer
from django.contrib.auth import password_validation
from rest_framework import serializers
from django.core.exceptions import ValidationError
from .models import Institution, KeyWord
from django.contrib.auth import get_user_model

User = get_user_model()

class UserSerializer(ModelSerializer):
    class Meta:
        model = User
        fields = (
            'id', 'username', 'first_name', 'password', 'email'
        )
        extra_kwargs = {
            'password': {'write_only': True},
        }

    def validate_password(self, value):
        try:
            password_validation.validate_password(value)
        except ValidationError as exc:
            raise serializers.ValidationError(str(exc))
        return value
            
    def create(self, validated_data):
        user = super().create(validated_data)
        user.set_password(validated_data['password'])
        user.is_active = True
        user.save()
        return user
            
    def update(self, instance, validated_data):
        user = super().update(instance, validated_data)
        if 'password' in validated_data:
            user.set_password(validated_data['password'])
            user.save()
        return user

class KeyWordSerializer(ModelSerializer):
    class Meta:
        model = KeyWord
        fields = (
            'id', 'name'
        )

class InstitutionSerializer(ModelSerializer):
    user = serializers.CharField(source='user.first_name', read_only=True)

    class Meta:
        model = Institution
        fields = (
            'id', 'user', 'long', 'lat', 'keywords', 'description', 'cpforcnpj', 'is_active'
        )