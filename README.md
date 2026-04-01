# Movie Database Manager - Multi-User, SQL & OMDb API

[![Python Version](https://img.shields.io/badge/python-3.x-blue.svg)](https://www.python.org/downloads/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Pylint Score](https://img.shields.io/badge/pylint-9.56%2F10-brightgreen.svg)](https://www.pylint.org/)
[![Database: SQLite](https://img.shields.io/badge/database-SQLite-lightgrey.svg)](https://sqlite.org/index.html)

A professional, full-featured **Movie Database Application** that supports multiple user profiles. Each user manages their own private library with deep data enrichment via the **OMDb API**, persistent storage through **SQLAlchemy (SQLite)**, and individual web gallery generation.

---

## 🚀 Key Features

- 👥 **Multi-User Profiles**: Create and switch between private movie collections with separate data contexts.
- 💾 **Reliable SQL Persistence**: Efficient storage management using SQLAlchemy and SQLite with auto-migration.
- 🌐 **OMDb API Integration**: Fetch rich metadata (Director, Actors, Genre, Plot) and posters automatically.
- 🎨 **Enhanced CLI Experience**: Vibrant, color-coded terminal interface with intuitive navigation and login screens.
- 🔍 **Interactive Info View**: Generate individual IMDb-style detail pages for each movie.
- 📉 **Comprehensive Statistics**: Real-time analysis of ratings (Average, Best, Worst).
- 💻 **Static Site Generation**: Professional HTML gallery generator to showcase your entire collection online.

---

## 📁 Project Structure

```text
.
├── main.py                    # Application Entry Point
├── users.py                   # User Profile Management & Login Utility
├── movies.py                  # Core Logic, CLI Menus & Web Generation
├── trm_colors.py              # Visual UI Styling Utilities
├── data/
│   └── movies.db              # SQLite Database (Auto-created if missing)
├── storage/
│   ├── __init__.py            # Package Initializer
│   └── movie_storage_sql.py   # Data Access Layer (SQLAlchemy Persistence)
├── _static/
│   ├── index_template.html    # Base Layout Template
│   ├── style.css              # Custom Gallery CSS (Responsive Design)
│   ├── no_poster.jpg          # Fallback Asset
│   └── details/               # Individual Movie Detail Pages (Auto-generated)
├── README.md                  # Comprehensive Documentation
├── requirements.txt           # Dependency Manifest
└── .gitignore                 # VCS Exclusions
```

---

## ⚙️ Setup & Installation

### 1. Prerequisites
- **Python 3.10+**
- Active **OMDb API Key** (Get it free at [omdbapi.com](https://www.omdbapi.com/apikey.aspx))

### 2. Installation & Run
Clone the repository and install dependencies:

```bash
git clone <repository-url>
cd Movie_Project-SQL_HTML_and_API
pip install -r requirements.txt
python3 main.py
```

---

## 🛠️ Usage

1. **Profile Selection**: Launch the app and select an existing user or create a new one.
2. **Management Options**: Add movies by title (fetched from OMDb), add personal notes, or browse stats.
3. **Web Generation**: Choice **"7"** generates a full web gallery (including detail pages) and opens it in your browser.
4. **Switch User**: Choice **"8"** allows you to switch profiles without restarting.

---

## 📦 Core Technologies

- **SQLAlchemy**: Robust database abstraction layer.
- **Requests**: High-performance API communication with timeout handling.
- **SQLite**: Local, lightweight data persistence.
- **OS/JSON**: Dynamic file management and metadata serialization.

---

## 📝 License
This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.
