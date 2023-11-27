
from django.contrib import admin
from django.urls import path
from django.db.models import Q
from django.shortcuts import render
from yemek_tarifleri.models import Recipe
from . import views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('signup/', views.signup, name='signup'),
    path('login/', views.user_login, name='login'),
    path('logout/', views.user_logout, name='logout'),
]
