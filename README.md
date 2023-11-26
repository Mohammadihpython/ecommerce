[![Django CI](https://github.com/Mohammadihpython/ecommerce/actions/workflows/ci-cd.yml/badge.svg)](https://github.com/Mohammadihpython/ecommerce/actions/workflows/ci-cd.yml) ![Coverage](https://img.shields.io/badge/coverage-96%25-brightgreen)
# Ecommerce
A Django Shop API with Elastic Search
## Table of Contents
- [About](#about)
- [Features](#features)
- [Installation](#installation)
- [Usage](#usage)
- [Technologies Used](#technologies-used)
- [Contributing](#contributing)
- [License](#license)

## About
This project is an eCommerce platform built using Django and Django REST Framework, integrating Elasticsearch for product search functionality and OTP (One-Time Password) authentication. The project is containerized with Docker for easy setup and utilizes Celery for handling asynchronous tasks.


## Features

### 1. Product Search with Elasticsearch

- Implemented Elasticsearch for efficient and powerful product search.
- Enables users to search for products with autocomplete suggestions, filtering, and relevance-based results.

### 2. OTP Authentication

- Integrated OTP-based authentication for secure user logins.
- Utilized one-time passwords sent via email or SMS for user verification.

### 3. Docker Setup

- Dockerized the project for simplified deployment and environment consistency.
- Compose file included for easy setup of the entire development environment.

### 4. Celery for Asynchronous Tasks

- Utilized Celery for handling asynchronous tasks such as sending SMSs, background processing, and task scheduling.
- Improved performance by executing time-consuming tasks asynchronously.


### 5. Pytest for Testing

- Implemented Pytest for automated testing of various components and functionalities.
- Ensured code reliability and maintainability through comprehensive test coverage.

### 6. CI with GitHub Actions

- Set up continuous integration using GitHub Actions for automated testing, linting, and deployment.
- Ensured code quality and consistency in the development workflow.

## Installation

### Prerequisites

- Docker installed on your system

1. Clone the repository:
```
https://github.com/Mohammadihpython/ecommerce.git
```
```
cd ecommerce
```
2. Set up environment variables:
configure your environments in .env folder like:
   - DJANGO_SECRET_KEY
   - DATABASE_DB
   - .......

3. Start Docker containers:
```
run: docker compose -f local.yml up --build
```

4.Run Django's createsuperuser command
 ```
 docker-compose exec django bash
 ```
 ```
 python manage.py createsuperuser
 ```
 ```
  exit
```

5. Access the application:
Visit http://localhost:8000/ in your browser to access the application

## Usage

1. **Product Search**:
- Use the search bar on the platform to search for products.
- Explore autocomplete suggestions, filters, and relevant search results powered by Elasticsearch.

2. **User Authentication**:
- Register as a new user or log in using OTP-based authentication.
- Receive OTP via email or SMS for user verification.

3. **Admin Dashboard**:
- Access the admin dashboard to manage products, users, orders, etc.
- Perform CRUD operations on products and user data.

4. **Asynchronous Tasks**:
- Experience improved performance due to the asynchronous handling of tasks like sending emails or processing large data sets using Celery.

5. **Testing with Pytest**:
- Run automated tests using Pytest to ensure code reliability.
- Execute tests with `pytest` command and view test results and coverage.

6. **CI with GitHub Actions**:
- Utilize the predefined GitHub Actions workflows for automated testing, linting, and deployment.
- View CI status and check build, test, and deployment logs directly on GitHub.

7. **Customization**:
- Explore and modify the codebase to customize the platform according to your specific requirements.


## Technologies Used

- Django
- Django REST Framework
- Elasticsearch
- Docker
- Celery
- Pytest
- GitHub Actions
- Other relevant technologies and libraries used in the project




## Contributing
Explain how others can contribute to your project. Include guidelines for pull requests and issue reporting.

## License
This project is licensed under the [License Name] License - see the [LICENSE](LICENSE) file for details.
