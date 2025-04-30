# caregenius/models.py

from django.db import models

class User(models.Model):
    # Django crée automatiquement un champ id AutoField en tant que PK,
    # mais tu peux le redéfinir explicitement si tu veux contrôler son nom ou son type :
    id = models.AutoField(primary_key=True)
    
    first_name  = models.CharField(max_length=150)
    last_name   = models.CharField(max_length=150)
    email_user  = models.EmailField(unique=True)
    password    = models.CharField(max_length=128)
    
    age         = models.IntegerField()
    height      = models.FloatField(help_text="Taille en mètres")
    weight      = models.FloatField(help_text="Poids en kilogrammes")
    
    # pour un texte libre, on utilise TextField
    pathology   = models.TextField(blank=True)

    def __str__(self):
        return f"{self.first_name} {self.last_name}"
