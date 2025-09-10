from django.shortcuts import render ,redirect
from products.models import Products
from .models import CartItem
from django.contrib.auth.models import User
# Create your views here.

def view_cart(request):
    cart = CartItem.objects.filter(user=request.user)

    total_price = sum( item.post.price * item.quntity for item in cart)
    context = {
        "number_cart":cart,
        'total':total_price,
    }
    return render(request,"cart/cart.html",context)

def add_cart(request,id):
    get_post = Products.objects.get(id=id)
    cart_id ,create = CartItem.objects.get_or_create(post=get_post,user=request.user)

    quantity = int(request.POST.get("quantity",1))

    cart_id.quntity += quantity
    cart_id.save()
    return redirect("cart")

def cart_from_remove(request,id):
    cart = CartItem.objects.get(id=id)
    cart.delete()
    return redirect("cart")