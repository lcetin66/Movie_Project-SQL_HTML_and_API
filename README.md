# Movie Database Manager - SQL, HTML and API

[![Python Version](https://img.shields.io/badge/python-3.x-blue.svg)](https://www.python.org/downloads/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Pylint Score](https://img.shields.io/badge/pylint-10.0%2F10-brightgreen.svg)](https://www.pylint.org/)
[![Database: SQLite](https://img.shields.io/badge/database-SQLite-lightgrey.svg)](https://sqlite.org/index.html)

A professional, full-featured **Movie Database Application** that allows users to manage their movie libraries with ease. This tool integrates the **OMDb API** for rich data enrichment and utilizes **SQLAlchemy** with **SQLite** for robust, cross-platform data persistence.

---

## 🚀 Key Features

- 💾 **Reliable SQL Persistence**: Efficient storage management using SQLAlchemy and SQLite.
- 🌐 **OMDb API Integration**: Fetch movie titles, years, ratings, and posters automatically with optimized request handling.
- 🎨 **Enhanced CLI Experience**: Vibrant, color-coded terminal interface with intuitive navigation.
- 🎯 **Smart Deletion**: Partial title matching search with a confirmation mechanism to prevent accidental data loss.
- 📉 **Rich Statistics**: Comprehensive analysis of movie collection (average, median, top-rated).
- 🔍 **Flexible Searching**: Find movies using even just one or two letters, with dynamic listing of matches.
- 💻 **Static Site Generation**: Professional HTML gallery generator to showcase your collection in a responsive web view.

---

## 📁 Project Structure

```text
.
├── main.py                    # Application Entry Point
├── movies.py                  # Core Logic, Business Rules & Command Handling
├── trm_colors.py              # Visual UI Styling Utilities
├── data/
│   └── movies.db              # SQLite Database (Auto-created if missing)
├── storage/
│   ├── __init__.py            # Package Initializer
│   └── movie_storage_sql.py   # Data Access Layer (SQLAlchemy Logic)
├── _static/
│   ├── index_template.html    # Base Layout Template
│   ├── index.html             # Generated Web View
│   ├── style.css              # Custom Gallery CSS
│   └── no_poster.jpg          # Fallback Asset
├── README.md                  # Professional Documentation
├── requirements.txt           # Dependency Manifest
└── .gitignore                 # VCS Exclusions
```

---

## ⚙️ Setup & Installation

### 1. Prerequisite
- **Python 3.10+** installed.
- An internet connection for API requests.

### 2. Installation
Clone the repository and install the dependencies:

```bash
git clone <repository-url>
cd Movie_Project-SQL_HTML_and_API
pip install -r requirements.txt
```

### 3. API Configuration
Get a free API key at [omdbapi.com](https://www.omdbapi.com/apikey.aspx). The app will prompt you for it on first run and save it locally.

---

## 🛠️ Usage

Simply run the main script from the root directory:

```bash
python3 main.py
```

### Advanced Functionality:
- **Smart Delete**: Type a few letters of a movie name. The app will list all matches. If exactly one is found, it asks for your final confirmation.
- **Auto-Web Export**: Option 9 generates a complete HTML gallery in the `_static/` folder.
- **Fail-safe Entry**: If a movie isn't found on OMDb, the app gracefully switches to manual input mode.

---

## 📦 Dependencies

- `requests`: Optimized API communication with dedicated timeouts.
- `sqlalchemy`: Powerful database abstraction for SQLite.

---

## 📝 License
This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.
