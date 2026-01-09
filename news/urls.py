from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import NewsViewSet, HomeNewsSummaryView, HotInParliamentView

router = DefaultRouter()
router.register(r'', NewsViewSet, basename='news')

urlpatterns = [
    path('home-summary/', HomeNewsSummaryView.as_view(), name='home-news-summary'),
    path('hot-in-parliament/', HotInParliamentView.as_view(), name='hot-in-parliament'),
    path('', include(router.urls)),
]