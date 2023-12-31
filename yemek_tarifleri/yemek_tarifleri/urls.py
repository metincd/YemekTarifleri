
from django.contrib import admin
from django.urls import path
from django.db.models import Q
from django.shortcuts import render
from yemek_tarifleri.yemek_tarifleri.models import Recipe
from . import views
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('admin/', admin.site.urls),
    path('signup/', views.signup, name='signup'),
    path('login/', views.user_login, name='login'),
    path('logout/', views.user_logout, name='logout'),
    path('top-rated/', views.top_rated_recipes, name='top_rated_recipes'),
    path('latest/', views.latest_recipes, name='latest_recipes'),
    path('most-commented/', views.most_commented_recipes, name='most_commented_recipes'),
    path('chef-recommended/', views.chef_recommended, name='chef_recommended'),
    path('', views.home, name='home'),
    path('add-recipe/', views.add_recipe, name='add_recipe'),
    path('profile/', views.profile, name='profile'),
    path('recipe/<int:pk>/', views.recipe_detail, name='recipe_detail'),
    path('en-tarifler/', views.en_tarifler, name='en_tarifler'),
    path('category/<category>/', views.category_recipes, name='category_recipes'),
    path('profile/<str:username>/', views.user_profile, name='user_profile'),
    path('calorie-calculator/', views.calorie_calculator, name='calorie_calculator'),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)