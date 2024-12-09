import json
from django.http import HttpRequest, JsonResponse
from django.contrib.auth import get_user_model, authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import Group
from rest_framework.decorators import api_view
from rest_framework.response import Response
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

def setUserDonator(request: HttpRequest):
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            username = data.get('username')
            user = User.objects.get(username=username)
            grupo, criado = Group.objects.get_or_create(name='Donator')
            user.groups.add(grupo)
            user.save()
            return JsonResponse({'message': 'Usuário definido como doador.'})
        except json.JSONDecodeError:
            return JsonResponse({'message': 'Invalid JSON'}, status=400)

def setUserInstitution(request: HttpRequest):
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            username = data.get('username')
            user = User.objects.get(username=username)
            grupo, criado = Group.objects.get_or_create(name='Institution')
            user.groups.add(grupo)
            user.save()
            return JsonResponse({'message': 'Usuário definido como instituição.'})
        except json.JSONDecodeError:
            return JsonResponse({'message': 'Invalid JSON'}, status=400)

def loginView(request: HttpRequest):
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            username = data.get('username')
            password = data.get('password')
            user = authenticate(request, username=username, password=password)
            if user is not None:
                login(request, user)
                message = 'Usuário autenticado com sucesso.'
                return JsonResponse({'message': message})
            message = 'Credenciais inválidas.'
            return JsonResponse({'message': message}, status=400)
        except json.JSONDecodeError:
            return JsonResponse({'message': 'Invalid JSON'}, status=400)
        
def logoutView(request: HttpRequest):
    if request.method == 'POST':
        logout(request)
        message = 'Usuário desconectado!'
        return JsonResponse({'message': message})
    
def createInstitution(request: HttpRequest):
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            username = data.get('username')
            user = User.objects.get(username=username)
            try:
                user.groups.get(name='Institution')
                institution = Institution(user=user)
                institution.description = data.get('description')
                try:
                    institution.lat = data.get('lat')
                    institution.long = data.get('long')
                except:
                    message = 'Localização inválida.'
                    return JsonResponse({'message': message}, status=400)
                institution.save()
                message = 'Instituição criada com sucesso.'
                return JsonResponse({'message': message})
            except:
                message = 'Usuário não é uma instituição.'
                return JsonResponse({'message': message}, status=400)
        except json.JSONDecodeError:
            return JsonResponse({'message': 'Invalid JSON'}, status=400)
        
def deleteUser(request: HttpRequest):
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            username = data.get('username')
            password = data.get('password')
            user = authenticate(request, username=username, password=password)
            if user is not None:
                user.is_active = False
                user.save()
                message = 'Usuário desativado.'
                return JsonResponse({'message': message})
            else:
                message = 'Senha inválida.'
                return JsonResponse({'message': message}, status=400)
        except json.JSONDecodeError:
            return JsonResponse({'message': 'Invalid JSON'}, status=400)

@api_view(['GET'])        
@login_required
def checkAuth(request: HttpRequest):
    return Response({'authenticated': True, 'username': request.user.username})