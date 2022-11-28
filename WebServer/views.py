from django.shortcuts import render, redirect
from django.contrib.auth import logout, authenticate, login as auth_login
from django.contrib import messages
from .models import Sitios, Usuario
from .forms import UserForm
import subprocess
import os
import crypt
import random
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


def sitios(request):
    if request.method == 'GET':
        if not request.user.is_anonymous:
            sitio = Sitios.objects.all()
            return render(request,'sitio.html',{
                'sitios':sitio,
            })
        else:
            return redirect('index')
        

def clientes(request):
    if request.method == 'GET':
        if not request.user.is_anonymous:
            users = Usuario.objects.all()
            return render(request,'cliente.html',{
                'users':users,
            })
    
        else:
            return redirect('index')
        
def agregarCliente(request):
    if request.method == 'GET':
        if not request.user.is_anonymous:
            return render(request,'addCliente.html')
        else:
            return redirect('index')
    elif request.method == 'POST':
        print( request.POST)
        nombreUser = request.POST.get('username')
        salt=getsalt()
        contraseña = request.POST.get('password')
        encPass = crypt.crypt(contraseña,salt)

        form = UserForm(request.POST or None, request.FILES or None)
        if form.is_valid():
            form.save()
            aux = Usuario.objects.filter(username=nombreUser)
            ruta = '/srv/www/htdocs/'+nombreUser
            aux.update(Path = ruta, estado='LIBRE')
            subprocess.call(['useradd', '-d',ruta,'-m', nombreUser,'-p',encPass])
            
            messages.success(request, "CORRECTO")

        else:
            messages.error(request, "ERROR")

        return redirect('clientes')


def agregarSitio(request):
    if request.method == 'GET':
        if not request.user.is_anonymous:
            usuarios = Usuario.objects.filter(estado='LIBRE')
            return render(request,'addSitio.html',{
                'usuarios':usuarios,
            })
        else:
            return redirect('index')
    elif request.method == 'POST':
        print( request.POST)
        nombreSitio = request.POST.get('dominio')
        cliente = request.POST.get('cliente')
        completo = "www."+nombreSitio.lower()+".com"
        aux = Usuario.objects.filter(id = int(cliente))
        aux.update(estado='OCUPADO')
        sit = Sitios(dominio = nombreSitio.lower(), user = aux.first(), completo = completo)
        sit.save()
        #subprocess.call(['useradd', '-d',ruta,'-m', nombreUser,'-p',encPass])
        f = open('/etc/hosts',"a")
        f.write('\n192.168.0.201   '+completo)
        f.close()

        docRoot = "/srv/www/htdocs/"+aux.first().username
        f = open('/etc/apache2/conf.d/vhost.conf',"a")
        f.write('<virtualHost *:80>')
        f.write('\nDocumentRoot "'+docRoot+'"')
        f.write('\nserverName      '+completo)
        f.write('\n</virtualHost>')
        f.close()
        messages.success(request, "CORRECTO")

        return redirect('sitios')

def getsalt(chars = os.times() + os.uname()):
	#Genera 2 caracteres para el SALT, tomando aleatorios de la concatenacion de times+uname
	return str(random.choice(chars)) + str(random.choice(chars))