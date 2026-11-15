# Appointly

A doctor appointment booking system built with Django. I made this as a personal project to practice building a full-stack app with real-world features.

## About This Project

The main idea is to let patients book doctor appointments online without calling the clinic. Right now the core parts are done — you can sign up with your phone number, browse doctors, and book a time slot. Doctors also have their own panel to manage their schedule and see upcoming appointments.

This project is still growing. I am actively adding new features and improving the codebase as I learn more.

## Features

Here is what the project can do right now:

**For Patients:**
- Login and sign up just with a phone number (OTP)
- Search doctors and filter them by specialty
- See doctor profiles and visit fees
- Book an appointment (time slots are generated based on the doctor's working hours)
- Patient dashboard to see and cancel appointments

**For Doctors:**
- Separate login flow
- Complete profile (name, specialty, address, fee)
- Set weekly working hours and capacity
- See upcoming appointments for the next 30 days

**UI/UX:**
- Dark and light mode
- Fully responsive (mobile and desktop)
- Persian (RTL) support
- Searchable dropdown for specialties (because there can be 100+ of them)

## Tech Stack

- **Backend:** Python, Django
- **Database:** PostgreSQL
- **Frontend:** HTML, Tailwind CSS, Vanilla JavaScript
- **DevOps:** Docker, Docker Compose

## Challenges I Faced and Solved

Building this project wasn't just about writing code. I ran into several real-world problems that took time to solve. Here are the main ones:

### 1. Custom User Model and OTP Authentication
Django's default User model uses usernames, but I needed phone number authentication. I had to create a custom `UserManager`, set `AUTH_USER_MODEL` in settings, and handle the migration process carefully to avoid conflicts with the built-in auth tables. I also implemented an OTP system that stores codes in the database and verifies them with a 2-minute expiration time.

### 2. Dynamic Booking Slots and Doctor Capacity
Instead of hardcoding time slots in HTML, doctors define their `WorkingHours` and a `capacity` (the number of patients they want to see) in the panel. The backend then calculates the time slots dynamically by dividing the total working minutes by the capacity. For example, if a doctor works for 2 hours with a capacity of 4, the system creates four 30-minute slots. It checks which ones are already booked and sends the available ones to the template.

### 3. Preventing Double Booking
When two users try to book the same slot simultaneously, we needed to prevent conflicts. I added a `UniqueConstraint` on the `Appointment` model for `(doctor, date, time)`. Now, the database itself rejects duplicate bookings at the same time, ensuring data integrity.

### 4. Docker and Database Migration Issues
While switching from SQLite to PostgreSQL in Docker, I faced `ModuleNotFoundError` and `DisallowedHost` errors. I fixed these by correctly configuring the `psycopg2-binary` package, setting the `DATABASES` host to the Docker service name (`db`), and adding `backend` to `ALLOWED_HOSTS`.

### 5. Doctor Registration Flow
Patients only need a name, but doctors need a lot more info. So I made a separate flow for doctors: after OTP verification, if they don't have a profile yet, they get redirected to a form to fill in their specialty, address, etc. Then I added a check in the doctor dashboard view to make sure only actual doctors can access it. If a normal user tries, they get redirected to the patient panel with an error message.

### 6. Fixing the Doctor Panel Form
When I first built the doctor panel, I had a bug where saving the schedule would crash because the view didn't return an HTTP response. I realized it was because I forgot to add a hidden input (`update_schedule`) to the form. After adding it and a fallback redirect in the view, it worked perfectly.

### 7. Doctor Access Check in Login
When building the doctor login, I first tried to check if a phone number belonged to a doctor by using `is_doctor=True` in the user query. But I got a `FieldError` because my custom `User` model doesn't have an `is_doctor` field. Instead, doctors are linked to users with a `OneToOneField`. To fix it, I used `hasattr(user, 'doctor')` to check if the relationship exists. It was a good lesson on how Django handles reverse relations and how to avoid adding unnecessary fields to the database.

### 8. Empty Images Crashing the Panel
After I added the image upload for doctors, the panel crashed with a `ValueError` saying `The 'image' attribute has no file associated with it`. I realized that when a doctor signs up, they don't have an image yet, but my template was trying to access `doctor.image.url` directly. I fixed it by wrapping the image tag with `{% if doctor.image %}` and showing a default emoji or placeholder instead. Now the panel works fine even if the doctor hasn't uploaded a photo yet.

## Tests

I wrote 15 tests covering the main parts:
- User creation and profile signals
- OTP generation and expiry
- Login and register views
- Panel access permissions (making sure patients can't access the doctor panel)
- Doctor and appointment models

I am still adding tests for the booking flow itself, like double booking and cancellation.


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


## Current Status

The core features of the project are complete. I built this mainly to practice building a real-world Django application, and I'm happy with how it turned out. The project is currently stable and I might add more features in the future if I have time, but the main goals are achieved.

## License

MIT License

Copyright (c) 2026 Zia Ziaei