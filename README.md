# Backend Project - Hexagonal Architecture with CQRS and Bundle-Contexts

This project demonstrates a complete backend system built with the following technologies and methodologies:

- **Hexagonal Architecture:** Clear separation of concerns between application layers
- **CQRS (Command Query Responsibility Segregation):** Separation of write and read operations
- **Contexts:** Two main contexts, `users` and `auth`, to handle user management and authentication respectively
- **RabbitMQ:** Asynchronous command processing
- **FastAPI:** For the presentation layer (API)
- **SQLAlchemy & PostgreSQL:** ORM and relational database
- **Alembic:** Database migrations
- **Unit Testing:** Implemented with `pytest` and `pytest-cov`

## Requirements

- **Docker** and **Docker Compose** for running the application
- **Python 3.9+** (optional, for local development without Docker)

## Setup and Run

### Using Docker



Build and run the application:

```bash
docker-compose up --build
```

The application will be available at http://localhost:8000.

### Local Development

Install dependencies:

```bash
pip install -r requirements.txt
```

Start the development server:

```bash
uvicorn src.main:app --reload
```

## API Endpoints

### Users Context
- POST /users: Create a new user
- GET /users/{user_id}: Retrieve user details by ID
- PUT /users/me: Update the profile of the authenticated user
- DELETE /users/me: Delete the authenticated user's account

### Auth Context
- POST /auth/login: Log in and get a JWT
- POST /auth/logout: Log out and invalidate a JWT (requires RabbitMQ for token blacklisting)

## Database and Migrations

Setup the database schema (if not already set up):

```bash
alembic upgrade head
```

Create new migrations:

```bash
alembic revision --autogenerate -m "Migration message"
```

## Core Concepts

### Hexagonal Architecture

The project adheres to the principles of hexagonal architecture:

Domain Layer contains the core business logic and use cases. Application Layer handles application-specific logic like orchestrating use cases or managing RabbitMQ commands. Infrastructure Layer implements persistence, messaging, and other integrations.

### CQRS

- Commands: Operations that modify data (create_user, update_user, delete_user)
- Queries: Operations that retrieve data (get_user_by_id)

## Environment Variables

Set the following environment variables in a .env file or your Docker environment:

```env
# RabbitMQ Configuration
RABBITMQ_HOST=localhost
RABBITMQ_PORT=5672
RABBITMQ_USER=guest
RABBITMQ_PASSWORD=guest

# JWT Configuration
JWT_SECRET=your_jwt_secret
JWT_ALGORITHM=HS256
JWT_EXPIRE_MINUTES=60

# Database Configuration
POSTGRES_USER=your_db_user
POSTGRES_PASSWORD=your_db_password
POSTGRES_DB=your_db_name
POSTGRES_HOST=localhost
POSTGRES_PORT=5432
```