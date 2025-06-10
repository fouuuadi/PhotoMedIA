from . import views
from django.urls import path
from .views import landing

app_name = 'caregenius'

#setup les urls quand va afficher sur le site 
urlpatterns = [
    path("index/", views.index, name="index"),
    path("connection/", views.connection, name="connection"),
    # path("inscription/", views.inscription, name="inscription"),
    path("dashboard_medicaments/", views.dashboard_medicaments, name="dashboard_medicaments"),
    path("dashboard_ordonnances/", views.dashboard_ordonnances, name="dashboard_ordonnances"),
    path("dashboard_radiographies/", views.dashboard_radiographies, name="dashboard_radiographies"),
    path("register/", views.register, name="register"),
    path("register/", views.register, name="register"),
    # path('analyse_image/', views.analyse_image, name='analyse_image'),
    path("landing/", landing, name="landing"),
    path('analyse_image_api/', views.analyse_image_api, name='analyse_image_api'),
    path('profil/', views.profil, name='profil'),
    path('profil_update/', views.profil_update, name='profil_update'),

]
