from django.contrib.auth.backends import RemoteUserBackend
from django.shortcuts import redirect, render
from django.contrib.auth.models import User
from .models import Employee 
from django.contrib.auth import login, logout, authenticate  
from django.contrib.auth import models 
from django.contrib.auth.decorators import login_required 


# * function_name : user_login -> function to get user login in system. 
# * start a session between user and system. 
def user_login(request): 
    context = {}
    # initalize userCredirError to False as user have not enetered anything yet. 
    context['userCreditError'] = False 
    # if login form submitted to server. 
    if request.method == "POST": 
        # fetch require data from login form server got. 
        user_email = request.POST.get('userEmail')
        user_password = request.POST.get('userPassword')
        # authenticate user using username and password. 
        user_employee = authenticate(username=user_email, password=user_password)
        print(user_employee)
        # if user is authenticated login user and redirect user to user DashBoard. 
        if user_employee is not None: 
            login(request, user_employee)
            return redirect('/')
        else: 
            # if user is not autenticated assign userCreditError to True 
            # and show alert on client side. 
            context['userCreditError'] = True 
            return render(request, 'users/login.html', context)         
    else: 
        # if user login page has been requted render login page. 
        return render(request, 'users/login.html', context) 



# * function_name : user_signup 
# * register new user and throw required exception if any integrit Error Occurs. 
def user_signup(request): 
    context = {}
    # initlize required variables. 
    # userExists is Flag to tell about integrity Error(Same Email Address used Again.)
    context['userExist'] = False 
    # user Registered Flag to tell user has been registered and can login now. 
    context['UserRegistered'] = False 
    context['UserLogined']  = False 

   
    if request.method == "POST": 
        # fetch required data from signup form. 
        user_email = request.POST.get('userEmail')
        user_password = request.POST.get('userPassword')
        user_first_name = request.POST.get('userFirstName')
        user_last_name = request.POST.get('userLastName')
        user_address = request.POST.get('userAddress')
        user_phone_number = request.POST.get('userTelNumber')
        user_group = request.POST.get('userLevel')
        print(user_email, user_password, user_first_name, user_last_name, user_phone_number, user_address, user_group)
        try:
            # add user to about dataBase. 
            new_employee = User.objects.create_user(username = user_email, 
                email=user_email, 
                first_name = user_first_name, 
                last_name = user_last_name, 
                password = user_password, 
                )
            new_employee.save()

            # this part of code ---------------------------- for testing purpose. ;
            print("-----------------------------------------------")
            print(authenticate(username = user_email, password = user_password))
            print("-----------------------------------------------")
            # this part of code ---------------------------- for testing purpose. ; 
            
            new_employee_data = Employee.objects.create(employee_id = new_employee, 
              employee_level = user_group, 
              employee_address=user_address, 
              employee_phone=user_phone_number)
            
            # user is registered get user online than. login user on system. 
            context['UserRegistered'] = True  
            login(request, new_employee)
            context['UserLogined'] = True 
            context['userExist'] = False 
            return redirect('/')

        except: # if any Integrity Error Found. 
            context['userExist'] = True 
            return render(request, 'users/signup.html', context)

    else: 
        print("------------------")
        return render(request, 'users/signup.html', context) # render signup page. 


# user can views his profile, TODO : this section need lots of updated.
@login_required 
def user_profile(request): 
    context = {}

    return render(request, 'users/userProfile.html', context) # user profile render. 

# function for user logout. 
def user_logout(request): 
    context = {}
    logout(request) 
    return redirect('/user/login')