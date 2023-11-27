
from django.contrib import admin
from django.urls import path
from django.db.models import Q
from django.shortcuts import render
from yemek_tarifleri.models import Recipe

urlpatterns = [
    path('admin/', admin.site.urls),
]

def search_recipes(request):
    query = request.GET.get('q')
    if query:
        recipes = Recipe.objects.filter(Q(title__icontains=query) | Q(ingredients__icontains=query))
    else:
        recipes = Recipe.objects.all()
    return render(request, 'search_results.html', {'recipes': recipes})
