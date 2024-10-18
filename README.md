# Starnavi Project

## Overview

    This is a test task for Starnavi on position "Python Developer". Author: Stepanenko Daniil Romanovich

## Setup

### Using SQLite

**Clone the Repository**:

    git clone https://github.com/excommunicades/Starnavi.git
    cd Starnavi

### Install Dependencies: Make sure to have a virtual environment set up, then run:

    pip install -r requirements.txt
    

    DEBUG = True

    ALLOWED_HOSTS = []

    DATABASES = {
        'default': {
            'ENGINE': 'django.db.backends.sqlite3',
            'NAME': BASE_DIR / 'db.sqlite3',
        }
    }

#### Execute to run tests:  
    pytest posts/tests/ -v

    Run the Development Server: Start the server with the following command: python3 manage.py runserver 
    Run the Development Server: Start the server with the following command: python manage.py runserver

##### You can access the application at http://127.0.0.1:8000/.

# Using Docker with PostgreSQL

    git clone https://github.com/excommunicades/Starnavi.git
    cd Starnavi

### env-file:

    # DB Settings
    POSTGRES_DB=Starnavi
    POSTGRES_USER=postgres
    POSTGRES_PASSWORD=12345
    
    # DJANGO Settings
    DJANGO_SETTINGS_MODULE=Starnavi.settings

### DJANGO Settings


    Configure settings.py: Ensure your settings.py file contains the following configurations for PostgreSQL:

    DEBUG = False

    ALLOWED_HOSTS = ['0.0.0.0', 'localhost', '127.0.0.1']

    DATABASES = {
        'default': {
            'ENGINE': 'django.db.backends.postgresql',
            'NAME': os.getenv('POSTGRES_DB'),
            'USER': os.getenv('POSTGRES_USER'),
            'PASSWORD': os.getenv('POSTGRES_PASSWORD'),
            'HOST': 'db',
            'PORT': '5432',
        }
    }

### Build and Run the Docker Container: Run the following command to build and start the Docker containers:

    docker-compose up --build

##### Your application should now be accessible for example 1/3 at http://0.0.0.0:8000/. Or any other allowed hosts.
#
#
#
#
### Stop and down Docker Container: Run the following command to stop and down the Docker containers:
    docker-compose down
#
#
#
#
##### Follow the instructions for the setup that fits your needs—SQLite for quick local testing or Docker with PostgreSQL for a more production-like environment. If you encounter any issues, feel free to check the project documentation or raise an issue in the repository.

#
#
#
#
#