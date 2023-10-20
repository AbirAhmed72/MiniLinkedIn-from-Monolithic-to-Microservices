

# Distributed MiniLinkedIn

Distributed MiniLinkedIn is a microservices-based implementation of a social media platform, inspired by LinkedIn. This project was developed as part of the transition from a monolithic architecture to microservices.

## Project Structure

- **nginx:** Nginx acts as the reverse proxy server, routing requests to appropriate microservices.
- **user_service:** Manages user-related operations.
- **post_service:** Handles post creation and management.
- **notification_service:** Manages user notifications.
- **minio:** Provides object storage for the application.
- **mini-linkedin-final-frontend:** Client side for the application.

## Technologies Used

- **FastAPI:** FastAPI is a modern, fast (high-performance), web framework for building APIs with Python 3.7+.
- **PostgreSQL:** PostgreSQL is a powerful, open-source object-relational database system.
- **SQLAlchemy:** SQLAlchemy is a versatile ORM(Object Relational Mapper).
- **MinIO:** MinIO is a high-performance, distributed object storage system.
- **React.js:** React.js is a client-side javascript framework.
- **Docker** Docker is a containerization tool.
- **docker-compose** docker-compose is an orchestration tool.

## Setup and Installation

1. Build and start the services(from the Distributed_MiniLinkedIn folder):

    ```bash
    docker-compose up
    ```

2. Access the application:

   - Type localhost in your browser

## Usage

- **User Service:** Manages user profiles, authentication, and registration
- **Post Service:** Handles posts(texts and/or images)
- **Notification Service:** Manages user notifications.


---

Feel free to customize the content further based on your specific project details and requirements.