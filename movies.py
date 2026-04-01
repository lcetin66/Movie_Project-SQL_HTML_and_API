"""
Module for movie management tasks, CLI menus, and website generation.
"""

import os
import json
import webbrowser
from statistics import mean

import random
import requests
import storage.movie_storage_sql as movie_storage
from trm_colors import RED, GREEN, YELLOW, CYAN, RESET


def get_non_empty_input(msg: str) -> str:
    """
    Prompts user for input until a non-empty string is given.
    Returns None if interrupted.
    """
    while True:
        try:
            val = input(msg).strip()
            if not val:
                print(f"{RED}The input can't be left blank!{RESET}")
                continue
            return val
        except (EOFError, KeyboardInterrupt):
            return None


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


def command_list_movies(movies: dict[str, dict]) -> None:
    """Prints all movies for the current user."""
    if not movies:
        print(f"{RED}No movies found!{RESET}")
        return

    print(f"\n{GREEN}{len(movies)}{RESET} movies in total:")
    for title, info in movies.items():
        note_str = f" - Note: {info['note']}" if info.get('note') else ""
        print(f"{title} ({info['year']}){note_str}")


def command_add_movie(movies: dict[str, dict]) -> None:
    """Fetches movie from OMDB and adds it to the user's storage."""
    api_key = get_omdb_user_api_key()
    if not api_key:
        return

    while True:
        title = get_non_empty_input("\nEnter movie name: ")
        if title is None:
            return

        print(f"Searching for '{title}' on OMDB...")
        try:
            url = f"http://www.omdbapi.com/?t={title}&apikey={api_key}"
            response = requests.get(url, timeout=10)
            movie_data = response.json()
        except requests.RequestException as e:
            print(f"{RED}Error connecting to API: {e}{RESET}")
            return

        if not movie_data or movie_data.get("Response") == "False":
            print(f"{RED}Error: Movie not found on OMDB!{RESET}")
            if input("Enter manually? (y/n): ").lower() != "y":
                return

            y_in = get_non_empty_input("Enter year: ")
            if y_in is None:
                return
            year = int(y_in) if y_in.isdigit() else 0
            rating, imdb_id, countries, full_data_json = 0.0, None, None, None
            poster = None
        else:
            title = movie_data.get("Title", title)
            year_str = movie_data.get("Year", "0")
            year = int(year_str[:4]) if year_str[:4].isdigit() else 0

            rating_str = movie_data.get("imdbRating", "0")
            try:
                rating = float(rating_str)
            except (ValueError, TypeError):
                rating = 0.0

            imdb_id = movie_data.get("imdbID", None)
            countries = movie_data.get("Country", None)
            full_data_json = json.dumps(movie_data)
            poster = movie_data.get("Poster", None)
            if poster == "N/A":
                poster = None

        movie_storage.add_movie(title, year, rating, poster, imdb_id, countries, full_data_json)
        movies[title] = {
            "year": year,
            "rating": rating,
            "poster": poster,
            "note": None,
            "imdb_id": imdb_id,
            "countries": countries,
            "full_data": full_data_json
        }
        return


def command_delete_movie(movies: dict[str, dict]) -> None:
    """
    Prompt the user to enter a movie title and then delete it from the database.
    Supports partial matching and asks for confirmation.
    """
    while True:
        del_movie_name = get_non_empty_input("\nEnter movie name to delete (or 0 to cancel): ")
        if del_movie_name is None or del_movie_name == '0':
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

        movie_storage.delete_movie(found_key)
        del movies[found_key]  # Remove from local dictionary
        break


def command_update_movie(movies: dict[str, dict]) -> None:
    """Allows user to add/edit a personal note for a movie."""
    title = get_non_empty_input("\nEnter movie name: ")
    if title is None:
        return

    if title in movies:
        note = get_non_empty_input("Enter movie note: ")
        if note is None:
            return
        movie_storage.update_movie_note(title, note)
        movies[title]["note"] = note
        print(f"Movie '{GREEN}{title}{RESET}' successfully updated.")
    else:
        print(f"{RED}Movie '{title}' not found!{RESET}")


def print_movies_by_rating(movies: dict[str, dict]) -> tuple[list[float], list[str], list[str], float]:
    """
    It prints the names of films with a specific rating (Best and Worst).
    Returns (ratings, best_movies, worst_movies, sum_of_ratings).
    """
    ratings = [info["rating"] for info in movies.values()]
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

    print(f'\nBest movies ({GREEN}{best_rating}{RESET}):')
    for movie in best_movies:
        print(f"- {movie}")

    print(f'\nWorst movies ({RED}{worst_rating}{RESET}):')
    for movie in worst_movies:
        print(f"- {movie}")

    return ratings, best_movies, worst_movies, sum_of_ratings


def command_movie_stats(movies: dict[str, dict]) -> None:
    """
    Output various statistics about the films in the database:
    - Average film rating
    - Median rating
    - Best movies
    - Worst movies
    """
    if not movies:
        print(f"{RED}No movies found to calculate statistics.{RESET}")
        return

    ratings, _, _, total_rating = print_movies_by_rating(movies)

    # average
    average_rating = round(total_rating / len(movies), 1)
    print(f"\nAverage rating: {GREEN}{average_rating}{RESET}")

    # median
    sorted_ratings = sorted(ratings)
    length = len(sorted_ratings)

    if length % 2 == 1:
        median_rating = sorted_ratings[length // 2]
    else:
        median_rating = (sorted_ratings[length // 2 - 1] + sorted_ratings[length // 2]) / 2

    print(f"Median rating: {GREEN}{round(median_rating, 1)}{RESET}")


def command_random_movie(movies: dict[str, dict]) -> None:
    """Picks a random movie from the dictionary."""
    if not movies:
        print(f"{RED}Empty list!{RESET}")
        return
    name = random.choice(list(movies.keys()))
    print(f"\nRandom pick: {GREEN}{name}{RESET} ({movies[name]['rating']})")


def get_flag_html(countries_str: str) -> str:
    """Helper to convert OMBd Country string to FlagCDN img tags."""
    if not countries_str:
        return ""

    mapping = {
        "USA": "us", "UK": "gb", "United Kingdom": "gb", "Germany": "de",
        "France": "fr", "Italy": "it", "Spain": "es", "Canada": "ca",
        "Turkey": "tr", "Japan": "jp", "South Korea": "kr", "China": "cn",
        "India": "in", "Australia": "au", "Denmark": "dk", "Sweden": "se"
    }

    countries = [c.strip() for c in countries_str.split(",")]
    flags = ""
    for country in countries[:2]:
        code = mapping.get(country)
        if code:
            flags += (f'<img src="https://flagcdn.com/16x12/{code}.png" '
                      f'alt="{country}" style="margin-left: 5px; vertical-align: '
                      f'middle;" title="{country}">')
    return flags


def command_generate_website(movies: dict[str, dict], username: str = "index") -> None:
    """Generate static HTML website and individual detail pages."""
    static_dir = "_static"
    details_dir = os.path.join(static_dir, "details")
    os.makedirs(details_dir, exist_ok=True)

    template_path = os.path.join(static_dir, "index_template.html")
    filename = f"{username.lower()}.html" if username else "index.html"
    output_path = os.path.join(static_dir, filename)

    if not os.path.exists(template_path):
        print(f"{RED}Error: Template file not found at {template_path}{RESET}")
        return

    with open(template_path, "r", encoding="utf-8") as f_in:
        template = f_in.read()

    movie_grid_html = ""
    for title, info in movies.items():
        imdb_id = info.get("imdb_id", "tt0000000")
        poster_url = (info.get("poster") or "img/no_poster.jpg")
        note = info.get("note") or ""
        year = info.get("year", "Unknown")
        countries = info.get("countries")
        flags_html = get_flag_html(countries)

        # Create individual Detail Page
        detail_filename = f"{imdb_id}.html"
        detail_path = os.path.join(details_dir, detail_filename)
        generate_detail_page(detail_path, title, info)

        imdb_url = f'https://www.imdb.com/title/{imdb_id}/'
        local_detail_url = f"details/{detail_filename}"
        note_html = f'<div class="movie-note">{note}</div>' if note else ""

        movie_grid_html += f"""
            <li>
                <div class="movie">
                    <div class="poster-container">
                        <a href="{imdb_url}" target="_blank">
                            <img class="movie-poster" src="{poster_url}" alt="{title}"/>
                        </a>
                        {note_html}
                    </div>
                    <div class="movie-title">{title}</div>
                    <div class="movie-info-row">
                        <span class="movie-year">{year}</span>
                        <span class="movie-flags">{flags_html}</span>
                        <a href="{local_detail_url}" class="info-btn">ⓘ Info</a>
                    </div>
                </div>
            </li>
        """

    new_html = template.replace("__TEMPLATE_TITLE__", f"{username}'s Favorite Movies")
    new_html = new_html.replace("__TEMPLATE_MOVIE_GRID__", movie_grid_html)

    with open(output_path, "w", encoding="utf-8") as f_out:
        f_out.write(new_html)

    print(f"{GREEN}Website and detail pages generated successfully!{RESET}")
    webbrowser.open(f"file://{os.path.abspath(output_path)}")


def generate_detail_page(path, title, info):
    """Creates a detailed IMDb-style page for a single movie."""
    data = {}
    try:
        if info.get("full_data"):
            data = json.loads(info["full_data"])
    except (json.JSONDecodeError, TypeError):
        pass

    fields = [
        "Director", "Actors", "Genre", "Runtime",
        "Released", "Awards", "BoxOffice", "Plot"
    ]
    details_html = ""
    for field in fields:
        val = data.get(field, "N/A")
        if val != "N/A":
            details_html += f"<p><strong>{field}:</strong> {val}</p>"

    html = f"""
    <html>
    <head>
        <title>{title} - Details</title>
        <link rel="stylesheet" href="../style.css" />
        <style>
            .detail-container {{
                display: flex;
                padding: 50px;
                max-width: 1000px;
                margin: auto;
                background: #1e1e1e;
                margin-top: 50px;
                border-radius: 12px;
                box-shadow: 0 10px 30px rgba(0,0,0,0.5);
            }}
            .detail-poster {{
                width: 300px;
                height: 450px;
                object-fit: cover;
                border-radius: 8px;
            }}
            .detail-content {{ padding-left: 40px; flex: 1; }}
            .back-btn {{
                color: #27ae60;
                text-decoration: none;
                display: inline-block;
                margin-bottom: 20px;
            }}
        </style>
    </head>
    <body style="background: #121212; color: white; font-family: Segoe UI, sans-serif;">
        <div class="detail-container">
            <div>
                <img src="{info.get('poster')}" class="detail-poster">
            </div>
            <div class="detail-content">
                <a href="javascript:history.back()" class="back-btn">← Back to List</a>
                <h1>{title} ({info.get('year')})</h1>
                <hr style="border: 0; border-top: 1px solid #333; margin: 20px 0;">
                {details_html}
            </div>
        </div>
    </body>
    </html>
    """
    with open(path, "w", encoding="utf-8") as f_out:
        f_out.write(html)


def menu_selection(movies: dict, username: str) -> bool:
    """Main menu selection controller."""
    while True:
        print(f"\n********** My Movies Database ({username}) **********")
        print("\n0. Exit")
        print("1. List movies")
        print("2. Add movie")
        print("3. Delete movie")
        print("4. Enter movie note")
        print("5. Stats")
        print("6. Random")
        print("7. Website")
        print("8. Switch User")

        choice_in = input("\nEnter choice (0-8): ").strip()
        if choice_in == "0":
            return False
        if choice_in == "8":
            return True

        actions = {
            "1": lambda: command_list_movies(movies),
            "2": lambda: command_add_movie(movies),
            "3": lambda: command_delete_movie(movies),
            "4": lambda: command_update_movie(movies),
            "5": lambda: command_movie_stats(movies),
            "6": lambda: command_random_movie(movies),
            "7": lambda: command_generate_website(movies, username),
        }

        if choice_in in actions:
            actions[choice_in]()
            input("\nPress enter to continue...")
        else:
            print(f"{RED}Invalid entry!{RESET}")
