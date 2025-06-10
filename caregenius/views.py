from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.http import JsonResponse
from django.contrib.auth.hashers import make_password, check_password
from django.contrib import messages
from .models import User
from .open import analyser_image

# Create your views here.
def index(request):
    
    # Django va chercher Hello.html dans caregenius/templates/caregenius/
    #return HttpResponse('Hello')
    return render(request, 'caregenius/index.html')


def connection(request):
    if request.method == 'POST':
        pseudo_user = request.POST.get('pseudo')
        password = request.POST.get('password')

        try:
            user = User.objects.get(pseudo=pseudo_user)
            
            if check_password(password, user.password):
                # 🔐 Stocker l'identifiant dans la session
                request.session['user_id'] = user.id

                messages.success(request, 'Connexion réussie !')
                return redirect('caregenius:dashboard_medicaments')# proprement vers la page d'accueil
            else:
                messages.error(request, 'Mot de passe incorrect.')
        except User.DoesNotExist:
            messages.error(request, 'Utilisateur non trouvé.')

    return render(request, 'caregenius/connection.html')

def register(request):
    if request.method == 'POST':
        print("Formulaire soumis")
        pseudo = request.POST.get('pseudo')
        password = request.POST.get('password')
        confirm_password = request.POST.get('Cpassword')
        gender = request.POST.get('gender')
        age = request.POST.get('age')
        height = request.POST.get('height')
        weight = request.POST.get('weight')
        pathology = request.POST.get('pathology')
        pregnant = request.POST.get('pregnant')
        if pregnant == 'yes':
            is_pregnant = True
        elif pregnant == 'no':
            is_pregnant = False
        else:
            is_pregnant = None

        if password != confirm_password:
            messages.error(request, 'Les mots de passe ne correspondent pas.')
            return render(request, 'caregenius/register.html')

        if User.objects.filter(pseudo=pseudo).exists():
            messages.error(request, 'Un compte avec ce pseudo existe déjà.')
            return render(request, 'caregenius/register.html')

        hashed_password = make_password(password)
        try:
            User.objects.create(
                pseudo=pseudo,
                password=hashed_password,
                age=age,
                height=height,
                weight=weight,
                pathology=pathology,
                gender=gender,
                is_pregnant=is_pregnant
            )
            messages.success(request, 'Inscription réussie !')
            return redirect('caregenius:connection')  # redirection ici
        except Exception as e:
            messages.error(request, f'Erreur lors de l\'inscription : {str(e)}')
            return render(request, 'caregenius/register.html')

    return render(request, 'caregenius/register.html')

def landing(request):
    # rend le template landing.html
    return render(request, 'caregenius/landing.html')

def dashboard_medicaments(request):
    # Vérifie si l'utilisateur est connecté
    # if 'user_id' not in request.session:
    #     return redirect('caregenius:connection')
    # rend le template dashboard.html
    return render(request, 'caregenius/dashboard_medicaments.html')

def dashboard_ordonnances(request):
    # Vérifie si l'utilisateur est connecté
    if 'user_id' not in request.session:
        return redirect('caregenius:connection')
    # rend le template dashboard.html
    return render(request, 'caregenius/dashboard_ordonnances.html')

def dashboard_radiographies(request):
    # Vérifie si l'utilisateur est connecté
    if 'user_id' not in request.session:
        return redirect('caregenius:connection')
    # rend le template dashboard.html
    return render(request, 'caregenius/dashboard_radiographies.html')


# def register(request):
#     # rend le template register.html
#     return render(request, 'caregenius/register.html')

#analyse l'image et renvoie le résultat
# def analyse_image(request):
#     # Vérifie si l'utilisateur est connecté
#     if 'user_id' not in request.session:
#         return redirect('caregenius:connection')

#     user_id = request.session['user_id']
#     user = User.objects.get(id=user_id)

#     if request.method == 'POST' and request.FILES.get('image'):
#         image_file = request.FILES.get('image')
#         print("Image reçue :", image_file.name)
#         resultat = analyser_image(
#             image_file,
#             user.gender,
#             user.age,
#             user.weight,
#             user.height,
#             user.pathology,
#             user.is_pregnant
#         )
#         # Récupérer le texte extrait et le résultat de l'analyse et l'envoyer au template
#         return render(request, 'caregenius/dashboard_medicaments.html', {
#             'result': resultat
#         })

def analyse_image_api(request):
    if request.method == 'POST' and request.FILES.get('image'):
        # Récupère l'utilisateur comme dans ta fonction existante
        user_id = request.session.get('user_id')
        if not user_id:
            return JsonResponse({'error': 'Non authentifié'}, status=401)
        user = User.objects.get(id=user_id)

        image_file = request.FILES.get('image')
        resultat = analyser_image(
            image_file,
            user.gender,
            user.age,
            user.weight,
            user.height,
            user.pathology,
            user.is_pregnant
        )
        return JsonResponse({'result': resultat})
    return JsonResponse({'error': 'Requête invalide'}, status=400)

#envoi des informations de l'utilisateur à la page dashboard
def profil(request):
    # Vérifie si l'utilisateur est connecté
    if 'user_id' not in request.session:
        return redirect('caregenius:connection')

    user_id = request.session['user_id']
    user = User.objects.get(id=user_id)

    # Récupère les informations de l'utilisateur
    context = {
        'pseudo': user.pseudo,
        'height': user.height,
        'weight': user.weight,
        'pathology': user.pathology,
        'gender': user.gender
    }
    # Rendre le template dashboard.html avec les informations de l'utilisateur  
    return render(request, 'caregenius/profil.html', context)

def profil_update(request):
    # Vérifie si l'utilisateur est connecté
    if 'user_id' not in request.session:
        return redirect('caregenius:connection')

    user_id = request.session['user_id']
    user = User.objects.get(id=user_id)

    if request.method == 'POST':
        # Met à jour les informations de l'utilisateur
        user.pseudo = request.POST.get('pseudo')
        user.height = request.POST.get('height')
        user.weight = request.POST.get('weight')
        user.pathology = request.POST.get('pathology')
        user.gender = request.POST.get('gender')
        user.save()

        messages.success(request, 'Vos informations ont été mises à jour avec succès !')

    # Récupère les informations de l'utilisateur
    context = {
        'pseudo': user.pseudo,
        'height': user.height,
        'weight': user.weight,
        'pathology': user.pathology,
        'gender': user.gender
    }
    # Rendre le template dashboard.html avec les informations de l'utilisateur  
    return render(request, 'caregenius/profil.html', context)

def logout(request):
    # Supprime l'identifiant de l'utilisateur de la session
    if 'user_id' in request.session:
        del request.session['user_id']
        messages.success(request, 'Déconnexion réussie !')
    else:
        messages.error(request, 'Vous n\'êtes pas connecté.')

    # Redirige vers la page de connexion
    return redirect('caregenius:connection')