from django.conf.urls import include
from django.urls import re_path
from rest_framework.routers import DefaultRouter
from .views import UserViewSet, InstitutionViewSet, CategoryViewSet, DonationViewSet, DonatedByViewSet

router = DefaultRouter()
router.register(r'usuario', UserViewSet)
router.register(r'instituicao', InstitutionViewSet)
router.register(r'categoria', CategoryViewSet)
router.register(r'doacao', DonationViewSet)
router.register(r'doadopor', DonatedByViewSet)

urlpatterns = [
    re_path('^', include(router.urls)),
]