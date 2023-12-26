from django.shortcuts import render
from django.http import HttpResponse
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth import login, logout, authenticate
from django.shortcuts import render, redirect
from django.contrib.auth.forms import UserCreationForm
from django.db.models import Q
from yemek_tarifleri.yemek_tarifleri.models import Recipe, Comment, Rating, User, Ingredient
from django.shortcuts import render
from django.db.models import Avg, Count
from .forms import RecipeForm, IngredientFormSet
from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404, render, redirect
from .forms import CommentForm, RatingForm
from django.contrib import messages
from decimal import Decimal


def welcome(request):
    return HttpResponse("Welcome to recipes homepage!")

def home(request):
    recipes = Recipe.objects.all().order_by('-created_at')
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
            return redirect('home')
    else:
        form = UserCreationForm()
    return render(request, 'signup.html', {'form': form})


def user_login(request):
    if request.method == 'POST':
        form = AuthenticationForm(data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            return redirect('home')
    else:
        form = AuthenticationForm()
    return render(request, 'login.html', {'form': form})


def user_logout(request):
    logout(request)
    return redirect('home')


def search_recipes(request):
    query = request.GET.get('q')
    if query:
        recipes = Recipe.objects.filter(Q(title__icontains=query) | Q(ingredients__icontains=query))
    else:
        recipes = Recipe.objects.all()
    return render(request, 'search_results.html', {'recipes': recipes})


def category_recipes(request, category):
    recipes = Recipe.objects.filter(category=category)
    if not recipes.exists():
        return render(request, 'category_recipes.html', {'message': f"Bu kategoride ({category}) henüz tarif eklenmemiş."})
    return render(request, 'category_recipes.html', {'recipes': recipes})


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
    top_rated_recipes = Recipe.objects.annotate(
        average_rating=Avg('ratings__score'),
        num_ratings=Count('ratings')
    ).order_by('-average_rating')[:5]
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
    average_rating_display = 'Henüz puan verilmemiş' if average_rating is None else f"{average_rating:.2f}"

    if request.method == 'POST':
        if 'submit_comment' in request.POST:
            comment_form = CommentForm(request.POST)
            if comment_form.is_valid():
                comment = comment_form.save(commit=False)
                comment.recipe = recipe
                comment.author = request.user
                comment.save()
                return redirect('recipe_detail', pk=pk)
        elif 'submit_rating' in request.POST:
            rating_form = RatingForm(request.POST)
            if rating_form.is_valid():
                rating, created = Rating.objects.get_or_create(
                    recipe=recipe, 
                    user=request.user, 
                    defaults={'score': rating_form.cleaned_data['score']}
                )
                if created:
                    messages.success(request, 'Puanınız kaydedildi.')
                else:
                    messages.info(request, 'Zaten bu tarife puan verdiniz.')
                return redirect('recipe_detail', pk=pk)
    else:
        comment_form = CommentForm()
        rating_form = RatingForm()

    return render(request, 'recipe_detail.html', {
        'recipe': recipe,
        'steps': recipe.steps.split('\n') if recipe.steps else [],
        'comments': comments,
        'average_rating': average_rating_display,
        'comment_form': comment_form,
        'rating_form': rating_form
    })

def user_profile(request, username):
    user = get_object_or_404(User, username=username)
    recipes = Recipe.objects.filter(created_by=user)
    return render(request, 'user_profile.html', {'profile_user': user, 'recipes': recipes})

def calorie_calculator(request):
    food_list = {
        "Tavuk göğsü": 0.23,
        "Zeytinyağı": 8.8,
        "Sarımsak": 1.49,
        "Soğan": 0.4,
        "Tuz": 0,
        "Karabiber": 2.55,
        "Domates": 0.18,
        "Dolmalık biber": 0.2,
        "Havuç": 0.41,
        "Mantar": 0.22,
        "Patates": 0.77,
        "Limon": 0.29,
        "Misket limonu": 0.3,
        "Kimyon": 3.75,
        "Kırmızı biber": 2.8,
        "Tarçın": 2.6,
        "Muskat": 5.2,
        "Zencefil": 3.4,
        "Fesleğen": 0.23,
        "Kekik": 2.8,
        "Zaman otu": 2.8,
        "Biberiye": 2.7,
        "Maydanoz": 0.36,
        "Kişniş": 2.3,
        "Dereotu": 2.7,
        "Taze soğan": 0.32,
        "Soya sosu": 0.53,
        "Sirke": 0.18,
        "Bal": 3,
        "Şeker": 4,
        "Esmer şeker": 3.8,
        "Un": 3.64,
        "Pirinç": 3.61,
        "Makarna": 3.7,
        "Ekmek": 2.65,
        "Süt": 0.42,
        "Krema": 2.9,
        "Tereyağı": 7.2,
        "Peynir": 4.02,
        "Yumurta": 1.43,
        "Yoğurt": 0.59,
        "Hindistan cevizi sütü": 2.3,
        "Dana eti": 2.5,
        "Domuz eti": 2.45,
        "Pastırma": 2.5,
        "Jambon": 1.45,
        "Hindi": 1.06,
        "Balık": 2.08,
        "Karides": 1.02,
        "Yengeç": 0.87,
        "Istakoz": 0.89,
        "Tofu": 0.76,
        "Fasulye": 3.4,
        "Mercimek": 3.3,
        "Nohut": 3.6,
        "Bezelye": 3.1,
        "Mısır": 3.65,
        "Ispanak": 0.23,
        "Kara lahana": 0.49,
        "Marul": 0.14,
        "Salatalık": 0.12,
        "Kabak": 0.16,
        "Patlıcan": 0.25,
        "Balkabağı": 0.26,
        "Brokoli": 0.34,
        "Karnabahar": 0.25,
        "Kuşkonmaz": 0.2,
        "Taze fasulye": 0.31,
        "Kereviz": 0.16,
        "Avokado": 1.6,
        "Elma": 0.52,
        "Muz": 0.89,
        "Portakal": 0.47,
        "Çilek": 0.32,
        "Yaban mersini": 0.57,
        "Ahududu": 0.52,
        "Üzüm": 0.69,
        "Karpuz": 0.3,
        "Ananas": 0.5,
        "Mango": 0.6,
        "Şeftali": 0.39,
        "Erik": 0.46,
        "Kiraz": 0.5,
        "Armut": 0.57,
        "Fındık": 6.4,
        "Badem": 5.8,
        "Ceviz": 6.5,
        "Yer fıstığı": 5.6,
        "Kaju": 5.5,
        "Pekan cevizi": 6.8,
        "Susam": 5.7,
        "Ayçiçeği çekirdeği": 5.8,
        "Balkabağı çekirdeği": 5.6,
        "Keten tohumu": 5.3,
        "Chia tohumu": 4.9,
        "Kinoa": 3.7,
        "Yulaf": 3.9,
        "Arpa": 3.5,
        "Çavdar": 3.4,
        "Mısır unu": 3.6,
        "Kabartma tozu": 0,
        "Karbonat": 0,
        "Maya": 3.1,
        "Vanilya özütü": 3,
        "Badem özütü": 3.2,
        "Limon suyu": 0.25,
        "Portakal suyu": 0.47,
        "Akçaağaç şurubu": 2.6,
        "Melas": 2.9,
        "Soya sütü": 0.54,
        "Badem sütü": 0.13,
        "Pirinç sütü": 0.47,
        "Hindistan cevizi yağı": 8.8,
        "Bitkisel yağ": 8.8,
        "Kanola yağı": 8.8,
        "Ayçiçeği yağı": 8.8,
        "Susam yağı": 8.8,
        "Hardal": 1.6,
        "Ketçap": 1.0,
        "Mayonez": 7.2,
        "Acı sos": 0.6,
        "Worcestershire sosu": 0.2,
        "Balık sosu": 0.2,
        "Teriyaki sosu": 1.3,
        "BBQ sos": 1.0,
        "Salsa": 0.4,
        "Guacamole": 1.6,
        "Humus": 1.7,
        "Tahin": 5.9,
        "Pesto": 2.9,
        "Marinara sosu": 0.5,
        "Alfredo sosu": 1.4,
        "Kari tozu": 3.3,
        "Zerdeçal": 3.1,
        "Safran": 3.1,
        "Kakule": 3.1,
        "Rezene tohumu": 3.4,
        "Hardal tohumu": 5.2,
        "Haşhaş tohumu": 5.3,
        "Yıldız anason": 3.3,
        "Karanfil": 2.7,
        "Defne yaprağı": 3.1,
        "Chili tozu": 2.8,
        "Kırmızı biber pulu": 3.1,
        "Acı kırmızı biber": 3.2,
        "Jalapeno biberi": 0.4,
        "Habanero biberi": 0.4,
        "Serrano biberi": 0.4,
        "Chipotle": 2.8,
        "Ancho chili": 2.9,
        "Pasilla chili": 3.0,
        "Guajillo chili": 3.0,
        "Arbol chili": 3.0,
        "Yeşil soğan": 0.32,
        "Pırasa": 0.61,
        "Arpacık soğanı": 0.4,
        "Kırmızı soğan": 0.4,
        "Beyaz soğan": 0.4,
        "Sarı soğan": 0.4,
        "Sarımsak tozu": 3.3,
        "Soğan tozu": 3.1,
        "Chili sosu": 0.9,
        "Sriracha": 1.0,
        "Tabasco": 0.1,
        "Buffalo sosu": 1.0,
        "Ranch sosu": 2.3,
        "Mavi peynir sosu": 2.5,
        "İtalyan sosu": 2.0
    }
    return render(request, 'calorie_calculator.html', {'food_list': food_list})