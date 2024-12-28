AUTHORS

Luís Rafael Albuquerque Figueiredo
2024182622
uc2024182622@student.uc.pt

# Secure Web Application: Vulnerability Demonstration and Mitigation

This project demonstrates the implementation of secure and vulnerable versions of a web application with the goal of identifying and mitigating common vulnerabilities like SQL Injection, XSS, and CSRF. The project is structured into two exercises: developing functionalities with secure and insecure implementations, and using security tools for testing and analysis.

---

## Table of Contents

- [Overview](#overview)
- [Setup and Installation](#setup-and-installation)
- [Project Structure](#project-structure)
- [Features](#features)
  - [1. Authentication](#1-authentication)
  - [2. Message Posting](#2-message-posting)
  - [3. Book Search](#3-book-search)
- [Security Tools Used](#security-tools-used)
- [How to Run Security Scans](#how-to-run-security-scans)
  - [Using OWASP ZAP](#using-owasp-zap)
  - [Using SpotBugs](#using-spotbugs)
- [Vulnerabilities Demonstrated](#vulnerabilities-demonstrated)

---

## Overview

The project implements a Python Flask web application integrated with PostgreSQL, showcasing both secure and vulnerable implementations of typical web functionalities. The goal is to highlight the importance of secure coding practices and demonstrate how vulnerabilities can be exploited and mitigated.

---

## Setup and Installation

### Prerequisites

- Python 3.8
- PostgreSQL
- Virtual Environment (venv) for Python
- OWASP ZAP

### Installation

1. Clone the repository:
   ```bash
   git clone <repository-url>
   cd <repository-folder>

Create a virtual environment:
    python3 -m venv venv
    source venv/bin/activate  # On Windows: venv\Scripts\activate

Install dependencies:
    pip install -r requirements.txt

Set up the database:
    Start your PostgreSQL server.
    Run the schema.sql file to create the necessary tables:
        psql -U <username> -d <database> -f schema.sql

Run the application:
    flask run

Access the app in your browser:
    http://127.0.0.1:5000

Project Structure:
.
├── __pycache__/
│   ├── db_connection.cpython-313.pyc
│   ├── test_connection.cpython-313.pyc
├── app/
│   ├── __pycache__/
│   ├── templates/
│   ├── tests/
│   │   ├── __pycache__/
│   │   ├── __init__.py
│   │   ├── test_app.py
│   │   ├── test_routes.py
│   │   └── __init__.py
│   ├── app.py
│   ├── models.py
├── README.md
├── routes.py
├── venv/
├── db_connection.py
├── docker-compose.yml
├── requirements.txt
├── run.py
└── test_connection.py

Features:

1. Authentication
    Secure Version: Uses parameterized queries and bcrypt hashing for password storage.
    Vulnerable Version: Vulnerable to SQL Injection due to direct query concatenation.
2. Message Posting
    Secure Version: Sanitizes inputs to prevent XSS attacks.
    Vulnerable Version: No input sanitization, allowing stored XSS attacks.
3. Book Search
    Secure Version: Uses parameterized queries to prevent SQL Injection.
    Vulnerable Version: Direct query concatenation allows SQL Injection.

Security Tools Used:

    OWASP ZAP:
    Used for automated vulnerability scanning and reporting.

How to Run Security Scans:

Using OWASP ZAP
    Start the OWASP ZAP application.
    Set the target URL to http://127.0.0.1:5000.
    Run the Automated Scan.
    Export the report in HTML format.

Vulnerabilities Demonstrated:

Vulnerability	    Location	                Description
SQL Injection	    /vulnerable_login	        Bypass authentication using SQL Injection in the login query.
XSS	                /vulnerable_messages	    Execute JavaScript code stored in the database to attack end-users.
SQL Injection	    /vulnerable_books/search	Exploit search functionality to retrieve all database records.