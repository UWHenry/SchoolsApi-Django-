# Project README
This README provides instructions and information for setting up and running the project. The project uses Docker Compose to orchestrate the deployment of multiple services, including a Django backend, a PostgreSQL database, and Nginx for routing.

This project creates backend restful apis:
* CRUD endpoints are created for schools, courses, administrators, teachers and students
    * administrators, courses, teachers and students are related to 1 school
    * A course can have 0 to 1 teachers and 0 to many students 
* ```GET /api/schools/:schoolId:/stats``` returns the school's stats
* ```POST /api/transfer``` moves a student from one class to another

## Table of Contents
* [Prerequisites](#prerequisites)
* [Installation](#installation)
* [Usage](#usage)
* [Technologies Used](#technologies-used)
* [Project Structure](#project-structure)

## Prerequisites
Before you proceed, make sure you have the following installed on your machine:
* Docker & Docker Compose: https://www.docker.com/get-started
  
## Installation
1. Clone the repository to your local machine:
    ```bash
    git clone <repository_url>
    cd <repository_directory>
    ```
2. Build and start the services using Docker Compose:
   ```bash
   docker compose up -d
   ```

## Usage
Once the services are up and running, you can access the application through a web browser.
* Backend API: https://localhost/
* Swagger API documentation: https://localhost/swagger

## Technologies Used
* Django: Backend framework for building the API.
    * Django Rest Framework for restful APIs
    * drf_yasg for swagger documentation
    * Django Cors Header for cors
* PostgreSQL: Database management system.
* Nginx: Web server and reverse proxy server.

## Project Structure
* project/: Contains the Flask backend application.
* nginx/: Contains Nginx configuration files.
* docker-compose.yml: Defines the services and their configurations.