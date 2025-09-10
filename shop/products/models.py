from django.db import models
from django.contrib.auth.models import User
from profiles.models import Profiles
# Create your models here.

class Category(models.Model):
    name = models.CharField(max_length=200,db_index=True)
    slug = models.SlugField(max_length=200,db_index=True)

    class Meta:
        ordering = ("name",)
        verbose_name = 'category'
        verbose_name_plural = 'categories'
    
    def __str__(self,):
        return self.name

class Products(models.Model):
    category = models.ForeignKey(Category,on_delete=models.CASCADE,related_name="products")
    name = models.CharField(max_length=250,db_index=True)
    slug = models.SlugField(max_length=250,db_index=True)
    image = models.ImageField(upload_to="products/%Y/%m/%d/",blank=True)
    description = models.TextField()
    price = models.PositiveIntegerField()
    available = models.BooleanField(default=True)
    created = models.DateField(auto_now_add=True)
    updated = models.DateField(auto_now=True)
    class Meta:
        ordering = ("name",)
        index_together = (("id","slug"),)
    
    def __str__(self):
        return self.name
    
class Comment(models.Model):
    post = models.ForeignKey(Products,on_delete=models.CASCADE,related_name="comments")
    username = models.ForeignKey(User,on_delete=models.CASCADE,related_name="userforcomment")
    body = models.TextField()
    created = models.DateField(auto_now_add=True)

    class Meta:
        ordering = ("created",)

    def __str__(self):
        return f"post for product {self.post} name is {self.username}"

