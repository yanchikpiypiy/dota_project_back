# Dota 2 Heroes API

## Overview
This API provides detailed information about Dota 2 heroes, designed to be used by a front-end application.

## Built With
- **FastAPI** - For building the API
- **SQLAlchemy** - For database interactions
- **Pydantic** - For data validation and serialization

## Features
- Retrieve details of all Dota 2 heroes
- Fetch specific hero data by ID or name
- Provide hero attributes, abilities, and roles

## Installation & Setup
1. **Clone the repository:**
   ```sh
   git clone https://github.com/yanchikpiypiy/dota_project_back.git
   cd dota_project_back
2. **Create a virtual environment:**
   ```sh
   python -m venv venv
   source venv/bin/activate  # On Windows use: venv\Scripts\activate
4. **Install dependencies**
   ```sh
   pip install -r requirements.txt
6. **Run the api server**
   ```sh
   python src/main.py --webserver
