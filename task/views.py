from django.db.models.query_utils import Q
from django.http import request
from django.http.response import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from django.contrib.auth.models import User
from django.contrib import auth
from .models import login_user
import re
# from django.http import HttpResponse

# Create your views here.
def signup(request):
    if request.method == "POST":
        
        if request.POST['password'] == request.POST['cpassword']:
            try:
                user = User.objects.get(username=request.POST['username'])
                return render(request,'task/signup.html',{'error':"Username Has already been taken"})
            except User.DoesNotExist:
                user = User.objects.create_user(username=request.POST['username'],password=request.POST['password'],email=request.POST['email'])
                phone_number=request.POST['phone']
                first_name=request.POST['fname']
                last_name=request.POST['lname']
                email=request.POST['email']
            if (len(request.POST['password'])<8):
                return render(request,'task/signup.html',{'error':"Password too Short, Should Contain ATLEAST 1 Uppercase,1 lowercase,1 special Character and 1 Numeric Value"})

            elif not re.search(r"[\d]+",request.POST['password']):
                return render(request,'task/signup.html',{'error':"Your Password must contain Atleast 1 Numeric "})
            elif not re.findall('[A-Z]', request.POST['password']):   
                return render(request,'task/signup.html',{'error':"Your Password must contain Atleast 1 UpperCase Letter "})

            elif not re.findall('[a-z]',request.POST['password']):
                return render(request,'task/signup.html',{'error':"Your Password must contain Atleast 1 lowercase Letter "})
            elif not re.findall('[()[\]{}|\\`~!@#$%^&*_\-+=;:\'",<>./?]', request.POST['password']):   
                return render(request,'task/signup.html',{'error':"Your Password must contain Atleast 1 Specail character "})
            else:
                if login_user.objects.filter(email=email).exists():
                    return render(request,'task/signup.html',{'error':"This Email Already Exists"})
                elif login_user.objects.filter(phone_number=phone_number).exists():
                    return render(request,'task/signup.html',{'error':"This Phone number Already Exists"})
                else:
                    newlogin_user= login_user(phone_number=phone_number,user=user,first_name=first_name,last_name=last_name,email=email)
                    newlogin_user.save()
                    auth.login(request,user)
                    return HttpResponse('<h1>You have been successfully signed in!<h1>')
        else:
            return render(request,'task/signup.html',{'error':"You Entered Wrong Password"})
            
        
    else:
        return render(request,'task/signup.html',)
    # return render(request,'task/task_home.html')
 
def login(request):
    if request.method == "POST":
        user = auth.authenticate(username=request.POST['username'],password=request.POST['password'])
        if user is not None:
            auth.login(request,user)
            matching=login_user.objects.filter(user=request.user)
            return render(request,'task/login_view.html',{'match':matching})
        else:
            return render(request,'task/login.html')
    else:
        return render(request,'task/login.html')



def search(request):
    if request.method == "POST":

        search = request.POST['search']
        if search:
            matching=login_user.objects.filter(Q(first_name__contains=search))
            if matching:
                return render(request,'task/search.html',{'match':matching,'search':search})
            else:
                return render(request,'task/search.html',{'error':'No result found'})
        else:
            return render(request,'task/search.html',{'error':'No result found'})
    return render(request,'task/search.html')
