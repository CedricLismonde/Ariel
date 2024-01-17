from django.db import models
from django.contrib.auth import get_user_model
import uuid
from datetime import datetime

User = get_user_model()

# Create your models here.
class Profile(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    id_user= models.IntegerField()
    
    username=models.CharField(max_length=25)
    email = models.EmailField()
    firstname=models.CharField(max_length=25)
    lastname=models.CharField(max_length=25)
    
    #profileimg
    profile_picture = models.ImageField(upload_to='profile_images',default='blank-profile-picture.png')
   
    #location = models.CharField(max_length=100,blank=True)
    #bio = models.TextField(blank=True)
    
    isbanned = models.BooleanField(default=False)
    islimited = models.BooleanField(default=False)
    def __str__(self):
        return self.user.username
    
class Recipe(models.Model):#Post
    recipe_id = models.UUIDField(primary_key=True,default=uuid.uuid4)
    user = models.CharField(max_length=100)
        #ingredient_id =models.CharField(max_length=200)
    recipe_title =models.CharField(max_length=50)
        #category = models.CharField(max_length=200)
        #cuisine_type =
        #cooking_time =
    preparation_step = models.CharField(max_length=400,default="None")
        
    tags = models.CharField(max_length=2000,blank=True)
        
    image = models.ImageField(upload_to='post_images')
        #video =
    nb_likes = models.IntegerField(default=0)
    created_at =models.DateTimeField(default=datetime.now)
    
    def __str__(self):
        return self.user
    
    def getTags(self):
        
        T=self.tags.split(' ')
        for i in range(len(T)):
            T[i]=('#'+T[i][0].upper()+T[i][1:].lower())
        return T

class Comment(models.Model):
    comment_id = models.UUIDField(primary_key=True,default=uuid.uuid4)
    recipe_id = models.CharField(max_length=100)
    user = models.CharField(max_length=100)
    txt = models.CharField(max_length=400,default="None")
    
    
    def __str__(self):
        return self.user
  

class LikeRecipe(models.Model):#LikePost
    post_id = models.CharField(max_length=500)
    username =models.CharField(max_length=100)
    
    def __str__(self):
        return self.username

class FollowersCount(models.Model):
    follower = models.CharField(max_length=(100))
    user = models.CharField(max_length=(100))
    
    def __str__(self):
        return self.user
    