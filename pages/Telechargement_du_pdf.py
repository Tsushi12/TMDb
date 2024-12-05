import streamlit as st

# Titre de la page
st.title("Téléchargement du fichier PDF")

# Chemin vers le fichier PDF
file_path = "TMDb_Streamlit__EL_BOUFFI__SAMBIANI.pdf"

# Lecture du fichier en mode binaire
try:
    with open(file_path, "rb") as file:
        file_data = file.read()
    
    # Bouton de téléchargement
    st.download_button(
        label="Télécharger le fichier PDF 📄",
        data=file_data,
        file_name="TMDb_Streamlit__EL_BOUFFI__SAMBIANI.pdf",
        mime="application/pdf"
    )
except FileNotFoundError:
    st.error("Le fichier PDF n'a pas été trouvé. Assurez-vous qu'il est bien placé à la racine du projet.")
