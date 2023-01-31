.. highlight:: console

.. author:: Finn <mail@f1nn.eu>
.. author:: brutus <brutus.dmc@googlemail.com>

.. tag:: lang-python
.. tag:: django
.. tag:: web
.. tag:: audience-developers

.. sidebar:: About

  .. image:: _static/images/django.svg
      :align: center

######
Django
######

.. tag_list::

Django_ is a high-level Python Web framework that encourages rapid development and clean, pragmatic design. Built by experienced developers, it takes care of much of the hassle of Web development, so you can focus on writing your app without needing to reinvent the wheel. It’s free and open source.

----

.. note:: For this guide you should be familiar with the basic concepts of

  * :manual:`Python <lang-python>` and its package manager pip

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

.. note:: We will use *"mysite"* as the project's name and will install it to `~/mysite`.

Installation
============

Install django.

::

 [isabell@stardust ~]$ pip3.11 install --user django
 [isabell@stardust ~]$

.. hint::

  Depending on your database configuration, additional modules like ``mysqlclient`` might be required.

Create Project
--------------

Create a django project. As stated, we will use "mysite" as the project's name.

::

 [isabell@stardust ~]$ django-admin startproject mysite
 [isabell@stardust ~]$

Migrate Database
----------------

::

 [isabell@stardust ~]$ python3.11 ~/mysite/manage.py migrate
 [isabell@stardust ~]$

Create Superuser
----------------

::

 [isabell@stardust ~]$ python3.11 ~/mysite/manage.py createsuperuser
 [isabell@stardust ~]$

Configuration
=============

Configure Hostname
------------------

Edit ``~/mysite/mysite/settings.py`` and edit the line ``ALLOWED_HOSTS = []`` to add your host name.

::

 ALLOWED_HOSTS = ['isabell.uber.space']

If you need to add multiple host names, separate them with commas like this:

::

 ALLOWED_HOSTS = ['isabell.uber.space', 'www.isabell.example']

Static Files
------------

.. warning:: FIXME: This section is outdated and needs a rewrite!

.. warning:: Replace ``<username>`` with your username! (4 times)

To deploy your application with uwsgi, create a file at ``~/uwsgi/apps-enabled/mysite.ini`` with the following content:

.. warning:: Replace ``<username>`` with your username! (4 times)

.. warning:: Ensure that ``static-map`` matches the path configured in django's ``STATIC_ROOT``. Otherwise all images, stylesheets and javascript will be missing from your site.

.. code-block:: ini
  :emphasize-lines: 2,3,9,17,18

  [uwsgi]
  base = /home/<username>/mysite/mysite
  chdir = /home/<username>/mysite

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

Setup Service
=============

Install Gunicorn
----------------

We will run Django as a WSGI app with `gunicorn <https://gunicorn.org/>`_ and
install the required package with pip.

::

  [isabell@stardust ~]$ pip3.11 install --user gunicorn

Create Service
--------------

After that, continue with setting it up as a service.

Create ``~/etc/services.d/mysite.ini`` with the following content:

.. code-block:: ini

  [program:mysite]
  directory=%(ENV_HOME)s/mysite
  command=gunicorn --error-logfile - --reload --bind 0.0.0.0:8000 mysite.wsgi:application
  startsecs=15

After creating the configuration, tell :manual:`supervisord <daemons-supervisord>` to refresh its configuration and start the service:

::

  [isabell@stardust ~]$ supervisorctl reread
  mysite: available
  [isabell@stardust ~]$ supervisorctl update
  mysite: updated process group
  [isabell@stardust ~]$ supervisorctl status
  mysite                            RUNNING   pid 26020, uptime 0:03:14
  [isabell@stardust ~]$

Your service should be in the state ``RUNNING``. If it still is in ``STARTING`` instead, no worries, you might just have to wait some time and try the command again (up to 15 seconds). It might already run fine anyway though. Oherwise check the logs in ``~/logs/supervisord.log``.

Configure Web Backend
---------------------

.. note::

    Django is running on port 8000.

.. include:: includes/web-backend.rst

Finishing Installation
======================

Perform a CURL request to Django's port to see if your installation succeeded:

::

 [isabell@stardust ~]$ curl -I https://isabell.uber.space
 HTTP/2 200
 date: Tue, 31 Jan 2023 16:10:23 GMT
 content-type: text/html; charset=utf-8
 content-length: 10681
 vary: Accept-Encoding
 server: gunicorn
 x-frame-options: SAMEORIGIN
 x-content-type-options: nosniff
 referrer-policy: strict-origin-when-cross-origin
 cross-origin-opener-policy: same-origin
 x-xss-protection: 1; mode=block
 strict-transport-security: max-age=31536000

 [isabell@stardust ~]$

If you don't see ``HTTP/2 200`` check your installation.

Best practices
==============

Security
--------

Change all default passwords. Look at folder permissions. Don't get hacked!


.. _Django: https://www.djangoproject.com/

----

Tested with Django 4.1.6, Python 3.11, Uberspace 7.15

.. author_list::
