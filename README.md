# 🛡️ Vulnerable FastAPI App for Cybersecurity Lab

This project is a minimal web application built with **FastAPI** to demonstrate two common web vulnerabilities:  
- **SQL Injection**
- **Cross-Site Scripting (XSS)**

> **Warning**: This application is intentionally vulnerable and should only be run in a safe, isolated environment.

---

## Features

- FastAPI-based backend
- Raw HTML interface for login, registration, and file upload
- SQLite database
- File upload endpoint for testing XSS
- Dockerized for consistent setup and teardown

---

## Prerequisites

- Docker installed on your system (https://docs.docker.com/get-docker/)

---

## How to Run

### 1. Clone the repository
```bash
git clone https://github.com/your-username/lab4-vulnerable-app.git
cd lab4-vulnerable-app
```
### 2. Build the Docker image
```bash
docker build -t lab4-app .
```
### 3. Run the Docker container
``` bash
docker run -d -p 8000:8000 --name lab4 lab4-app
```
### 4. Visit the App in Browser
Open: http://localhost:8000