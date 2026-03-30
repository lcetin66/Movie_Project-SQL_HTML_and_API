"""My Film Data Bank"""
import random
from datetime import date
import movie_storage as sm

RED = "\033[91m"
GREEN = "\033[92m"
RESET = "\033[0m"

def get_non_empty_input(prompt):
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

def list_movies(movies):
    """
    Display all films along with their ratings.
    Additionally, show the total number of films in the database.
    """
    print(f"{RED}{len(movies)}{RESET} movies in total")

    for movie, info in movies.items():
        year = info.get("year", "Unknown")
        rating = info.get("rating", "N/A")
        print(f"{movie} ({year}): {GREEN}{rating}{RESET}")

def add_movie(movies):
    """
    Prompt the user to enter a movie title and a rating.
    Validation of the input is not required (ratings between 1 and 10 are accepted).
    """
    while True:
        title = get_non_empty_input("Enter new movie name: ")
        if title is None:
            return

        # duplicate check
        if any(movie.lower() == title.lower() for movie in movies):
            print(f'Movie "{RED}{title}{RESET}" already exists!')
            continue

        # year
        year_input = get_non_empty_input("Enter a year: ")
        if year_input is None:
            return

        try:
            year = int(year_input)
        except ValueError:
            print("Invalid year of manufacture.")
            return

        current_year = date.today().year
        if year < 1888 or year > current_year:
            print("Invalid year of manufacture.")
            return

        # rating
        if year < 1888 or year > current_year:
            print("Invalid year of manufacture.")
            return

            # Rating
        while True:
            try:
                rating = float(input("Enter new movie rating (0-10): "))
                if 0 <= rating <= 10:
                    break
            except ValueError:
                print(f"{RED}Enter a rating between 0 and 10!{RESET}")

        sm.add_movie(title, year, rating)
        print(f'Movie "{GREEN}{title}{RESET}" successfully added.')
        return

def delete_movie(movies):
    """
    Prompt the user to enter a movie title and then delete it from the database.
    If the movie doesn't exist, an error message will be displayed, and the menu will reappear.
    """
    while True:
        del_movie_name = get_non_empty_input("Enter movie name to delete: ")
        if del_movie_name is None:
            break

        found_key = None
        for movie in movies:
            if movie.lower() == del_movie_name.lower():
                found_key = movie
                break

        if found_key is None:
            print(f'Movie "{RED}{del_movie_name}{RESET}" does not exist!')
            continue

        sm.delete_movie(found_key)
        print(f"Movie {RED}{found_key}{RESET} successfully {RED}deleted{RESET}.")
        enter_to_continue()
        break

def update_movie(movies):
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

        sm.update_movie(found_key, edited_movie_rating)
        print(f'Movie "{GREEN}{found_key}{RESET}" successfully updated.')
        break

def print_movies_by_rating(movies):
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

def movie_statistics(movies):
    """
    Output various statistics about the films in the database:
    - Average film rating
    - Median rating
    - Best film
    - Worst film
    """
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

def random_movie_selection(movies):
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

def movies_sorted_by_rating(movies):
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

def movies_sorted_by_year(movies):
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

def menu_selection(storage):
    """
    Movie database menu selection
    """
    while True:
        movies = storage.get_movies()
        actions = {
            1: lambda: list_movies(movies),
            2: lambda: add_movie(movies),
            3: lambda: delete_movie(movies),
            4: lambda: update_movie(movies),
            5: lambda: movie_statistics(movies),
            6: lambda: random_movie_selection(movies),
            7: lambda: movie_part_searching(movies),
            8: lambda: movies_sorted_by_rating(movies),
            9: lambda: movies_sorted_by_year(movies),
        }

        try:
            menu_choice = int(input("Enter choice (0-8): "))
            print()

            if menu_choice == 0:
                print("Bye!")
                break

            if menu_choice not in actions:
                print(f"Your selection must be an integer between {RED}0-8!{RESET}")
                continue

            actions[menu_choice]()
            enter_to_continue()

        except ValueError:
            print(f"{RED}Your selection must be an integer between 0-8!{RESET}")

def start_menu():
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
        "9. Movies sorted by year"
    ]
    for menu_list in menu:
        print(menu_list)
    print()

def enter_to_continue():
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

def main():
    """Dictionary to store the movies and the rating"""

    start_menu() # Menu list
    menu_selection(sm) # Menu choice


if __name__ == "__main__":
    main()
