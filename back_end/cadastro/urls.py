from django.conf.urls import include
from django.urls import re_path, path
from rest_framework.routers import DefaultRouter
from .views import UserViewSet, InstitutionViewSet, CategoryViewSet, DonationViewSet, DonatedByViewSet, login_view

router = DefaultRouter()
router.register(r'usuario', UserViewSet, basename='usuario')
router.register(r'instituicao', InstitutionViewSet, basename='instituicao')
router.register(r'categoria', CategoryViewSet, basename='categoria')
router.register(r'doacao', DonationViewSet, basename='doacao')
router.register(r'doadopor', DonatedByViewSet, basename='doadopor')

urlpatterns = [
    re_path('^', include(router.urls)),
    path('login_view/', login_view),
]