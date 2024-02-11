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

5. **Get an Expiring Link**: You can get an expiring link for an image using the `/api/v1/expiring-links/{image_id}`:

   ![Get Expiring Link](assets/get-expiring-link.png)

## Future Updates

This README is a work in progress and will be updated.
