Traefik Validator
======================

A simple command to validate traefik config files with traefik schema.

Traefik static config schema is from: https://json.schemastore.org/traefik-v2.json

Traefik dynamic config schema is from: https://json.schemastore.org/traefik-v2-file-provider.json

Installation
------------
Install the package:

.. code:: bash

    pip3 install django-zeromigrations

--------------

Usage
-----

Run the command:

.. code::

    validate_traefik -h
    
    >>> usage: validate_traefik [-h] [-s STATIC_CONFIG] [-d DYNAMIC_CONFIG]

    Validate traefik config file.

    optional arguments:
    -h, --help            show this help message and exit
    -s STATIC_CONFIG, --static-config STATIC_CONFIG     The static file path
    -d DYNAMIC_CONFIG, --dynamic-config DYNAMIC_CONFIG      The dynamic file path

For validating static config file:

.. code::

    validate_traefik -s <PATH_TO_YOUR_FILE>

For validating dynamic config file:

.. code::

    validate_traefik -d <PATH_TO_YOUR_FILE>

**Note that you can use both options at the same command.**
