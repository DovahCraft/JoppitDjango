from django.db import models
from django.contrib.auth.models import User

# Create your models here.
class Post(models.Model):
    #Title of the post
    title = models.CharField(max_length=69)
    #Url of the post
    url = models.URLField()
    #Who posted this
    poster = models.ForeignKey(User, on_delete=models.CASCADE)
    #When the post was created
    created = models.DateTimeField(auto_now_add=True)

    #Describes settings of the model
    class Meta: 
        #Orders the newest post first
        ordering = ["-created"]

#Inherits from models.Model
class Vote(models.Model):
    voter = models.ForeignKey(User, on_delete=models.CASCADE)
    post = models.ForeignKey(Post, on_delete=models.CASCADE)