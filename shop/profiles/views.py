from django.shortcuts import render ,get_object_or_404,redirect
from django.contrib.auth.decorators import login_required
from .forms import ProfileForms
from .models import Profiles
from django.contrib.auth.models import User


# Create your views here.
@login_required
def profile(request,uauthor):
    user_name = get_object_or_404(User,username=uauthor)
    profile_user = Profiles.objects.filter(uauthor=user_name).first()
    return render(request,"profile/profile.html",{"obj":user_name,"profile":profile_user})


@login_required
def edite_profile(request,uauthor):
    user = get_object_or_404(User,username=uauthor)
    get_informations = Profiles.objects.all().filter(uauthor=user).first()
    if request.method == "POST":
        form = ProfileForms(request.POST,request.FILES,instance=get_informations)
        if form.is_valid():
            get_user = form.save(commit=False)
            get_user.uauthor = user
            get_user.save()
            return redirect("profile",user)
        else:
            return render(request,"profile/edite_profile.html",)
            
    else:
        form = ProfileForms(instance=get_informations)
    return render(request,"profile/edite_profile.html",{"form":form,"get":get_informations})
