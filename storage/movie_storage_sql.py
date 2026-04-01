"""
This module provides SQL-based storage functionality for the movie project.
It handles database connection, table creation, and CRUD operations for movies using SQLAlchemy.
"""

import os
from sqlalchemy import create_engine, text
from sqlalchemy.exc import SQLAlchemyError
from trm_colors import RED, GREEN, RESET

# Configure the database path dynamically
CURRENT_DIR = os.path.dirname(os.path.abspath(__file__))
PROJECT_ROOT = os.path.dirname(CURRENT_DIR)
DATA_DIR = os.path.join(PROJECT_ROOT, "data")
os.makedirs(DATA_DIR, exist_ok=True)
DB_PATH = os.path.join(DATA_DIR, "movies.db")
DB_URL = f"sqlite:///{DB_PATH}"

# Create the engine
engine = create_engine(DB_URL, echo=False)

# Create the tables if they do not exist
try:
    with engine.connect() as connection:
        # Create movies table
        connection.execute(text("""
            CREATE TABLE IF NOT EXISTS movies (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                title TEXT UNIQUE NOT NULL,
                year INTEGER NOT NULL,
                rating REAL NOT NULL,
                poster TEXT
            )
        """))
        connection.commit()
except SQLAlchemyError as e:
    print(f"{RED}Database Initialization Error: {e}{RESET}")


def list_movies():
    """Retrieve all movies from the database."""
    with engine.connect() as conn:
        result = conn.execute(text("""
            SELECT 
                title, year, rating, poster
            FROM movies
        """))
        movies = result.fetchall()

    return {row[0]: {"year": row[1], "rating": row[2], "poster": row[3]} for row in movies}


def add_movie(title, year, rating, poster=None):
    """Add a new movie to the database."""
    with engine.connect() as conn:
        try:
            conn.execute(text("""
                INSERT 
                INTO movies 
                    (title, year, rating, poster)
                VALUES 
                    (:title, :year, :rating, :poster)
            """), {"title": title, "year": year, "rating": rating, "poster": poster})
            conn.commit()
            print(f'Movie "{GREEN}{title}{RESET}" successfully added.')
        except SQLAlchemyError as e:
            print(f"{RED}Error: {e}{RESET}")


def delete_movie(title):
    """Delete a movie from the database."""
    with engine.connect() as conn:
        try:
            conn.execute(text("""
                DELETE 
                FROM movies 
                WHERE title = :title
            """),
                             {"title": title})
            conn.commit()
            print(f'Movie "{RED}{title}{RESET}" successfully deleted.')
        except SQLAlchemyError as e:
            print(f"{RED}Error: {e}{RESET}")


def update_movie(title, rating):
    """Update a movie's rating in the database."""
    with engine.connect() as conn:
        try:
            conn.execute(text("""
                UPDATE 
                    movies 
                SET 
                    rating = :rating 
                WHERE 
                    title = :title
            """),
                               {"title": title, "rating": rating})
            conn.commit()
            print(f'Movie "{GREEN}{title}{RESET}" successfully updated.')
        except SQLAlchemyError as e:
            print(f"{RED}Error: {e}{RESET}")
