"""
Module for local user profile management and selection screen.
"""

import storage.movie_storage_sql as movie_storage
from trm_colors import RED, YELLOW, RESET


def prompt_create_profile():
    """
    Handles naming input for a new user and registers it with storage.
    """
    while True:
        name = input("Enter name for the new profile: ").strip()
        if not name:
            print(f"{RED}The profile name cannot be blank!{RESET}")
            continue

        user_id = movie_storage.get_or_create_user(name)
        if user_id:
            # Note: get_or_create_user already prints a success message if created
            return name

        print(f"{RED}Error: Could not create or access profile '{name}'.{RESET}")
        return None


def prompt_delete_user(profiles):
    """
    Shows list of users and handles deletion logic.
    """
    if not profiles:
        print(f"{RED}No profiles available to delete.{RESET}")
        return

    print("\nSelect profile to " + RED + "DELETE" + RESET + ":")
    for idx, name in enumerate(profiles, 1):
        print(f"{idx}. {name}")
    print("0. Cancel")

    choice = input("\nEnter number to delete: ").strip()

    if choice.isdigit() and 1 <= int(choice) <= len(profiles):
        selected_name = profiles[int(choice) - 1]
        confirm = input(f"Are you SURE you want to delete\n{RED}{selected_name}{RESET} and ALL their movies? (y/n): ").lower().strip()
        if confirm == 'y':
            if movie_storage.delete_user_profile(selected_name):
                print(f"User {RED}{selected_name}{RESET} deleted successfully.")
            else:
                print(f"{RED}Failed to delete user.{RESET}")
    elif choice != "0":
        print(f"{RED}Invalid selection.{RESET}")


def user_selection_screen():
    """
    Shows available user accounts and asks user to select or create one.
    Returns (username, movies) or None if exiting.
    """
    while True:
        movie_storage.set_current_user(None)  # Reset current user context
        profiles = list(movie_storage.get_user_profiles().keys())

        print("\n" + "=" * 40)
        print("Welcome to the Movie App! 🎬")
        print("=" * 40)
        print("\nSelect a user profile:")

        for idx, name in enumerate(profiles, 1):
            print(f"{idx}. {name}")

        print(f"{len(profiles) + 1}. Create new profile")
        print(f"{len(profiles) + 2}. {RED}Delete profile{RESET}")
        print("0. Exit Application")

        choice = input("\nEnter choice: ").strip()

        if choice == "0":
            return None

        # Select existing profile
        if choice.isdigit() and 1 <= int(choice) <= len(profiles):
            selected_name = profiles[int(choice) - 1]
            movie_storage.set_current_user(selected_name)
            print(f"\nWelcome back, {YELLOW}{selected_name}{RESET}! "
                  f"Accessing your private collection...")
            return selected_name, movie_storage.list_movies()

        # Create new profile
        if choice == str(len(profiles) + 1):
            new_name = prompt_create_profile()
            if new_name:
                movie_storage.set_current_user(new_name)
                return new_name, movie_storage.list_movies()

        # Delete profile
        if choice == str(len(profiles) + 2):
            prompt_delete_user(profiles)
            continue

        print(f"{RED}Invalid entry! Please select a valid option.{RESET}")
