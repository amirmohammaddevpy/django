from django.shortcuts import render,get_object_or_404,redirect
from .models import Products ,Category,Comment
from .forms import CommentForms 
# Create your views here.

def list_products(request):
    query = request.GET.get("q")
    if query:
        obj = Products.objects.filter(name__icontains=query)
    else:
        obj = Products.objects.all().filter(available=True)
    return render(request,"index/home.html",{"products":obj})


def detail_product(request,slug):
    obj = get_object_or_404(Products,slug=slug)
    comment = Comment.objects.filter(post=obj)

    filter_product = Products.objects.filter(category=obj.category).exclude(id=obj.id)

    if request.method == "POST":
        form_comments = CommentForms(request.POST)
        if form_comments.is_valid():
            user = form_comments.save(commit=False)
            user.username = request.user
            user.post = obj
            user.save()
            return redirect("detail_product",slug=slug)
    else:
        form_comments= CommentForms()
    context = {
        'product':obj,
        'comments':comment,
        'similar_products':filter_product,
        'form_comments':form_comments,
    }
    return render(request,"index/detail.html",context)