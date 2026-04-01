# Movie Project - SQL, HTML and API

[![Python Version](https://img.shields.io/badge/python-3.x-blue.svg)](https://www.python.org/downloads/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Pylint Score](https://img.shields.io/badge/pylint-10.0%2F10-brightgreen.svg)](https://www.pylint.org/)
[![Database: SQLite](https://img.shields.io/badge/database-SQLite-lightgrey.svg)](https://sqlite.org/index.html)

This project is a comprehensive **Movie Database Application** that enables users to manage their personal movie collections efficiently. It integrates the **OMDb API** to fetch dynamic movie details and utilizes **SQLAlchemy** for local data persistence in an **SQLite** database.

---

## 🚀 Features

- 💾 **Robust Persistence**: Seamlessly manage your movie collection in a local SQL database.
- 🌐 **Real-time Data Fetching**: Automatically retrieve titles, years, ratings, and posters via the OMDb API.
- 🎨 **Enhanced CLI**: Interactive, color-coded command-line interface for an intuitive user experience.
- 📊 **Insightful Statistics**: Detailed analysis of your collection, including average ratings, medians, and top performers.
- 🔍 **Advanced Search & Sort**: Quickly find movies or organize your list by release year and IMDb rating.
- 💻 **Static Site Generator**: Create a professional, responsive HTML gallery to showcase your collection.

---

## 📁 Project Structure

```text
.
├── main.py                    # Application Entry Point
├── movies.py                  # Core Logic & Command Handling
├── trm_colors.py              # Terminal UI Styling Utilities
├── data/
│   └── movies.db              # Persistent SQLite Storage
├── storage/
│   ├── __init__.py            # Package Initializer and global configuration
│   └── movie_storage_sql.py   # Database Access Layer (SQLAlchemy / SQLite)
├── _static/
│   ├── index_template.html    # Base HTML layout template
│   ├── index.html             # Generated website output
│   ├── style.css              # Custom styling for the gallery
│   └── no_poster.jpg          # Fallback image resource
├── README.md                  # Project Documentation
├── requirements.txt           # Dependency Manifest
└── .gitignore                 # Version Control Exclusions
```

---

## ⚙️ Setup Instructions

### 1. Prerequisite
Ensure you have **Python 3.x** installed on your system.

### 2. Installation
Clone the repository and install the required dependencies:

```bash
git clone <repository-url>
cd 20260330-Movie_Project-SQL_HTML_and_API
pip install -r requirements.txt
```

### 3. API Configuration
You will need a free API key from OMDb. You can obtain one by registering at [omdbapi.com](https://www.omdbapi.com/apikey.aspx).

---

## 🛠️ Usage

Execute the application with the following command:

```bash
python main.py
```

### Navigating the App:
- **Add Movie**: Enter a title; the app fetches details automatically.
- **Search**: Find movies by any part of their title.
- **Stats**: View a quick summary of your ratings.
- **Generate Website**: Export your collection to a beautiful web view (check `_static/index.html`).

---

## 📦 Dependencies

The application relies on the following Python modules:
- `requests`: For API communication.
- `sqlalchemy`: For database abstraction and ORM/Core functionality.

---

## 📝 License
This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for details.
