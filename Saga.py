import streamlit as st
import requests

# Clé API pour accéder à l'API The Movie Database (TMDb)
api_key = '6a2a705c0c740a478c412dedfbd387c5'

# Fonction pour rechercher l'ID d'un film en utilisant son titre
def search_movie_id(movie_title):
    # URL de recherche pour l'API TMDb avec le titre du film
    search_url = f"https://api.themoviedb.org/3/search/movie?api_key={api_key}&query={movie_title}"
    response = requests.get(search_url)  # Effectuer la requête GET pour récupérer les résultats
    data = response.json()  # Convertir la réponse JSON en un dictionnaire Python
    
    # Si des résultats sont trouvés, on renvoie l'ID du premier film trouvé
    if data['results']:
        return data['results'][0]['id']
    else:
        return None  # Si aucun film n'est trouvé, on renvoie None

# Fonction pour obtenir les films d'une saga en fonction de l'ID du film
def get_saga_movies(movie_id):
    # URL pour obtenir les détails du film avec l'ID
    url = f"https://api.themoviedb.org/3/movie/{movie_id}?api_key={api_key}"
    response = requests.get(url)  # Effectuer la requête GET pour obtenir les détails du film
    data = response.json()  # Convertir la réponse JSON en un dictionnaire Python
    
    # Vérifier si le film appartient à une collection (saga)
    if 'belongs_to_collection' in data and data['belongs_to_collection']:
        collection_id = data['belongs_to_collection']['id']  # Récupérer l'ID de la collection
        # Obtenir les films de cette collection (saga)
        collection_url = f"https://api.themoviedb.org/3/collection/{collection_id}?api_key={api_key}"
        collection_response = requests.get(collection_url)  # Effectuer la requête GET pour obtenir les films de la collection
        collection_data = collection_response.json()  # Convertir la réponse JSON en un dictionnaire
        
        # Si la collection a des films associés (parties de la saga), les retourner
        if 'parts' in collection_data:
            return collection_data['parts']
    
    return []  # Si le film ne fait pas partie d'une saga, renvoyer une liste vide

# Titre de l'application Streamlit
st.title("Films de la saga d'un film")

# Champ de saisie pour entrer le titre du film
movie_title = st.text_input("Entrez le titre du film:")

# Si un titre de film est entré
if movie_title:
    # Rechercher l'ID du film à partir du titre
    movie_id = search_movie_id(movie_title)
    
    # Si l'ID du film est trouvé
    if movie_id:
        # Obtenir les films de la saga en utilisant l'ID du film
        saga_movies = get_saga_movies(movie_id)
        
        # Si des films de la saga sont trouvés
        if saga_movies:
            st.write(f"Films de la saga de '{movie_title}':")
            # Afficher les titres des films de la saga et leurs dates de sortie
            for movie in saga_movies:
                st.write(f"- {movie['title']} ({movie['release_date']})")
        else:
            st.write(f"'{movie_title}' ne fait pas partie d'une saga ou aucun film lié n'a été trouvé.")
    else:
        st.write(f"Aucun film trouvé avec le titre '{movie_title}'.")
