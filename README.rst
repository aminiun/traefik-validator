Traefik Validator
======================

A simple command to validate traefik config files with traefik schema.

Traefik static config schema is from: https://json.schemastore.org/traefik-v2.json

Traefik dynamic config schema is from: https://json.schemastore.org/traefik-v2-file-provider.json

Installation
------------
First install the package:

.. code:: bash

    pip3 install django-zeromigrations

Then add it to your ``INSTALLED_APPS``:

.. code:: python

    INSTALLED_APPS = [
        ...
        "zero_migrations"
    ]

--------------

Usage
-----

First, run the command:

.. code::

    python manage.py zeromigrations

    I suggest to make a backups from both your migrations and django_migrations table (just in case).
    1- make backup
    2- restore last backup
    3- just proceed

If you choose ``1- make backup``, it would make a backup then zero
migrations.

If you choose ``2- restore last backup``, it tries to restore the latest
backup that can be found. If not backup found, it would raise an error.

If you choose ``3- just proceed``, it assumes that you already have your
own backup and start setting migrations zero.
