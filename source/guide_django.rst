.. highlight:: console

.. author:: Finn <mail@f1nn.eu>

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

----

.. note:: For this guide you should be familiar with the basic concepts of

  * :manual:`Python <lang-python>` and its package manager pip
  * :manual:`supervisord <daemons-supervisord>`

License
=======

All relevant legal information can be found here

  * https://www.djangoproject.com/trademarks/

Prerequisites
=============

Your URL needs to be setup:

::

 [isabell@stardust ~]$ uberspace web domain list
 isabell.uber.space
 [isabell@stardust ~]$

Installation
============

Step 1
------

.. include:: includes/install-uwsgi.rst

Step 2
------
Install django

::

 [isabell@stardust ~]$ pip3.6 install django --user
 [isabell@stardust ~]$


Create a django project. We will use "MyDjangoProject" during this guide.

::

 [isabell@stardust ~]$ django-admin startproject MyDjangoProject
 [isabell@stardust ~]$

Migrate database

::

 [isabell@stardust ~]$ python3.6 ~/MyDjangoProject/manage.py migrate
 [isabell@stardust ~]$


Configuration
=============

Configure Hostname
------------------

Edit ``~/MyDjangoProject/MyDjangoProject/settings.py`` and edit the line ``ALLOWED_HOSTS = []`` to add your host name.

::

 ALLOWED_HOSTS = ['isabell.uber.space']

If you need to add multiple host names, seperate thim with commas like this:

::

 ALLOWED_HOSTS = ['isabell.uber.space', 'www.isabell.example']

MySQL
-----

To be able to use django 2.2 you need to use MySQL instead of sqlite,
since the sqlite provided by uberspace is not supported anymore. But since
you can just use a MySQL provided by uberspace, this isn't so bad ;)

Open ``~/MyDjangoProject/MyDjangoProject/settings.py`` and
edit the database block to look like this

::

  DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',
	      'NAME': 'DB_NAME',
       	'USER': 'DB_USER',
        'PASSWORD': 'DB_PASSWORD',
       	'HOST': 'localhost',
    }
  }


Your MySQL credentials can be found in the uberspace datasheet.

Configure web server
--------------------

.. note::

    Django is running on port 8000.

.. include:: includes/web-backend.rst

Setup daemon
------------

To deploy your application with uwsgi, create a file at ``~/uwsgi/apps-enabled/myDjangoProject.ini`` with the following content:

.. warning:: Replace ``<username>`` with your username! (4 times)

.. code-block:: ini
  :emphasize-lines: 2,3,16,17

  [uwsgi]
  base = /home/<username>/MyDjangoProject/MyDjangoProject
  chdir = /home/<username>/MyDjangoProject

  http = :8000
  master = true
  wsgi-file = %(base)/wsgi.py
  touch-reload = %(wsgi-file)

  app = wsgi

  #virtualenv = %(chdir)/venv

  plugin = python

  uid = <username>
  gid = <username>

Test installation
-----------------

Perform a CURL request to djangos port to see if your installation succeeded:

::

 [isabell@stardust ~]$ curl -I localhost:8000
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
