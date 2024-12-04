import streamlit as st
import base64
from pathlib import Path

# Définir la configuration de la page en tout premier
st.set_page_config(
    page_title="Application personnalisée",
    page_icon="🌟",
    layout="wide",
    initial_sidebar_state="collapsed",  # La barre latérale est réduite au début
)

# Fonction pour charger une image en base64
def load_image_as_base64(file_path):
    with open(file_path, "rb") as image_file:
        return base64.b64encode(image_file.read()).decode()

# Chargement de l'image de fond (doit être dans le même dossier que le script)
current_directory = Path(__file__).parent  # Chemin relatif au script
background_image_path = current_directory / "image_de_fond.jpg"  # Nom de l'image
background_image_base64 = load_image_as_base64(background_image_path)

# CSS pour l'image de fond et les styles personnalisés
page_css = f"""
<style>
    /* Arrière-plan de la page principale */
    .stApp {{
        background-image: url("data:image/jpeg;base64,{background_image_base64}");
        background-size: cover;
        background-position: center;
        background-repeat: no-repeat;
    }}
    /* Style du titre (h1) avec contour externe noir */
    h1 {{
        font-family: 'Arial', sans-serif;
        font-size: 4em;
        color: white;
        text-shadow: 
            3px 3px 0 black, 
            -3px -3px 0 black, 
            -3px 3px 0 black, 
            3px -3px 0 black, 
            3px 0 0 black, 
            -3px 0 0 black, 
            0 3px 0 black, 
            0 -3px 0 black;
    }}
    /* Style du texte classique avec contour externe noir */
    .stMarkdown p {{
        font-family: 'Arial', sans-serif;
        font-size: 1.8em;
        color: white;
        text-shadow: 
            2px 2px 0 black, 
            -2px -2px 0 black, 
            -2px 2px 0 black, 
            2px -2px 0 black, 
            2px 0 0 black, 
            -2px 0 0 black, 
            0 2px 0 black, 
            0 -2px 0 black;
    }}
</style>
"""

# Application des styles personnalisés à la page principale
st.markdown(page_css, unsafe_allow_html=True)

# Changer le thème global
st.markdown("""
    <style>
        /* Changer la couleur du texte de la barre latérale */
        .css-1d391kg a {
            color: white;
        }

        /* Ajouter des bordures autour de la barre latérale */
        .css-1d391kg {
            border: 2px solid white;
        }

        /* Mettre en haut la barre latérale comme un menu en haut (ça ne peut pas être fait directement via CSS, il faut une solution différente dans Streamlit) */
    </style>
""", unsafe_allow_html=True)

# Titre principal de la page
st.title("Bienvenue !")

# Message explicatif
st.write("Choisissez une page dans la barre latérale.")
