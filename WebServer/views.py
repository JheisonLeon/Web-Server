from django.shortcuts import render, redirect

# Create your views here.
def index(request):
    """if request.method == 'GET':
        if not request.user.is_anonymous:
            if request.user.email.endswith('@delegacion.com'):
                return redirect('delegacionTorneo')
            elif request.user.email.endswith('@admin.com'):
                return redirect('torneos')
        else:
            torneosProgreso = Torneo.objects.filter(torneo_estado=1)
            aux = []
            for i in range(len(torneosProgreso)):
                aux.append(i+1)
            return render(request, 'index.html', {
                "torneos": torneosProgreso,
                "longitud": aux
            })"""
    if request.method == 'GET':
        return render(request, 'index.html')