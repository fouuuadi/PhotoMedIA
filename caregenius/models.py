
# Create your models here.
# caregenius/models.py

from django.db import models

class User(models.Model):
    # Django crée automatiquement un champ id AutoField en tant que PK,
    id = models.AutoField(primary_key=True)
    
    pseudo   = models.CharField(max_length=150)
    password    = models.CharField(max_length=128)
    
    age         = models.IntegerField()
    height      = models.FloatField(help_text="Taille en mètres")
    weight      = models.FloatField(help_text="Poids en kilogrammes")
    gender      = models.CharField(max_length=10, choices=[('M', 'Homme'), ('F', 'Femme'), ('O', 'Autre')], default='M')
    is_pregnant = models.BooleanField(null=True, blank=True, help_text="Applicable uniquement si genre = Femme")
    # pour un texte libre, on utilise TextField
    pathology   = models.TextField(blank=True)

    def __str__(self):
        return self.pseudo