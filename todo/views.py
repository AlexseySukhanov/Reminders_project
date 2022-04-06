from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth.models import User
from django.db import IntegrityError
from django.contrib.auth import login, logout, authenticate
from .forms import ReminderForm
from .models import Reminder
from django.utils import timezone
from django.contrib.auth.decorators import login_required

#decorator login_required used to prevent acsess to reminders of other users

# used for homepage render
def home(request):
    return render(request,'todo/home.html')

# used for existing user login
def loginuser(request):
    if request.method == 'GET':
        return render(request,'todo/loginuser.html',{'form':AuthenticationForm()})
    else:
        if request.method == 'POST':
            username = request.POST['username']
            password = request.POST['password']
            user = authenticate(request, username=username, password=password)
            if user is not None:
                login(request,user)
                return redirect('currentuser')
            else:
                return render(request,'todo/loginuser.html',{'error':'Input valid username and password','form':AuthenticationForm()})

# used for register new user
def authuser(request):
    if request.method == 'GET':
        return render(request,'todo/authuser.html',{'form':UserCreationForm()})
    else:
        if request.POST['password1'] == request.POST['password2']:
            try:
                user = User.objects.create_user(request.POST['username'],password=request.POST['password1'])
                user.save()
                login(request,user)
                return redirect('currentuser')
            except IntegrityError:
                return render(request,'todo/authuser.html',{'error':'This user name already exists, please choose another','form':UserCreationForm()})
        else:
            return render(request,'todo/authuser.html',{'error':'Passwords did not match','form':UserCreationForm()})

# used for view reminders of current user
@login_required
def currentuser(request):
    reminders = Reminder.objects.filter(user=request.user, reminder_date__isnull=True)
    return render(request,'todo/currentuser.html',{'reminders':reminders})

# used for view complited reminders of current user
@login_required
def completed_reminders(request):
    completed_reminders = Reminder.objects.filter(user=request.user, reminder_date__isnull=False).order_by('-reminder_date')
    return render(request,'todo/completed_reminders.html',{'completed_reminders':completed_reminders})

# used for user logout
@login_required
def logoutuser(request):
     if request.method == 'POST':
         logout(request)
         return redirect('home')

# used for creating new reminder for current user
@login_required
def createtodo(request):
    if request.method == 'GET':
        return render(request,'todo/createtodo.html',{'form':ReminderForm()})
    else:
        try:
            form = ReminderForm(request.POST)
            newreminder = form.save(commit = False)
            newreminder.user = request.user
            newreminder.save()
            return redirect('currentuser')
        except ValueError:
            return render(request,'todo/createtodo.html',{'form':ReminderForm(),'error':'Bad data entered! '})

# used for viewing choosed reminder of current user
@login_required
def view_reminder(request,reminder_pk):
    reminder = get_object_or_404(Reminder, pk = reminder_pk, user = request.user)
    if request.method == 'GET':
        form = ReminderForm(instance = reminder)
        return render(request,'todo/view_reminder.html',{'reminder':reminder, 'form':form})
    else:
        try:
            form = ReminderForm(request.POST, instance = reminder)
            form.save()
            return redirect('currentuser')
        except ValueError:
            return render(request,'todo/view_reminder.html',{'reminder':reminder, 'form':form,'error':'Bad data entered! '})

# used for complittion of choosed reminder
@login_required
def complete_reminder(request, reminder_pk):
    reminder = get_object_or_404(Reminder, pk = reminder_pk, user = request.user)
    if request.method == 'POST':
        reminder.reminder_date = timezone.now()
        reminder.save()
        return redirect('currentuser')

#used for deletion of choosed reminder
@login_required
def delete_reminder(request, reminder_pk):
    reminder = get_object_or_404(Reminder, pk = reminder_pk, user = request.user)
    if request.method == 'POST':
        reminder.delete()
        return redirect('currentuser')
