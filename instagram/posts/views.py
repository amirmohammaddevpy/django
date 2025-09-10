from django.shortcuts import render ,redirect ,get_object_or_404
from .models import Post ,CommentPost
from django.contrib.auth.decorators import login_required
from django.views.decorators.http import require_POST
from django.http import JsonResponse
from .forms import CreatePost ,CommentPostForm
from actions.utils import create_action
# Create your views here.

def detail_post(request,id,slug):
    user = get_object_or_404(Post,id=id,slug=slug)
    form = CommentPostForm()
    if request.method == "POST":
        try:
            get_id_comment = request.POST.get("id")
            action = request.POST.get("action")
            if get_id_comment and action:
                try:
                    comment_like = CommentPost.objects.get(id=get_id_comment)
                    if action == "like":
                        comment_like.likes.add(request.user)
                    else:
                        comment_like.likes.remove(request.user)
                    return JsonResponse({"status":"OK"})
                except:
                    return JsonResponse({"status":"error"})
        except:
            get_id_comment=None
            action = None
            
        else:
            if request.method == "POST":
                form = CommentPostForm(request.POST)
                if form.is_valid():
                    try:
                        comment = form.save(commit=False)
                        comment.post = get_object_or_404(Post,id=id,slug=slug)
                        comment.user = request.user
                        comment.save()
                        create_action(request.user , "commnets")
                        form = CommentPostForm()
                        return JsonResponse({"status":"Ok"})
                    except:
                        return JsonResponse({"status":"Error"})
            else:
                form = CommentPostForm()
    return render(request,"posts/detail.html",{'user':user,'form':form})

@login_required
def create_post(request):
    if request.method == "POST":
        form = CreatePost(request.POST ,files=request.FILES)
        if form.is_valid():
            user = form.save(commit=False)
            user.user = request.user
            user.save()
            create_action(request.user,"Created post",user)
            return redirect("profile:profile",request.user)
    else:
        form = CreatePost()
    return render(request,"account/create.html",{'form':form})

@login_required
@require_POST
def like_post(request):
    post_id = request.POST.get("id")
    action = request.POST.get("action")
    if post_id and action:
        try:
            post = Post.objects.get(id=post_id)
            if action == "like":
                post.user_like.add(request.user)
                create_action(request.user , "likes",post)
            else:
                post.user_like.remove(request.user)
                create_action(request.user , "dislike",post)
            return JsonResponse({"status":"ok"})
        except:
            pass
        return JsonResponse({"status":"error"})