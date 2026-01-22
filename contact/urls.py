from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import ContactSubmissionViewSet, DonationSubmissionViewSet, FeedbackViewSet

router = DefaultRouter()
router.register(r'submissions', ContactSubmissionViewSet, basename='contact-submission')
router.register(r'donations', DonationSubmissionViewSet, basename='donation-submission')
router.register(r'feedback', FeedbackViewSet, basename='feedback')

urlpatterns = [
    path('', include(router.urls)),
]