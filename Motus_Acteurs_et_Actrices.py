import streamlit as st
import random
import requests

# Clé API
api_key = '6a2a705c0c740a478c412dedfbd387c5'

# Initialisation des clés dans `st.session_state`
if 'target_name' not in st.session_state:
    st.session_state.target_name = ""
if 'movie_title' not in st.session_state:
    st.session_state.movie_title = ""
if 'guesses' not in st.session_state:
    st.session_state.guesses = []
if 'remaining_attempts' not in st.session_state:
    st.session_state.remaining_attempts = 10
if 'progress_display' not in st.session_state:
    st.session_state.progress_display = []
if 'game_started' not in st.session_state:
    st.session_state.game_started = False

# Fonction pour chercher les acteurs principaux d'un film
def get_random_actor_and_movie(movie_titles):
    selected_movie = random.choice(movie_titles)
    search_url = f"https://api.themoviedb.org/3/search/movie?api_key={api_key}&query={selected_movie}"
    response = requests.get(search_url)
    if response.status_code == 200:
        data = response.json()
        results = data.get('results', [])
        if results:
            movie_id = results[0]['id']
            credits_url = f"https://api.themoviedb.org/3/movie/{movie_id}/credits?api_key={api_key}"
            response = requests.get(credits_url)
            if response.status_code == 200:
                data = response.json()
                cast = data.get('cast', [])
                if cast:
                    selected_actor = random.choice(cast[:5])  # Prenez un acteur parmi les 5 premiers
                    return extract_last_name(selected_actor['name']), selected_movie
    return None, None

# Fonction pour extraire les noms de famille
def extract_last_name(name):
    return name.split()[-1]

# Fonction pour créer un affichage progressif
def update_progress_display(guess, target, progress):
    target = target.lower()
    guess = guess.lower()
    updated_progress = list(progress)

    for i, char in enumerate(guess):
        if i < len(target) and char == target[i]:
            updated_progress[i] = f":green[{char}]"  # Bien placé
        elif char in target and char not in progress:
            updated_progress[i] = f":orange[{char}]"  # Mal placé
        else:
            updated_progress[i] = char  # La lettre est absente, affichée normalement

    return updated_progress

# Fonction principale du jeu Motus
def motus_game():
    st.title("Motus : Devinez le nom de famille d'un acteur !")

    # Liste enrichie de titres de films
    movie_titles = [
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
        'The Land Before Time', 'The Land Before Time II', 'The Land Before Time III', 'The Land Before Time IV', 'The Land Before Time V'
    ]

    # Bouton pour démarrer ou redémarrer le jeu
    if st.button("Start"):
        last_name, movie = get_random_actor_and_movie(movie_titles)
        if last_name and movie:
            st.session_state.target_name = last_name
            st.session_state.movie_title = movie
            st.session_state.guesses = []
            st.session_state.remaining_attempts = 10
            st.session_state.progress_display = [""] * len(last_name)  # Vide les espaces, pas de "_"
            st.session_state.game_started = True
        else:
            st.error("Impossible de récupérer un nom d'acteur. Réessayez.")

    # Vérification si le jeu est lancé
    if st.session_state.game_started:
        target_name = st.session_state.target_name
        movie_title = st.session_state.movie_title
        guesses = st.session_state.guesses
        remaining_attempts = st.session_state.remaining_attempts
        progress_display = st.session_state.progress_display

        # Affichage du film de l'acteur
        st.subheader(f"L'acteur recherché a joué dans le film : {movie_title}")

        # Affichage du nombre de lettres
        st.subheader(f"Le nom de famille comporte {len(target_name)} lettres.")
        st.write("Progrès actuel :")
        st.write("".join(progress_display))

        # Affichage des tentatives précédentes
        st.subheader("Vos tentatives")
        for guess, feedback in guesses:
            st.write(feedback)

        # Tentative actuelle
        if remaining_attempts > 0:
            guess = st.text_input("Entrez votre proposition :", key=f"input_{remaining_attempts}").strip().lower()

            # Si le bouton valider est pressé
            if st.button("Valider"):
                if len(guess) != len(target_name):
                    st.warning(f"Le nom doit comporter {len(target_name)} lettres.")
                else:
                    feedback = update_progress_display(guess, target_name, progress_display)
                    st.session_state.progress_display = feedback
                    guesses.append((guess, "".join(feedback)))
                    st.session_state.guesses = guesses
                    st.session_state.remaining_attempts -= 1

                    # Vérification de la victoire
                    # On compare sans les couleurs, juste les lettres
                    if guess == target_name.lower():  # Vérification directe du nom complet
                        st.success(f"Félicitations ! Vous avez trouvé : {target_name}")
                        st.balloons()
                        st.session_state.game_started = False
                        st.stop()

        # Défaite
        if remaining_attempts == 0:
            st.error(f"Vous avez perdu ! Le nom était : {target_name}")
            st.session_state.game_started = False
            st.stop()

        # Tentatives restantes
        st.info(f"Il vous reste {remaining_attempts} tentatives.")

# Exécution de l'application
motus_game()
