from . import views
from django.urls import path

#setup les urls quand va afficher sur le site 
urlpatterns = [
    path("index/", views.index, name="index")
]
