# Appointly

A modern doctor appointment booking platform built with Django. This is a full-stack personal project to practice building a real-world application with a focus on clean architecture and user experience.

## About This Project

Appointly is designed to make booking doctor appointments simple and fast. Users can browse doctors, view their profiles, and book available time slots without needing to make a phone call. 

*Note: This project is currently in progress. I am actively building the backend logic, database structure, and OTP authentication system.*

## Current Progress

- **Frontend:** Fully responsive UI with dark/light theme, mobile menu, OTP input handling, and custom animations (built with Tailwind CSS and Vanilla JavaScript).
- **Backend:** Switched to PostgreSQL for production-ready database management.
- **Authentication:** Custom User model designed for phone number authentication (OTP-based) instead of traditional usernames.

## Tech Stack

- **Backend:** Python, Django
- **Database:** PostgreSQL
- **Frontend:** HTML, Tailwind CSS, Vanilla JavaScript
- **DevOps:** Docker, Docker Compose

## What I Learned & Challenged

*(This section will be updated as I build the backend)*

- **Database Migration:** Transitioned from SQLite to PostgreSQL inside Docker, handling custom user models and migration dependencies.
- **Custom Authentication:** Designed a custom User model using `AbstractUser` to allow phone number login and a custom `UserManager`.

## How to Run This Project

### Using Docker

```bash
git clone https://github.com/rezaziaei28/Appointly.git
docker-compose up --build
docker-compose exec backend python manage.py migrate
docker-compose exec backend python manage.py createsuperuser
```

## Then open 
http://localhost:8000 


## License

MIT License

Copyright (c) 2026 Zia Ziaei