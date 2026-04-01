"""
Main entry point for the Multi-User Movie Database application.
"""

from users import user_selection_screen
from movies import menu_selection


def main():
    """
    Main application loop. Handles profile selection and jumps into
    the main movie database menu for that user.
    """
    while True:
        # Step 1: Login / Profile Selection
        selection = user_selection_screen()
        if selection is None:
            break

        username, movies = selection

        # Step 2: Main Movie Application Loop
        while True:
            should_switch_user = menu_selection(movies, username)

            if should_switch_user:
                break  # Go back to Step 1 (Profile Selection)

            print("\nShutting down. Enjoy your movies! 🎥🍿\n")
            return


if __name__ == "__main__":
    main()
