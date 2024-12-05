# Importation des bibliothèques nécessaires
import streamlit as st  # Utilisé pour créer l'interface web avec Streamlit
import requests  # Utilisé pour envoyer des requêtes HTTP à l'API

# Clé API pour accéder à l'API de The Movie Database (TMDb)
api_key = '6a2a705c0c740a478c412dedfbd387c5'

# Fonction pour rechercher l'ID d'un film à partir de son titre
def search_movie_id(movie_title):
    # Construction de l'URL de recherche de film
    search_url = f"https://api.themoviedb.org/3/search/movie?api_key={api_key}&query={movie_title}"
    
    # Envoi de la requête à l'API et récupération de la réponse
    response = requests.get(search_url)
    data = response.json()  # Conversion de la réponse en format JSON
    
    # Vérification si des résultats ont été trouvés
    if data['results']:
        # Retourner l'ID du premier film trouvé
        return data['results'][0]['id']
    else:
        # Aucun film trouvé, retourner None
        return None

# Fonction pour obtenir le budget et les recettes d'un film en utilisant son ID
def get_budget_and_revenue(movie_id):
    # Construction de l'URL pour récupérer les détails du film
    url = f"https://api.themoviedb.org/3/movie/{movie_id}?api_key={api_key}"
    
    # Envoi de la requête à l'API et récupération de la réponse
    response = requests.get(url)
    data = response.json()  # Conversion de la réponse en format JSON
    
    # Récupération du budget et des recettes, avec des valeurs par défaut si non disponibles
    budget = data.get('budget', 0)  # Si 'budget' est absent, retourner 0
    revenue = data.get('revenue', 0)  # Si 'revenue' est absent, retourner 0
    
    # Formatage du budget et des recettes pour les afficher en millions de dollars
    budget_formatted = f"${budget / 1_000_000:.2f} million" if budget > 0 else "Non disponible"
    revenue_formatted = f"${revenue / 1_000_000:.2f} million" if revenue > 0 else "Non disponible"
    
    # Retourner le budget et les recettes formatés
    return budget_formatted, revenue_formatted

# Titre de l'application Streamlit
st.title("Coût et recettes d'un film")

# Entrée de texte pour que l'utilisateur entre le titre du film
movie_title = st.text_input("Entrez le titre du film:")

# Vérification si l'utilisateur a entré un titre
if movie_title:
    # Recherche de l'ID du film en utilisant le titre
    movie_id = search_movie_id(movie_title)
    
    # Si un ID de film a été trouvé
    if movie_id:
        # Récupération du budget et des recettes pour ce film
        budget, revenue = get_budget_and_revenue(movie_id)
        
        # Affichage des informations de budget et de recettes
        st.write(f"**Budget** : {budget}")
        st.write(f"**Recettes** : {revenue}")
    else:
        # Si aucun film n'est trouvé, afficher un message d'erreur
        st.write(f"Aucun film trouvé avec le titre '{movie_title}'.")
