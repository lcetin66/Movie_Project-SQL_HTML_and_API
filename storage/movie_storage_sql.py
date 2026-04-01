"""
This module provides SQL-based storage functionality for the movie project.
It handles database connection, table creation, and CRUD operations for movies using SQLAlchemy.
Now includes multi-user support with automatic schema migration.
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

# Initialize global current user state
CURRENT_USER_ID = None
CURRENT_USERNAME = None


def init_db():
    """Create the tables if they do not exist and handle migration if needed."""
    try:
        with engine.connect() as connection:
            # 1. Create users table
            connection.execute(text("""
                CREATE TABLE IF NOT EXISTS users (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    username TEXT UNIQUE NOT NULL
                )
            """))

            # 2. Create movies table
            connection.execute(text("""
                CREATE TABLE IF NOT EXISTS movies (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    title TEXT NOT NULL,
                    year INTEGER NOT NULL,
                    rating REAL NOT NULL,
                    poster TEXT,
                    note TEXT,
                    imdb_id TEXT,
                    countries TEXT,
                    full_data TEXT
                )
            """))

            # 3. MIGRATIONS: Check for missing columns and add them one by one
            cursor = connection.execute(text("PRAGMA table_info(movies)"))
            columns = [row[1] for row in cursor.fetchall()]

            if "user_id" not in columns:
                connection.execute(text(
                    "ALTER TABLE movies ADD COLUMN user_id INTEGER REFERENCES users(id)"
                ))

            if "note" not in columns:
                connection.execute(text("ALTER TABLE movies ADD COLUMN note TEXT"))

            if "imdb_id" not in columns:
                connection.execute(text("ALTER TABLE movies ADD COLUMN imdb_id TEXT"))

            if "countries" not in columns:
                connection.execute(text("ALTER TABLE movies ADD COLUMN countries TEXT"))

            if "full_data" not in columns:
                connection.execute(text("ALTER TABLE movies ADD COLUMN full_data TEXT"))

            print(f"{GREEN}Database schema synchronized successfully.{RESET}")

            connection.commit()
    except SQLAlchemyError as e:
        print(f"{RED}Database Initialization Error: {e}{RESET}")


def list_users():
    """Returns a list of all registered users."""
    with engine.connect() as conn:
        result = conn.execute(text("SELECT id, username FROM users ORDER BY username"))
        return result.fetchall()


def get_user_profiles():
    """Helper to return {username: id} dictionary for users.py."""
    users = list_users()
    return {u[1]: u[0] for u in users}


def set_current_user(username):
    """Sets the active user session context by looking up the username."""
    global CURRENT_USER_ID, CURRENT_USERNAME
    if username is None:
        CURRENT_USER_ID = None
        CURRENT_USERNAME = None
        return

    with engine.connect() as conn:
        result = conn.execute(
            text("SELECT id FROM users WHERE username = :name"),
            {"name": username}
        )
        row = result.fetchone()
        if row:
            CURRENT_USER_ID = row[0]
            CURRENT_USERNAME = username
        else:
            CURRENT_USER_ID = None
            CURRENT_USERNAME = None


def get_or_create_user(username):
    """Get user ID by username, or create if new. Also sets context."""
    global CURRENT_USER_ID, CURRENT_USERNAME
    with engine.connect() as conn:
        try:
            # Try to find existing user
            result = conn.execute(
                text("SELECT id FROM users WHERE username = :username"),
                {"username": username}
            )
            user = result.fetchone()

            if user:
                CURRENT_USER_ID = user[0]
                CURRENT_USERNAME = username
            else:
                # Create new user
                conn.execute(
                    text("INSERT INTO users (username) VALUES (:username)"),
                    {"username": username}
                )
                conn.commit()
                # Get the new ID
                result = conn.execute(
                    text("SELECT id FROM users WHERE username = :username"),
                    {"username": username}
                )
                CURRENT_USER_ID = result.fetchone()[0]
                CURRENT_USERNAME = username

            return CURRENT_USER_ID
        except SQLAlchemyError as e:
            print(f"{RED}User error: {e}{RESET}")
            return None


def list_movies():
    """Retrieve all movies for the CURRENT user."""
    if CURRENT_USER_ID is None:
        return {}

    with engine.connect() as conn:
        result = conn.execute(text("""
            SELECT
                title, year, rating, poster, note, imdb_id, countries, full_data
            FROM movies
            WHERE user_id = :user_id
        """), {"user_id": CURRENT_USER_ID})
        movies = result.fetchall()

    return {row[0]: {
        "year": row[1], "rating": row[2], "poster": row[3],
        "note": row[4], "imdb_id": row[5], "countries": row[6],
        "full_data": row[7]
    } for row in movies}


def add_movie(title, year, rating, poster=None, imdb_id=None, countries=None, full_data=None):
    """Add a new movie for the CURRENT user."""
    if CURRENT_USER_ID is None:
        print(f"{RED}Error: No user logged in.{RESET}")
        return

    with engine.connect() as conn:
        try:
            conn.execute(text("""
                INSERT
                INTO movies
                    (title, year, rating, poster, note, user_id, imdb_id, countries, full_data)
                VALUES
                    (:title, :year, :rating, :poster, :note, :user_id, :imdb_id, :countries, :full_data)
            """), {
                "title": title, "year": year, "rating": rating,
                "poster": poster, "note": None, "user_id": CURRENT_USER_ID,
                "imdb_id": imdb_id, "countries": countries, "full_data": full_data
            })
            conn.commit()
            print(f"✅ Movie '{GREEN}{title}{RESET}' added to {CURRENT_USERNAME}'s collection!")
        except SQLAlchemyError as e:
            print(f"{RED}Error: {e}{RESET}")


def delete_movie(title):
    """Delete a movie for the CURRENT user."""
    if CURRENT_USER_ID is None:
        return

    with engine.connect() as conn:
        try:
            conn.execute(text("""
                DELETE
                FROM movies
                WHERE title = :title AND user_id = :user_id
            """),
                          {"title": title, "user_id": CURRENT_USER_ID})
            conn.commit()
            print(f'Movie "{RED}{title}{RESET}" successfully deleted from your list.')
        except SQLAlchemyError as e:
            print(f"{RED}Error: {e}{RESET}")


def update_movie_note(title, note):
    """Update a movie's note for the CURRENT user."""
    if CURRENT_USER_ID is None:
        return

    with engine.connect() as conn:
        try:
            conn.execute(text("""
                UPDATE
                    movies
                SET
                    note = :note
                WHERE
                    title = :title AND user_id = :user_id
            """),
                           {"title": title, "note": note, "user_id": CURRENT_USER_ID})
            conn.commit()
            print(f'Movie {GREEN}{title}{RESET} successfully updated.')
        except SQLAlchemyError as e:
            print(f"{RED}Error: {e}{RESET}")


# Initialize the database immediately when imported
init_db()
