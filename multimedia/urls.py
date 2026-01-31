from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import XSpaceViewSet, PodcastViewSet, GalleryViewSet, PollViewSet, XPollEmbedViewSet

router = DefaultRouter()
router.register(r'x-spaces', XSpaceViewSet, basename='xspace')
router.register(r'podcasts', PodcastViewSet, basename='podcast')
router.register(r'gallery', GalleryViewSet, basename='gallery')
router.register(r'polls', PollViewSet, basename='poll')
router.register(r'x-poll-embeds', XPollEmbedViewSet, basename='xpollembed')

urlpatterns = [
    path('', include(router.urls)),
]

