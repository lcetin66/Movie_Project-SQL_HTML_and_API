"""
My Film Data Bank
"""

import random
import os
import webbrowser
import requests
from storage import movie_storage_sql as storage
from trm_colors import RED, GREEN, RESET


def get_non_empty_input(prompt: str) -> str | None:
    """
    A common function for input fields that must not be left blank.
    If the user leaves it blank, it will warn them and ask again.
    """
    while True:
        value = input(prompt).strip()

        if value == "":
            print(f"The movie title {RED}can't be left blank!{RESET}")
            continue

        if value == "0":
            enter_to_continue()
            return None

        return value


def command_list_movies(movies: dict[str, dict[str, int | float]]) -> None:
    """Retrieve and display all movies from the database."""
    print(f"{RED}{len(movies)}{RESET} movies in total")
    for movie, data in movies.items():
        print(f"{movie} ({data['year']}): {data['rating']}")


def get_omdb_user_api_key() -> str | None:
    """
    Get and validate API key from user.
    Returns the key if valid, or None if invalid or blank.
    """
    # Check if API key is already saved
    if os.path.exists("api_key.txt"):
        with open("api_key.txt", "r", encoding="utf-8") as fileobject:
            api_key = fileobject.read().strip()
        print(f"{GREEN}Using saved API Key: {api_key}{RESET}")
        return api_key

    print("\n" + "=" * 60)
    print("OMDB API Key Registration")
    print("=" * 60)
    print("\nTo use the movie search feature, you need an API key from OMDB.")
    print("You can get a free API key by registering at:\nhttps://www.omdbapi.com/apikey.aspx")
    print("\n" + "=" * 60 + "\n")

    api_key = input("Please enter your OMDB API key: ").strip()
    if not api_key:
        print(f"{RED}API key can't be left blank!{RESET}")
        return None

    params = {
        "apikey": api_key,
        "s": "test"
    }
    try:
        response = requests.get("http://www.omdbapi.com/", params=params, timeout=5)
        data = response.json()

        if data.get("Response") == "False":
            error_msg = data.get("Error", "Unknown error")
            print(f"{RED}Error: {error_msg}{RESET}")
            return None

        print(f"{GREEN}API Key is valid.{RESET}")
        # Save the API key to a file
        with open("api_key.txt", "w", encoding="utf-8") as fileobject:
            fileobject.write(api_key)
        return api_key

    except requests.exceptions.RequestException as e:
        print(f"{RED}Connection error: {e}{RESET}")
        return None


def get_omdb_movie_info(api_key: str, title: str) -> dict[str, str | int | float] | None:
    """
    Get movie information from OMDb API.
    """
    params = {
        "apikey": api_key,
        "t": title.strip()
    }
    try:
        response = requests.get("http://www.omdbapi.com/", params=params, timeout=5)
        movie_data = response.json()

        if movie_data.get("Response") == "False":
            return None

        return movie_data
    except requests.exceptions.RequestException as e:
        print(f"{RED}Connection error: {e}{RESET}")
        return None


def command_add_movie(movies: dict[str, dict[str, int | float]]) -> None:
    """
    Prompt the user to enter a movie title, fetch its info from OMDb API,
    and add it to the database.
    """
    api_key = get_omdb_user_api_key()
    if not api_key:
        return

    while True:
        title = get_non_empty_input("Enter new movie name: ")
        if title is None:
            continue
        if any(movie.lower() == title.lower() for movie in movies):
            print(f'Movie "{RED}{title}{RESET}" already exists!')
            continue

        movie_data = get_omdb_movie_info(api_key, title)

        poster = None
        # If the movie is not found, notify user and ask if they want to manually enter details.
        if not movie_data or movie_data.get("Response") == "False":
            print(f"{RED}The movie '{title}' does not exist on OMDb.{RESET}")
            if input("Would you like to manually enter the movie details? (y/n): ").lower() != "y":
                continue

            # Manual Input Fallback
            year_input = get_non_empty_input("Enter a year: ")
            if year_input is None:
                return # Back to menu if user entered 0
            try:
                year = int(year_input)
            except ValueError:
                print("Invalid year.")
                continue

            rating_input = get_non_empty_input("Enter new movie rating (0-10): ")
            if rating_input is None:
                return # Back to menu if user entered 0
            try:
                rating = float(rating_input)
            except ValueError:
                print("Invalid rating.")
                continue

            poster = input("Enter movie poster URL (optional, press Enter to skip): ").strip()
            if not poster:
                poster = None
        else:
            # API Success - Use data from OMDb
            title = movie_data.get("Title", title)
            # Fetch first 4 digits of Year (handles "2008-2013" cases)
            year_str = movie_data.get("Year", "0")
            year_digits = ''.join(filter(str.isdigit, year_str))
            year = int(year_digits[:4]) if year_digits else 0
            
            # Robust imdbRating parsing
            rating_str = movie_data.get("imdbRating", "0")
            try:
                rating = float(rating_str)
            except ValueError:
                rating = 0.0
                
            poster = movie_data.get("Poster", "")
            if poster == "N/A":
                poster = None
                
            print(f"Movie found: {GREEN}{title}{RESET} ({year}) - Rating: {rating}")

        storage.add_movie(title, year, rating, poster)
        # Update local dictionary so it shows up in "List movies" immediately
        movies[title] = {"year": year, "rating": rating, "poster": poster}
        return


def command_delete_movie(movies: dict[str, dict[str, int | float]]) -> None:
    """
    Prompt the user to enter a movie title and then delete it from the database.
    Supports partial matching and asks for confirmation.
    """
    while True:
        del_movie_name = get_non_empty_input("Enter movie name to delete (or 0 to cancel): ")
        if del_movie_name is None:
            return

        # Find all movies that contain the input string (case-insensitive)
        matches = [movie for movie in movies if del_movie_name.lower() in movie.lower()]

        if not matches:
            print(f'{RED}No movie found matching "{del_movie_name}"{RESET}')
            continue

        # If multiple movies found, list them and ask to be more specific
        if len(matches) > 1:
            print(f"\n{GREEN}Multiple movies found matching '{del_movie_name}':{RESET}")
            for movie in matches:
                info = movies[movie]
                print(f"  - {movie} ({info['year']})")
            print(f"\n{RED}Please enter the more specific movie name from the list above.{RESET}\n")
            continue

        # Exactly one match found
        found_key = matches[0]
        info = movies[found_key]
        
        while True:
            confirm = input(f"Are you sure you want to delete '{RED}{found_key}{RESET}' ({info['year']})? (y/n): ").lower()
            if confirm == 'n':
                print("Deletion cancelled.")
                return
            if confirm == 'y':
                break
            print("Please enter 'y' or 'n'.")

        storage.delete_movie(found_key)
        del movies[found_key]  # Remove from local dictionary
        break


def command_update_movie(movies: dict[str, dict[str, int | float]]) -> None:
    """
    If the film exists, the user will be prompted to enter a new rating.
    The film's rating will then be updated in the database. Input validation is not required.
    """
    while True:
        edit_movie = get_non_empty_input("Enter movie name: ")
        if edit_movie is None:
            break

        found_key = None
        for movie_name in movies:
            if movie_name.lower() == edit_movie.lower():
                found_key = movie_name
                break

        if found_key is None:
            print(f'Movie "{RED}{edit_movie}{RESET}" does not exist!')
            continue

        while True:
            try:
                edited_movie_rating = float(input("Enter new movie rating (0-10): "))
                if 0 <= edited_movie_rating <= 10:
                    break
            except ValueError:
                print(f"{RED}Enter a number between 0 and 10!{RESET}")

        storage.update_movie(found_key, edited_movie_rating)
        movies[found_key]["rating"] = edited_movie_rating # Update local dictionary
        break


def print_movies_by_rating(movies: dict[str, dict[str, int | float]]) -> None:
    """
    It prints the names of films with a specific rating. title: "Best" or "Worst"
    """
    ratings = []
    for info in movies.values():
        ratings.append(info["rating"])
    best_rating = max(ratings)
    worst_rating = min(ratings)
    sum_of_ratings = sum(ratings)

    best_movies = []
    worst_movies = []
    for title, info in movies.items():
        if info["rating"] == best_rating:
            best_movies.append(title)
        if info["rating"] == worst_rating:
            worst_movies.append(title)

    print(f'Best movies ({GREEN}{best_rating}{RESET}):')
    for movie in best_movies:
        print(f"- {movie}")

    print()

    print(f'Worst movies ({RED}{worst_rating}{RESET}):')
    for movie in worst_movies:
        print(f"- {movie}")
    print()
    return ratings, best_movies, worst_movies, sum_of_ratings


def movie_statistics(movies: dict[str, dict[str, int | float]]) -> None:
    """
    Output various statistics about the films in the database:
    - Average film rating
    - Median rating
    - Best film
    - Worst film
    """
    if not movies:
        print(f"{RED}No movies found to calculate statistics.{RESET}")
        return

    ratings, _, _, total_rating = print_movies_by_rating(movies)

    # average
    average_rating = round(total_rating / len(movies), 1)
    print(f"Average rating: {GREEN}{average_rating}{RESET}")

    # median
    sorted_ratings = sorted(ratings)
    length = len(sorted_ratings)

    if length % 2 == 1:
        median_rating = sorted_ratings[length // 2]
    else:
        median_rating = (sorted_ratings[length // 2 - 1] + sorted_ratings[length // 2]) / 2

    print(f"Median rating: {GREEN}{round(median_rating, 1)}{RESET}")


def random_movie_selection(movies: dict[str, dict[str, int | float]]) -> None:
    """
    Output a random movie from the database along with its rating.
    """
    random_movie = random.choice(list(movies.keys()))
    rating = movies[random_movie]["rating"]
    print(f"Your movie for tonight: {random_movie}, "
          f"it's rated {GREEN}{rating}{RESET}")


def movie_part_searching(movies):
    """
    If the user enters "the", the film The Shawshank Redemption should be found.
    """
    search_movie_part = input("Enter part of movie name: ").lower()
    found = False

    for movie, info in movies.items():
        if search_movie_part in movie.lower():
            print(f'{movie} ({info["year"]}), {GREEN}{info["rating"]}{RESET}')
            found = True

    if not found:
        print(f"{RED}Movie not found{RESET}")


def movies_sorted_by_rating(movies: dict[str, dict[str, int | float]]) -> None:
    """
    Display all films with their ratings in descending order.
    This means the highest-rated film is shown first and the lowest-rated film last.
    """
    movies_by_rating = {}
    for movie, info in movies.items():
        rating = info["rating"]
        if rating not in movies_by_rating:
            movies_by_rating[rating] = []
        movies_by_rating[rating].append(movie)

    sorted_rating = dict(sorted(movies_by_rating.items(), reverse=True))

    for rating, movie_list in sorted_rating.items():
        for movie in movie_list:
            year = movies[movie]["year"]
            print(f"{movie} ({year}), {GREEN}{rating}{RESET}")
    return movies_by_rating


def movies_sorted_by_year(movies: dict[str, dict[str, int | float]]) -> None:
    """
    Movies are sorted from newest to oldest for “y” and from oldest to newest for “n”.
    """
    movies_by_year = {}
    for movie, info in movies.items():
        year = info["year"]
        if year not in movies_by_year:
            movies_by_year[year] = []
        movies_by_year[year].append(movie)

    while True:
        reverse = input("Do you want the latest movies first? (Y/N) ").lower()
        if reverse in ("y", "yes"):
            select = True
            break
        if reverse in ("n", "no"):
            select = False
            break
        print("Please enter Y or N.")

    sorted_rating = dict(sorted(movies_by_year.items(), reverse=select))

    for year, movie_list in sorted_rating.items():
        for movie in movie_list:
            rating = movies[movie]["rating"]
            print(f"{movie} {GREEN}{year}{RESET}, {rating}")


def command_generate_website(movies: dict[str, dict[str, int | float]]) -> None:
    """
    Generate a website with the movie database.
    """
    with open("_static/index_template.html", "r", encoding="utf-8") as fileobject:
        website_content = fileobject.read()
        movie_grid = ""
    for movie, data in movies.items():
        poster = data.get('poster')
        if poster:
            poster_html = f'<img class="movie-poster" src="{poster}" alt="{movie}">'
        else:
            poster_html = '<img class="movie-poster" src="no_poster.jpg" alt="No Poster">'

        movie_grid += f"""
        <li>
            <div class="movie">
                {poster_html}
                <div class="movie-title">{movie}</div>
                <div class="movie-year">{data['year']}</div>
            </div>
        </li>
        """
    website_content = website_content.replace(
        "__TEMPLATE_TITLE__", "My Movies Database"
    ).replace(
        "__TEMPLATE_MOVIE_GRID__", movie_grid
    )
    with open("_static/index.html", "w", encoding="utf-8") as fileobject:
        fileobject.write(website_content)
    file_path = os.path.abspath("_static/index.html")
    print(f"{GREEN}Website generated successfully.{RESET}\n")
    print(f"You can view the website at: file://{file_path}")
    webbrowser.open(f"file://{file_path}")


def menu_selection(movies: dict[str, dict[str, int | float]]) -> None:
    """
    Movie database menu selection
    """
    while True:
        actions = {
            1: lambda: command_list_movies(movies),
            2: lambda: command_add_movie(movies),
            3: lambda: command_delete_movie(movies),
            4: lambda: command_update_movie(movies),
            5: lambda: movie_statistics(movies),
            6: lambda: random_movie_selection(movies),
            7: lambda: movie_part_searching(movies),
            8: lambda: movies_sorted_by_rating(movies),
            9: lambda: command_generate_website(movies),
        }

        try:
            menu_choice = int(input("Enter choice (0-9): "))
            print()
        except ValueError:
            print(f"{RED}Your selection must be an integer between 0-9!{RESET}")
            continue

        if menu_choice == 0:
            print("Bye!\n")
            break

        if menu_choice not in actions:
            print(f"Your selection must be an integer between {RED}0-9!{RESET}")
            continue

        actions[menu_choice]()
        enter_to_continue()


def start_menu() -> None:
    """
    Menu list that opens after each transaction
    """
    print("*" * 10 + " My Movies Database " + "*" * 10)
    print()
    menu = [
        "0. Exit",
        "1. List movies",
        "2. Add movie",
        "3. Delete movie",
        "4. Update movie",
        "5. Stats",
        "6. Random movie",
        "7. Search movie",
        "8. Movies sorted by rating",
        "9. Generate website"
    ]
    for menu_list in menu:
        print(menu_list)
    print()


def enter_to_continue() -> None:
    """
    User's transaction progress check
    """
    print()
    while True:
        choice_continue = input("Press enter to continue")
        if choice_continue == "":
            print()
            start_menu()
            break
