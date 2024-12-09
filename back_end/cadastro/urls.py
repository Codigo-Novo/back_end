from django.conf.urls import include
from django.urls import re_path, path
from rest_framework.routers import DefaultRouter
from .views import *

router = DefaultRouter()
router.register(r'usuario', UserViewSet, basename='usuario')
router.register(r'instituicao', InstitutionViewSet, basename='instituicao')
router.register(r'categoria', CategoryViewSet, basename='categoria')
router.register(r'doacao', DonationViewSet, basename='doacao')
router.register(r'doadopor', DonatedByViewSet, basename='doadopor')

urlpatterns = [
    re_path('^', include(router.urls)),
    path('loginView/', loginView),
    path('logoutView/', logoutView),
    path('setUserDonator/', setUserDonator),
    path('setUserInstitution/', setUserInstitution),
    path('createInstitution/', createInstitution),
    path('deleteUser/', deleteUser),
    path('checkAuth/', checkAuth),
]