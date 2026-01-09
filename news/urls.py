from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import NewsViewSet, HomeNewsSummaryView, HotInParliamentView, HotInParliamentDetailView

router = DefaultRouter()
router.register(r'', NewsViewSet, basename='news')

urlpatterns = [
    path('home-summary/', HomeNewsSummaryView.as_view(), name='home-news-summary'),
    path('hot-in-parliament/', HotInParliamentView.as_view(), name='hot-in-parliament'),
    path('hot-in-parliament/<slug:slug>/', HotInParliamentDetailView.as_view(), name='hot-in-parliament-detail'),
    path('', include(router.urls)),
]