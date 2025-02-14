import json
from collections import Counter
from django.http import HttpRequest, JsonResponse
from django.contrib.auth import get_user_model, authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import Group
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from rest_framework.mixins import (
    CreateModelMixin, ListModelMixin, RetrieveModelMixin, UpdateModelMixin
)
from rest_framework.permissions import AllowAny
from rest_framework.viewsets import GenericViewSet
from .models import Institution, KeyWord
from .serializers import UserSerializer, InstitutionSerializer, KeyWordSerializer

User = get_user_model()

# Create your views here.

class UserViewSet(GenericViewSet, CreateModelMixin,
                  RetrieveModelMixin, UpdateModelMixin, 
                  ListModelMixin):
      serializer_class = UserSerializer
      queryset = User.objects.all()
      permission_classes = [AllowAny]

class KeyWordViewSet(GenericViewSet, CreateModelMixin,
                  RetrieveModelMixin, UpdateModelMixin, 
                  ListModelMixin):
      serializer_class = KeyWordSerializer
      queryset = KeyWord.objects.all()
      permission_classes = [AllowAny]

class InstitutionViewSet(GenericViewSet, CreateModelMixin,
                  RetrieveModelMixin, UpdateModelMixin, 
                  ListModelMixin):
      serializer_class = InstitutionSerializer
      queryset = Institution.objects.all()
      permission_classes = [AllowAny]

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
            user = request.user
            try:
                user.groups.get(name='Institution')
                try:
                    institution = Institution.objects.get(user=user.pk)
                    message = 'Instituição já foi criada.'
                    return JsonResponse({'message': message}, status=400)
                except:
                    institution = Institution(user=user)
                    institution.description = data.get('description')
                    institution.cpforcnpj = data.get('cpforcnpj')
                    institution.lat = data.get('lat')
                    institution.long = data.get('long')
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
    return Response({'authenticated': True, 'username': request.user.username, 'id': request.user.id})

@api_view(['GET'])        
@login_required
def checkInstitution(request: HttpRequest):
    if request.user.groups.filter(name='Institution').exists():
        return Response({'institution': True, 'username': request.user.username, 'id': Institution.objects.get(user=request.user.id).pk})
    else:
        return Response({'institution': False}, status=400)

@api_view(['GET'])
@permission_classes([AllowAny])          
def getTrendKeyWords(request: HttpRequest, n):
    try:
        n = int(n)
    except ValueError:
        return Response({"error": "Invalid value for 'n'. It must be an integer."}, status=400)
    hash = Counter()
    institutions = Institution.objects.all()
    for institution in institutions:
        for keyword in institution.keywords.all():
            hash[keyword] += 1  
    sorted_keywords = hash.most_common(n)
    serialized_keywords = [
        {"keyword": KeyWordSerializer(keyword).data, "count": count}
        for keyword, count in sorted_keywords
    ]
    return Response({"keywords": serialized_keywords})

@api_view(['POST'])
def addKeyWordInstitution(request: HttpRequest):
    try:
        data = request.data
    except json.JSONDecodeError:
        return JsonResponse({'message': 'Invalid JSON'}, status=400)
    institutionUsername = data.get('institutionUsername')
    keywordId = data.get('keywordId')
    try:
        user = User.objects.get(username=institutionUsername)
    except:
        return JsonResponse({'message': 'Usuário inválido.'}, status=400)
    try:
        institution = Institution.objects.get(user=user.pk)
    except:
        return JsonResponse({'message': 'Instituição inválida'}, status=400)
    try:
        keyword = KeyWord.objects.get(pk=keywordId)
    except:
        return JsonResponse({'message': 'KeyWord não existe.'}, status=400)
    institution.keywords.add(keyword)
    institution.save()
    return JsonResponse({'message': 'Success'})

@api_view(['POST'])
def removeKeyWordInstitution(request: HttpRequest):
    try:
        data = request.data
    except json.JSONDecodeError:
        return JsonResponse({'message': 'Invalid JSON'}, status=400)
    institutionUsername = data.get('institutionUsername')
    keywordId = data.get('keywordId')
    try:
        user = User.objects.get(username=institutionUsername)
    except:
        return JsonResponse({'message': 'Usuário inválido.'}, status=400)
    try:
        institution = Institution.objects.get(user=user.pk)
    except:
        return JsonResponse({'message': 'Instituição inválida'}, status=400)
    try:
        keyword = KeyWord.objects.get(pk=keywordId)
    except:
        return JsonResponse({'message': 'KeyWord não existe.'}, status=400)
    institution.keywords.remove(keyword)
    institution.save()
    return JsonResponse({'message': 'Success'})