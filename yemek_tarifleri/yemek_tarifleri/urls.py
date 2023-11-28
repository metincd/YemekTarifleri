
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
    path('top-rated/', views.top_rated_recipes, name='top_rated_recipes'),
    path('latest/', views.latest_recipes, name='latest_recipes'),
    path('most-commented/', views.most_commented_recipes, name='most_commented_recipes'),
    path('chef-recommended/', views.chef_recommended, name='chef_recommended'),
]
