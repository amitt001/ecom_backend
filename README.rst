============
ECOM Backend
============

An eCommerce website backend, that supports add/search/delete/modify products functionality.

Technology Used:
================

Python, Django, Django-rest

Get the Sources:
================

    git clone https://github.com/amitt001/ecom_backend.git

Testing:
========

For testing I am using Django tests. To run tests::

    python -m unittest

Setup:
======

Automatic::

    1. chmod +x setup.sh

    2. ./setup.sh

Manual::

    1. Intall pip(`sudo apt-get/yum install pip`).

    2. Install virtualenv(`sudo apt-get/yum install virtualenv`).

    3. Create virtualenv and activate it(`virtualenv env && source env/bin/activate`).

    4. Install required packages(`pip install -r requirements.txt`).

    5. Goto ecom_api directory(`cd ecom_api`).

    6. Create database(`python manage.py makemigrations && python manage.py migrate`).

    7. Test and run(`python manage.py test && python manage.py runserver`)

Open http://127.0.0.1:8000/


Permissions:
============

By default all the product management endpoints have `IsAuthenticatedOrReadOnly` permissions i.e. an anonymous or unauthenticated user can only see the product. For modifying product data(PUT, POST, DELETE) user need to register and use token.

To use django-rest UI for api testing edit settings.py REST_FRAMEWORK -> DEFAULT_PERMISSION_CLASSES to `rest_framework.permissions.AllowAny`.

Database:
=========

This app uses SQLite as the database.
This app uses Django ORM for DB access. So, other SQL DBs like MySQL, PostgreSQL, etc can also be used just by adding the DB info in settings.py file(no need to change any code).


