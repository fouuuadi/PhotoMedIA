# forms.py
from django import forms
from .models import CustomUser

class CustomUserForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput)  # Champ pour le mot de passe

    class Meta:
        model = CustomUser
        fields = ['first_name', 'last_name', 'gender', 'age', 'email', 'password']

    def clean_password(self):
        password = self.cleaned_data.get('password')
        if len(password) < 8:  # Valider que le mot de passe a une longueur minimale de 8 caractères
            raise forms.ValidationError('Le mot de passe doit contenir au moins 8 caractères.')
        return password
