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
    form=IngredientForm,
    can_delete=True
)

class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ['content']
        
class RatingForm(forms.ModelForm):
    score = forms.ChoiceField(choices=[(i, i) for i in range(1, 11)], widget=forms.Select(), label="Puan")

    class Meta:
        model = Rating
        fields = ['score']