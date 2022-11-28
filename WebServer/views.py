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
        complemento = request.POST.get('subdominio')
        cliente = request.POST.get('cliente')
        completo = "www."+nombreSitio.lower()+complemento
        aux = Usuario.objects.filter(id = int(cliente))
        aux.update(estado='OCUPADO')
        sit = Sitios(dominio = nombreSitio.lower(), user = aux.first(), completo = completo)
        sit.save()
        #subprocess.call(['useradd', '-d',ruta,'-m', nombreUser,'-p',encPass])
        f = open('/etc/hosts',"a")
        f.write('\n192.168.0.201   '+completo)
        f.close()

        docRoot = "/srv/www/htdocs/"+aux.first().username
        g = open('/etc/apache2/conf.d/vhost.conf',"a")
        g.write('\n<virtualHost *:80>')
        g.write('\nDocumentRoot "'+docRoot+'"')
        g.write('\nserverName      '+completo)
        g.write('\n</virtualHost>')
        g.close()

        subprocess.call(['touch', docRoot+'/index.html'])
        h = open(docRoot+'/index.html',"a")
        h.write('\nPAGINA CORRESPONDIENTE A'+aux.first().username)
        h.close()

        subdominio = complemento
        i = open('/etc/named.conf',"a")
        i.write('\nzone "'+nombreSitio.lower()+subdominio+'" in {')
        i.write('\n\tallow-transfer {any;};')
        i.write('\n\tfile "master/'+nombreSitio.lower()+subdominio+'";')
        i.write('\n\ttype master;')
        i.write('\n};')
        i.close()

        subprocess.call(['touch', '/var/lib/named/master/'+nombreSitio.lower()+subdominio])
        k = open('/var/lib/named/master/'+nombreSitio.lower()+subdominio,"a")
        k.write('\n$TTL 2d')
        k.write('\n@               IN SOA          VM2ASO. root.VM2ASO. (')
        k.write('\n                       2022111100      ;serial')
        k.write('\n                       3h      ;refresh')
        k.write('\n                       1h      ;retry')
        k.write('\n                       1w      ;expiry')
        k.write('\n                       1d)     ;minimum')
        k.write('\n'+nombreSitio.lower()+subdominio+'. IN NS      ns.'+nombreSitio.lower()+subdominio+'.')
        k.write('\nns.'+nombreSitio.lower()+subdominio+'.   IN A      192.168.0.201')
        k.write('\nwww      IN CNAME    ns.'+nombreSitio.lower()+subdominio+'.')
        k.close()

        j = open('/var/lib/named/master/0.168.192.in-addr.arpa',"a")
        j.write('\n0.168.192.in-addr.arpa. IN NS        ns.'+nombreSitio.lower()+subdominio+'.')
        j.write('\n201      IN PTR      ns.'+nombreSitio.lower()+subdominio+'.')
        j.close()
        subprocess.call(['systemctl', 'restart','apache2'])
        subprocess.call(['service', 'named','restart'])
        messages.success(request, "CORRECTO")

        return redirect('sitios')

def getsalt(chars = os.times() + os.uname()):
	#Genera 2 caracteres para el SALT, tomando aleatorios de la concatenacion de times+uname
	return str(random.choice(chars)) + str(random.choice(chars))