from django.shortcuts import render ,redirect ,get_object_or_404
from .forms import Register ,LoginForm ,CodeRegister
from django.contrib.auth import authenticate, login,logout
from random import randint
from django.core.mail import send_mail
from django.contrib.auth.models import User
from django.conf import settings

# Create your views here.


def register(request):
    context = {}
    
    if request.method == "POST":
        form = Register(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.set_password(form.cleaned_data['password'])
            user.is_active = False
            user.save()

            request.session['user_id'] = user.id
            code = randint(11111, 99999)
            request.session['code_verify'] = code

            email_address = user.email

            subject = "localhost:8000"
            message = f"Your verification code is {code}"

            if email_address:
                try:
                    send_mail(subject, message, settings.EMAIL_HOST_USER, [email_address])
                    context['result'] = "Email sent successfully."
                    return redirect("verify")
                except Exception as e:
                    context['result'] = f"Failed to send email: {e}"
            else:
                context['result'] = "Please provide an email address."
    else:
        form = Register()

    context['form'] = form
    return render(request, "user/register.html", context)

    
def login_user(request):
    if request.method == "POST":
        form = LoginForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            user = authenticate(request,username=username,password=password)
            if user is not None:
                login(request,user)
                return redirect("list_product")
            else:
                form.add_error(None, "Invalid username or password")
    else:
        form=LoginForm()
    return render(request,"user/login.html",{'form':form})

def logout_user(request):
    logout(request)
    return redirect("login")

def code_verify(request):
    user_id = request.session.get("user_id")
    code = request.session.get("code_verify")
    try:
        user = User.objects.get(id=user_id)
    except User.DoesNotExist:
        return redirect("register")
    
    if request.method == "POST":
        form = CodeRegister(request.POST)
        if form.is_valid():
            form_code = form.cleaned_data['code']
            if str(form_code) == str(code):
                user.is_active=True
                login(request,user)
                user.save()
                return redirect("list_product")
            else:
                print("code is valid!!")
                return redirect("verify")
    else:
        form = CodeRegister(request.POST)
    return render(request,"user/verify.html",{"form":form})

def resend_code(request):
    context = {}

    code = randint(11111, 99999)
    request.session['code_verify'] = code

    user_id = request.session.get("user_id")
    if not user_id:
        return redirect("register")

    try:
        user = User.objects.get(id=user_id)
    except User.DoesNotExist:
        context['result'] = "User not found."
        return redirect("register")

    subject = "localhost:8000"
    message = f"Your verification code is {code}"

    try:
        send_mail(subject, message, settings.EMAIL_HOST_USER, [user.email])
        context['result'] = "Email sent successfully."
    except Exception as e:
        context['result'] = f"Failed to send email: {e}"

    return redirect("verify")