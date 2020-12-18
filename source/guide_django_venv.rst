.. highlight:: console

.. author:: devspiff

.. tag:: lang-python
.. tag:: web
.. tag:: audience-developers

.. sidebar:: About

  .. image:: _static/images/django.svg
      :align: center

##########
Django
##########

.. tag_list::

Django_ is a high-level Python Web framework that encourages rapid development and clean, pragmatic design. Built by experienced developers, it takes care of much of the hassle of Web development, so you can focus on writing your app without needing to reinvent the wheel. It’s free and open source.
This guide will show you how to set up 2 Django instances each in their own virtual environment: "test_project" and "website_project". In this guide I have used python3 in command line examples. Adjust this according to the python version your project is using. If your project is using python3.9, use python3.9. However, when you have a virtual environment activated, use just "python". This will use the proper python version in your venv. Calling other python versions explicitly may create chaos with permissions and dependencies.


----

.. note:: For this guide you should be familiar with the basic concepts of

  * :manual:`Python <lang-python>` and its package manager pip
  * Virtual Environments for Python

License
=======

All relevant legal information can be found here

  * https://www.djangoproject.com/trademarks/


Installation
============

Step 1
------

.. include:: includes/install-uwsgi.rst

Step 2
------
Setup two virtual environments, each in their respective folder and install Django in each one.

::

 [isabell@stardust ~]$ mkdir test
 [isabell@stardust ~]$ mkdir website

Create venv and activate it. Upgrade pip and install Django. Create a Django project.
::

 [isabell@stardust ~]$ cd test
 [isabell@stardust ~]$ python3 -m venv test_venv
 [isabell@stardust ~]$ source ./test_venv/bin/activate
 (test_venv) [isabell@stardust ~]$ pip install --upgrade pip
 (test_venv) [isabell@stardust ~]$ pip install django
 (test_venv) [isabell@stardust ~]$ django-admin startproject test_project

Repeat for second project.
::

 [isabell@stardust ~]$ cd website
 [isabell@stardust ~]$ python3 -m venv website_venv
 [isabell@stardust ~]$ source ./website_venv/bin/activate
 (website_venv) [isabell@stardust ~]$ pip install --upgrade pip
 (website_venv) [isabell@stardust ~]$ pip install django
 (website_venv) [isabell@stardust ~]$ django-admin startproject webstie_project


.. hint::

  Depending on your database configuration, additional modules like ``mysqlclient`` might be required.
  
  The database settings for using the mysql databases that Uberspace provides could look like this:
  
::
  
 DATABASES = {
     'default': {
         'ENGINE': 'django.db.backends.mysql',
         'OPTIONS': {
             'init_command': "SET sql_mode='STRICT_TRANS_TABLES'",
      'read_default_file': str(BASE_DIR.joinpath("db.cnf")),
         },
     }
 }
 
The db.cnf file will be located in the same folder as the manage.py. Values you have to adjust are marked with a *:

::

 [client]
 database = *database_name
 user = *username
 password = *password
 host = localhost
 default-character-set = utf8
 sql_mode = STRICT_TRANS_TABLES

Migrate database. (Remember to do it for both projects.)

::

 (website_venv) [isabell@stardust ~]$ python ~/website_venv/manage.py migrate



Configuration
=============

Configure Hostname
------------------

Edit ``~/MyDjangoProject/MyDjangoProject/settings.py`` and edit the line ``ALLOWED_HOSTS = []`` to add your host name.

::

 ALLOWED_HOSTS = ['isabell.uber.space']

If you need to add multiple host names, separate them with commas like this:

::

 ALLOWED_HOSTS = ['isabell.uber.space', 'www.isabell.example']

Configure web server
--------------------

.. note::

    Django is running on port 8000 by default. We will make one instance run at 8000 and the second one at 8010.

.. include:: includes/web-backend.rst

The above commands need to be changed as follows.

::

 uberspace web backend set --http /test --port 8000
 uberspace web backend set --http /website --port 8010

Your test space will be running at "isabell.uber.space/test/" and the website will be running at "isabell.uber.space/website/".



Setup daemon
------------

Finally we need to create two files at ``~/uwsgi/apps-enabled/``, one called test_project.ini and one called website_project.ini.

.. warning:: Replace ``<username>`` with your username! (4 times)

.. warning:: Ensure that ``static-map`` matches the path configured in django's ``STATIC_ROOT``. Otherwise all images, stylesheets and javascript will be missing from your site.

.. code-block:: ini
  :emphasize-lines: 2,3,9,17,18

  [uwsgi]
  base = /home/<username>/MyDjangoProject/MyDjangoProject
  chdir = /home/<username>/MyDjangoProject

  http = :8000
  master = true
  wsgi-file = %(base)/wsgi.py
  touch-reload = %(wsgi-file)
  static-map = /static=%(base)/static

  app = wsgi

  #virtualenv = %(chdir)/venv

  plugin = python

  uid = <username>
  gid = <username>

Test installation
-----------------

Perform a CURL request to djangos port to see if your installation succeeded:

::

 [isabell@stardust ~]$ curl -I https://isabell.uber.space
 HTTP/1.1 200 OK
 Content-Type: text/html
 X-Frame-Options: SAMEORIGIN
 Content-Length: 16348
 [isabell@stardust ~]$

If you don't see ``HTTP/1.1 200 OK`` check your installation.



Finishing installation
======================

Point your browser to URL and create a user account.

Best practices
==============

Security
--------

Change all default passwords. Look at folder permissions. Don't get hacked!


.. _Django: https://www.djangoproject.com/

----

Tested with Django 2.0.5, Uberspace 7.1.6

.. author_list::
