# 🚚 RouteMaster — Route & Delivery Management System
![Python](https://img.shields.io/badge/Python-3.10%2B-blue?logo=python)
![Django](https://img.shields.io/badge/Django-6.0.1-green?logo=django)
![License](https://img.shields.io/badge/License-MIT-yellow)
![PostgreSQL](https://img.shields.io/badge/Database-PostgreSQL-336791?logo=postgresql)
![WhiteNoise](https://img.shields.io/badge/Static-WhiteNoise-lightgrey)
![AWS](https://img.shields.io/badge/Deployed-AWS-orange?logo=amazon-aws)

**RouteMaster** is a Django-based web application for managing logistics operations — all from a single, easy-to-use interface.

🌐 **Live Demo**: [http://13.63.13.75](http://13.63.13.75)

---

## 📋 Table of Contents

- [Features](#-features)
- [Tech Stack](#-tech-stack)
- [Apps & System Overview](#-apps-and-system-overview)
- [User Roles & Permissions](#-user-roles--permissions)
- [REST API](#-rest-api)
- [Screenshots](#-screenshots)
- [Dependencies](#-dependencies)
- [Project Structure](#-project-structure)
- [Getting Started](#-getting-started)
- [Running the App](#-running-the-app)
- [Setting Up PostgreSQL](#-setting-up-postgresql)
- [Static Files with WhiteNoise](#-static-files-with-whitenoise)
- [License](#-license)

---

## ✨ Features

- **Driver Management** – Manages drivers and driver specializations
- **Vehicle Management** – Manages a fleet of vehicles
- **Route Planning** – Define and manage routes, delivery points and assignments
- **Admin Panel** – Manage all data through Django's built-in admin interface
- **User Authentication** – Register, login, and logout functionality
- **Role-Based Permissions** – Different access levels based on user group
- **REST API** – Admin-only endpoint built with Django REST Framework
- **Dark Mode** – Registered users can toggle between light and dark theme, with their preference saved to their profile

---

## 🗂 Apps and System Overview

### `accounts`
Handles everything related to register, login and logout users

### `common`
Contains utility functions, and any cross-app models or mixins. Other apps import from here to avoid code duplication.

### `drivers`
Handles everything related to drivers.

### `vehicles`
Manages the vehicle fleet. Includes vehicle registration, type categorization, capacity info.

### `routes`
The core of the application. Allows planners to create, update and delete Delivery Points, Routes and Assignments (assign vehicles and drivers to routes).


- Each **Route** consists of multiple **Delivery Points**
- **Assignments** link Drivers and Vehicles to specific Routes
- The system ensures organized planning and execution of deliveries

---


## 👥 User Roles & Permissions

The application supports user registration, login, and logout. Once registered, users are assigned to a group that determines their access level.

| Action | Anonymous | Registered (no group) | Drivers group | Managers group |
|---|---|---|---|---|
| View public pages | ✅ | ✅ | ✅ | ✅ |
| Register / Login | ✅ | — | — | — |
| View lists | ❌ | ✅ | ✅ | ✅ |
| View details | ❌ | ❌ | ✅ | ✅ |
| Create / Edit / Delete | ❌ | ❌ | ❌ | ✅ |

---

## 🔌 REST API

RouteMaster includes a RESTful API endpoint built with **Django REST Framework**.

### Endpoint

| Method | URL | Description | Permission |
|---|---|---|---|
| GET | `/accounts/api/users/` | Returns a list of all registered users | Admin only |

### Example Response

```json
[
    {
        "employee_id": "000001",
        "first_name": "Manager",
        "last_name": "One",
        "email": "manager@routemaster.com"
    },
    {
        "employee_id": "000002",
        "first_name": "Driver",
        "last_name": "One",
        "email": "driver@routemaster.com"
    }
]
```

> 🔒 This endpoint requires the requesting user to be a Django superuser (`IsAdminUser` permission).

---

## 📸 Screenshots

<table> <tr> <td align="center"> 
<img src="docs/images/HomePage.png" width="500" alt="Home Page"/><br> 
<sub>Home Page</sub> </td> <td align="center"> 
<img src="docs/images/ListPage.png" width="500" alt="List Page"/><br> 
<sub>List Page</sub> </td> </tr> </table>
<table> <tr> <td align="center"> 
<img src="docs/images/DetailsPage.png" width="500" alt="Details Page"/><br> 
<sub>Details Page</sub> </td> <td align="center"> 
<img src="docs/images/AddPage.png" width="500" alt="Add Page"/><br> 
<sub>Add Page</sub> </td> </tr> </table>
<table> <tr> <td align="center"> 
<img src="docs/images/EditPage.png" width="500" alt="Edit Page"/><br> 
<sub>Edit Page</sub> </td> <td align="center"> 
<img src="docs/images/DeletePage.png" width="500" alt="Delete Page"/><br> 
<sub>Delete Page</sub> </td> </tr> </table>

---

## 🛠 Tech Stack

| Layer | Technology |
|------------|-------------------------------------|
| Backend | Python / Django |
| REST API | Django REST Framework |
| Frontend | HTML / Django Templates / Bootstrap |
| Database | PostgreSQL |
| Static Files | Whitenoise |
| Deployment | AWS EC2 |

---

## 📁 Project Structure
```
logistics-delivery-planner/
│
├── logisticsDeliveryPlanner/   # Main Django project settings
├── accounts/                   # Accounts management app
├── common/                     # Shared utilities, base models, mixins
├── drivers/                    # Drivers management app
├── vehicles/                   # Vehicles management app
├── routes/                     # Routes, Delivery Points and Assignments management app
├── templates/                  # HTML templates
├── static/                     # Static assets (images)
├── manage.py
├── requirements.txt            # Project dependencies
├── .env-example                # Example environment config
└── README.md
```

---

## 📦 Dependencies

All dependencies are listed in `requirements.txt`. Here's what each one does:

| Package | Version | Description |
|---|---|---|
| `Django` | 6.0.1 | The core web framework powering the entire application |
| `djangorestframework` | 3.17.1 | Toolkit for building RESTful APIs with Django — used for the admin users endpoint |
| `asgiref` | 3.11.0 | ASGI compatibility layer required by Django for async support |
| `psycopg2-binary` | 2.9.11 | PostgreSQL database adapter for Python — connects Django to your Postgres database |
| `python-dotenv` | 1.2.1 | Loads environment variables from the `.env` file into the app at runtime |
| `sqlparse` | 0.5.5 | SQL query formatter used internally by Django for readable query output |
| `tzdata` | 2025.3 | Timezone database used by Django for accurate timezone handling across environments |
| `whitenoise` | 6.11.0 | Serves static files directly from Django when `DEBUG = False`, without needing a separate web server like Nginx |

---

## 🚀 Getting Started

### Prerequisites

- Python 3.10+
- pip
- virtualenv (recommended)
- PostgreSQL (see [Setting Up PostgreSQL](#-setting-up-postgresql))

### Installation

**1. Clone the repository**
```bash
git clone https://github.com/Milenski1987/logistics-delivery-planner.git
cd logistics-delivery-planner
```

**2. Create and activate a virtual environment**

* *Windows:*
```bash
    python -m venv venv
    venv\Scripts\activate
```
* *macOS/Linux:*
```bash
    python3 -m venv venv
    source venv/bin/activate
```

**3. Install dependencies**
```bash
pip install -r requirements.txt
```

**4. Set up environment variables**

Create a `.env` file in the root directory (next to `manage.py`). You can copy the example file:
```bash
cp .env-example .env
```

Then fill in your values:

| Variable | Example Value | Description                                                                                                 |
|---|---|-------------------------------------------------------------------------------------------------------------|
| `SECRET_KEY` | `django-insecure-xxxx...` | Django's secret key used for cryptographic signing. Generate a new one for production — never share it publicly |
| `DEBUG` | `True` | Controls debug mode — set to `False` in production                                                          |
| `DB_NAME` | `routemaster` | Name of your PostgreSQL database                                                                            |
| `DB_USER` | `routemaster_user` | PostgreSQL username with access to the database                                                             |
| `DB_PASSWORD` | `your_password` | Password for the PostgreSQL user                                                                            |
| `DB_HOST` | `127.0.0.1` | Database host — use `127.0.0.1` for local development                                                       |
| `DB_PORT` | `5432` | Database port — `5432` is the PostgreSQL default
| `ALLOWED_HOSTS` | `127.0.0.1,localhost` | Comma-separated list of allowed hosts — add your server IP or domain in production |
| `CSRF_TRUSTED_ORIGINS` | `http://127.0.0.1,http://localhost` | Trusted origins for CSRF protection — add your server URL in production ||


> 💡 To generate a secure `SECRET_KEY` for production, run:
> ```bash
> python -c "from django.core.management.utils import get_random_secret_key; print(get_random_secret_key())"
> ```

---


**5. Apply migrations (added data migration to populate database)**
```bash
python manage.py migrate
```

Demo users created via migration:

Superuser<br>
employee_id: 000000<br>
password: admin123

Manager<br>
employee_id: 000001<br>
password: manager123

Driver<br>
employee_id: 000002<br>
password: driver123

---

**6. Create a superuser (optional)**
```bash
python manage.py createsuperuser
```

**7. Collect static files**
```bash
python manage.py collectstatic
```

---

## ▶️ Running the App
```bash
python manage.py runserver
```

Then open your browser at: [http://127.0.0.1:8000](http://127.0.0.1:8000)

The admin panel is available at: [http://127.0.0.1:8000/admin](http://127.0.0.1:8000/admin)

---


## 🐘 Setting Up PostgreSQL

### 1. Install PostgreSQL

**macOS (Homebrew):**
```bash
brew install postgresql@15
brew services start postgresql@15
```

**Ubuntu / Debian:**
```bash
sudo apt update
sudo apt install postgresql postgresql-contrib
sudo systemctl start postgresql
sudo systemctl enable postgresql
```

**Windows:**

Download and run the installer from [postgresql.org/download/windows](https://www.postgresql.org/download/windows/)

---

### 2. Create the Database and User

Open the PostgreSQL shell:
```bash
# macOS / Linux
psql postgres

# Ubuntu (switch to the postgres system user first)
sudo -u postgres psql
```

Then run the following SQL commands:
```sql
CREATE DATABASE database_name_of_your_choice;
CREATE USER username_of_your_choice WITH PASSWORD 'passowrd_of_your_choice';
ALTER ROLE username_of_your_choice SET client_encoding TO 'utf8';
ALTER ROLE username_of_your_choice SET default_transaction_isolation TO 'read committed';
ALTER ROLE username_of_your_choice SET timezone TO 'UTC';
GRANT ALL PRIVILEGES ON DATABASE database_name_of_your_choice TO username_of_your_choice;
\q
```

Replace 'database_name_of_your_choice' with name you want for your database.

Replace 'username_of_your_choice' with name you want for your username.

Replace 'passowrd_of_your_choice' with paswword you want for your username password.

---

### 3. Configure `settings.py`

Make sure your `DATABASES` setting reads from your `.env` file:
```python
import os
from dotenv import load_dotenv

load_dotenv()

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': os.getenv('DB_NAME'),
        'USER': os.getenv('DB_USER'),
        'PASSWORD': os.getenv('DB_PASSWORD'),
        'HOST': os.getenv('DB_HOST'),
        'PORT': os.getenv('DB_PORT'),
    }
}
```

---

## 🗂 Static Files with WhiteNoise

In production, Django doesn't serve static files (CSS, JS, images) on its own — it expects a dedicated web server like Nginx to handle that. For a project of this scale, setting up a separate server just for static files adds unnecessary complexity.

**WhiteNoise** solves this by letting Django serve its own static files efficiently, with no extra infrastructure needed.

**How it's used in this project:**

WhiteNoise is registered as a middleware in `settings.py`, placed directly after Django's `SecurityMiddleware`:
```python
MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'whitenoise.middleware.WhiteNoiseMiddleware',  # serves static files in production
    ...
]
```

Static files are collected into `staticfiles/` via `collectstatic` and served from there:
```python
STATIC_URL = 'static/'
STATIC_ROOT = BASE_DIR / 'staticfiles'   # where WhiteNoise serves files from
STATICFILES_DIRS = [BASE_DIR / 'static'] # your source static files
```

`DEBUG` is controlled via the `.env` file and read in `settings.py` like this:
```python
DEBUG = os.getenv('DEBUG', 'True') == 'True'
```

- Local development → set `DEBUG=True` in your `.env`
- Production → set `DEBUG=False` in your `.env` — WhiteNoise will then take over static file serving automatically

---


## 📄 License

This project is licensed under the [MIT License](LICENSE).