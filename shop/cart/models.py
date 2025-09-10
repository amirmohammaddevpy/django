from django.db import models
from products.models import Products
from django.contrib.auth.models import User
# Create your models here.
class CartItem(models.Model):
    post = models.ForeignKey(Products,on_delete=models.CASCADE)
    quntity = models.PositiveIntegerField(default=0)
    user = models.ForeignKey(User,on_delete=models.CASCADE)
    date_added = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.quntity} x {self.post.name} "