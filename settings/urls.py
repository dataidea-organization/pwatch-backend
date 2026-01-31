from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import PageHeroImageViewSet

router = DefaultRouter()
router.register(r'page-hero-images', PageHeroImageViewSet, basename='page-hero-image')

urlpatterns = [
    path('', include(router.urls)),
]
