from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth.models import User
from django.contrib.auth import login, logout, authenticate
from django.db import IntegrityError
from task import forms, models
from django.utils import timezone
from django.contrib.auth.decorators import login_required


# Create your views here.

@login_required
def delete_task(request,id):
    task = get_object_or_404(models.Task, pk=id, user=request.user)
    if request.method == 'POST':
        task.delete()
        return redirect('tasks')

@login_required
def complete_task(request,id):
    task = get_object_or_404(models.Task, pk=id, user=request.user)
    if request.method == 'POST':
        task.datecompleted = timezone.now()
        task.save()
        return redirect('tasks')

@login_required
def task_detail(request, id):
    if request.method == 'GET':
        task = get_object_or_404(models.Task,pk=id, user=request.user)
        form = forms.TaskForm(instance=task)
        return render(request, 'task_detail.html', {
            'task': task,
            'form': form
        })
    else:
        try:
            task = get_object_or_404(models.Task,pk=id, user=request.user)
            form = forms.TaskForm(request.POST,instance=task)
            form.save()
            return redirect('tasks')
        except ValueError:
            return render(request, 'task_detail.html', {
                'task': task,
                'form': form,
                'error': 'Error updating task'
            })

    
@login_required
def create_tasks(request):

    if request.method == 'GET':
        return render(request, 'create_tasks.html',{
            'form': forms.TaskForm
        })
    else:
        try:
            f = forms.TaskForm(request.POST)
            t = f.save(commit=False)
            t.user = request.user
            t.save()
            return redirect('tasks')
        except ValueError:
            return render(request, 'create_tasks.html',{
                'form': forms.TaskForm,
                'error': 'Please provide valid data'
            })
        
def home(request):
    return render(request, 'home.html')

@login_required
def tasks(request):
    tasks = models.Task.objects.filter(
        user=request.user,
        datecompleted__isnull=True)
    return render(request, 'tasks.html',{
        'tasks': tasks
    })
@login_required
def tasks_completed(request):
    tasks = models.Task.objects.filter(
        user=request.user,
        datecompleted__isnull=False).order_by('-datecompleted')
    return render(request, 'tasks.html',{
        'tasks': tasks
    })

@login_required
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
            return redirect('tasks')
    

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
                return redirect('tasks')
            except IntegrityError:
                return render(request, 'signup.html', {
                    'form' : UserCreationForm,
                    'error' : 'Username already exists'
                })
        return render(request, 'signup.html', {
                    'form' : UserCreationForm,
                    'error' : 'Password do not match'
                })

