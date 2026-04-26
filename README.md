# 🏢 Employee Management System (Backend API)

## 📌 Overview

This project is a backend system for managing employees, users, and departments within an organization. It is built using FastAPI and follows a structured service-layer architecture for clean and maintainable code.

## 🚀 Features

* User management (creation, authentication)
* Employee management (add, update, delete, view)
* Department management
* Role-Based Access Control (RBAC)
* Secure JWT authentication
* CRUD operations with relational data handling
* Advanced SQL queries for data analysis

## 🔐 Authentication & Authorization

* JWT-based authentication
* Role-based access control (Admin, User, etc.)
* Protected routes based on permissions

## 🏗️ Tech Stack

* FastAPI
* SQLAlchemy (ORM)
* PostgreSQL
* REST API Development
* Git & GitHub

## 📊 Database Design

* Relational database with foreign key relationships
* Efficient querying using SQLAlchemy ORM
* Use of advanced SQL features:

  * Aggregations
  * Window Functions (ROW_NUMBER, RANK, PARTITION BY)

## ⚙️ Setup Instructions

1. Clone the repository:
   git clone (https://github.com/akhilchelat/fastapi-backend-project/tree/main)

2. Navigate to project directory:
   cd employee-management-system

3. Create virtual environment:
   python -m venv venv

4. Activate environment:
   Windows: venv\Scripts\activate
   Linux/Mac: source venv/bin/activate

5. Install dependencies:
   pip install -r requirements.txt

6. Run the application:
   uvicorn app.main:app --reload

## 🌐 Deployment

* Deployed on Render with environment-based configuration

## 🚧 Future Improvements

* Pagination and filtering
* Performance optimization
* API rate limiting
* Frontend integration

## 👤 Author

Akhil Chelat
