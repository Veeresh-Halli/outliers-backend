# Outliers Backend

This document will guide you through the setup and installation process for the Outliers Backend project, which is built using Django Rest Framework (DRF). Follow these steps to get the project up and running on your local development environment.

## Prerequisites

Before you begin, ensure that you have the following prerequisites installed on your system:

- Python 3.9.0
- PostgreSQL (with a user and database configured)

## Getting Started

1. **Clone the Repository**:

   Clone the Outliers Backend project repository from GitHub using the following command:

   ```bash
   git clone https://github.com/Veeresh-Halli/outliers-backend.git
   ```

2. **Navigate to the Project Directory**:

   Change your working directory to the project folder:

   ```bash
   cd outliers-backend
   ```

3. **Create an Environment File (.env)**:

   In the project directory, create a file named .env and add the following environment variables:

   ```bash
   SECRET_KEY="ADD_SECRET_KEY_ANYTHING"
   DEBUG=True  # Use "True" in development mode
   DB_NAME=your_postgres_db_name
   DB_USER=your_postgres_user
   DB_PASSWORD=your_postgres_password
   DB_HOST=127.0.0.1  # Use "127.0.0.1" for the local PostgreSQL server
   DB_PORT=5432
   ```
   Replace your_postgres_db_name, your_postgres_user, and your_postgres_password with your PostgreSQL database details.

4. **Configure Allowed Hosts**:

   Open the settings.py file in the project directory. In the ALLOWED_HOSTS list, add the following entries:

   ```bash
   ALLOWED_HOSTS = ['localhost', '127.0.0.1']
   ```

5. **Configure CORS Allowed Hosts**:

   In the same settings.py file, locate the CORS_ALLOWED_HOSTS setting and add the following entries:

   ```bash
   CORS_ALLOWED_HOSTS = [
   'http://localhost:3000',
   'http://127.0.0.1:3000',
   ]
   ```

6. **Install Dependencies**:

   Install the project dependencies using pip:

   ```bash
   pip install -r requirements.txt
   ```

7. **Database Migration**:

   Apply the database migrations to create the necessary database tables:

   ```bash
   python manage.py migrate
   ```

8. **Run the Development Server**:

   Start the development server:

   ```bash
   python manage.py runserver
   ```
   You should see output indicating that the server is running at `http://127.0.0.1:8000/`.