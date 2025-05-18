# GitHub Repository Manager

A Django web application for managing GitHub repositories - creating, connecting to existing repositories, and uploading files.

## Features

- **User Authentication**: Using Django's built-in authentication system
- **GitHub Integration**: Configure GitHub tokens for API access
- **Repository Management**:
  - Create new repositories
  - Connect to existing repositories
  - Upload files to repositories
  - Automatic GitHub Actions workflow setup
- **Modern UI**: Bootstrap-based responsive design

## Installation

1. Clone the repository:

```bash
git clone <repository-url>
cd django_github_manager
```

2. Create and activate a virtual environment:

```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

3. Install dependencies:

```bash
pip install -r requirements.txt
```

4. Apply migrations:

```bash
python manage.py migrate
```

5. Create a superuser:

```bash
python manage.py createsuperuser
```

6. Run the development server:

```bash
python manage.py runserver
```

7. Access the application at http://localhost:8000

## Usage

1. Sign up for an account or log in
2. Configure your GitHub credentials with a personal access token
3. Create a new repository or connect to an existing one
4. Upload files to your repository

## Requirements

- Python 3.8+
- Django 3.2+
- Requests library
- Git (installed on the server)

## License

MIT License 