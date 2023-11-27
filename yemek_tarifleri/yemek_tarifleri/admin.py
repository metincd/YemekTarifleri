from django.contrib import admin
from .models import Profile, Recipe, Comment, Rating

admin.site.register(Profile)
admin.site.register(Recipe)
admin.site.register(Comment)
admin.site.register(Rating)