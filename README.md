# Inventory Management System API
## Project Overview
This project is a Backend API for an Inventory Management System built using Django Rest Framework (DRF). It provides secure CRUD operations on inventory items, supports JWT-based authentication, and incorporates Redis caching to enhance performance.

## Features
#### Secure Authentication: JWT-based user authentication.
#### CRUD Functionality: Create, Read, Update, and Delete inventory items.
#### Redis Caching: Frequently accessed items are cached for performance.
#### Logging: Tracks API usage and errors.
#### Unit Testing: Comprehensive unit tests for all API endpoints.


## Tech Stack
#### Backend Framework: Django Rest Framework
#### Database: PostgreSQL
#### Caching: Redis
#### Authentication: JWT (JSON Web Tokens)
#### Testing: Django Test Framework

## Setup Instructions
### Prerequisites
Python 3.8 or higher  
PostgreSQL  
Redis  
Virtual Environment (recommended)

#### 1. Clone the Repository
git clone https://github.com/yourusername/inventory-management-api.git  
cd inventory-management-api

#### 2. Create and Activate a Virtual Environment
python -m venv venv  
venv\Scripts\activate

#### 3. Install Required Packages
pip install -r requirements.txt

#### 4. Set Up PostgreSQL Database
##### Create a new PostgreSQL database:
CREATE DATABASE inventory_db;  
CREATE USER db_user WITH PASSWORD 'db_password';  
GRANT ALL PRIVILEGES ON DATABASE inventory_db TO db_user;  

##### Update settings.py with your database credentials:
DATABASES = {  
    'default': {  
        'ENGINE': 'django.db.backends.postgresql',  
        'NAME': 'inventory_db',  
        'USER': 'db_user',  
        'PASSWORD': 'db_password',  
        'HOST': 'localhost',  
        'PORT': '5432',  
    }  
}


#### 5. Apply Migrations
python manage.py makemigrations  
python manage.py migrate


#### 6. Run Redis Server
Ensure Redis is installed and running:  
redis-server

#### 7. Run the Development Server
python manage.py runserver  

## API Endpoints 
#### Authentication Endpoints:
POST `/api/token/`: Obtain JWT token.  
POST `/api/token/refresh/`: Refresh JWT token.  

#### CRUD Endpoints (/api/items/):
POST `/api/items/`: Create a new item.  
GET `/api/items/<item_id>/`: Get details of an item (supports Redis caching).  
PUT `/api/items/<item_id>/`: Update item details.  
DELETE `/api/items/<item_id>/`: Delete an item.  

## Request Example:

POST `/api/items/`  
{  
    "name": "Test item",  
    "description": "Test description."  
}  


## Running Tests
python manage.py test  

Logging
The logging configuration is set up in settings.py. API usage, errors, and other significant events will be logged to a file named debug.log.  

| Project Structure |
|------------------|
| inventory_management/
│
├── inventory_backend/        # Main Django app folder
│   ├── __init__.py
│   ├── settings.py
│   ├── urls.py
│   ├── wsgi.py
│
├── items/                    # App to manage inventory items
│   ├── __init__.py
│   ├── admin.py
│   ├── apps.py
│   ├── models.py
│   ├── serializers.py
│   ├── views.py
│   ├── urls.py
│   ├── tests.py
│
└── manage.py |

## Deployment
To deploy this project, consider using Docker or platforms like Heroku or AWS.

## Contributing
Feel free to open an issue or submit a pull request if you find a bug or have suggestions for improvement.

Let me know if you need any adjustments or additional details in this README!
