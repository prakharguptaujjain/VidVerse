"""
URL configuration for backend_django project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.2/topics/http/urls/
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
from django.urls import path
from users import views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('signup/', views.signup, name='signup'),
    path('login/', views.login, name='login'),
    path('get_csrf_token/', views.get_csrf_token, name='get_csrf_token'),
    path('content/new/', views.Contents.new, name='new_content'),
    path('content/trending/', views.Contents.trending, name='trending_content'),
    path('content/search/', views.Contents.search, name='search_content'),
    path('content/liked_videos/', views.Contents.liked_videos, name='liked_videos'),
    path('content/subscribed/', views.Contents.subscribed, name='subscribe'),
    path('user_video_interaction/', views.user_video_interaction, name='user_video_interaction'),
    path('user_channel_interaction/', views.user_channel_interaction, name='user_channel_interaction'),
    path('creator/', views.creator_dashboard, name='channel_dashboard'),
    path('advertiser/', views.advertiser_dashboard, name='advertiser_dashboard'),
    path('video_info/', views.video_info, name='video_info')
]
