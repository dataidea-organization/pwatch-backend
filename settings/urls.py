from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import PageHeroImageViewSet, CitizensVoiceFeedbackLinksView

router = DefaultRouter()
router.register(r'page-hero-images', PageHeroImageViewSet, basename='page-hero-image')

urlpatterns = [
    path('citizens-voice-feedback/', CitizensVoiceFeedbackLinksView.as_view()),
    path('', include(router.urls)),
]
