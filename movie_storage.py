"""
This module provides JSON-based storage functionality for the movie project.
It handles reading from and writing to a JSON file named #data.json.
"""

import json


def get_movies():
    """
    Returns a dictionary of dictionaries that
    contains the movies information in the database.

    The function loads the information from the JSON
    file and returns the data.
    """
    try:
        with open("#data.json", "r", encoding="utf-8") as fileobject:
            data = json.load(fileobject)
    except FileNotFoundError:
        data = {}
        with open("#data.json", "w", encoding="utf-8") as fileobject:
            json.dump(data, fileobject, indent=4)
    return data


def save_movies(movies):
    """
    Save movies to the movie's database.
    """
    try:
        with open("#data.json", "w", encoding="utf-8") as fileobject:
            json.dump(movies, fileobject, indent=4)
    except IndentationError:
        print("IndentationError: unexpected indent")


def add_movie(title, year, rating):
    """
    Adds a movie to the movie's database.
    Loads the information from the JSON file, add the movie,
    and saves it. The function doesn't need to validate the input.
    """
    movies = get_movies()
    movies[title] = {
        "year": year,
        "rating": rating
    }
    save_movies(movies)


def delete_movie(title):
    """
    Deletes a movie from the movie's database.
    Loads the information from the JSON file, deletes the movie,
    and saves it. The function doesn't need to validate the input.
    """
    movies = get_movies()
    found_key = None

    for movie in movies:
        if movie.lower() == title.lower():
            found_key = movie
            break
    if found_key is None:
        return

    del movies[found_key]
    save_movies(movies)


def update_movie(title, rating):
    """
    Updates a movie from the movie's database.
    Loads the information from the JSON file, updates the movie,
    and saves it. The function doesn't need to validate the input.
    """
    movies = get_movies()

    if title not in movies:
        return

    movies[title]["rating"] = rating
    save_movies(movies)
