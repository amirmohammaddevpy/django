from django.db import models

# Create your models here.
class Discount(models.Model):
    code_discount = models.CharField(max_length=5,null=False,blank=False)
    price_discount = models.PositiveIntegerField(null=True,blank=True)
    start_time = models.DateTimeField(auto_now_add=True)
    end_time = models.DateTimeField(null=True,blank=True)

    def __str__(self):
        return self.code_discount