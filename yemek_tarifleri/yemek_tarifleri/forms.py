from django import forms
from django.forms import inlineformset_factory
from .models import Recipe, Ingredient, Comment, Rating

class RecipeForm(forms.ModelForm):
    class Meta:
        model = Recipe
        fields = ['title', 'instructions', 'image', 'category']

class IngredientForm(forms.ModelForm):
    class Meta:
        model = Ingredient
        fields = ['name', 'quantity', 'unit']

IngredientFormSet = inlineformset_factory(
    Recipe,
    Ingredient,
    fields=('name', 'quantity', 'unit'),
    extra=3,
    can_delete=True
)

class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ['content']
        
class RatingForm(forms.ModelForm):
    class Meta:
        model = Rating
        fields = ['score']
