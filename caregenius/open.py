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

<div class="patient-data">
    <h2 class="section-title">👤 Données patient</h2>
    <ul class="patient-info">
        <li><strong>Sexe :</strong> {sexe}</li>
        <li><strong>Âge :</strong> {age} ans</li>
        <li><strong>Taille :</strong> {taille} cm</li>
        <li><strong>Poids :</strong> {poids} kg</li>
        <li><strong>Pathologies connues :</strong> {pathologies}</li>
        <li><strong>Enceinte :</strong> {"Oui" if grossesse else "Non"}</li>
    </ul>
</div>

<div class="analysis-instructions">
    <h2 class="section-title">🔎 Ta mission</h2>
    <p>En tant qu’assistant médical, analyse le texte ci-dessus et produis un compte-rendu clair, structuré et pertinent en HTML. Le compte-rendu doit être utile pour un professionnel de santé ou un patient cherchant à comprendre les informations médicales contenues dans le texte. Le texte peut contenir des erreurs d'OCR, mais concentre-toi sur les informations médicales pertinentes.</p>
</div>

<div class="analysis-structure">
    <h3 class="subsection-title">Voici les éléments à inclure dans le rendu HTML :</h3>
    <ol class="analysis-list">
        <li>Une section avec les <strong>molécules ou médicaments identifiés</strong> (nom et classe si possible).</li>
        <li>Une section pour la <strong>posologie recommandée</strong> (si identifiable).</li>
        <li>Une section pour les <strong>indications possibles</strong> (raisons pour lesquelles ce traitement peut être prescrit).</li>
        <li>Une section pour les <strong>contre-indications ou précautions</strong> selon les données patient.</li>
        <li>Une section pour les <strong>effets secondaires courants</strong>.</li>
        <li>Une section pour un <strong>avis global ou des recommandations</strong>.</li>
    </ol>
</div>

<div class="error-handling">
    <h3 class="subsection-title">Si le texte ne semble pas médical ou est trop brouillon :</h3>
    <ul class="error-list">
        <li>Répond avec un message HTML clair indiquant : "Veuillez prendre une autre photo."</li>
        <li>Explique clairement si l’erreur vient de la photo ou de l’analyse OCR/API.</li>
    </ul>
</div>

<p class="note">Structure le HTML avec des balises comme <code>&lt;h2&gt;</code>, <code>&lt;p&gt;</code>, <code>&lt;ul&gt;</code>, <code>&lt;li&gt;</code>, etc., pour que le rendu soit clair et bien organisé. Ajoute des classes CSS aux balises pour permettre un stylage ultérieur (par exemple, <code>class="section-title"</code> pour les titres).</p>

<p class="final-note">Sois clair, précis et amical.</p>
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
