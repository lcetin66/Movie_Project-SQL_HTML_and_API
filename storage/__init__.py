import os

# Configure the database path relative to the project root
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
# Note: we want the data folder to be in the project root, not inside storage/
# So we go up one level.
ROOT_DIR = os.path.dirname(BASE_DIR)
DB_PATH = os.path.join(ROOT_DIR, "data", "movies.db")
DB_URL = f"sqlite:///{DB_PATH}"
