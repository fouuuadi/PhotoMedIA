import os
from openai import OpenAI
from dotenv import load_dotenv
import easyocr
from PIL import Image
import numpy as np
from io import BytesIO
import requests

# Chargement de la clé API depuis le fichier .env
load_dotenv()
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

def analyser_image(image_file, sexe, age, poids, taille, pathologies, grossesse):
    # === 1. OCR avec EasyOCR ===
    reader = easyocr.Reader(['fr'], gpu=False)

    # Chargement de l'image locale ou distante
    if isinstance(image_file, str) and image_file.startswith("http"):
        response = requests.get(image_file)
        image = Image.open(BytesIO(response.content)).convert("RGB")
    else:
        image = Image.open(image_file).convert("RGB")

    image_np = np.array(image)
    results = reader.readtext(image_np)
    texte_extrait = "\n".join([text for _, text, _ in results]).strip()

    if not texte_extrait:
        return "Aucun texte n'a été détecté sur l'image. Veuillez prendre une autre photo."

    print("Texte extrait :\n", texte_extrait)

    # === 2. Interprétation médicale avec OpenAI ===
    prompt = f"""
Voici le texte extrait d'une ordonnance ou d'une notice de médicament :

{texte_extrait}

Sachant que le patient est une {sexe} de {age} ans de taille {taille} cm, pesant {poids} kg avec les pathologies suivantes : {pathologies} et est {'enceinte' if grossesse else 'non enceinte'} et qu 'il peut avoir des erreurs dans le texte extrait mais que tu dois te concentrer sur les informations médicales pertinentes.

- Résume les informations importantes.
- Mentionne les contre-indications potentielles ou précautions.
- Donne un avis général utile.
Si le contenu n'est pas médical ou semble sans rapport, réponds simplement : "Veuillez prendre une autre photo.". suivi de pourquoi il faut prendre une autre photo. est ce une erreur de l'utilisateur ou une erreur de l'api.
"""

    try:
        response = client.chat.completions.create(
            model="gpt-4o",
            messages=[
                {"role": "system", "content": "Tu es un assistant médical très précis. Il peut y avoir des erreurs dans le texte extrait, mais tu dois te concentrer sur les informations médicales pertinentes."},
                {"role": "user", "content": prompt}
            ],
            temperature=0.5
        )
        print("Réponse de l'API :\n", response.choices[0].message.content.strip())
        return response.choices[0].message.content.strip()
    

    except Exception as e:
        return f"Une erreur est survenue lors de l'analyse : {str(e)}"

# Test
if __name__ == "__main__":
    result = analyser_image(
        "C:/Users/modes/Downloads/doliprane.jpg",  
        "femme", 30, 65,171, "hypertension", False
    )
    print("\nRésultat de l'analyse :\n", result)
