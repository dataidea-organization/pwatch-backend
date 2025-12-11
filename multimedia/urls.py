from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import XSpaceViewSet

router = DefaultRouter()
router.register(r'x-spaces', XSpaceViewSet, basename='xspace')

urlpatterns = [
    path('', include(router.urls)),
]

