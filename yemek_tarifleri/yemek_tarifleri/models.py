from django.db import models
from django.contrib.auth.models import User
from decimal import Decimal


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
    steps = models.TextField(verbose_name='Tarif Adımları', default='')

    category = models.CharField(
        max_length=200,
        choices=CATEGORY_CHOICES,
        default='TR'
    )
    
    def calculate_total_calories(self):
        total_calories = sum(ingredient.calculate_calories() for ingredient in self.ingredients.all())
        return total_calories

    def __str__(self):
        return self.title
    
    
class Ingredient(models.Model):
    FOOD_LIST = {
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

    '''UNIT_CHOICES = [
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
    ]'''
    UNIT_CHOICES = [
        ('GRM', 'gram'),
       
    ]
    
    FOOD_CHOICES = [(name, name) for name in FOOD_LIST.keys()]

    recipe = models.ForeignKey(Recipe, related_name='ingredients', on_delete=models.CASCADE)
    name = models.CharField(max_length=100, choices=FOOD_CHOICES)
    quantity = models.DecimalField(max_digits=5, decimal_places=2)
    unit = models.CharField(max_length=4, choices=UNIT_CHOICES)
    
    def calculate_calories(self):
        calorie_per_unit = self.FOOD_LIST.get(self.name, 0)
        calorie_per_unit = Decimal(calorie_per_unit)
        return self.quantity * calorie_per_unit

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

    class Meta:
        unique_together = ('recipe', 'user')
    
    
class Favorite(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    recipe = models.ForeignKey(Recipe, on_delete=models.CASCADE)
