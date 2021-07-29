.. highlight:: console

.. author:: GodMod <godmod@eqdkp-plus.eu>
.. tag:: lang-python
.. tag:: django
.. tag:: presentations
.. tag:: web
.. tag:: assemblies
.. tag:: meetings
.. tag:: audience-business

.. sidebar:: About

  .. image:: _static/images/openslides.svg
      :align: center

##########
OpenSlides
##########

.. tag_list::

OpenSlides is a free, web-based presentation and assembly system for managing and projecting agenda, motions, and elections of assemblies.

----

.. note:: For this guide you should be familiar with the basic concepts of

  * :manual:`Python <lang-python>` and its package manager pip
  * :manual:`supervisord <daemons-supervisord>`
  * :manual:`Web Backends <web-backends>`
  * :manual:`MySQL <database-mysql>`

License
=======

OpenSlides_ is released under the `MIT License`_.

Prerequisites
=============

Your URL needs to be setup:

::

 [isabell@stardust ~]$ uberspace web domain list
 isabell.uber.space
 [isabell@stardust ~]$

.. include:: includes/my-print-defaults.rst

Installation
============

Install Python packages
-----------------------
Install the OpenSlides Python package:

::

 [isabell@stardust ~]$ pip3.7 install openslides mysqlclient --user
 [...]
 Running setup.py install for pyrsistent ... done
 Running setup.py install for PyPDF2 ... done
 Running setup.py install for roman ... done
 Running setup.py install for websockets ... done
 Running setup.py install for openslides ... done
 Running setup.py install for mysqlclient ... done
 [...]
 [isabell@stardust ~]$

Check if OpenSlides is installed by typing:

::

 [isabell@stardust ~]$ openslides --version
 3.3
 [isabell@stardust ~]$

Create Database
---------------
For performance reasons, we will use a :manual:`MySQL <database-mysql>` database for storing the OpenSlides data. It is recommended to use an :manual_anchor:`additional database <database-mysql.html#additional-databases>` (e.g. ``isabell_openslides``) instead of the default database.

.. code-block:: console

 [isabell@stardust ~]$ mysql --verbose --execute="CREATE DATABASE ${USER}_openslides"
 --------------
 CREATE DATABASE isabell_openslides
 --------------
 [isabell@stardust ~]$


Create configuration
--------------------
Run the following command to create the configuration:

::

 [isabell@stardust ~]$ openslides createsettings
 Settings created at /home/isabell/.config/openslides/settings.py
 [isabell@stardust ~]$

Open the file ``~/.config/openslides/settings.py`` and replace the existing database configuration (``DATABASES``) with the following one:

::

    DATABASES = {
        'default': {
            'ENGINE': 'django.db.backends.mysql',
            'NAME': 'isabell_openslides',
            'USER': 'isabell',
            'PASSWORD': 'MySuperSecretPassword',
            'HOST': 'localhost',
            'PORT': '',
            'OPTIONS': {
                'init_command': "SET sql_mode='STRICT_TRANS_TABLES'",
            },
        }
    }
    # This will suppress an error, which already was converted into a warning, see https://code.djangoproject.com/ticket/31144
    SILENCED_SYSTEM_CHECKS = ['mysql.E001']

Check the beginning of the guide for your :manual_anchor:`database credentials <database-mysql.html#login-credentials>` and replace name, user and password with your database name and database credentials.

Then, we will populate the database by running the following command:

::

 [isabell@stardust ~]$ openslides migrate
 Operations to perform:
   Apply all migrations: agenda, assignments, auth, contenttypes, core, mediafiles, motions, sessions, topics, users
 Running migrations:
   Applying contenttypes.0001_initial... OK
 [...]
 [2021-04-11 20:59:34 +0200] [21317] [INFO] openslides.core.apps [zxnj] Updated config variables
 [isabell@stardust ~]$


Create web backend
------------------

.. note::

    OpenSlides is running on port 8000.

.. include:: includes/web-backend.rst


Create service
--------------

You should set up a service that keeps OpenSlides alive while you are gone. We will use ``daphne`` as an ASGI backend server for the OpenSlides application. Create the file ``~/etc/services.d/openslides.ini`` with the following content:

.. code-block:: ini

 [program:openslides]
 command=daphne -b 0.0.0.0 -p 8000 openslides.asgi:application
 autostart=true
 autorestart=true
 stopsignal=INT

.. include:: includes/supervisord.rst

If it's not in state RUNNING, check your configuration.


Access OpenSlides
-----------------
Now point your Browser to your installation URL ``https://isabell.uber.space``.

Use ``admin`` as username and ``admin`` as password for your first login. You should change this password at ``https://isabell.uber.space/users/password`` immediately after login!


Configuration
=============

You can find the configuration file of OpenSlides at ``~/.config/openslides/settings.py``. There you can make settings for SMTP, Redis, SAML etc.


Updates
=======

.. note:: Check the update feed_ regularly to stay informed about the newest version.


If there is a new version available, update the following command to update your OpenSlides python package:

::

 [isabell@stardust ~]$ servicectl stop openslides
 [isabell@stardust ~]$ pip3.7 install --upgrade openslides
 [...]
        Successfully uninstalled openslides-3.2
     Running setup.py install for openslides ... done
 Successfully installed openslides-3.3
 [...]
 [isabell@stardust ~]$ servicectl start openslides
 [isabell@stardust ~]$

Backup
======

Backup the following directories:

  * ``~/.local/share/openslides/``
  * ``~/.config/openslides/``

Additionally, backup the MySQL database:

.. code-block:: console

  [isabell@stardust ~]$ mysqldump isabell_openslides | xz - > ~/isabell_openslides.sql.xz

Debugging
=========

In case of problems, the log file ``~/logs/supervisord.log`` is the first point for you.

Moreover, you can adjust the logging of OpenSlides. For example, you can log the outputs to a file. To achieve that, edit the file ``~/.config/openslides/settings.py`` an replace the existing ``LOGGING`` section with the following one:

::

  LOGGING = {
      'version': 1,
      'disable_existing_loggers': False,
      'formatters': {
          'gunicorn': {
              'format': '{asctime} [{process:d}] [{levelname}] {name} {message}',
              'style': '{',
              'datefmt': '[%Y-%m-%d %H:%M:%S %z]',
          },
      },
      'handlers': {
          'console': {
              'class': 'logging.StreamHandler',
              'formatter': 'gunicorn',
          },
      'file': {
              'class': 'logging.FileHandler',
              'filename': '/home/isabell/logs/openslides.log',
          },
      },
      'loggers': {
          'django': {
              'handlers': ['file'],
              'level': os.getenv('DJANGO_LOG_LEVEL', 'INFO'),
          },
          'openslides': {
              'handlers': ['file'],
              'level': os.getenv('OPENSLIDES_LOG_LEVEL', 'INFO'),
          }
      },
  }

This will log everything to the file ``/home/isabell/logs/openslides.log`` instead being displayed in the console.


.. _OpenSlides: https://openslides.com/
.. _feed: https://github.com/OpenSlides/OpenSlides/releases.atom
.. _MIT License: https://github.com/OpenSlides/OpenSlides/blob/master/LICENSE

----

Tested with OpenSlides 3.3 and Uberspace 7.9.0.0

.. author_list::
