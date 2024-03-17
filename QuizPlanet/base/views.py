from django.shortcuts import render
from django.shortcuts import HttpResponse
from django.contrib.auth.models import User
from account.models import Profile

# Create your views here.
def home(request):
    if(request.user.is_authenticated):
        user_object2 = User.objects.get(username=request.user)
        user_profile =Profile.objects.get(user=user_object2)
        
        context={"user_profile2":user_profile}
        return render(request,'welcome.html',context)
    else:
        return render(request,'welcome.html')
        