![Python](https://img.shields.io/badge/-Python-3776AB?style=flat-square&logo=python&logoColor=white)
![Django](https://img.shields.io/badge/-Django-092E20?style=flat-square&logo=django&logoColor=white)
![Django REST Framework](https://img.shields.io/badge/-Django%20REST%20Framework-092E20?style=flat-square&logo=django&logoColor=white)
![Celery](https://img.shields.io/badge/-Celery-37814A?style=flat-square&logo=celery&logoColor=white)
![Redis](https://img.shields.io/badge/-Redis-DC382D?style=flat-square&logo=redis&logoColor=white)
![pytest](https://img.shields.io/badge/-pytest-0A9EDC?style=flat-square&logo=pytest&logoColor=white)
![Docker](https://img.shields.io/badge/-Docker-2496ED?style=flat-square&logo=docker&logoColor=white)

# Thumbnails API

## Description

This project is a RESTful API for creating and managing image thumbnails. It also allows for creating expiring links to the images, which can be used to provide temporary access to the original images.

Images and thumbnails are stored on AWS S3, thumbnails are generated asynchronously using Celery.

The entire application is Dockerized, which simplifies deployment and ensures consistency across different environments.

Additionally, API documentation is available via Swagger and Redoc.

## Account Tiers

This API supports three built-in account tiers: Basic, Premium, and Enterprise.

- **Basic**: Users can upload images and receive a link to a 200x200px thumbnail.

- **Premium**: In addition to the Basic tier features, users also receive a link to a 400x400px thumbnail and a link to the original image.

- **Enterprise**: In addition to the Premium tier features, users can fetch an expiring link to the image. The link can be set to expire between 300 and 30000 seconds.

## Admin Capabilities

Admin users have the ability to extend the functionality of the API. They can add new account tiers, modify the capabilities of existing tiers, and create new sizes of thumbnails.

## Usage

This API allows you to upload images and generate thumbnails. Here's a quick overview of the functionality:

1. **API Root**: The API root provides an overview of all the available endpoints:

   ![API Root](assets/api-root.png)

2. **Upload an Image**: You can upload an image using the `/api/v1/images/` endpoint:

   ![Upload Image](assets/upload-image.png)

3. **Get an Image**: You can get a specific image using the `/api/v1/images/{image_id}/` endpoint:

   ![Get Image](assets/get-image.png)

4. **Make an Expiring Link**: You can make an expiring link for an image using the `/api/v1/expiring-links/` endpoint:

   ![Make Expiring Link](assets/make-expiring-link.png)

5. **Get an Expiring Link**: You can get an expiring link for an image using the `/api/v1/expiring-links/{image_id}/` endpoint:

   ![Get Expiring Link](assets/get-expiring-link.png)

## Local Installation

1. **Clone the repository**:

   ```bash
   git clone https://github.com/EWitkowska/thumbnails_api.git

   ```

2. **Navigate into the directory**:

   ```bash
   cd thumbnails_api

   ```

3. **Install the requirements**:

   ```bash
   pip install -r requirements.txt

   ```

4. **Set up the environment variables**:

   Create a `.env` file in the root directory and set the following variables.
   You can use the `.env.template` file as a starting point:

   ```bash
    SECRET_KEY=
    DEBUG=

    POSTGRES_HOST=
    POSTGRES_PORT=5432
    POSTGRES_DB=
    POSTGRES_USER=
    POSTGRES_PASSWORD=

    AWS_STORAGE_BUCKET_NAME=
    AWS_REGION=
    AWS_ACCESS_KEY_ID=
    AWS_SECRET_ACCESS_KEY=
    AWS_S3_FILE_OVERWRITE=True
    AWS_QUERYSTRING_AUTH=False

    REDIS_URL=redis://redis:6379/1
    CELERY_BROKER_URL=redis://redis:6379/1
    CELERY_RESULT_BACKEND=redis://redis:6379/1
   ```

   Please note that you need to configure AWS S3 on your own. Make sure to replace the AWS variables with your actual AWS S3 bucket name, region, access key ID, secret access key, and other settings.

5. **Run the migrations:**:

   ```bash
   python manage.py migrate

   ```

6. **Load the fixtures**:

   ```bash
   python manage.py load_fixtures

   ```

7. **Run the server**:

   ```bash
   python manage.py runserver
   ```

   Now, you can access the application at http://127.0.0.1:8000

## Docker Installation

1. **Clone the repository**:

   ```bash
   git clone https://github.com/EWitkowska/thumbnails_api.git
   ```

2. **Navigate into the directory**:

   ```bash
   cd thumbnails_api
   ```

3. **Set up the environment variables**:

   Create a `.env` file in the root directory and set the following variables.
   You can use the `.env.template` file as a starting point:

   ```bash
    SECRET_KEY=
    DEBUG=

    POSTGRES_HOST=
    POSTGRES_PORT=5432
    POSTGRES_DB=
    POSTGRES_USER=
    POSTGRES_PASSWORD=

    AWS_STORAGE_BUCKET_NAME=
    AWS_REGION=
    AWS_ACCESS_KEY_ID=
    AWS_SECRET_ACCESS_KEY=
    AWS_S3_FILE_OVERWRITE=True
    AWS_QUERYSTRING_AUTH=False

    REDIS_URL=redis://redis:6379/1
    CELERY_BROKER_URL=redis://redis:6379/1
    CELERY_RESULT_BACKEND=redis://redis:6379/1
   ```

   Please note that you need to configure AWS S3 on your own. Make sure to replace the AWS variables with your actual AWS S3 bucket name, region, access key ID, secret access key, and other settings.

4. **Build the Docker image**:

   ```bash
   docker-compose build
   ```

5. **Run the Docker containers**:

   ```bash
   docker-compose up
   ```

   Now, you can access the application at http://127.0.0.1:80

## Demo Data

For demo purposes I've added users, an admin user, and predefined thumbnail dimensions to the database.

## Demo Credentials

For the admin account - can log in to Django admin:

- **Email**: admin@example.com
- **Password**: Blank2211

For users:

- **Email**: user1@example.com
- **Password**: Blank2211

- **Email**: user2@example.com
- **Password**: Blank2211

- **Email**: user3@example.com
- **Password**: Blank2211

## API Documentation

This API uses both Swagger and Redoc for documentation and interactive exploration of the API's endpoints. You can access the Swagger and Redoc UIs at:

- **Swagger UI**:

  - **Local Installation**: [http://127.0.0.1:8000/api/v1/schema/swagger-ui/](http://127.0.0.1:8000/api/v1/schema/swagger-ui/)
  - **Docker Installation**: [http://127.0.0.1:80/api/v1/schema/swagger-ui/](http://127.0.0.1:80/api/v1/schema/swagger-ui/)

- **Redoc UI**:
  - **Local Installation**: [http://127.0.0.1:8000/api/v1/schema/redoc/](http://127.0.0.1:8000/api/v1/schema/redoc/)
  - **Docker Installation**: [http://127.0.0.1:80/api/v1/schema/redoc/](http://127.0.0.1:80/api/v1/schema/redoc/)
