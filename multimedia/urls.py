from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import XSpaceViewSet, PodcastViewSet, GalleryViewSet, PollViewSet

router = DefaultRouter()
router.register(r'x-spaces', XSpaceViewSet, basename='xspace')
router.register(r'podcasts', PodcastViewSet, basename='podcast')
router.register(r'gallery', GalleryViewSet, basename='gallery')
router.register(r'polls', PollViewSet, basename='poll')

urlpatterns = [
    path('', include(router.urls)),
]

