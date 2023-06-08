from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.contrib import messages,auth
from django.contrib.auth.models import User
from datetime import datetime
import json

from .models import TimeTracker
# Create your views here.

# Global variables
start_time = None
elapsed_time = 0
stopwatch_active = False
current_session = 0

# Function to update the stopwatch every second
def update_stopwatch():
    global elapsed_time, current_session
    if stopwatch_active:
        elapsed_seconds = int((datetime.now() - start_time).total_seconds())
        current_session=elapsed_seconds
        elapsed_hours = elapsed_seconds // 3600
        elapsed_minutes = (elapsed_seconds % 3600) // 60
        elapsed_seconds = elapsed_seconds % 60
        elapsed_time = f"{elapsed_hours:02d}:{elapsed_minutes:02d}:{elapsed_seconds:02d}"
    else:
        elapsed_time = "00:00:00"

# Django view for the index page
# @login_required
def index(request):
    return render(request, 'index.html')

# Django view to start the stopwatch
def start(request):
    global start_time, stopwatch_active
    start_time = datetime.now()
    stopwatch_active = True
    update_stopwatch()
    return render(request, 'index.html', {'elapsed_time': elapsed_time})

# Django view to stop the stopwatch
def stop(request):    
    global stopwatch_active
    stopwatch_active = False
    response_data = {'elapsed_time': str(elapsed_time)}
    return HttpResponse(json.dumps(response_data), content_type='application/json')

# Django view to get the elapsed time as JSON
def get_elapsed_time(request):
    update_stopwatch()
    response_data = {'elapsed_time': elapsed_time}
    return HttpResponse(json.dumps(response_data), content_type='application/json')

def login(request):       
    if request.method=='POST':
        username = request.POST['username']
        password = request.POST['password']

        user= auth.authenticate(username=username, password=password)
        if user is None: #user is not registered
            messages.info(request,'User is not registered!!')
            return redirect('/register')
        else:
            auth.login(request, user)            
            time_tracker= TimeTracker(user=request.user, login_time=datetime.now())
            # time_tracker.save()
            return redirect('/index')        
    return render(request,'login.html')
    

def register(request):
    if request.method == 'POST':
        username = request.POST["username"];
        email = request.POST["email"];
        password = request.POST["password"];
        password2 = request.POST["password2"];
         
        if(password==password2):
            if User.objects.filter(email = email).exists():
                messages.info(request, 'Email Already Exists')
                return redirect('/register')
            elif User.objects.filter(username=username).exists():
                messages.info(request,'Username Already Exists')
                return redirect('/register')
            else:
                # user = User
                user =User.objects.create_user(username=username,password= password,email=email)
                user.save()
                return redirect('/login')
        else:
            messages.info(request, 'Password does not match')
            return redirect('/register')
    return render(request,'register.html')

def logout(request):    
    time_tracker = TimeTracker.objects.filter(user=request.user, logout_time__isnull=True).order_by('-login_time').first()
    if time_tracker:
        time_tracker.logout_time= datetime.now()
        time_tracker.total_time= current_session
        time_tracker.save()
    auth.logout(request)
    return redirect('/login')     