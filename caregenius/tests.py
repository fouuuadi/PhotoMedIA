from django.test import TestCase
from django.urls import reverse
from .models import User
from django.contrib.auth.hashers import make_password
from django.core.files.uploadedfile import SimpleUploadedFile


class ConnectionViewTests(TestCase):
    def setUp(self):
        self.user = User.objects.create(
            pseudo="testuser",
            password=make_password("password123"),
            gender='Male',
            age=30,
            height=170,
            weight=70,
            pathology="none",
            is_pregnant=False
        )

    def test_valid_connection(self):
        response = self.client.post(reverse('caregenius:connection'), {
            'pseudo': 'testuser',
            'password': 'password123'
        })
        self.assertRedirects(response, reverse('caregenius:dashboard_medicaments'))

    def test_invalid_connection(self):
        response = self.client.post(reverse('caregenius:connection'), {
            'pseudo': 'testuser',
            'password': 'wrongpassword'
        })
        self.assertContains(response, 'Mot de passe incorrect.')


class RegisterViewTests(TestCase):
    def test_valid_registration(self):
        response = self.client.post(reverse('caregenius:register'), {
            'pseudo': 'newuser',
            'password': 'password123',
            'Cpassword': 'password123',
            'gender': 'male',
            'age': 25,
            'height': 180,
            'weight': 75,
            'pathology': 'none',
            'pregnant': 'no'
        })
        self.assertRedirects(response, reverse('caregenius:connection'))
        self.assertTrue(User.objects.filter(pseudo='newuser').exists())

    def test_password_mismatch(self):
        response = self.client.post(reverse('caregenius:register'), {
            'pseudo': 'newuser',
            'password': 'password123',
            'Cpassword': 'wrongpassword'
        })
        self.assertContains(response, 'Les mots de passe ne correspondent pas.')

    def test_duplicate_pseudo(self):
        user = User.objects.create(
            pseudo='existinguser',
            password=make_password("password123"),
            gender="Male",
            age=30,
            height=170,
            weight=70,
            pathology="none",
            is_pregnant=False
        )
        response = self.client.post(reverse('caregenius:register'), {
            'pseudo': 'existinguser',
            'password': 'password123',
            'Cpassword': 'password123'
        })
        self.assertContains(response, 'Un compte avec ce pseudo existe déjà.')



class UserModelTests(TestCase):
    def test_user_creation(self):
        user = User.objects.create(
            pseudo="testuser",
            password=make_password("password123"),
            gender="male",
            age=25,
            height=180,
            weight=75,
            pathology="none",
            is_pregnant=False
        )
        self.assertEqual(user.pseudo, "testuser")


class ProtectedViewTests(TestCase):
    def test_redirect_if_not_logged_in(self):
        response = self.client.get(reverse('caregenius:dashboard_medicaments'))
        self.assertRedirects(response, reverse('caregenius:connection'))
