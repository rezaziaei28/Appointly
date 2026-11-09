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

## Challenges I Faced and Solved

Building this project wasn't just about writing code. I ran into several real-world problems that took time to solve. Here are the main ones:

### 1. Custom User Model and OTP Authentication
Django's default User model uses usernames, but I needed phone number authentication. I had to create a custom `UserManager`, set `AUTH_USER_MODEL` in settings, and handle the migration process carefully to avoid conflicts with the built-in auth tables. I also implemented an OTP system that stores codes in the database and verifies them with a 2-minute expiration time.

### 2. Dynamic Booking Slots (Not Hardcoded)
Instead of hardcoding time slots in HTML, I built a system where doctors define their `WorkingHours` in the admin panel. The backend then calculates available 30-minute slots for the next 30 days, checks which ones are already booked, and sends them to the template. This ensures that only truly available times are shown to the patient.

### 3. Preventing Double Booking
When two users try to book the same slot simultaneously, we needed to prevent conflicts. I added a `UniqueConstraint` on the `Appointment` model for `(doctor, date, time)`. Now, the database itself rejects duplicate bookings at the same time, ensuring data integrity.

### 4. Docker and Database Migration Issues
While switching from SQLite to PostgreSQL in Docker, I faced `ModuleNotFoundError` and `DisallowedHost` errors. I fixed these by correctly configuring the `psycopg2-binary` package, setting the `DATABASES` host to the Docker service name (`db`), and adding `backend` to `ALLOWED_HOSTS`.

### 5. Doctor Panel Access Logic
When building the doctor dashboard, I had to make sure that only users who are actually registered as doctors can access it. I added a check in the view that looks up the `Doctor` model by the logged-in user. If the user is not a doctor, they are redirected to the patient panel with an error message.

## Future Roadmap

- Writing automated tests for the booking flow.
- Integrating a real SMS provider (like Kavenegar) for OTP delivery in production.
- Implementing an online payment gateway for booking fees.

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