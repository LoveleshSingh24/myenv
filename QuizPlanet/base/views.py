from django.shortcuts import render
from django.shortcuts import HttpResponse
from django.contrib.auth.models import User
from account.models import Profile
from django.contrib.auth.decorators import login_required
from quiz.models import UserRank
# Create your views here.

def home(request):
    leaderboard_users = UserRank.objects.order_by('rank')[:4]
    if request.user.is_authenticated:
        user_object = User.objects.get(username=request.user)
        user_profile2 = Profile.objects.get(user=user_object)
        context = {"user_profile2": user_profile2, "leaderboard_users": leaderboard_users}
    else:
        context = {"leaderboard_users": leaderboard_users}
    return render(request, 'welcome.html', context)

@login_required(login_url='login')
def leaderboard_view(request):
    leaderboard_users = UserRank.objects.order_by('rank')
    user_object = User.objects.get(username=request.user)
    user_profile2 = Profile.objects.get(user=user_object)
    context = {"leaderboard_users": leaderboard_users, "user_profile2": user_profile2}
    return render(request, "leaderboard.html", context)

def dashboard_view(request):
    user_object = User.objects.get(username=request.user)
    user_profile2 = Profile.objects.get(user=user_object)
    context={"user_profile2":user_profile2}
    return render(request,"dashboard.html",context)
