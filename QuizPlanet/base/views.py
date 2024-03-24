from django.shortcuts import render
from django.shortcuts import HttpResponse
from django.contrib.auth.models import User
from account.models import Profile
from django.contrib.auth.decorators import login_required
# Create your views here.

@login_required(login_url='login')
def home(request):
    if(request.user.is_authenticated):
        user_object = User.objects.get(username=request.user)
        user_profile2 =Profile.objects.get(user=user_object)
        
        context={"user_profile2":user_profile2}
        return render(request,'welcome.html',context)
    else:
        context={}
        return render(request,'welcome.html',context)
        