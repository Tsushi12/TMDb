import requests
import streamlit as st
import matplotlib.pyplot as plt

# Clé API pour accéder à l'API The Movie Database (TMDb)
api_key = '6a2a705c0c740a478c412dedfbd387c5'

# Liste des films sélectionnés
selected_movies = [
    "Iron Man", "The Incredible Hulk", "Iron Man 2", "Thor", 
    "Captain America: The First Avenger", "The Avengers",
    "Iron Man 3", "Thor: The Dark World", "Captain America: The Winter Soldier", 
    "Guardians of the Galaxy", "Avengers: Age of Ultron", "Ant-Man",
    "Captain America: Civil War", "Doctor Strange", "Guardians of the Galaxy Vol. 2", 
    "Spider-Man: Homecoming", "Thor: Ragnarok", "Black Panther", 
    "Avengers: Infinity War", "Ant-Man and the Wasp", "Captain Marvel", 
    "Avengers: Endgame", "Spider-Man: Far From Home", "Black Widow", 
    "Shang-Chi and the Legend of the Ten Rings", "Eternals", 
    "Spider-Man: No Way Home", "Doctor Strange in the Multiverse of Madness", 
    "Thor: Love and Thunder", "Black Panther: Wakanda Forever", 
    "Ant-Man and the Wasp: Quantumania", "Guardians of the Galaxy Vol. 3", 
    "The Marvels", "Deadpool & Wolverine"
]

# Fonction pour rechercher l'ID d'un film en utilisant son titre
def search_movie_id(movie_title):
    search_url = f"https://api.themoviedb.org/3/search/movie?api_key={api_key}&query={movie_title}"
    response = requests.get(search_url)
    data = response.json()
    if data['results']:
        return data['results'][0]['id']
    return None

# Fonction pour obtenir les informations financières d'un film
def get_movie_financials(movie_id):
    financial_url = f"https://api.themoviedb.org/3/movie/{movie_id}?api_key={api_key}&language=en-US"
    response = requests.get(financial_url)
    data = response.json()
    revenue = data.get('revenue', 0)
    budget = data.get('budget', 0)
    return revenue, budget

# Liste pour stocker les recettes et les coûts
revenues = []
budgets = []
movie_titles = []

# Récupérer les informations pour chaque film
for movie in selected_movies:
    movie_id = search_movie_id(movie)
    if movie_id:
        revenue, budget = get_movie_financials(movie_id)
        revenues.append(revenue)
        budgets.append(budget)
        movie_titles.append(movie)

# Créer le graphique
fig, ax = plt.subplots(figsize=(10, 6))
ax.plot(movie_titles, revenues, label="Recettes", color="green", marker='o')
ax.plot(movie_titles, budgets, label="Coûts", color="red", marker='x')
ax.set_xticklabels(movie_titles, rotation=90)
ax.set_xlabel("Films")
ax.set_ylabel("Montant en dollars")
ax.set_title("Recettes et Coûts des Films Marvel")
ax.legend()

# Afficher le graphique avec Streamlit
st.pyplot(fig)
