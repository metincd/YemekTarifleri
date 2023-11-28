from django.contrib import admin
from .models import Profile, Recipe, Ingredient, Comment, Rating

class IngredientInline(admin.TabularInline):
    model = Ingredient
    extra = 1

class RecipeAdmin(admin.ModelAdmin):
    inlines = [IngredientInline]
    list_display = ('title', 'created_by', 'created_at', 'is_chef_recommended')
    search_fields = ['title', 'instructions']
    
admin.site.register(Profile)
admin.site.register(Recipe, RecipeAdmin)
admin.site.register(Comment)
admin.site.register(Rating)
