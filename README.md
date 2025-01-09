# FastAPI PostgreSQL Setup

This project uses **FastAPI** for the backend and **PostgreSQL** as the database. Follow the steps below to set up the development environment, configure PostgreSQL, and run the backend server.

---

## Prerequisites

Before you begin, make sure you have the following installed:

- **Docker**: For running PostgreSQL in a container.
- **Python**: Version 3.7 or above.
- **pip**: Python package manager.
- **Uvicorn**: ASGI server for FastAPI.

If you don’t have these tools installed, refer to the official documentation:
- [Docker installation](https://docs.docker.com/get-docker/)
- [Python installation](https://www.python.org/downloads/)
- [Uvicorn installation](https://www.uvicorn.org/)

---

## Step 1: Set Up PostgreSQL with Docker

1. **Pull the PostgreSQL Docker Image**

   To run PostgreSQL in a container, first pull the official PostgreSQL image:

   ```bash
   docker pull postgres

2. **Run PostgreSQL Container**
   docker run --name my-postgres -e POSTGRES_USER=myuser -e POSTGRES_PASSWORD=mypassword -e POSTGRES_DB=mydb -p 5432:5432 -d postgres

## Step 2: Set Up Python Backend

1. **Create Virtual Environment**

   To run PostgreSQL in a container, first pull the official PostgreSQL image:

   ```bash
   docker pull postgres

2. **Activate Virtual Environment**
   source venv/bin/activate (Linux)
   venv\Scripts\activate (Windows)

3. **Install Required Libraries**
   pip install fastapi[all] sqlalchemy asyncpg databases pydantic psycopg2-binary uvicorn python-dotenv

## Step 3: Run the FastAPI Application
   uvicorn app.main:app --reload

## Step 4: Deactivate the virtual environment
1. **When you're done working in your project, you can deactivate the virtual environment**
   deactivate



