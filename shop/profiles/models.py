from django.db import models
from django.contrib.auth.models import User
# Create your models here.

class Profiles(models.Model):
    uauthor = models.ForeignKey(User,on_delete=models.CASCADE)
    image = models.ImageField(upload_to="profile/user/",default="images/download.jfif")
    phone = models.CharField(max_length=11)
    address = models.TextField()

    def __str__(self):
        return f"{self.uauthor.username}"
    
