from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import (
    NewsViewSet,
    HomeNewsSummaryView,
    NewsCommentListCreateView,
)

router = DefaultRouter()
router.register(r'', NewsViewSet, basename='news')

urlpatterns = [
    path('home-summary/', HomeNewsSummaryView.as_view(), name='home-news-summary'),
    path('<slug:slug>/comments/', NewsCommentListCreateView.as_view(), name='news-comments'),
    path('', include(router.urls)),
]
