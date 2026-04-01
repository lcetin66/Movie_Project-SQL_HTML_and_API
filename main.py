"""
Main function to run the movie database application.
"""

from storage import movie_storage_sql as storage
from movies import start_menu, menu_selection

def main() -> None:
    """Main function to run the movie database application."""
    start_menu() # Menu list
    movies = storage.list_movies()
    menu_selection(movies) # Menu choice


if __name__ == "__main__":
    main()
