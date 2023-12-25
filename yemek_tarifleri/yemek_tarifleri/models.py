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
        ('MAIN', 'Ana Yemekler'),
        ('APP', 'Aperatifler'),
        ('DES', 'Tatlılar'),
        ('VEGAN', 'Vegan'),
        ('VEG', 'Vejetaryen'),
        ('SEA', 'Deniz Ürünleri'),
        ('SOUP', 'Çorbalar'),
        ('SALAD', 'Salatalar'),
        ('QUICK', 'Hızlı ve Kolay'),
        ('HEALTHY', 'Sağlıklı Tarifler'),
        ('SP', 'Special'),
    ]
    title = models.CharField(max_length=200)
    instructions = models.TextField()
    created_by = models.ForeignKey(User, on_delete=models.CASCADE)
    image = models.ImageField(upload_to='recipes/')
    created_at = models.DateTimeField(auto_now_add=True)
    is_chef_recommended = models.BooleanField(default=False)

    category = models.CharField(
        max_length=200,
        choices=CATEGORY_CHOICES,
        default='TR'
    )

    def __str__(self):
        return self.title
    
    
class Ingredient(models.Model):
    UNIT_CHOICES = [
        ('YKSK', 'Yemek Kaşığı'),
        ('CKSK', 'Çay Kaşığı'),
        ('BRD', 'Bardak'),
        ('KG', 'Kilogram'),
        ('GR', 'Gram'),
        ('TM', 'Tutam'),
        ('AVC', 'Avuç'),
        ('GZK', 'Göz Kararı'),
        ('ADT', 'Adet'),
        ('YDM', 'Yudum'),
        ('KP', 'Kepçe'),
    ]

    recipe = models.ForeignKey(Recipe, related_name='ingredients', on_delete=models.CASCADE)
    name = models.CharField(max_length=100)
    quantity = models.DecimalField(max_digits=5, decimal_places=2)
    unit = models.CharField(max_length=4, choices=UNIT_CHOICES)

    def __str__(self):
        return f"{self.quantity} {self.get_unit_display()} {self.name}"
    
    
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
