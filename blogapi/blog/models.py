from django.db import models
from django.contrib.auth.models import User
# Create your models here.

class Blog(models.Model):
    name = models.CharField(max_length=250)
    descriptions = models.CharField(max_length=100)
    body = models.TextField()
    author = models.ForeignKey(User,related_name="users",on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    def __str__(self):
       return self.name + " " + self.author.username