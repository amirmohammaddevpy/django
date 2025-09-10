from django.shortcuts import render,get_object_or_404
from cart.models import CartItem
from django.contrib.auth.models import User
from profiles.models import Profiles
from django.contrib.auth.decorators import login_required
from .forms import DiscountForm
from .models import Discount
from django.utils import timezone

# Create your views here.
@login_required
def checkout(request, user):
    obj = get_object_or_404(User, username=user)
    cart = CartItem.objects.filter(user=request.user)
    total = sum(item.quntity * item.post.price for item in cart)
    informations = Profiles.objects.get(uauthor=request.user)

    discount_amount = 0
    final_total = total
    form = DiscountForm()

    if request.method == "POST":
        form = DiscountForm(request.POST)
        if form.is_valid():
            code = form.cleaned_data["code_discount"]

            try:
                discount = Discount.objects.filter(code_discount=code).first()

                now = timezone.now()
                if discount.end_time < now:
                    form.add_error("code_discount","The discount code has expired.")
                else:
                    discount_amount = discount.price_discount or 0
                    final_total = max(total - discount_amount,0)
            except:
                form.add_error("code_discount","The discount code is not valid.")
        else:
            form = DiscountForm()
    context = {
        "obj": obj,
        "user": informations,
        "cart": cart,
        "total": total,
        "final_total": final_total,
        "form": form,
        "discount_amount": discount_amount,
    }

    return render(request, "cart/checkout.html", context)
