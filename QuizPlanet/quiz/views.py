from django.shortcuts import render
from django.shortcuts import render
from django.contrib import messages
from django.shortcuts import redirect
from django.contrib.auth.models import User,auth
from account.models import Profile
from django.contrib.auth.decorators import login_required
from .models import Quiz,Category
from django.db.models import Q

# Create your views here.
@login_required(login_url='login')
def all_quiz_view(request):
    if(request.user.is_authenticated):
        user_object = User.objects.get(username=request.user)
        user_profile2 =Profile.objects.get(user=user_object)

    quizzes = Quiz.objects.order_by('-created_at')
    categories=Category.objects.all()

    context={"user_profile2":user_profile2,"quizzes":quizzes,"categories":categories}
    return render(request,"all-quiz.html", context)

@login_required(login_url='login')
def search_view(request,category):
    user_object = User.objects.get(username=request.user)
    user_profile2 =Profile.objects.get(user=user_object)

    #search by category
    if request.GET.get('q') != None :
        q=request.GET.get('q')
        query=Q(title__icontains=q) | Q(description__icontains=q)
        quizzes=Quiz.objects.filter(query).order_by('-created_at')
    #serach by search bar
    elif category != " ":
        quizzes=Quiz.objects.filter(category__name=category).order_by('-created_at')
    else:
        quizzes = Quiz.objects.order_by('-created_at')

    categories = Category.objects.all()

    context={"user_profile2":user_profile2,"quizzes":quizzes,"categories":categories}
    return render(request,"all-quiz.html", context)