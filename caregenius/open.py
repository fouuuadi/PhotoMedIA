import easyocr
import requests
from PIL import Image
from io import BytesIO
import openai

# === CONFIGURATION ===
OPENAI_API_KEY = "sk-..." 
PROFILE = {
    "sexe": "femme",
    "âge": 65,
    "poids": 60
}
image_url = "https://media.istockphoto.com/id/1199617301/fr/photo/bo%C3%AEte-de-m%C3%A9dicaments-contre-la-douleur-et-la-fi%C3%A8vre-du-parac%C3%A9tamol.jpg?b=1&s=612x612&w=0&k=20&c=oHYwM8TKebAWFp33SLKSL59RFZjWJuQDeyC-WfOrxGo="

# === 1. EXTRACTION DE TEXTE VIA OCR ===
print("\n--- Étape 1 : Extraction de texte ---\n")
image = Image.open(BytesIO(requests.get(image_url).content)).convert("RGB")
image.save("temp.jpg")

reader = easyocr.Reader(['fr']) 
results = reader.readtext("temp.jpg")

# Fusionner tous les morceaux de texte
texte_extrait = "\n".join([text for _, text, _ in results])
print(texte_extrait)

# === 2. INTERPRÉTATION AVEC CHATGPT MEME SI C'EST MELANGE N'IMPORTE COMMENT? ON UTILISE UN MODELE TRES PUISSANT DONC PAS DE PROBLEME ===
# print("\n--- Étape 2 : Envoi à ChatGPT ---\n")
# openai.api_key = OPENAI_API_KEY

# prompt = f"""
# Voici le texte extrait d'un emballage ou d'une notice de médicament :

# {texte_extrait}

# Sachant que le patient est une {PROFILE['sexe']} de {PROFILE['âge']} ans, pesant {PROFILE['poids']} kg :

# - Résume les informations importantes.
# - Mentionne les contre-indications potentielles ou précautions.
# - Donne un avis général utile.
# """

# response = openai.ChatCompletion.create(
#     model="gpt-4",
#     messages=[
#         {"role": "system", "content": "Tu es un assistant médical très précis."},
#         {"role": "user", "content": prompt}
#     ],
#     temperature=0.7
# )

# print("\n--- Réponse de ChatGPT ---\n")
# print(response['choices'][0]['message']['content'])
