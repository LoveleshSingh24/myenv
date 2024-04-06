from django.shortcuts import render,redirect
from django.shortcuts import HttpResponse
from django.contrib.auth.models import User
from account.models import Profile
from django.contrib.auth.decorators import login_required,user_passes_test
from quiz.models import UserRank,Quiz,QuizSubmission,Question
import datetime
import math
from .models import Message,Blog
from django.contrib import messages
from django.db.models.functions import ExtractYear
from django.db.models import Count



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

def is_superuser(user):
    return user.is_superuser


@user_passes_test(is_superuser)
@login_required(login_url='login')
def dashboard_view(request):
    user_object = User.objects.get(username=request.user)
    user_profile2 = Profile.objects.get(user=user_object)

    #total user 
    total_user=User.objects.all().count()
    total_quizzes=Quiz.objects.all().count()
    total_quiz_submit=QuizSubmission.objects.all().count()
    total_question=Question.objects.all().count()

    today_user=User.objects.filter(date_joined__date=datetime.date.today()).count()
    today_quizzes_objs=Quiz.objects.filter(created_at__date=datetime.date.today()).count()
    today_quiz_submit=QuizSubmission.objects.filter(submitted_at__date=datetime.date.today()).count()

    today_question=0
    for _ in range(today_quizzes_objs):
        today_question += Question.objects.filter(quiz__created_at__date=datetime.date.today()).count()

    #gain 
        def gain_percentage(total,today):
            if total > 0 and today > 0:
                gain = math.floor((today* 100)/total)
                return gain
        gain_users = gain_percentage(total_user,today_user)
        gain_quizzes = gain_percentage(total_quizzes,today_quizzes_objs)
        gain_quiz_submit = gain_percentage(total_quiz_submit,today_quiz_submit)
        gain_question = gain_percentage(total_question,today_question)
    

    #inbox message 
    messages = Message.objects.filter(created_at__date=datetime.date.today()).order_by('-created_at')

        
    context={"user_profile2":user_profile2,
             "total_user":total_user,
             "total_question":total_question , 
             "total_quizzes":total_quizzes,
             "total_quiz_submit":total_quiz_submit,
             "today_users":today_user,
             "today_quizzes":today_quizzes_objs,
             "today_quiz_submit":today_quiz_submit,
             "today_question":today_question,
             "gain_users":gain_users,
             "gain_quizzes":gain_quizzes,
             "gain_quiz_submit":gain_quiz_submit,
             "gain_question":gain_question,
             "messages":messages}
    return render(request,"dashboard.html",context)


def about_view(request):
    
    if request.user.is_authenticated:
            user_object = User.objects.get(username=request.user)
            user_profile2 = Profile.objects.get(user=user_object)
            context = {"user_profile2": user_profile2,}
            return render(request,'about.html',context)
    else:
            context = {}
            return render(request,'about.html',context)
    
def blogs_view(request):
    year_blog_count = (
        Blog.objects
        .annotate(year=ExtractYear('created_at'))
        .filter(status='public')
        .values('year')
        .annotate(count=Count('id'))
        .order_by('-year')
)

    blogs = Blog.objects.filter(status='public').order_by('-created_at')
    if request.user.is_authenticated:
        user_object = User.objects.get(username=request.user)
        user_profile2 = Profile.objects.get(user=user_object)
        context = {"user_profile2": user_profile2,'year_blog_count':year_blog_count,'blogs':blogs}
        return render(request,'blogs.html',context)
    else:
        context = {'year_blog_count':year_blog_count,'blogs':blogs}
        return render(request,'blogs.html',context)

@login_required(login_url='login')
def blog_view(request,blog_id):

    blog=Blog.objects.filter(id=blog_id).first()

    if request.user.is_authenticated:
        user_object = User.objects.get(username=request.user)
        user_profile2 = Profile.objects.get(user=user_object)
        context = {"user_profile2": user_profile2,"blog":blog}
        return render(request,'blog.html',context)

@login_required(login_url='login')  
def downloads_view(reqest):
        user_object = User.objects.get(username=reqest.user)
        user_profile2 = Profile.objects.get(user=user_object)
        context = {"user_profile2": user_profile2,}
        return render(reqest,'downloads.html',context)

@login_required(login_url='login') 
def contact_view(request):
    user_object = User.objects.get(username=request.user)
    user_profile2 = Profile.objects.get(user=user_object)
    
    if request.method == "POST":
        subject = request.POST.get('subject')
        message = request.POST.get('message')
        
        if subject is not None and message is not None:
            form = Message.objects.create(user=request.user, subject=subject, message=message)
            form.save()
            messages.success(request, "Message is submitted, we will get back to you soon")
            return redirect("profile", request.user.username)
        else:
             message.error(request,"Error! caused while sending the message")
             return redirect('contact')
    context = {"user_profile2": user_profile2}
    return render(request, 'contact.html', context)

@user_passes_test(is_superuser)
@login_required(login_url='login') 
def message_view(request,id):
        user_object = User.objects.get(username=request.user)
        user_profile2 = Profile.objects.get(user=user_object)

        message=Message.objects.filter(id=int(id)).first()
        if not message.is_read:
             message.is_read=True
             message.save()

        context = {"user_profile2": user_profile2,"message":message}
        return render(request,'message.html',context)
 
def terms_and_conditions(request):
    if request.user.is_authenticated:
        user_object = User.objects.get(username=request.user)
        user_profile2 = Profile.objects.get(user=user_object)
        context = {"user_profile2": user_profile2,}
        return render(request,'terms-conditions.html',context)
    else:
        context = {}
        return render(request,'terms-conditions.html',context)

def search_user(request):
     return render(request,"")