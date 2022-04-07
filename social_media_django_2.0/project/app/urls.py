"""project URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.0/topics/http/urls/
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
from xml.etree.ElementInclude import include
from django.contrib import admin
from django.urls import path
from app import views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('',views.index,name='index'),
    path('register',views.user_register,name='register'),
    path('activate/<uidb64>/<token>', views.activate, name='activate'),
    path('login',views.user_login,name='login'),
    path('logout',views.user_logout,name='logout'),
    path('social',views.social,name='social'),
    path("facebook_search", views.facebook_search, name='facebook_search'),
    path("twitter_search", views.twitter_search, name='twitter_search'),
    path("youtube_search",views.youtube_search, name='youtube_search'),
    path("google_search", views.google_search, name='google_search'),
    # path("upload_file", views.upload_file, name='upload_file' ),
    path("facbook_download", views.facbook_download, name='facbook_download'), 
    path("twitter_download", views.twitter_download, name='twitter_download'),  
    path("youtube_download", views.youtube_download, name='youtube_download'),  
    path("google_download", views.google_download, name='google_download'), 
    path("fb_dashbaord/<str:path>", views.fb_dashboard, name='fb_dashboard'), 
    path("tw_dashbaord/<str:path>", views.tw_dashboard, name='tw_dashboard'), 
    path("gl_dashbaord/<str:path>", views.gl_dashboard, name='gl_dashboard'), 
    path("yt_dashbaord/<str:path>", views.yt_dashboard, name='yt_dashboard'), 
    path("profile/<int:user_id>", views.user_profile, name='profile'), 
    path("download", views.download, name='download'), 
    path("analytics", views.analytics, name='analytics'), 
    
]
