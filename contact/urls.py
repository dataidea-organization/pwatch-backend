from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import ContactSubmissionViewSet, DonationSubmissionViewSet

router = DefaultRouter()
router.register(r'submissions', ContactSubmissionViewSet, basename='contact-submission')
router.register(r'donations', DonationSubmissionViewSet, basename='donation-submission')

urlpatterns = [
    path('', include(router.urls)),
]