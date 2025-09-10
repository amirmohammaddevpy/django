from django.shortcuts import render
from posts.models import Post
from actions.models import Action
from myuser.models import MyUser
from django.db.models import Count
from django.contrib.auth.decorators import login_required
# Create your views here.
@login_required(login_url="profile:login")
def home_page(request):
    user = request.user
    post = Post.objects.filter(user=user).order_by("-created")
    posts = Post.objects.none()
    for friends in user.following.all():
        frind_post = Post.objects.filter(user=friends)
        posts = post | frind_post
    else:
        posts = Post.objects.all()
    actions = Action.objects.exclude(user=user)
    following_ids = user.following.values_list("id" ,flat=True)
    if following_ids:
        actions = actions.filter(user_id__in=following_ids)[:10]
    user_following = MyUser.objects.filter(id__in=following_ids)
    suggest_list = MyUser.objects.none()
    for follow in user_following.all():
        for suggest_user in follow.following.all():
            if not suggest_user.id in following_ids and suggest_user != user:
                suggest_user = MyUser.objects.filter(id=suggest_user.id)
                suggest_list |= suggest_user
    suggest_list = suggest_list[:10]
    print(suggest_list)
    return render(request,"pages/home.html",{"posts":posts,"actions":actions,"suggets":suggest_list})

@login_required(login_url="profile:login")
def explor(request):
    post = Post.objects.order_by('total_like')
    return render(request,"pages/explor.html",{"posts":post})