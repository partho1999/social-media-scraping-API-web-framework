from unicodedata import name
from django.contrib import admin
from django.urls import path
from app import views
urlpatterns = [
    path("", views.index, name='home'),
    path("register", views.register, name='register'),
    path("login", views.Login, name='login'),
    path("search", views.search, name='search')  
]   