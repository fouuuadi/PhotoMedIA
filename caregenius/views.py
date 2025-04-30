from django.shortcuts import render
from django.http import HttpResponse

# Create your views here.
def index(request):
    
    # Django va chercher Hello.html dans caregenius/templates/caregenius/
    #return HttpResponse('Hello')
    return render(request, 'caregenius/index.html')

def landing(request):
    # rend le template landing.html
    return render(request, 'caregenius/landing.html')
