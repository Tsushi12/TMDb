import streamlit as st  # Importation de Streamlit pour créer une interface web interactive
import requests  # Importation de la bibliothèque requests pour effectuer des requêtes HTTP

# Clé API pour accéder à l'API de TheMovieDB
api_key = '6a2a705c0c740a478c412dedfbd387c5'

# Fonction qui recherche l'ID d'un film à partir de son titre
def search_movie_id(movie_title):
    # URL de l'API pour rechercher un film par son titre
    search_url = f"https://api.themoviedb.org/3/search/movie?api_key={api_key}&query={movie_title}"
    response = requests.get(search_url)  # Requête HTTP GET pour obtenir la réponse
    data = response.json()  # Conversion de la réponse JSON en dictionnaire Python
    
    # Vérification si des résultats sont renvoyés par l'API
    if data['results']:
        return data['results'][0]['id']  # Retourne l'ID du premier film trouvé
    else:
        return None  # Retourne None si aucun film n'a été trouvé

# Fonction qui récupère les sociétés de production d'un film à partir de son ID
def get_production_companies(movie_id):
    # URL de l'API pour récupérer les détails d'un film à partir de son ID
    url = f"https://api.themoviedb.org/3/movie/{movie_id}?api_key={api_key}"
    response = requests.get(url)  # Requête HTTP GET pour obtenir la réponse
    data = response.json()  # Conversion de la réponse JSON en dictionnaire Python
    
    # Vérification si la clé 'production_companies' existe dans les données retournées
    if 'production_companies' in data:
        return data['production_companies']  # Retourne la liste des sociétés de production
    else:
        return []  # Retourne une liste vide si aucune société de production n'est trouvée

# Titre de la page Streamlit
st.title("Liste des sociétés de production d'un film")

# Champ de saisie pour entrer le titre du film
movie_title = st.text_input("Entrez le titre du film:")

# Si un titre de film est saisi, on exécute le processus
if movie_title:
    # Recherche de l'ID du film à partir du titre
    movie_id = search_movie_id(movie_title)
    
    # Si un ID de film est trouvé
    if movie_id:
        # Récupération des sociétés de production du film
        production_companies = get_production_companies(movie_id)
        
        # Si des sociétés de production sont trouvées, on les affiche
        if production_companies:
            st.write(f"Sociétés de production de '{movie_title}':")
            for company in production_companies:  # On parcourt la liste des sociétés de production
                st.write(f"- {company['name']}")  # Affichage du nom de chaque société
        else:
            st.write(f"Aucune société de production trouvée pour '{movie_title}'.")  # Message si aucune société n'est trouvée
    else:
        st.write(f"Aucun film trouvé avec le titre '{movie_title}'.")  # Message si le film n'est pas trouvé
