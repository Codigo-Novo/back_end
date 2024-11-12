from django.shortcuts import render
from django.http import HttpRequest
from django.contrib.auth import get_user_model
from rest_framework.mixins import (
    CreateModelMixin, ListModelMixin, RetrieveModelMixin, UpdateModelMixin
)
from rest_framework.viewsets import GenericViewSet
from .serializers import UserSerializer

User = get_user_model()

# Create your views here.

class UserViewSet(GenericViewSet, CreateModelMixin,
                  RetrieveModelMixin, UpdateModelMixin, 
                  ListModelMixin):
      serializer_class = UserSerializer
      queryset = User.objects.all()