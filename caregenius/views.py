from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.contrib.auth.hashers import make_password, check_password
from django.contrib import messages
from .models import User

# Create your views here.
def index(request):
    
    # Django va chercher Hello.html dans caregenius/templates/caregenius/
    #return HttpResponse('Hello')
    return render(request, 'caregenius/index.html')


def connection(request):
    if request.method == 'POST':
        email_user = request.POST.get('email')
        password = request.POST.get('password')

        try:
            user = User.objects.get(email_user=email_user)
            
            if check_password(password, user.password):
                # 🔐 Stocker l'identifiant dans la session
                request.session['user_id'] = user.id
                request.session['email_user'] = user.email_user  # optionnel

                messages.success(request, 'Connexion réussie !')
                return redirect('caregenius:landing')# proprement vers la page d'accueil
            else:
                messages.error(request, 'Mot de passe incorrect.')
        except User.DoesNotExist:
            messages.error(request, 'Utilisateur non trouvé.')

    return render(request, 'caregenius/connection.html')

def register(request):
    if request.method == 'POST':
        # Récupérer les données du formulaire
        first_name = request.POST.get('first_name')
        last_name = request.POST.get('last_name')
        email_user = request.POST.get('email')
        password = request.POST.get('password')
        gender = request.POST.get('gender')
        age = request.POST.get('age')
        height = request.POST.get('height')
        weight = request.POST.get('weight') 
        pathology = "none"  
        confirm_password = request.POST.get('Cpassword') 
        # Hachage du mot de passe
        if password != confirm_password:
            # Gérer l'erreur de confirmation de mot de passe
            messages.error(request, 'Les mots de passe ne correspondent pas.')
            return render(request, 'caregenius/register.html', {'error': 'Les mots de passe ne correspondent pas.'})
        hashed_password = make_password(password)
        # Enregistrement dans la base de données
        try:
            User.objects.create(
                    first_name=first_name,
                    last_name=last_name,
                    email_user=email_user,
                    password=make_password(password),
                    age=age,
                    height=height,
                    weight=weight,
                    pathology=pathology
                )
            messages.success(request, 'Inscription réussie !')
        except Exception as e:
            # Gérer l'erreur d'insertion
            messages.error(request, f'Erreur lors de l\'inscription : {str(e)}')
            return render(request, 'caregenius/register.html', {'error': str(e)})
        # Logique pour gérer l'inscription
    
    # Django va chercher Hello.html dans caregenius/templates/caregenius/
    #return HttpResponse('Hello')
    return render(request, 'caregenius/register.html')

def landing(request):
    # rend le template landing.html
    return render(request, 'caregenius/landing.html')

def register(request):
    # rend le template register.html
    return render(request, 'caregenius/register.html')
