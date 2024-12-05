import streamlit as st
import requests
import random
import re  # Pour nettoyer la ponctuation

# Définition de la clé API de TMDB
api_key = '6a2a705c0c740a478c412dedfbd387c5'

# Liste de films populaires pour la randomisation (à remplacer par ta liste complète de films)
movie_list = [
   'Iron Man 2', 'Thor: The Dark World', 'Avengers: Age of Ultron', 'Captain America: Civil War', 
   'Doctor Strange', 'Ant-Man and the Wasp', 'Black Panther', 'Avengers: Infinity War', 
   'Avengers: Endgame', 'Spider-Man: Far From Home', 'Spider-Man: No Way Home', 
   'Black Widow', 'Shang-Chi and the Legend of the Ten Rings', 'Eternals', 'Doctor Strange in the Multiverse of Madness',
   'Thor: Love and Thunder', 'Black Panther: Wakanda Forever', 'Ant-Man and the Wasp: Quantumania', 'Guardians of the Galaxy Vol. 3',
   'Blade', 'Blade II', 'Blade: Trinity', 'X-Men: The Last Stand', 'X-Men Origins: Wolverine', 'X-Men: First Class', 
   'X-Men: Days of Future Past', 'X-Men: Apocalypse', 'X-Men: Dark Phoenix', 'Logan', 'Deadpool', 'Deadpool 2', 
   'Fantastic Four', 'Fantastic Four: Rise of the Silver Surfer', 'Fantastic Four (2015)', 'The Incredible Hulk', 'Venom', 
   'Venom: Let There Be Carnage', 'Ghost Rider', 'Ghost Rider: Spirit of Vengeance', 'Daredevil', 'Elektra', 'The Punisher', 
   'The Punisher: War Zone', 'Hancock', 'Kick-Ass', 'Kick-Ass 2', 'The New Mutants', 'Guardians of the Galaxy Vol. 2', 
   'A Nightmare on Elm Street', 'The Exorcist', 'The Ring', 'It', 'The Blair Witch Project', 'The Grudge', 'Poltergeist', 
   'The Texas Chainsaw Massacre', 'Halloween', 'Friday the 13th', 'Scream', 'The Conjuring', 'The Nun', 'Insidious', 
   'Annabelle', 'Hereditary', 'Midsommar', 'The Babadook', 'The Witch', 'Get Out', 'Us', 'A Quiet Place', 'The Cabin in the Woods', 
   'The Mist', 'It Follows', 'The Invisible Man', 'Don’t Breathe', 'The Autopsy of Jane Doe', 'The Descent', 'The Others', 
   'Train to Busan', 'World War Z', '28 Days Later', 'Shaun of the Dead', 'Zombieland', '28 Weeks Later', 'The Walking Dead', 
   'Scream 2', 'Scream 3', 'Scream 4', 'The Host', 'Cloverfield', 'Pacific Rim', 'Battle Los Angeles', 'World War Z', 
   'Godzilla', 'Kong: Skull Island', 'King Kong', 'Pacific Rim Uprising', 'Jurassic World: Fallen Kingdom', 
   'Jurassic World', 'The Meg', 'Jaws', 'Deep Blue Sea', 'Trolls', 'Monsters Inc.', 'Monsters University', 'The Lego Movie', 
   'The Lego Movie 2: The Second Part', 'Shrek', 'Shrek 2', 'Shrek the Third', 'Shrek Forever After', 'Kung Fu Panda', 
   'Kung Fu Panda 2', 'Kung Fu Panda 3', 'How to Train Your Dragon', 'How to Train Your Dragon 2', 'How to Train Your Dragon: The Hidden World',
   'The Croods', 'The Croods: A New Age', 'Madagascar', 'Madagascar: Escape 2 Africa', 'Madagascar 3: Europe\'s Most Wanted', 
   'Hotel Transylvania', 'Hotel Transylvania 2', 'Hotel Transylvania 3: Summer Vacation', 'Minions', 'Despicable Me', 
   'Despicable Me 2', 'Despicable Me 3', 'Sing', 'Sing 2', 'Ralph Breaks the Internet', 'Frozen', 'Frozen II', 'Tangled', 
   'Moana', 'Pocahontas', 'Beauty and the Beast', 'Cinderella', 'Aladdin', 'The Lion King', 'Mulan', 'The Little Mermaid', 
   'Dumbo', 'The Jungle Book', 'Pinocchio', 'Snow White and the Seven Dwarfs', 'Peter Pan', 'Sleeping Beauty', 
   'The Sword in the Stone', 'Robin Hood', 'Wreck-It Ralph', 'Zootopia', 'The Princess and the Frog', 'The Emperor\'s New Groove', 
   'Hercules', 'Atlantis: The Lost Empire', 'Lilo & Stitch', 'Bolt', 'The Good Dinosaur', 'Cars', 'Cars 2', 'Cars 3', 
   'Finding Nemo', 'Finding Dory', 'Wall-E', 'Toy Story', 'Toy Story 2', 'Toy Story 3', 'Toy Story 4', 'Inside Out', 
   'Soul', 'Luca', 'Raya and the Last Dragon', 'The Incredibles', 'The Incredibles 2', 'Up', 'A Bug\'s Life', 
   'Monsters vs Aliens', 'Cloudy with a Chance of Meatballs', 'The Polar Express', 'The Angry Birds Movie', 'Paddington', 
   'Paddington 2', 'Arthur Christmas', 'The Book of Life', 'Coraline', 'ParaNorman', 'Kubo and the Two Strings', 'Missing Link', 
   'Laika', 'The Boxtrolls', 'Isle of Dogs', 'Spider-Man: Into the Spider-Verse', 'Spider-Man: Across the Spider-Verse', 
   'The Lego Batman Movie', 'The Lego Ninjago Movie', 'Rango', 'The Simpsons Movie', 'Beavis and Butt-Head Do America', 
   'South Park: Bigger, Longer & Uncut', 'Ferdinand', 'Epic', 'Ice Age', 'Ice Age: The Meltdown', 'Ice Age: Dawn of the Dinosaurs', 
   'Ice Age: Continental Drift', 'Ice Age: Collision Course', 'Rio', 'Rio 2', 'The Lorax', 'Dr. Seuss\' The Grinch', 'Sing', 
   'Monster Family', 'Norm of the North', 'Ice Age: A Mammoth Christmas', 'Home', 'Shrek the Halls', 'Kung Fu Panda Holiday', 
   'Mickey\'s Once Upon a Christmas', 'Arthur Christmas', 'Frozen Fever', 'Santa Claus Is Comin\' to Town', 'Rudolph the Red-Nosed Reindeer', 
   'Charlie Brown Christmas', 'A Charlie Brown Thanksgiving', 'A Charlie Brown Christmas', 'Frosty the Snowman', 'The Grinch', 
   'Christmas Carol', 'The Peanuts Movie', 'The Lion King 2: Simba\'s Pride', 'The Lion Guard: Return of the Roar', 
   'Lion Guard: The Rise of Scar', 'The Secret Life of Pets', 'The Secret Life of Pets 2', 'Despicable Me 3', 'The Angry Birds Movie 2', 
   'Moomins on the Riviera', 'Anastasia', 'Balto', 'Bambi', 'Lady and the Tramp', 'The Fox and the Hound', 'Oliver & Company', 
   'The Rescuers', 'The Rescuers Down Under', 'The Aristocats', 'The Great Mouse Detective', 'The Black Cauldron', 
   'The Land Before Time', 'The Land Before Time II', 'The Land Before Time III', 'The Land Before Time IV', 'The Land Before Time V']

# Fonction pour nettoyer les titres en supprimant la ponctuation et les espaces excédentaires
def clean_title(title):
    # Supprimer tous les caractères non alphabétiques et convertir en minuscules
    cleaned = re.sub(r'\W+', ' ', title.lower())  # \W+ supprime tout sauf les lettres et chiffres, remplace par un espace
    return cleaned.strip()

# Fonction pour rechercher un film par titre
def search_movie_id(movie_title):
    search_url = f"https://api.themoviedb.org/3/search/movie?api_key={api_key}&query={movie_title}"
    response = requests.get(search_url)
    data = response.json()
    if data['results']:
        return data['results'][0]['id']  # Retourner l'id du premier film trouvé
    return None

# Fonction pour récupérer les détails d'un film avec son id
def get_movie_details(movie_id):
    movie_url = f"https://api.themoviedb.org/3/movie/{movie_id}?api_key={api_key}"
    response = requests.get(movie_url)
    return response.json()

# Fonction pour récupérer les crédits du film (acteurs, réalisateurs)
def get_movie_credits(movie_id):
    credits_url = f"https://api.themoviedb.org/3/movie/{movie_id}/credits?api_key={api_key}"
    response = requests.get(credits_url)
    return response.json()

# Fonction pour récupérer les genres du film
def get_movie_genres(movie_id):
    movie_details = get_movie_details(movie_id)
    return [genre['name'] for genre in movie_details['genres']]

# Fonction pour récupérer les sociétés de production du film
def get_movie_production_companies(movie_id):
    movie_details = get_movie_details(movie_id)
    return [company['name'] for company in movie_details['production_companies']]

# Fonction pour récupérer l'année de sortie du film
def get_movie_release_year(movie_id):
    movie_details = get_movie_details(movie_id)
    return movie_details['release_date'][:4]

# Fonction principale du jeu
def play_game():
    # Initialisation des variables du jeu
    if 'movie_id' not in st.session_state:
        st.session_state.movie_id = None
        st.session_state.movie_title = ''
        st.session_state.attempts = 0
        st.session_state.guesses = []
        st.session_state.indicators = []

    # Affichage de l'interface du jeu
    st.title('Jeu de devinette de films')

    # Ajouter un bouton "Start" pour commencer une nouvelle partie
    start_button = st.button('Start')
    
    if start_button:
        # Réinitialiser toutes les variables du jeu au début de chaque partie
        st.session_state.movie_id = None
        st.session_state.movie_title = ''
        st.session_state.attempts = 0
        st.session_state.guesses = []  # Réinitialiser les tentatives
        st.session_state.indicators = []  # Réinitialiser les indices

        # Sélectionner un film aléatoire de la liste
        random_movie = random.choice(movie_list)
        st.session_state.movie_title = random_movie

        # Recherche de l'ID du film choisi
        movie_id = search_movie_id(random_movie)
        st.session_state.movie_id = movie_id
        
        # Récupérer les informations du film
        st.session_state.production_companies = get_movie_production_companies(movie_id)
        st.session_state.genres = get_movie_genres(movie_id)
        st.session_state.actors = get_movie_credits(movie_id)['cast']
        st.session_state.release_year = get_movie_release_year(movie_id)

        # Initialiser les indices
        st.session_state.indicators = [f"Sociétés de production: {', '.join(st.session_state.production_companies)}"]

    # Si un film est choisi, commencer à afficher les indices et permettre des tentatives
    if st.session_state.movie_id is not None:
        # Ajouter les indices au fur et à mesure des tentatives
        if st.session_state.attempts >= 1 and len([i for i in st.session_state.indicators if i.startswith("Genre(s)")]) == 0:
            st.session_state.indicators.append(f"Genre(s): {', '.join(st.session_state.genres)}")

        if st.session_state.attempts >= 2 and len([i for i in st.session_state.indicators if i.startswith("Un acteur")]) == 0:
            actor = random.choice(st.session_state.actors)['name']
            st.session_state.indicators.append(f"Un acteur: {actor}")

        if st.session_state.attempts >= 3 and len([i for i in st.session_state.indicators if i.startswith("Année de sortie")]) == 0:
            st.session_state.indicators.append(f"Année de sortie: {st.session_state.release_year}")

        if st.session_state.attempts >= 4 and len([i for i in st.session_state.indicators if i.startswith("Un autre acteur")]) == 0:
            actor = random.choice(st.session_state.actors)['name']
            st.session_state.indicators.append(f"Un autre acteur: {actor}")

        if st.session_state.attempts >= 5 and len([i for i in st.session_state.indicators if i.startswith("Un troisième acteur")]) == 0:
            actor = random.choice(st.session_state.actors)['name']
            st.session_state.indicators.append(f"Un troisième acteur: {actor}")

        if st.session_state.attempts >= 6 and len([i for i in st.session_state.indicators if i.startswith("Réalisateur(s)")]) == 0:
            st.session_state.indicators.append(f"Réalisateur(s): {', '.join([crew['name'] for crew in get_movie_credits(st.session_state.movie_id)['crew'] if crew['job'] == 'Director'])}")

        if st.session_state.attempts >= 7 and len([i for i in st.session_state.indicators if i.startswith("Les 3 premières lettres du titre")]) == 0:
            st.session_state.indicators.append(f"Les 3 premières lettres du titre: {st.session_state.movie_title[:3]}")

        # Afficher les indices
        for indicator in st.session_state.indicators:
            st.write(indicator)

        # Afficher le champ de saisie avec des suggestions filtrées
        movie_title_input = st.text_input("Devinez le titre du film:", key="movie_input")

        # Nettoyer l'entrée de l'utilisateur
        cleaned_input = clean_title(movie_title_input)

        # Filtrage de la liste des films en fonction des mots du titre
        if cleaned_input:
            suggestions = []
            for movie in movie_list:
                cleaned_movie_title = clean_title(movie)
                movie_words = cleaned_movie_title.split()  # Diviser le titre en mots

                # Vérifier si chaque mot du titre commence par l'entrée de l'utilisateur
                for word in movie_words:
                    if word.startswith(cleaned_input):
                        suggestions.append(movie)
                        break  # Ajouter le film si l'un des mots correspond

        else:
            suggestions = []

        # Afficher les suggestions sous le champ de saisie
        if suggestions:
            st.write("Suggestions :")
            for suggestion in suggestions:
                if st.button(suggestion):  # Chaque suggestion devient un bouton cliquable
                    st.session_state.attempts += 1
                    st.session_state.guesses.append(suggestion)
                    if suggestion.lower() == st.session_state.movie_title.lower():
                        st.success("Félicitations, vous avez deviné le film !")
                        return  # Le jeu est terminé si l'utilisateur a trouvé
                    else:
                        st.error(f"Tentative incorrecte. Il vous reste {10 - st.session_state.attempts} tentatives.")
                        if st.session_state.attempts >= 10:
                            st.error(f"Vous avez perdu ! Le film était : {st.session_state.movie_title}")
                            return  # Arrêter le jeu quand l'utilisateur a perdu

        # Afficher les tentatives précédentes
        st.write("Tentatives précédentes:")
        for i, guess in enumerate(st.session_state.guesses):
            st.write(f"{i + 1}: {guess}")

# Fonction pour réinitialiser le jeu
def reset_game():
    st.session_state.movie_id = None
    st.session_state.movie_title = ''
    st.session_state.attempts = 0
    st.session_state.guesses = []  # Réinitialiser les tentatives
    st.session_state.indicators = []  # Réinitialiser les indices

if __name__ == "__main__":
    st.sidebar.button('Reinitialiser le jeu', on_click=reset_game)
    play_game()
