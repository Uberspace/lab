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

Django_ is a high-level Python Web framework that encourages rapid development and clean, pragmatic design. Built by experienced developers, it takes care of much of the hassle of Web development, so you can focus on writing your app without needing to reinvent the wheel. It's free and open source.

----

.. note:: For this guide, you should be familiar with the basic concepts of

  * :manual:`Python <lang-python>` and its package manager pip
  * :manual:`Supervisord <daemons-supervisord>` to set up your service

License
=======

All relevant legal information can be found here

  * https://www.djangoproject.com/trademarks/

Prerequisites
=============

Your URL needs to be setup:

.. include:: includes/web-domain-list.rst

.. note:: For this guide we will use *mysite* as the project's name and will install it to ``~/mysiteproject``.

Installation
============

Install the latest Django version.

::

 [isabell@stardust ~]$ pip3.11 install --user django
 [isabell@stardust ~]$

.. hint::

  Depending on your database configuration, additional modules like ``mysqlclient`` might be required.

Create Project
--------------

Create a top-level directory for your project somewhere. We use `~/mysiteproject` for this guide.

::

 [isabell@stardust ~]$ mkdir ~/mysiteproject
 [isabell@stardust ~]$

.. warning:: While it does not matter how you name it and where you put it, we suggest that you do **not** put this directory under any path served to the web (e.g. ``~/html``), to avoid exposing your files.

Create a new Django project under the created directory. For this guide, we call the project ``mysite``.

::

 [isabell@stardust ~]$ django-admin startproject mysite ~/mysiteproject
 [isabell@stardust ~]$

.. warning:: Avoid naming your project after built-in Python or Django components (e.g. ``django`` or ``test``).

You are now ready, to start your Django project.

Configuration
=============

Setup Database
--------------

By default, Django uses an SQLite database. That's fine for this guide.

.. hint:: You might want to use *Postgres* or *MariaDB* though…

    While out of scope for this guide, most of the time it is easy to set up: We provide :manual:`MariaDB <database-mysql>` out of the box and :manual:`Postgres <database-postgresql>` after a little bit of setup on your part. To use them with Django usually just means to ``pip install --user …`` an additional module and `setting some parameters in Django <https://docs.djangoproject.com/en/stable/ref/databases/>`_ to connect to it.

Create Database
---------------

We use the default SQLite database for this guide, so we do not need to change any settings. If you want to use another database, make sure that you have configured Django correctly and installed the needed requirements **before** this step.

Now run the migrations, to create the needed database tables.

.. code-block:: console
    :emphasize-lines: 1

    [isabell@stardust ~]$ python3.11 ~/mysiteproject/manage.py migrate
    Operations to perform:
        Apply all migrations: admin, auth, contenttypes, sessions
    Running migrations:
        Applying contenttypes.0001_initial... OK
        Applying auth.0001_initial... OK
        Applying admin.0001_initial... OK
        Applying admin.0002_logentry_remove_auto_add... OK
        Applying admin.0003_logentry_add_action_flag_choices... OK
        Applying contenttypes.0002_remove_content_type_name... OK
        Applying auth.0002_alter_permission_name_max_length... OK
        Applying auth.0003_alter_user_email_max_length... OK
        Applying auth.0004_alter_user_username_opts... OK
        Applying auth.0005_alter_user_last_login_null... OK
        Applying auth.0006_require_contenttypes_0002... OK
        Applying auth.0007_alter_validators_add_error_messages... OK
        Applying auth.0008_alter_user_username_max_length... OK
        Applying auth.0009_alter_user_last_name_max_length... OK
        Applying auth.0010_alter_group_name_max_length... OK
        Applying auth.0011_update_proxy_permissions... OK
        Applying auth.0012_alter_user_first_name_max_length... OK
        Applying sessions.0001_initial... OK
    [isabell@stardust ~]$

Create Superuser
----------------

To access Django's admin interface, you need to create a superuser account. You can do this later, or even skip this step if you do not need it; but we do it now, just in case.

You have to interactively supply a **username**, **email**, and **password**. Usually, you can just accept the suggested (i.e. your) *username* and skip the *email*, if you do not plan to use it inside Django. You should pick a decent password though!

.. code-block:: console
    :emphasize-lines: 1,4,5

    [isabell@stardust ~]$ python3.11 ~/mysiteproject/manage.py createsuperuser
    Username (leave blank to use 'isabell'):
    Email address:
    Password:
    Password (again):
    Superuser created successfully.
    [isabell@stardust ~]$

Configure Hostname
------------------

Edit ``~/mysiteproject/mysite/settings.py`` and edit the line ``ALLOWED_HOSTS = []`` to add your host name.

.. code-block:: python

    ALLOWED_HOSTS = ['isabell.uber.space']

If you need to add multiple hostnames, separate them with commas like this:

.. code-block:: python

    ALLOWED_HOSTS = ['isabell.uber.space', 'www.isabell.example']

Static Files
------------

.. note:: Instead of using *Apache* to serve your static assets - as we do below - you can instead use `WhiteNoise <https://whitenoise.evans.io/>`_. It's pretty quick to set up for Django, needs no Uberspace-specific configuration, and serves static files pretty well.

Serving static files is explained thoroughly in `Django's documentation <https://docs.djangoproject.com/en/stable/howto/static-files/>`_. We just need a few steps to set it up:

1. set `STATIC_ROOT <https://docs.djangoproject.com/en/stable/ref/settings/#static-root>`_ in ``settings.py`` to point to a directory that is served for your site - we use ``~/html/static`` here - and create the directory:

    .. code-block:: python

        STATIC_ROOT = '/home/isabell/html/static'

    .. code-block:: console
        :emphasize-lines: 1

        [isabell@stardust ~]$ mkdir ~/html/static
        [isabell@stardust ~]$

2. Run the ``collectstatic`` Django management command. This collects all the static files for your project and copies them to the directory you set in ``STATIC_ROOT``.

    .. code-block:: console
        :emphasize-lines: 1,10

        [isabell@stardust ~]$ python3.11 ~/mysiteproject/manage.py collectstatic
        You have requested to collect static files at the destination
        location as specified in your settings:

            /home/isabell/html/static

        This will overwrite existing files!
        Are you sure you want to do this?

        Type 'yes' to continue, or 'no' to cancel: yes

        130 static files copied to '/home/isabell/html/static'.
        [isabell@stardust ~]$

    .. important:: You need to run the ``collectstatic`` command every time you change your static files.

3. Add a **web backend**, to tell *Apache* to serve the path set in ``STATIC_URL`` (if you kept the default this should be ``/static/``).

    .. code-block:: console
        :emphasize-lines: 1

        [isabell@stardust ~]$ uberspace web backend set --apache /static
        Set backend for /static to apache.
        [isabell@stardust ~]$

.. note:: For this to work, you need to keep ``STATIC_ROOT`` and ``STATIC_URL`` "aligned" (i.e. your web root plus the path from  ``STATIC_URL`` matches ``STATIC_ROOT``). As in this example.

Setup Service
=============

Install Gunicorn
----------------

We will run Django as a WSGI app with `gunicorn <https://gunicorn.org/>`_ and
install the required package with pip.

::

  [isabell@stardust ~]$ pip3.11 install --user gunicorn
  [isabell@stardust ~]$

Create Service
--------------

After that, continue with setting it up as a service.

Create ``~/etc/services.d/mysite.ini`` with the following content (take care to adapt the given directory and project name according to your chosen values):

.. code-block:: ini
    :emphasize-lines: 2,3

    [program:mysite]
    directory=%(ENV_HOME)s/mysiteproject
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

Your service should be in the state ``RUNNING``. If it still is in ``STARTING`` instead, no worries! You might just have to wait sometime and try the command again (up to 15 seconds). It might already run fine anyway though. Otherwise check the logs in ``~/logs/supervisord.log``.

Configure Web Backend
---------------------

.. note::

    Gunicorn is running Django on port 8000 (as configured in the service file).
    So make sure to replace ``<port>`` in the example below with ``8000``.

.. include:: includes/web-backend.rst

Your backend should now point to the service; let's check it:

.. code-block:: console
    :emphasize-lines: 1

    [isabell@stardust ~]$ uberspace web backend list
    / http:8000 => OK, listening: PID 23161, /usr/bin/python3.11 /home/isabell/.local/bin/gunicorn --error-logfile - --reload --bind 0.0.0.0:8000 mysite.wsgi:application

    [isabell@stardust ~]$

Finishing Installation
======================

Perform a CURL request to the configured URL, to see if your installation succeeded:

.. code-block:: console
    :emphasize-lines: 1,2

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


Updates
=======

You can find a `list of supported versions`_ on the official `Django`_ site. If you want to keep track of new releases, you can check the `release-monitor`_.

Upgrading is documented in detail in the `official docs`_.

.. _official docs: https://docs.djangoproject.com/en/stable/howto/upgrade-version/
.. _list of supported versions: https://www.djangoproject.com/download/#supported-versions
.. _release-monitor: https://release-monitoring.org/project/3828/
.. _Django: https://www.djangoproject.com/

----

Tested with Django 4.1.6, Python 3.11, Uberspace 7.15

.. author_list::
