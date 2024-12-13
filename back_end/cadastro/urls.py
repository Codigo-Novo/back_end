from django.conf.urls import include
from django.urls import re_path, path
from rest_framework.routers import DefaultRouter
from .views import *

router = DefaultRouter()
router.register(r'usuario', UserViewSet, basename='usuario')
router.register(r'instituicao', InstitutionViewSet, basename='instituicao')
router.register(r'palavraschave', KeyWordViewSet, basename='palavraschave')

urlpatterns = [
    re_path('^', include(router.urls)),
    path('loginView/', loginView),
    path('logoutView/', logoutView),
    path('setUserDonator/', setUserDonator),
    path('setUserInstitution/', setUserInstitution),
    path('createInstitution/', createInstitution),
    path('deleteUser/', deleteUser),
    path('checkAuth/', checkAuth),
    path('checkInstitution/', checkInstitution),
    path('getTrendKeyWords/<int:n>/', getTrendKeyWords),
    path('addKeyWordInstitution/', addKeyWordInstitution),
    path('removeKeyWordInstitution/', removeKeyWordInstitution),
]