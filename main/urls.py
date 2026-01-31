"""
URL configuration for main project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/6.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('admin/media-download/', views.media_download_page, name='media_download_page'),
    path('admin/media-download/<str:folder_name>/', views.download_media_folder, name='download_media_folder'),
    path('admin/', admin.site.urls),
    path('ckeditor/', include('ckeditor_uploader.urls')),
    path('api/search/', views.GlobalSearchView.as_view(), name='global-search'),
    path('api/trackers/', include('trackers.urls')),
    path('api/news/', include('news.urls')),
    path('api/blog/', include('blog.urls')),
    path('api/multimedia/', include('multimedia.urls')),
    path('api/resources/', include('resources.urls')),
    path('api/contact/', include('contact.urls')),
    path('api/about/', include('about.urls')),
    path('api/home/', include('home.urls')),
    path('api/chatbot/', include('chatbot.urls')),
    path('api/settings/', include('settings.urls')),
]

# Serve media files in development
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
