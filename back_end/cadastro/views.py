from django.shortcuts import render
from django.http import HttpRequest
from django.contrib.auth import get_user_model
from django.contrib.auth.models import Group
from rest_framework.mixins import (
    CreateModelMixin, ListModelMixin, RetrieveModelMixin, UpdateModelMixin
)
from rest_framework.viewsets import GenericViewSet
from .models import Institution, Category, Donation, DonatedBy
from .serializers import UserSerializer, InstitutionSerializer, CategorySerializer, DonationSerializer, DonatedBySerializer

User = get_user_model()

# Create your views here.

class UserViewSet(GenericViewSet, CreateModelMixin,
                  RetrieveModelMixin, UpdateModelMixin, 
                  ListModelMixin):
      serializer_class = UserSerializer
      queryset = User.objects.all()

class CategoryViewSet(GenericViewSet, CreateModelMixin,
                  RetrieveModelMixin, UpdateModelMixin, 
                  ListModelMixin):
      serializer_class = CategorySerializer
      queryset = Category.objects.all()

class InstitutionViewSet(GenericViewSet, CreateModelMixin,
                  RetrieveModelMixin, UpdateModelMixin, 
                  ListModelMixin):
      serializer_class = InstitutionSerializer
      queryset = Institution.objects.all()

class DonationViewSet(GenericViewSet, CreateModelMixin,
                  RetrieveModelMixin, UpdateModelMixin, 
                  ListModelMixin):
      serializer_class = DonationSerializer
      queryset = Donation.objects.all()

class DonatedByViewSet(GenericViewSet, CreateModelMixin,
                  RetrieveModelMixin, UpdateModelMixin, 
                  ListModelMixin):
      serializer_class = DonatedBySerializer
      queryset = DonatedBy.objects.all()

def setUserDonator(request, pk):
    if request.method == 'POST':
        user = User.objects.get(pk=pk)
        grupo = Group.objects.get(name='Donator')
        user.groups.add(grupo)
        user.save()

def setUserInstitution(request, pk):
    if request.method == 'POST':
        user = User.objects.get(pk=pk)
        grupo = Group.objects.get(name='Institution')
        user.groups.add(grupo)
        user.save()