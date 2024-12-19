import requests
import pandas as pd
import streamlit as st
import matplotlib.pyplot as plt

# API Key de TMDB
API_KEY = "6a2a705c0c740a478c412dedfbd387c5"

# Liste des films du MCU
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

def fetch_movie_details(title):
    """Récupérer les détails d'un film à partir de l'API TMDB."""
    url = f"https://api.themoviedb.org/3/search/movie?api_key={API_KEY}&query={title}"
    response = requests.get(url)
    data = response.json()

    if data['results']:
        movie_id = data['results'][0]['id']
        details_url = f"https://api.themoviedb.org/3/movie/{movie_id}?api_key={API_KEY}"
        details_response = requests.get(details_url)
        details = details_response.json()

        return {
            "title": details.get('title', "N/A"),
            "release_date": details.get('release_date', "N/A"),
            "budget": details.get('budget', 0),
            "revenue": details.get('revenue', 0)
        }
    else:
        return {
            "title": title,
            "release_date": "Not Found",
            "budget": "N/A",
            "revenue": "N/A"
        }

def calculate_average_budget_revenue(df):
    """Calculer les moyennes du budget et des revenus par année."""
    df['year'] = pd.to_datetime(df['release_date'], errors='coerce').dt.year
    yearly_stats = df.groupby('year').agg(
        avg_budget=('budget', 'mean'),
        avg_revenue=('revenue', 'mean')
    ).reset_index()
    
    return yearly_stats

def plot_graphs(df):
    """Tracer les graphiques des budgets et revenus du MCU."""
    # Tracer les courbes des budgets et des revenus
    fig, ax = plt.subplots(figsize=(10, 6))
    
    # Courbe des budgets
    ax.plot(df['year'], df['avg_budget'], label='Budget Moyen', color='blue', marker='o', linestyle='-', markersize=5)
    
    # Courbe des revenus
    ax.plot(df['year'], df['avg_revenue'], label='Revenu Moyen', color='green', marker='o', linestyle='-', markersize=5)

    # Ajouter des labels et un titre
    ax.set_title('Budget et Revenus Moyens des Films MCU', fontsize=16)
    ax.set_xlabel('Année', fontsize=12)
    ax.set_ylabel('Montant (en $)', fontsize=12)
    ax.legend()

    # Afficher le graphique
    st.pyplot(fig)

def display_data():
    """Afficher les films et leurs données dans Streamlit."""
    st.title("Marvel Cinematic Universe (MCU) Movies")

    # Tableau pour stocker les informations sur les films
    movie_data = []

    for title in selected_movies:
        details = fetch_movie_details(title)

        # Calculer le seuil comme 3 * budget
        budget = details['budget']
        revenue = details['revenue']
        seuil = budget * 3 if isinstance(budget, (int, float)) else "N/A"
        rentabilite = revenue - budget if isinstance(revenue, (int, float)) else "N/A"

        # Ajouter la ligne au tableau
        movie_data.append([
            details['title'], details['release_date'], budget, revenue, seuil, rentabilite
        ])

    # Créer un DataFrame pandas pour afficher dans Streamlit
    df = pd.DataFrame(movie_data, columns=["Titre", "Date", "Budget", "Revenue", "Seuil", "Rentabilité"])

    # Afficher le tableau des films
    st.subheader("Détails des films MCU")
    st.dataframe(df)

    # Calculer les moyennes par année
    averages_df = calculate_average_budget_revenue(df)

    # Afficher les moyennes
    st.subheader("Moyennes par année")
    st.dataframe(averages_df)

    # Afficher le graphique des budgets et des revenus
    plot_graphs(averages_df)

# Exécuter l'application Streamlit
if __name__ == "__main__":
    display_data()
