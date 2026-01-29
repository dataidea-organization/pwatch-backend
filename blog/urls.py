from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import BlogViewSet, HomeBlogSummaryView, BlogCommentListCreateView

router = DefaultRouter()
router.register(r'', BlogViewSet, basename='blog')

urlpatterns = [
    path('home-summary/', HomeBlogSummaryView.as_view(), name='home-blog-summary'),
    path('<slug:slug>/comments/', BlogCommentListCreateView.as_view(), name='blog-comments'),
    path('', include(router.urls)),
]

