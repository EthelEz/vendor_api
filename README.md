# Vendor API

This is the backend API for the vendor management system. It is built with Django and Django REST Framework.

## Prerequisites

- Docker
- Docker Compose

## Getting Started

1.  **Clone the repository:**

    ```bash
    git clone <repository-url>
    cd vendor_api
    ```

2.  **Create a `.env` file:**

    Create a `.env` file in the `vendor_api` directory and add the following environment variables. These are used to configure the database connection and other services.

    ```env
    DB_NAME=postgres
    DB_USER=postgres
    DB_PASSWORD=postgres
    DB_HOST=db
    DB_PORT=5432
    STRIPE_SECRET_KEY=your_stripe_secret_key
    ```

3.  **Build and run the application:**

    Use Docker Compose to build the images and run the containers:

    ```bash
    docker compose up --build
    ```

    The API will be running at `http://localhost:8000`.

## Admin Access

The API includes a Django admin interface for managing the application's data.

1.  **Create a superuser:**

    To access the admin panel, you first need to create a superuser account. Run the following command:

    ```bash
    docker compose exec web python manage.py create_superuser
    ```

    This will create a superuser with the following credentials:
    - **Username:** `dollar_queen`
    - **Email:** `dollarqueen@gmail.com`
    - **Password:** `Vwbuyfa@900`

2.  **Access the admin panel:**

    You can now access the admin panel by navigating to `http://localhost:8000/admin/` in your web browser and logging in with the superuser credentials.

## API Endpoints

The API documentation is available at the following endpoints:

-   **Swagger UI:** `http://localhost:8000/api/schema/swagger-ui/`
-   **Redoc:** `http://localhost:8000/api/schema/redoc/`