from django.shortcuts import render,redirect
from django.http import HttpResponse
from .forms import CreateUserForm
from django.contrib import messages
from django.contrib.auth import login,authenticate,logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
# Create your views here.

def home(request):
    return render(request,'base.html')




def registerPage(request):
    form=CreateUserForm()
    if request.method=='POST':
        form=CreateUserForm(request.POST)
        if form.is_valid():
            user=form.save()
            username=form.cleaned_data.get('username')

            messages.success(request,'Account was Created for ' + username)
            return redirect('login')

    context={'form':form}
    return render(request,'account/register.html',context)






def loginPage(request):
    if request.method=='POST':
        username=request.POST.get('username')
        password=request.POST.get('password')
        user=authenticate(request,username=username,password=password)

        if user is not None:
            login(request,user)
            messages.success(request,'welcome ' + username)
            return redirect('/userpage')

        else:
            messages.warning(request,'Username or Password is incorrect')
    context={}
    return render(request,'account/login.html',context)

def logoutUser(request):
    logout(request)
    return redirect('login')




#
# def signup(request):
#     if request.method=='POST':
#         name=request.POST.get('name','')
#         username=request.POST.get('username','')
#         mail=request.POST.get('email','')
#         password=request.POST.get('password','')
#         conf_pass=request.POST.get('confirm_password','')
#
#
#         if password == conf_pass:
    #             user_obj=User.objects.create_user(first_name = name, password = password , email = mail , username = username)
#             print(user_obj)
#             user_obj.save()
#     return redirect('/')
#
# def user_login(request):
#     if request.method=='POST':
#         user_name=request.POST.get('username','')
#         user_password=request.POST.get('password1','')
#
#         #if user account exists or not
#         user=authenticate(username=user_name,password=user_password)
#
#         if user is not None:
#             login(request,user)
#             return HttpResponse("logged in")
#         else:
#             return HttpResponse("invalid creddentials")
