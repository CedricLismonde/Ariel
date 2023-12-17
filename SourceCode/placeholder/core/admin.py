from django.contrib import admin
from .models import Profile, Recipe, LikeRecipe, FollowersCount

# Register your models here.
admin.site.register(Profile)
admin.site.register(Recipe)
admin.site.register(LikeRecipe)
admin.site.register(FollowersCount)