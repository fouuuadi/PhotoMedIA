# 📸 PhotoMedIA

**PhotoMedIA** est une plateforme intelligente permettant d'obtenir des informations sur un médicament ou une ordonnance en téléversant simplement une photo. Basée sur Django et conteneurisée avec Docker, l'application utilise des services modernes pour l'analyse d'image et l'extraction de données médicales.

---

## 🚀 Fonctionnalités

* 📸 Téléversement d'images d'ordonnances ou de médicaments
* 🧠 Extraction intelligente d'informations via traitement d'image / OCR
* 💊 Détection automatique des noms de médicaments, posologies, etc.
* 🔐 Authentification utilisateur


---

## 🐳 Déploiement avec Docker

### 1. Prérequis

* [Docker](https://www.docker.com/)
* [Docker Compose](https://docs.docker.com/compose/)
* Un fichier `.env` avec les variables d’environnement

### 2. Cloner le projet

```bash
git clone https://github.com/fouuuadi/PhotoMedIA.git
cd photomedia
```

### 3. Créer un fichier `.env`

```env
DJANGO_SECRET_KEY=changeme
DEBUG=True
ALLOWED_HOSTS=localhost,127.0.0.1
SUPABASE_DATABASE_URL=postgres://USER:PASSWORD@HOST:PORT/DBNAME
OPENAI_API_KEY=sk.........
```

### 4. Démarrer le projet

```bash
docker compose up --build
```

L’application sera disponible sur : [http://localhost:8000/caregenius/landing](http://localhost:8000/caregenius/landing)

---

## 📁 Structure du projet

```
photomedia/
├── manage.py
├── photomedia/           
├── caregenius/            
├── Dockerfile
├── docker-compose.yml
└── requirements.txt
└── deploiementDocker/

```

---

## 📦 Intégration continue (CI/CD)

Le projet utilise **GitHub Actions** pour automatiser :

* ✅ Lancement des tests Django
* 🐳 Construction & push de l'image Docker sur DockerHub si tests réussis

```yaml
name: Build and Push to DockerHub
on:
  workflow_run:
    workflows: ["Django Tests"]
    types: [completed]
```

---

## ✅ Tests unitaires

Les tests vérifient les modèles, vues, URLs:

```bash
docker compose run web python manage.py test
```

---

## 🐳 Image DockerHub

Disponible ici :
[https://hub.docker.com/r/modestin/caregenius](https://hub.docker.com/r/modestin/caregenius)


```bash
cd deploiementDocker
```
```bash
docker compose up --build
```
---

## 🧩 Technologies utilisées

* Django 5.2
* PostgreSQL (via Supabase)
* Docker & Docker Compose
* GitHub Actions CI/CD
* OCR/PyTesseract et OpenAI

---

## 👤 Auteurs

Projet conçu et maintenu par :

- Linkedin [Lissanou Modestin HOUNGA](https://www.linkedin.com/in/modestin/)
- Linkedin [LAMNAOUAR Fouad](https://www.linkedin.com/in/fouad-lamnaouar-196019234/)
- Github [ABBES Amine](https://github.com/ABBESAmine)

---

## 📝 Licence

Gratuit.
