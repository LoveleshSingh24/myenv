from django.shortcuts import render
from django.shortcuts import HttpResponse
from django.contrib.auth.models import User
from account.models import Profile

# Create your views here.
def home(request):
    user_object=User.objects.get(username=request.user)
    user_profile3=Profile.objects.get(user=user_object)
    
    context={"user_pro":user_profile3}
    return render(request,'welcome.html',context)