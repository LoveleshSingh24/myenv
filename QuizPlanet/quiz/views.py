from django.shortcuts import render
from django.shortcuts import render
from django.contrib import messages
from django.shortcuts import redirect
from django.contrib.auth.models import User,auth
from account.models import Profile
from django.contrib.auth.decorators import login_required
from .models import Quiz,Category
from django.db.models import Q
from quiz.models import QuizSubmission
from django.shortcuts import get_object_or_404

# Create your views here.
@login_required(login_url='login')
def all_quiz_view(request):
    if(request.user.is_authenticated):
        user_object = User.objects.get(username=request.user)
        user_profile2 =Profile.objects.get(user=user_object)

    quizzes = Quiz.objects.order_by('-created_at')
    categories=Category.objects.all()

    context={"user_profile2":user_profile2,"quizzes":quizzes,"categories":categories,'quiz':'active'}
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


@login_required(login_url='login')
def quiz_view(request, quiz_id):
    user_object = User.objects.get(username=request.user)
    user_profile2 = get_object_or_404(Profile, user=user_object)

    quiz = Quiz.objects.filter(id=quiz_id).first()

    total_questions = quiz.question_set.all().count()

    if request.method == "POST":
        
        # Get the score
        score = int(request.POST.get('score', 0))

        # Check if the user has already submiited the quiz
        if QuizSubmission.objects.filter(user=request.user, quiz=quiz).exists():
            messages.success(request, f"This time you got {score} out of {total_questions}")
            return redirect('quiz', quiz_id)
        
        # save the new quiz submission
        submission = QuizSubmission(user=request.user, quiz=quiz, score=score)
        submission.save()
        
        messages.success(request, f"Quiz Submitted Successfully. You got {score} out of {total_questions}")
        return redirect('quiz', quiz_id)

    context = {"user_profile2": user_profile2, "quiz": quiz}
    return render(request, 'quiz.html', context)
