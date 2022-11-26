from django.shortcuts import render, redirect
from django.contrib.auth import logout, authenticate, login as auth_login
from django.contrib import messages
# Create your views here.
def index(request):
    
    if request.method == 'GET':
        if not request.user.is_anonymous:
            return  redirect('home')
        else:
            return render(request,'index.html')
    elif request.method == 'POST':
        email = request.POST.get('email')
        password = request.POST.get('password')
        user = authenticate(request, username=email, password=password)
        if user is not None:
            auth_login(request, user)
            return redirect('home')
        else:
            messages.warning(request, "Usuario Incorrecto")
            return render(request, 'index.html')  

def cerrarSesion(request):
    logout(request)
    return redirect('index')

def home(request):
    if request.method == 'GET':
        if not request.user.is_anonymous:
            return render(request,'home.html')
        else:
            return redirect('index')
        