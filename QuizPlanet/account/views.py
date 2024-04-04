from django.shortcuts import render
from django.contrib import messages
from django.shortcuts import redirect
from django.contrib.auth.models import User,auth
from . models import Profile
from django.contrib.auth.decorators import login_required
from quiz.models import QuizSubmission

# Create your views here.
# Create your views here.
def register(request):
    if(request.user.is_authenticated):
        return redirect('profile',request.user.username)
    
    if request.method == "POST":
        # post method takes the name field 
        email = request.POST.get('email')
        username = request.POST.get('username')
        password = request.POST.get('pass')
        password2 = request.POST.get('pass2')

        # password should match password2 
        if password == password2:

            #check if mail is not same
            if User.objects.filter(email=email).exists():
                messages.error(request, "Email Alredy Exist Register")
            #check if usernmae exit in database 
            elif User.objects.filter(username=username).exists():
                messages.error(request, "Username Alredy Exist")
            #create user
            else:
                user=User.objects.create_user(username=username,email=email,password=password)
                #save to db
                user.save();

                #log in the user and redirect to profile
                user_login=auth.authenticate(username=username,password=password)
                
                #auth login take the credential 
                auth.login(request,user_login)

                #create profile for new user
                user_model = User.objects.get(username=username)
                new_profile = Profile.objects.create(user=user_model)
                new_profile.save()
                
                #redirect to profile page
                return redirect('profile',user_model.username) #todo #or username
        else:
            messages.error(request, "Passwords do not match!")
            return redirect('register')

    # If the method is not POST or passwords matched, render the register page
    return render(request, 'register.html')


@login_required(login_url='login')
def profile(request,username):
    #profile user
    user_object2=User.objects.get(username=username);
    user_profile2=Profile.objects.get(user=user_object2)

    #request user
    user_object = User.objects.get(username=request.user)
    user_profile =Profile.objects.get(user=user_object)

    submissions = QuizSubmission.objects.filter(user=user_object2)




    context={"user_profile":user_profile2,"user_profile2": user_profile,"submissions":submissions}
    return render(request,"profile.html",context)

@login_required(login_url="login")
def editProfile(request):
    user_object2 = User.objects.get(username=request.user)
    user_profile =Profile.objects.get(user=user_object2)

    if request.method == "POST":
        #img
        if request.FILES.get('profile_img') != None:
            user_profile.profile_img=request.FILES.get('profile_img')
            user_profile.save()
        
        #email
        if request.POST.get('email') != None:
            u=User.objects.filter(email=request.POST.get('email')).first()

            if u==None:
                user_object2.email=request.POST.get('email')
                user_object2.save()
            else:
                if u != user_object2:
                    messages.info(request,"Email Alredy Used,Choose a diffrent email")
                    return redirect('edit_profile')
        
        
        #username
        if request.POST.get('username') != None:
            u=User.objects.filter(username=request.POST.get('username')).first()

            if u==None:
                user_object2.email=request.POST.get('username')
                user_object2.save()
            else:
                if u != user_object2:
                    messages.info(request,"Username Alredy Used,Choose a diffrent email")
                    return redirect('edit_profile')
        
        #firstname lastname
        user_object2.first_name=request.POST.get('firstname')
        user_object2.last_name=request.POST.get('lastname')

        user_object2.save()

         #location,bio ,gender
        user_profile.location =request.POST.get('location')
        user_profile.gender =request.POST.get('gender')
        user_profile.bio =request.POST.get('bio')
        user_profile.save();

        return redirect('profile',user_object2.username)
    
    context={"user_profile2":user_profile}
    return render(request,"profile-edit.html",context)


@login_required(login_url='login')
def deleteProfile(request):
    user_object = User.objects.get(username=request.user)
    user_profile = Profile.objects.get(user=user_object)

    if request.method == "POST":
        user_profile.delete()
        user_object.delete()
        return redirect('logout')

    context = {"user_profile2": user_profile}  # Consider renaming the context variable for clarity
    return render(request,'confirm.html', context)

def login(request):
    if(request.user.is_authenticated):
        return redirect('profile',request.user.username)

    #log in the user and redirect to profile
    if request.method=="POST":
        username=request.POST.get('username')
        password=request.POST.get('password')
        user=auth.authenticate(username=username,password=password)
        
        if user is not None :
            #auth login take the credential 
            auth.login(request,user)
            return redirect('profile',username)
        else:
            messages.error(request,"Credential Invalid !")
            return redirect('login')
        
    return render(request,'login.html')


@login_required(login_url='login')
def logout(request):
    auth.logout(request)
    return redirect('login')
