from django.shortcuts import render
from django.contrib import messages
from django.shortcuts import redirect
from django.contrib.auth.models import User,auth
from . models import Profile

# Create your views here.
# Create your views here.
def register(request):
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
                new_profile = Profile.objects.create(user=user_model,email_address=email)
                new_profile.save()
                
                #redirect to profile page
                return redirect('home') #todo
        else:
            messages.error(request, "Passwords do not match!")
            return redirect('register')

    # If the method is not POST or passwords matched, render the register page
    return render(request, 'register.html')