from django.shortcuts import render
from django.http import HttpResponse
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth import login, logout, authenticate
from django.shortcuts import render, redirect
from django.contrib.auth.forms import UserCreationForm
from django.db.models import Q
from yemek_tarifleri.yemek_tarifleri.models import Recipe, Comment, Rating
from django.shortcuts import render
from .models import Recipe, Comment
from django.db.models import Avg, Count
from .forms import RecipeForm, IngredientFormSet
from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404, render, redirect
from .forms import CommentForm, RatingForm
from django.contrib import messages



def welcome(request):
    return HttpResponse("Welcome to recipes homepage!")

def home(request):
    recipes = Recipe.objects.all()
    return render(request, 'home.html', {'recipes': recipes})

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
    recipes = Recipe.objects.annotate(
        average_rating=Avg('ratings__score'),
        num_ratings=Count('ratings')
    ).order_by('-average_rating')[:5]

    for recipe in recipes:
        if recipe.average_rating:
            recipe.average_rating = f"{recipe.average_rating:.2f}"
        else:
            recipe.average_rating = "Henüz puan verilmemiş"

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


def profile(request):
    return render(request, 'profile.html', {'user': request.user})


def add_recipe(request):
    if request.method == 'POST':
        form = RecipeForm(request.POST, request.FILES)
        formset = IngredientFormSet(request.POST, request.FILES)
        if form.is_valid() and formset.is_valid():
            recipe = form.save(commit=False)
            recipe.created_by = request.user
            recipe.save()
            formset.instance = recipe
            formset.save()
            form = RecipeForm()
            formset = IngredientFormSet()
            messages.success(request, 'Tarif başarıyla eklendi.')
            
    else:
        form = RecipeForm()
        formset = IngredientFormSet()
    return render(request, 'add_recipe.html', {'form': form, 'formset': formset})

def en_tarifler(request):
    #add top rated recipes and number of how many ratings
    top_rated_recipes = Recipe.objects.annotate(
        average_rating=Avg('ratings__score'),
        num_ratings=Count('ratings')
    ).order_by('-average_rating')[:5]
    #top_rated_recipes = Recipe.objects.annotate(average_rating=Avg('ratings__score')).order_by('-average_rating')[:5]
    latest_recipes = Recipe.objects.all().order_by('-created_at')[:5]
    most_commented_recipes = Recipe.objects.annotate(comment_count=Count('comments')).order_by('-comment_count')[:5]

    context = {
        'top_rated_recipes': top_rated_recipes,
        'latest_recipes': latest_recipes,
        'most_commented_recipes': most_commented_recipes,
    }

    return render(request, 'en_tarifler.html', context)


def recipe_detail(request, pk):
    recipe = get_object_or_404(Recipe, pk=pk)
    comments = Comment.objects.filter(recipe=recipe)
    ratings = Rating.objects.filter(recipe=recipe)
    average_rating = ratings.aggregate(Avg('score'))['score__avg']

    if average_rating is None:
        average_rating_display = 'Henüz puan verilmemiş'
    else:
        # average_rating varsa, iki ondalık basamağa yuvarla
        average_rating_display = f"{average_rating:.2f}"

    if request.method == 'POST':
        if 'submit_comment' in request.POST:  # Yorum formunun gönderilme işlemi
            comment_form = CommentForm(request.POST)
            if comment_form.is_valid():
                comment = comment_form.save(commit=False)
                comment.recipe = recipe
                comment.author = request.user
                comment.save()
                return redirect('recipe_detail', pk=pk)
        elif 'submit_rating' in request.POST:  # Puanlama formunun gönderilme işlemi
            rating_form = RatingForm(request.POST)
            if rating_form.is_valid():
                rating = rating_form.save(commit=False)
                rating.recipe = recipe
                rating.user = request.user
                rating.save()
                return redirect('recipe_detail', pk=pk)
    else:
        comment_form = CommentForm()
        rating_form = RatingForm()

    return render(request, 'recipe_detail.html', {
        'recipe': recipe,
        'comments': comments,
        'average_rating': average_rating_display,
        'comment_form': comment_form,
        'rating_form': rating_form
    })
