# Antichess Online

A modern, responsive website for playing the Antichess (Lose-All Chess) variant.
Built with Django (Backend) and Vue 3 (Frontend).

## Project Overview

Antichess is a chess variant where the goal is to lose all your pieces. Capturing is mandatory.
This project implements:
- Real-time gameplay using WebSockets.
- User authentication and profiles with Elo ratings.
- Matchmaking system.
- Modern dark-themed UI.

## Tech Stack

- **Backend:** Python, Django, Django REST Framework, Django Channels (WebSockets), python-chess.
- **Frontend:** Vue 3, Pinia (State Management), Vue Router, Vanilla CSS.

## Setup Instructions

### Prerequisites
- Python 3.10+
- Node.js 16+

### Backend Setup

1. Navigate to the backend directory:
   ```bash
   cd backend
   ```
2. Create and activate a virtual environment (optional but recommended).
3. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```
4. Run migrations:
   ```bash
   python manage.py migrate
   ```
5. Start the server:
   ```bash
   python manage.py runserver
   ```
   The API runs at `http://localhost:8000`.

### Frontend Setup

1. Navigate to the frontend directory:
   ```bash
   cd frontend
   ```
2. Install dependencies:
   ```bash
   npm install
   ```
3. Run the development server:
   ```bash
   npm run dev
   ```
   The app works at `http://localhost:5173`.
   
   *Note: Ensure the backend is running for API and WebSocket features to work.*

## How to Contribute

1. Fork the repository.
2. Create a feature branch (`git checkout -b feature/amazing-feature`).
3. Commit your changes.
4. Push to the branch.
5. Open a Pull Request.

### Development Guidelines
- Follow the existing code style (Vue Composition API, Python PEP8).
- Write tests for new backend logic.
- Ensure the linter passes before pushing.

## Credits
Created by Andrea Gobbetti.
