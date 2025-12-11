from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import HeroImageViewSet

router = DefaultRouter()
router.register(r'hero-images', HeroImageViewSet, basename='hero-image')

urlpatterns = [
    path('', include(router.urls)),
]

