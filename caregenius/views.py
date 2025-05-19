from django.shortcuts import render
from django.http import HttpResponse

# Create your views here.
def index(request):
    
    # Django va chercher Hello.html dans caregenius/templates/caregenius/
    #return HttpResponse('Hello')
    return render(request, 'caregenius/index.html')


def connection(request):
    
    # Django va chercher Hello.html dans caregenius/templates/caregenius/
    #return HttpResponse('Hello')
    return render(request, 'caregenius/connection.html')

def inscription(request):
    
    # Django va chercher Hello.html dans caregenius/templates/caregenius/
    #return HttpResponse('Hello')
    return render(request, 'caregenius/inscription.html')

def landing(request):
    # rend le template landing.html
    return render(request, 'caregenius/landing.html')

def register(request):
    # rend le template landing.html
    return render(request, 'caregenius/register.html')
