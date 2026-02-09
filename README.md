# Personalized Workout Generator 💪

A full-stack web app that generates personalized workouts based on the equipment you have and the type of training you want to do. Users can create accounts, save workouts, and track their progress over time.

This project was built as a portfolio piece to show how I think about full-stack development beyond just writing code — focusing on system design, data flow, and real user features.

---

## Why I built this

I wanted to build something that felt like a real product, not just a demo. The goal was to design and ship an app end-to-end, including:

- Turning user input into useful, structured output
- Designing clean client–server interactions
- Handling authentication and user state
- Storing and querying relational data
- Thinking through architecture and tradeoffs

I used modern AI-assisted development tools (Cursor) to move faster, but I stayed fully involved in the design, logic, and debugging of the system.

---

## What it does

- **Generates personalized workouts**
  - Based on equipment, exercise type, and reps
- **User accounts**
  - Register, log in, and log out
- **Save workouts**
  - Keep workouts you like for later
- **Track progress**
  - Log sets and reps
  - View workout and progress history
- **Exercise demos**
  - Embedded YouTube videos for form guidance
- **Simple, clean UI**
  - SPA-style navigation with dynamic views

---

## Tech stack

**Frontend**
- HTML
- CSS
- Vanilla JavaScript (Fetch API, async/await)

**Backend**
- Python
- Flask
- Flask-Login for authentication
- SQLAlchemy for database access

**Database**
- SQLite

---

## How it’s put together

- **Client**: Handles user input, state, and rendering
- **API**: Flask endpoints for authentication, workout generation, and persistence
- **Business logic**: Workout engine decides what to generate
- **Database**: Relational schema for users, workouts, and progress logs
- **Auth**: Session-based authentication with protected routes

---

## Project structure

├── app.py               # Flask app + API routes
├── models.py            # Database models (User, Workout, ProgressLog)
├── workout_engine.py    # Workout generation logic
├── index.html           # Frontend entry point
├── requirements.txt
├── static/
│   ├── css/
│   │   └── style.css
│   └── js/
│       └── app.js
├── workout.db           # SQLite database (created on first run)
├── LICENSE
├── README.md
└── .github/
    └── workflows/
        └── ci.yml
