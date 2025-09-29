from django.db import models
from django.contrib.auth.models import User

# Create your models here.

class Topic(models.Model):
    name = models.CharField(max_length=50)

    def __str__(self):
        return self.name
    

class Room(models.Model):
    topic = models.ForeignKey(Topic,on_delete=models.SET_NULL,null=True)
    host = models.ForeignKey(User,on_delete=models.SET_NULL,null=True)
    name = models.CharField(max_length=250,)
    participants = models.ManyToManyField(User,related_name="participants",blank=True)
    description = models.TextField(blank=True,null=True)
    update = models.DateTimeField(auto_now=True)
    created = models.DateTimeField(auto_now_add=True)
    image = models.ImageField(upload_to="room/image",blank=True,null=True)

    class Meta:
        ordering = ['-update','-created']

    def __str__(self):
        return self.name

class ProfileUser(models.Model):
    user = models.ForeignKey(User,related_name='profileuser',on_delete=models.CASCADE)
    image = models.ImageField(upload_to="image/user",default="images/default.png",blank=True,null=True)

    def __str__(self):
        return self.user.username
    
class Message(models.Model):
    user = models.ForeignKey(User,on_delete=models.CASCADE)
    room = models.ForeignKey(Room,on_delete=models.CASCADE)
    body = models.TextField()
    updated = models.DateTimeField(auto_now=True)
    created = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.body[0:50]