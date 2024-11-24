
---

# **Project Name**

A brief description of your project.

## **Table of Contents**

- Prerequisites
- Installation
- Database Setup
- Environment Variables
- Running Migrations
- Creating Superuser
- Running the Server
- Creating Tenants
- Usage
- Project Structure
- Contributing
- License

---

## **Prerequisites**

Before you begin, ensure you have the following installed on your machine:

- **Python 3.7 or higher**
- **PostgreSQL**
- **pipenv** (optional, you can use virtualenv and pip instead)
- **Git**

## **Installation**

1. **Clone the repository:**

   ```sh
   git clone https://github.com/yourusername/yourproject.git
   cd yourproject
   ```

2. **Create a virtual environment and activate it:**

   Using `pipenv`:

   ```sh
   pipenv shell
   ```

   Or using `virtualenv`:

   ```sh
   python -m venv venv
   source venv/bin/activate  # On Windows use `venv\Scripts\activate`
   ```

3. **Install the dependencies:**

   ```sh
   pip install -r requirements.txt
   ```

## **Database Setup**

1. **Install PostgreSQL:**

   Follow the instructions on the [PostgreSQL website](https://www.postgresql.org/download/) to install PostgreSQL on your system.

2. **Create a PostgreSQL database and user:**

   Open the PostgreSQL shell or use a GUI tool like pgAdmin.

   ```sql
   -- Replace 'your_db_name', 'your_db_user', and 'your_db_password' with your own values.

   CREATE DATABASE your_db_name;
   CREATE USER your_db_user WITH PASSWORD 'your_db_password';
   ALTER ROLE your_db_user SET client_encoding TO 'utf8';
   ALTER ROLE your_db_user SET default_transaction_isolation TO 'read committed';
   ALTER ROLE your_db_user SET timezone TO 'UTC';
   GRANT ALL PRIVILEGES ON DATABASE your_db_name TO your_db_user;
   ```

## **Environment Variables**

1. **Create a `.env` file in the root directory of your project:**

   ```sh
   touch .env
   ```

2. **Add the following environment variables to the `.env` file:**

   ```env
   SECRET_KEY='your_secret_key'
   DEBUG=True  # Set to False in production
   DB_NAME='your_db_name'
   DB_USER='your_db_user'
   DB_PASSWORD='your_db_password'
   DB_HOST='localhost'
   DB_PORT='5432'
   CALENDARIFIC_API_KEY='your_calendarific_api_key'  # Get from https://calendarific.com/
   ```

   - **SECRET_KEY:** Generate a secret key using:

     ```sh
     python -c "import secrets; print(secrets.token_urlsafe())"
     ```

## **Running Migrations**

1. **Apply migrations to the shared apps:**

   ```sh
   python manage.py migrate_schemas --shared
   ```

   - **Note:** Since your project uses `django-tenants`, use `migrate_schemas --shared` to apply migrations to shared apps only.

## **Creating Superuser**

1. **Create a superuser for the public tenant:**

   ```sh
   python manage.py create_superuser
   ```

   - **Note:** This may require custom management commands if you need to create superusers for specific tenants.

## **Running the Server**

1. **Start the development server:**

   ```sh
   python manage.py runserver
   ```

   The application will be accessible at [http://localhost:8000/](http://localhost:8000/).

## **Creating Tenants**

Since the project uses `django-tenants` for multi-tenancy, you need to create tenants and their associated domains.

1. **Create the public tenant:**

   ```sh
   python manage.py shell
   ```

   In the shell:

   ```python
   from client.models import Client, Domain

   # Create the public tenant
   public_tenant = Client(schema_name='public', name='Public Tenant')
   public_tenant.save()

   public_domain = Domain()
   public_domain.domain = 'localhost'  # For local development
   public_domain.tenant = public_tenant
   public_domain.is_primary = True
   public_domain.save()
   ```

2. **Create additional tenants:**

   ```python
   # Create a new tenant
   tenant = Client(schema_name='tenant1', name='Tenant 1')
   tenant.save()

   domain = Domain()
   domain.domain = 'tenant1.localhost'  # Replace with your tenant domain
   domain.tenant = tenant
   domain.is_primary = True
   domain.save()
   ```

   - **Note:** For local development with subdomains, you may need to adjust your `hosts` file or use a development tool that supports wildcard subdomains.

## **Usage**

- **Access the public tenant:**

  [http://localhost:8000/](http://localhost:8000/)

- **Access a tenant:**

  [http://tenant1.localhost:8000/](http://tenant1.localhost:8000/)

## **Project Structure**

Briefly explain the project structure and important files/directories.

```
yourproject/
├── client/                # Django app for tenant management
│   ├── models.py          # Contains the Client and Domain models
│   └── ...
├── system_management/     # Main Django app for your system
│   ├── views.py           # Contains the views for the application
│   ├── models.py          # Contains the SAID and Holiday models
│   └── ...
├── core/                  # Project configuration
│   ├── settings.py        # Django settings for the project
│   ├── urls.py            # URL configuration
│   └── ...
├── templates/             # HTML templates
│   └── system_management/
│       ├── home.html
│       └── results.html
├── manage.py              # Django management script
├── requirements.txt       # Project dependencies
└── README.md              # Project README file
```

## **Contributing**

If you would like to contribute to this project, please follow these steps:

1. Fork the repository.
2. Create a new branch:

   ```sh
   git checkout -b feature/YourFeature
   ```

3. Make your changes and commit them:

   ```sh
   git commit -m 'Add some feature'
   ```

4. Push to the branch:

   ```sh
   git push origin feature/YourFeature
   ```

5. Open a pull request.

## **License**

Include information about the project's license.

---

## **Additional Notes**

- **Django Tenants Configuration:**

  - **

SHARED_APPS

:** In your 

settings.py

, 

SHARED_APPS

 includes:

    ```python
    SHARED_APPS = [
        "django_tenants",
        "django.contrib.admin",
        "django.contrib.auth",
        "django.contrib.contenttypes",
        "django.contrib.sessions",
        "django.contrib.messages",
        "django.contrib.staticfiles",
        "client",
        "system_management",
    ]
    ```

  - **

TENANT_APPS

:** Contains tenant-specific apps:

    ```python
    TENANT_APPS = [
        "system_management",
    ]
    ```

  - **

TENANT_MODEL

 and 

TENANT_DOMAIN_MODEL

:**

    ```python
    TENANT_MODEL = "client.Client"
    TENANT_DOMAIN_MODEL = "client.Domain"
    ```

  - **Database Router:**

    ```python
    DATABASE_ROUTERS = (
        'django_tenants.routers.TenantSyncRouter',
    )
    ```

- **Database Configuration:**

  - Uses `django_tenants.postgresql_backend` as the database engine:

    ```python
    DATABASES = {
        "default": {
            'ENGINE': 'django_tenants.postgresql_backend',
            "NAME": env("DB_NAME"),
            "USER": env("DB_USER"),
            "PASSWORD": env("DB_PASSWORD"),
            "HOST": env("DB_HOST"),
            "PORT": env("DB_PORT"),
        }
    }
    ```

- **Static Files:**

  - Static files settings in 

settings.py

:

    ```python
    STATIC_URL = 'static/'
    STATIC_ROOT = os.path.join(BASE_DIR, 'static/')
    ```

  - Collect static files using:

    ```sh
    python manage.py collectstatic
    ```

- **Templates Directory:**

  - Templates are stored in the 

templates

 directory:

    ```python
    TEMPLATES = [
        {
            "BACKEND": "django.template.backends.django.DjangoTemplates",
            'DIRS': [os.path.join(BASE_DIR, 'templates')],
            # ...
        },
    ]
    ```

- **Environment Variables:**

  - Use 

environ

 module to manage environment variables:

    ```python
    import environ

    # Initialize environment variables
    env = environ.Env()
    environ.Env.read_env()
    ```

  - Access environment variables using 

env("VARIABLE_NAME")

.

- **Calendarific API:**

  - The project uses Calendarific API to fetch public holidays.
  - Add your API key to the `.env` file:

    ```env
    CALENDARIFIC_API_KEY='your_calendarific_api_key'
    ```

  - In 

settings.py

, access the API key:

    ```python
    CALENDARIFIC_API_KEY = env('CALENDARIFIC_API_KEY')
    ```

- **Allowed Hosts:**

  - For development, you may set:

    ```python
    ALLOWED_HOSTS = ['*']
    ```

    - **Note:** In production, specify the allowed hosts for security.

## **Common Issues**

- **Database Connection Error:**

  - Ensure your database credentials in the `.env` file are correct.
  - Verify that PostgreSQL is running and accessible.

- **Subdomain Access Issues:**

  - If you're unable to access tenant subdomains locally, consider modifying your `hosts` file.
  - For example, add the following lines to your `hosts` file:

    ```
    127.0.0.1   tenant1.localhost
    127.0.0.1   tenant2.localhost
    ```

- **Migration Issues:**

  - If you encounter issues with migrations, try deleting migration files and database tables, then run:

    ```sh
    python manage.py makemigrations
    python manage.py migrate_schemas --shared
    ```

- **Static Files Not Loading:**

  - Ensure you have run `collectstatic`.
  - Verify that the 

STATIC_ROOT

 and 

STATIC_URL

 settings are correctly configured.

---

By following this README, you should be able to set up and run the Django project with PostgreSQL and multi-tenancy support using `django-tenants`. The instructions are tailored based on your provided 

settings.py

, ensuring consistency with your project configuration.
