from django.shortcuts import render ,redirect ,get_object_or_404
from myuser.models import MyUser ,Contact
from django.contrib.auth.decorators import login_required
from django.views.decorators.http import require_POST
from django.contrib.auth import login ,authenticate
from .forms import RegisterForm ,ChangeProfile ,LoginForm
from django.contrib import messages
from posts.models import Post
from django.core.paginator import Paginator ,PageNotAnInteger ,EmptyPage
from random import randint
from django.http import JsonResponse
from django.template.loader import render_to_string
from actions.utils import create_action
# Create your views here.

@login_required
def dashbord(request,username):
    user = MyUser.objects.get(username=username)
    post = Post.objects.filter(user=user).order_by("-created")
    paginator = Paginator(post,6)
    try:
        page = request.GET.get("page")
        if page:
            post = paginator.page(page)
            return JsonResponse({
                "status":render_to_string("account/dashboard_posts_ajax.html",{"posts":post}, request=request )                       
            })
        else:
            post = paginator.page(1)
    except PageNotAnInteger:
        post = paginator.page(1)
    except EmptyPage:
        return JsonResponse({"status":"empty"})

    return render(request,"account/dashboard.html",{'user':user,'posts':post})

def login_user(request):
    if request.method == "POST":
        form = LoginForm(request.POST)
        if form.is_valid():
            cd = form.cleaned_data
            user = authenticate(request,phone=cd['phone'] , password=cd['password'])
            if user is not None:
                if user.is_active:
                    login(request,user)
                    return redirect("profile:profile" , user)
                else:
                    messages.error(request,"Your account is not active")
            else:
                messages.error(request,"Invalid username or password")
        else:
            messages.error(request,"Form is not valid")
    else:
        form = LoginForm()
    return render(request,"account/login.html",{'form':form})
            

def register_form(request):
    if request.method == "POST":
        form = RegisterForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            password1 = form.cleaned_data.get('password1')
            password2 = form.cleaned_data.get('password2')
            if password1 != password2:
                messages.error(request,"Password is not match!!!")
            else:
                user.set_password(password2)
                user.is_active = False
                user.save()
                
                request.session['user_id'] = user.id
                code = randint(00000,99999)
                request.session['code_verify'] = code

                print(code)
                return redirect("profile:verify")
        else:
            messages.error(request,"Form is not valid")
    else:
        form = RegisterForm()
    return render(request,"account/register.html",{'form':form})

def change_form(request,user):
    user = get_object_or_404(MyUser, username=user)
    if request.method == "POST":
        form = ChangeProfile(request.POST,request.FILES,instance=user)
        if form.is_valid():
            form.save()
            return redirect("profile:profile" , user)
        else:
            messages.error(request,"form is not valid")
    else:
        form = ChangeProfile(instance=user)
    return render(request,"account/change.html",{'form':form})

def verify_code(request):
    get_code = request.session.get('code_verify')
    code = request.POST.get("code")
    user_id = request.session.get('user_id')
    try:
        user = MyUser.objects.get(id=user_id)
    except MyUser.DoesNotExist:
        return redirect("profile:register")

    if request.method == "POST":
        if str(code) == str(get_code):
            user.is_active = True
            login(request,user)
            user.save()
            return redirect("profile:profile", request.user)
        else:
            return render(request,"account/verify.html")
    else:
        messages.error(request,"asdasd")
    return render(request,"account/verify.html")

def resend_code(request):
    user_id = request.session.get("user_id")
    context = {}

    code = code = randint(00000,99999)
    request.session['code_verify'] = code

    if not user_id:
        return redirect("register")

    try:
        user = MyUser.objects.get(id=user_id)
    except MyUser.DoesNotExist:
        context['result'] = "User not found."
        return redirect("register")
    
    print(code)
    return redirect("profile:verify")

@login_required
@require_POST
def user_fllowing(request):
    user_id = request.POST.get("id")
    action = request.POST.get("action")
    if user_id and action:
        try:
            user = MyUser.objects.get(id=user_id)
            if action == "follow":
                Contact.objects.get_or_create(user_from = request.user , user_to = user)
                create_action(request.user,"Follow",user)
            else:
                Contact.objects.filter(user_from = request.user, user_to = user).delete()
                create_action(request.user,"Unfollow",user)
            return JsonResponse({"status":"Ok"})
        except:
            return JsonResponse({"status":"error"})
    return JsonResponse({"status":"error"})