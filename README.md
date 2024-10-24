
---

# Expense Manager

## Overview

The Expense Manager is a web application designed to help users track their expenses and incomes efficiently. Users can manage their financial records, analyze spending habits, and make informed budgeting decisions. This application includes user authentication,preferences.

## Table of Contents

- [Features](#features)
- [Technologies Used](#technologies-used)
- [Installation](#installation)
- [Usage](#usage)
- [Project Structure](#project-structure)
- [Contributing](#contributing)
- [License](#license)

## Features

- User authentication (registration, login, password reset)
- Expense and income tracking
- Statistics and analytics for expenses and incomes
- Responsive design with a user-friendly interface
- Customizable user preferences
- Admin panel for managing users and data

## Technologies Used

- **Backend**: Django
- **Frontend**: HTML, CSS, JavaScript
- **Database**: Postgres
- **Dependencies**: Listed in `requirements.txt`

## Installation

1. Clone the repository:
   ```bash
   git clone https://github.com/HemanthhVV/expenditure-manager.git
   cd expenditure-manager
   ```

2. Create a virtual environment and activate it:
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows use `venv\Scripts\activate`
   ```

3. Install the required packages:
   ```bash
   pip install -r requirements.txt
   ```
4. If you don't prefer the any other db, Django uses the default file level db called sqlite3, Don't need any configuration in your settings.py, If you prefer other db, create a env file to configure the env variables to db and change the settings.py as follows:
    ```
    DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql', ##I've used postgres
        'NAME': os.environ.get('DB_NAME'),
        'USER':os.environ.get('DB_USER'),
        'PASSWORD':os.environ.get('DB_PASSWORD'),
        'HOST':os.environ.get('DB_HOST'),
        'PORT':os.environ.get('DB_PORT')
        }
    }
    ```

5. Run database migrations:
   ```bash
   python manage.py migrate
   ```

6. Create a superuser (optional, for admin access):
   ```bash
   python manage.py createsuperuser
   ```

7. Start the development server:
   ```bash
   python manage.py runserver
   ```

8. Open your web browser and navigate to `http://127.0.0.1:8000/` to access the application.

## Usage

- Register for an account or log in to your existing account.
- User can add, edit, and view expenses and incomes.
- Access statistical insights on your financial data by graphs.
- Manage user preferences through the settings section.

## Project Structure

```
expense_manager/
├── authentication/
│   ├── admin.py
│   ├── apps.py
│   ├── migrations/
│   ├── models.py
│   ├── tests.py
│   ├── urls.py
│   └── views.py
├── expenses/
│   ├── admin.py
│   ├── apps.py
│   ├── migrations/
│   ├── models.py
│   ├── tests.py
│   ├── urls.py
│   └── views.py
├── incomes/
│   ├── admin.py
│   ├── apps.py
│   ├── migrations/
│   ├── models.py
│   ├── tests.py
│   ├── urls.py
│   └── views.py
├── userpreferences/
│   ├── admin.py
│   ├── apps.py
│   ├── migrations/
│   ├── models.py
│   ├── tests.py
│   ├── urls.py
│   └── views.py
├── db.sqlite3
├── manage.py
├── requirements.txt
├── templates/
├── static/
└── expense_manager/
    ├── asgi.py
    ├── settings.py
    ├── urls.py
    └── wsgi.py
```

## Contributing

Contributions are welcome! Please follow these steps to contribute:

1. Fork the repository.
2. Create a new branch (`git checkout -b feature/YourFeature`).
3. Make your changes and commit them (`git commit -m 'Add some feature'`).
4. Push to the branch (`git push origin feature/YourFeature`).
5. Open a pull request.
