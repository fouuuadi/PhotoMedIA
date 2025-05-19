import easyocr
import openai
from PIL import Image
from io import BytesIO

openai.api_key = "sk-..."  

def analyser_image_medicament(image_file, sexe, age, poids):
    # === 1. OCR avec EasyOCR ===
    reader = easyocr.Reader(['fr'], gpu=False)
    image = Image.open(image_file).convert("RGB")
    image.save("temp.jpg")  # Optionnel : pour debug ou log

    results = reader.readtext("temp.jpg")
    texte_extrait = "\n".join([text for _, text, _ in results]).strip()

    if not texte_extrait:
        return "Aucun texte n'a été détecté sur l'image. Veuillez prendre une autre photo."

    # === 2. Interprétation médicale avec OpenAI ===
    prompt = f"""
Voici le texte extrait d'un emballage ou d'une notice de médicament :

{texte_extrait}

Sachant que le patient est une {sexe} de {age} ans, pesant {poids} kg :

- Résume les informations importantes.
- Mentionne les contre-indications potentielles ou précautions.
- Donne un avis général utile.
Si le contenu n'est pas médical ou semble sans rapport, réponds simplement : "Veuillez prendre une autre photo."
"""

    try:
        response = openai.ChatCompletion.create(
            model="gpt-4",
            messages=[
                {"role": "system", "content": "Tu es un assistant médical très précis."},
                {"role": "user", "content": prompt}
            ],
            temperature=0.5
        )

        output = response['choices'][0]['message']['content'].strip()
        return output

    except Exception as e:
        return f"Une erreur est survenue lors de l'analyse : {str(e)}"
