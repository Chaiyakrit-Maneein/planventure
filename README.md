# Planventure API

The **Planventure API** is a Flask-based RESTful backend for managing users and trips, featuring secure JWT authentication, user registration/login, and CRUD operations for trip planning. It is designed for easy integration with frontend applications and supports modern development workflows.

---

## Table of Contents

- [Features](#features)
- [Project Structure](#project-structure)
- [Getting Started](#getting-started)
  - [Prerequisites](#prerequisites)
  - [Installation](#installation)
  - [Environment Variables](#environment-variables)
  - [Database Initialization](#database-initialization)
  - [Running the Server](#running-the-server)
- [API Endpoints](#api-endpoints)
  - [Authentication](#authentication)
  - [Trips](#trips)
- [Authentication](#authentication-details)
- [Error Handling](#error-handling)
- [Development](#development)
- [Troubleshooting](#troubleshooting)
- [License](#license)

---

## Features

- User registration and login with email validation
- Secure password hashing (bcrypt)
- JWT-based authentication for protected routes
- CRUD operations for trips (create, read, update, delete)
- Per-user trip isolation
- Configurable via `.env` file
- CORS support for frontend integration
- Database migrations with Flask-Migrate

---

## Getting Started

### Prerequisites

- Python 3.8+
- pip
- (Recommended) [virtualenv](https://virtualenv.pypa.io/)
- SQLite (default) or PostgreSQL (with config changes)

---

### Installation

1. **Clone the repository:**

   ```sh
   git clone https://github.com/your-org/planventure.git
   cd planventure/planventure-api
   ```

2. Create a virtual environment and activate it:

   ```sh
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. Install the required dependencies:

   ```sh
   pip install -r requirements.txt
   ```

---

### Environment Variables

4. Create an `.env` file based on [.sample.env](/planventure-api/.sample.env):

   ```sh
   cp .sample.env .env
   ```

---

### Database Initialization

5. Initialize the database:

   ```sh
   flask db init
   flask db migrate
   flask db upgrade
   ```

---

### Running the Server

6. Start the Flask development server:

   ```sh
   flask run
   ```

---

## 📚 API Endpoints

### Authentication

- POST /auth/register - Register a new user
  {
  "email": "user@example.com",
  "password": "Test1234"
  }
- POST /auth/login - Login and receive a JWT token
  - Example request body:
    ```json
    {
      "email": "user@example.com",
      "password": "Test1234"
    }
    ```
  - Example response:
    ```json
    {
      "message": "Login successful",
      "token": "<JWT_TOKEN>",
      "user": {
        "id": 1,
        "email": "user@example.com"
      }
    }
    ```
- GET /logout - User logout

### Trips

Authentication Details
JWT tokens are issued on login and must be sent in the Authorization header for protected endpoints:
Tokens expire after 24 hours by default (configurable).

All trip endpoints require the Authorization: Bearer <your_token> header.

- GET /api/trips - Retrieve all trips for the authenticated user
- POST /api/trips - Create a new trip
  - Example request body:
    ```json
    {
      "name": "Summer Vacation",
      "destination": "Beach Resort",
      "description": "Trip to the beach with friends",
      "start_date": "2025-06-01",
      "end_date": "2025-06-03"
    }
    ```
- PUT /api/trips/<id> - Update an existing trip
- DELETE /api/trips/<id> - Delete a trip

---

## Error Handling

### Authentication Errors

- Example response for invalid authentication token:
  ```json
  {
    "error": {
      "code": "AUTH_002",
      "message": "Invalid authentication token. Please log in again.",
      "status": 401
    }
  }
  ```
  Development
  CORS is enabled for http://localhost:3000 by default (see config/cors_config.py).

Migrations: Use Flask-Migrate for schema changes:
flask db init
flask db migrate
flask db upgrade

Testing: Use Bruno or Postman for API testing. Example requests are in the login/ and planventure-api/planventure-api/ folders.

Troubleshooting
-Database file errors: Ensure the instance/ directory exists and is writable.
-Token errors: Make sure the same JWT_SECRET_KEY is used for both token generation and verification.
-CORS issues: Update allowed origins in cors_config.py.
-Environment variables: Double-check your .env file and restart the server after changes.

---

## 📝 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.
