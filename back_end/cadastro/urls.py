from django.conf.urls import include
from django.urls import re_path
from rest_framework.routers import DefaultRouter
from .views import UserViewSet

router = DefaultRouter()
router.register(r'usuario', UserViewSet)

urlpatterns = [
    re_path('^', include(router.urls)),
]