from . import views
from django.urls import path
from .views import landing

app_name = 'caregenius'

#setup les urls quand va afficher sur le site 
urlpatterns = [
    path("index/", views.index, name="index"),
    path("connection/", views.connection, name="connection"),
    path("inscription/", views.inscription, name="inscription"),
    path("register/", views.register, name="register"),
    #path("dashboard/", views.dashboard, name="dashboard"),
    path("landing/", landing, name="landing")
]
