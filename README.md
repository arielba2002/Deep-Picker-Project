# FastAPI PostgreSQL

This project uses **FastAPI** for the backend and **PostgreSQL** as the database. Follow the steps below to set up the development environment, configure PostgreSQL, and run the backend server.

---

## Prerequisites

Before you begin, make sure you have the following installed:

- **Docker**: For running PostgreSQL in a container.
- **Python**: Version 3.7 or above.
- **Poetry**: Dependency management and packaging tool for Python.

If you don’t have these tools installed, refer to the official documentation:
- [Docker installation](https://docs.docker.com/get-docker/)
- [Python installation](https://www.python.org/downloads/)
- [Poetry installation](https://python-poetry.org/docs/)

---

## Step 1: Set Up PostgreSQL with Docker

1. **Pull the PostgreSQL Docker Image**

   To run PostgreSQL in a container, first pull the official PostgreSQL image:

   ```bash
   docker pull postgres

2. **Run PostgreSQL Container**
   ```bash
   docker run --name my-postgres -e POSTGRES_USER=myuser -e POSTGRES_PASSWORD=mypassword -e POSTGRES_DB=mydb -p 5432:5432 -d postgres

## Step 2: Set Up Python Backend

1. **Create Virtual Environment**
  From the root of the project, run the following command to create a new virtual environment:
   ```bash
   python -m venv ./venv
   ```
   This command will create a new directory called venv in the current directory, which will contain the virtual environment for your project.

2. **Activate Virtual Environment**
   - **Linux**:
     ```bash
     source venv/bin/activate
     ```
   - **Windows (Command Prompt)**:
     ```bash
     venv\Scripts ctivate
     ```
   - **Windows (Git Bash)**:
     ```bash
     source venv/Scripts/activate
     ```

3. **Install Required Libraries**
   To install the project dependencies, use Poetry to install them:
   ```bash
   poetry install
   ```
   This will install all the necessary dependencies as defined in the pyproject.toml file.

## Step 3: Run the FastAPI Application
   Once the dependencies are installed, run the FastAPI server using Poetry:
   ```bash
   poetry run start
   ```
   This will start the FastAPI application with the command defined in the pyproject.toml file.



## Step 4: Deactivate the virtual environment
**When you're done working in your project, you can deactivate the virtual environment by running:**
   ```bash
   deactivate
   ```


# Frontend - React
To get the frontend up and running, From the frontend folder, Follow the steps below:

## Step 1: Install Dependencies
   ```bash
   npm install
   ```

## Step 2: Start the Server
   ```bash
   npm start
   ```
