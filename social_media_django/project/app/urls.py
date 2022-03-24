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
    path('login',views.user_login,name='login'),
    path('logout',views.user_logout,name='logout'),
    path('social',views.social,name='social'),
    path("facebook_search", views.facebook_search, name='facebook_search'),
    path("twitter_search", views.twitter_search, name='twitter_search'),
    path("youtube_search",views.youtube_search, name='youtube_search'),
    path("google_search", views.google_search, name='google_search'),
    path("upload_file", views.upload_file, name='upload_file' ),
    path("facbook_dowload", views.facbook_dowload, name='facbook_dowload'), 
    path("twitter_dowload", views.twitter_dowload, name='twitter_dowload'),  
    path("youtube_dowload", views.youtube_dowload, name='youtube_dowload'),  
    path("google_dowload", views.google_dowload, name='google_dowload'),   
    
]
