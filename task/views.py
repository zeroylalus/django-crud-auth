from django.shortcuts import render, redirect
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth.models import User
from django.contrib.auth import login, logout, authenticate
from django.db import IntegrityError


# Create your views here.

def home(request):
    return render(request, 'home.html')

def tasks(request):
    return render(request, 'tasks.html')

def signout(request):
    logout(request)
    return redirect('home')

def signin(request):

    if request.method == 'GET':
        return render(request, 'signin.html', {'form':AuthenticationForm})
    
    else:

        user = authenticate(
            request, username=request.POST['username'],
            password=request.POST['password'],
        )
        if user == None:
            return render(request, 'signin.html', {
                'form':AuthenticationForm,
                'error': 'Username or password is incorrect'
            })
        else:
            login(request, user)
            return render(request, 'tasks.html', {
                'form':AuthenticationForm,
                'signin':'Ya estas loggeado',
            })
    

def signup(request):

    if request.method == 'GET':
        return render(request, 'signup.html', {
            'form' : UserCreationForm
        })
    else:
        if request.POST['password1'] == request.POST['password2']:
            try:
                user = User.objects.create_user(
                username=request.POST['username'],
                password=request.POST['password1'])
                user.save()
                login(request, user)
                return render(request, 'tasks.html', {
                    'signup' : 'User created successfully'
                })
            except IntegrityError:
                return render(request, 'signup.html', {
                    'form' : UserCreationForm,
                    'error' : 'Username already exists'
                })
        return render(request, 'signup.html', {
                    'form' : UserCreationForm,
                    'error' : 'Password do not match'
                })

