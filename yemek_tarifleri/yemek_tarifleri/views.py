from django.shortcuts import render
from django.http import HttpResponse
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth import login, logout, authenticate
from django.shortcuts import render, redirect
from django.contrib.auth.forms import UserCreationForm
from django.db.models import Q
from yemek_tarifleri.models import Recipe
from django.shortcuts import render
from .models import Recipe, Comment
from django.db.models import Avg, Count


def welcome(request):
    return HttpResponse("Welcome to recipes homepage!")


def signup(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get('username')
            raw_password = form.cleaned_data.get('password1')
            user = authenticate(username=username, password=raw_password)
            login(request, user)
            return redirect('home') #ana sayfaya yönlendir
    else:
        form = UserCreationForm()
    return render(request, 'signup.html', {'form': form})


def user_login(request):
    if request.method == 'POST':
        form = AuthenticationForm(data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            return redirect('home') #ana sayfaya yönlendir
    else:
        form = AuthenticationForm()
    return render(request, 'login.html', {'form': form})


def user_logout(request):
    logout(request)
    return redirect('home') #logout olduktan sonra yönlendirilecek sayfa


def search_recipes(request):
    query = request.GET.get('q')
    if query:
        recipes = Recipe.objects.filter(Q(title__icontains=query) | Q(ingredients__icontains=query))
    else:
        recipes = Recipe.objects.all()
    return render(request, 'search_results.html', {'recipes': recipes})


#Top Recipes

def top_rated_recipes(request):
    recipes = Recipe.objects.annotate(average_rating=Avg('ratings__score')).order_by('-average_rating')[:5]
    return render(request, 'top_rated_recipes.html', {'recipes': recipes})


def latest_recipes(request):
    recipes = Recipe.objects.all().order_by('-created_at')[:5]
    return render(request, 'latest_recipes.html', {'recipes': recipes})


def most_commented_recipes(request):
    recipes = Recipe.objects.annotate(comment_count=Count('comments')).order_by('-comment_count')[:5]
    return render(request, 'most_commented_recipes.html', {'recipes': recipes})


def chef_recommended(request):
    recipes = Recipe.objects.filter(is_chef_recommended=True)[:5]
    return render(request, 'chef_recommended.html', {'recipes': recipes})
