from django.db import models
from django.contrib.auth.models import User


class Profile(models.Model):
    
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    bio = models.TextField(max_length=500, blank=True)
    
    def __str__(self):
        return self.user.username
    
    
class Category(models.Model):
    name = models.CharField(max_length=100)
    

class Recipe(models.Model):
    CATEGORY_CHOICES = [
        ('TR', 'Traditional'),
        ('IN', 'International'),
        ('SP', 'Special'),
    ]
    title = models.CharField(max_length=200)
    ingredients = models.TextField()
    instructions = models.TextField()
    created_by = models.ForeignKey(User, on_delete=models.CASCADE)
    image = models.ImageField(upload_to='recipes/')
    created_at = models.DateTimeField(auto_now_add=True)
    category = models.CharField(
        max_length=2,
        choices=CATEGORY_CHOICES,
        default='TR'
    )

    def __str__(self):
        return self.title
    
    
class Comment(models.Model):
    recipe = models.ForeignKey(Recipe, related_name='comments', on_delete=models.CASCADE)
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    
    
class Rating(models.Model):
    recipe = models.ForeignKey(Recipe, related_name='ratings', on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    score = models.IntegerField()
    
    
class Favorite(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    recipe = models.ForeignKey(Recipe, on_delete=models.CASCADE)
