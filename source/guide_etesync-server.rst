.. highlight:: console

.. author:: nepoh <hello@nepoh.eu>

.. tag:: lang-python
.. tag:: django
.. tag:: sync
.. tag:: privacy

.. sidebar:: About

  .. image:: _static/images/etesync.svg
      :align: center

##############
EteSync Server
##############

.. tag_list::

EteSync_ is a secure, end-to-end encrypted, and privacy respecting sync for your contacts, calendars and tasks.
You can set up your own `EteSync Server`_ to sync all your devices.
It is written in :manual:`Python <lang-python>` and based on the popular :lab:`Django-Framework <guide_django>`.

----

.. warning:: EteSync Server v2 has been released_ in October 2020. This guide is about installing EteSync Server v1
    and seems to be not applicable to v2.

.. note:: For this guide you should be familiar with the basic concepts of

    * :manual:`Python <lang-python>` and its package manager pip
    * :lab:`Django-Framework <guide_django>`
    * :manual:`web backends <web-backends>`
    * :manual:`supervisord <daemons-supervisord>`
    * :manual:`domains <web-domains>`
    * :manual:`MySQL <idatabase-mysql>`


License
=======

All relevant legal information can be found here:

  * https://github.com/etesync/server/blob/master/LICENSE


Prerequisites
=============

Your URL needs to be set up:

.. include:: includes/web-domain-list.rst

Install uWSGI
-------------

.. include:: includes/install-uwsgi.rst


Installation
============

Step 1
------

Clone the source code from Github to ``~/etesync_server``.

.. code-block:: console
    :emphasize-lines: 1

    [isabell@stardust ~]$ git clone https://github.com/etesync/server.git --branch v0.3.0 ~/etesync_server
    [isabell@stardust ~]$

Step 2
------

Install the requirements for `EteSync Server`_:

::

    [isabell@stardust ~]$ cd ~/etesync_server
    [isabell@stardust etesync_server]$ pip3.6 install -r requirements.txt --user
    [isabell@stardust etesync_server]$ pip3.6 install mysqlclient --user
    [isabell@stardust etesync_server]$

Step 3
------

Install the static files:

::

    [isabell@stardust etesync_server]$ mkdir /var/www/virtual/$USER/html/static/
    [isabell@stardust etesync_server]$ ln -s /var/www/virtual/$USER/html/static/
    [isabell@stardust etesync_server]$ python3.6 manage.py collectstatic

    152 static files copied to '/home/isabell/etesync_server/static'.
    [isabell@stardust etesync_server]$

Step 4: Basic configuration
---------------------------

Create the file ``~/etesync_server/etesync_site_settings.py`` and add the following line
(replace ``isabell`` with your own username and ``MySuperSecretPassword`` with your actual MySQL password):

.. code-block:: ini
    :emphasize-lines: 1,6,7,8

    ALLOWED_HOSTS = ['isabell.uber.space']

    DATABASES = {
      'default': {
        'ENGINE': 'django.db.backends.mysql',
        'NAME': 'isabell_etesync_server',
        'USER': 'isabell',
        'PASSWORD': 'MySuperSecretPassword',
        'HOST': '127.0.0.1',
        'PORT': '3306',
      }
    }

Step 5: Database setup
----------------------

Create a database:

::

    [isabell@stardust etesync_server]$ mysql -e "CREATE DATABASE ${USER}_etesync_server DEFAULT CHARACTER SET utf8 DEFAULT COLLATE utf8_general_ci;"
    [isabell@stardust etesync_server]$

Apply database migrations:

::

    [isabell@stardust etesync_server]$ python3.6 manage.py migrate
    [isabell@stardust etesync_server]$

Step 6: Security configuration
------------------------------

Perform a Django deployment check, which will give some configuration recommendations:

::

    [isabell@stardust etesync_server]$ python3.6 manage.py check --deploy
    System check identified some issues:

     WARNINGS:
    ...
    [isabell@stardust etesync_server]$

Open ``~/etesync_server/etesync_site_settings.py`` again and add the recommended configuration at the end:

.. code-block:: ini

    # Django deployment check recommendations
    SECURE_HSTS_SECONDS = 518400
    SECURE_HSTS_INCLUDE_SUBDOMAINS = True
    SECURE_CONTENT_TYPE_NOSNIFF = True
    SECURE_BROWSER_XSS_FILTER = True
    SECURE_SSL_REDIRECT = True
    SESSION_COOKIE_SECURE = True
    CSRF_COOKIE_SECURE = True
    X_FRAME_OPTIONS = 'DENY'
    SECURE_HSTS_PRELOAD = True

Perform the check again to make sure all warnings have been resolved:

::

    [isabell@stardust etesync_server]$ python3.6 manage.py check --deploy
    System check identified no issues (0 silenced).
    [isabell@stardust etesync_server]$


Step 7: Web backend configuration
---------------------------------

.. note::

    EteSync server is running on port 8000 in the default configuration.

.. include:: includes/web-backend.rst

And for the static files:

::

    [isabell@stardust ~]$ uberspace web backend set --apache /static
    Set backend for /static to apache.
    [isabell@stardust ~]$

Step 8: Daemon setup
--------------------

To deploy your application with ``uwsgi``, create a file at ``~/uwsgi/apps-enabled/etesync_server.ini`` with the following content:

.. code-block:: ini

    [uwsgi]
    chdir = $(HOME)/etesync_server
    base = %(chdir)/etesync_server

    http = :8000
    master = true
    wsgi-file = %(base)/wsgi.py
    touch-reload = %(wsgi-file)
    static-map = /static=%(base)/static

    app = wsgi

    plugin = python

Restart ``uwsgi``:

::

    [isabell@stardust ~]$ supervisorctl restart uwsgi
    uwsgi: stopped
    uwsgi: started
    [isabell@stardust ~]$

Step 9: Test your installation
------------------------------

Perform a CURL request to your URL (e.g. ``https://isabell.uber.space``) to see if your installation succeeded:

::

    [isabell@stardust ~]$ curl -I https://isabell.uber.space
    HTTP/2 200
    ...
    [isabell@stardust ~]$

If you don't see ``HTTP/2 200`` check your installation.


Usage
=====

First, you have to create an admin user:

.. warning:: Set your own username, email and password (twice).
             Select a secure password which differs from the password used for your Uberspace account.

.. code-block:: console
    :emphasize-lines: 3,4,5,6

    [isabell@stardust ~]$ cd ~/etesync_server
    [isabell@stardust etesync_server]$ python3.6 manage.py createsuperuser
    Username (leave blank to use 'isabell'):
    Email address: isabell@uber.space
    Password:
    Password (again):
    Superuser created successfully.
    [isabell@stardust etesync_server]$

.. warning:: It is not recommended to use the admin user in daily life (i.e. for syncing data between your devices).
             So, go to ``https://isabell.uber.space/admin``, log in with your admin user credentials
             and create a separate non-privileged user.

Now you can install the EteSync_ app on your device(s) and connect to your EteSync server
using your URL (e.g. ``https://isabell.uber.space``) and the non-privileged user's credentials.


Backup
======

Relevant data to be backed up is the SQL database and the file ``~/etesync_server/secret.txt``.
They both are included in the :manual:`backups <basics-backup>` of your whole Uberspace.
But since your contacts and calendar data may be too important to loose, consider setting up a separate backup strategy.

To create backups automatically, create a file ``~/bin/backup-etesync-server`` with the following content (replace ``isabell_etesync_server`` with your own database name):

.. code-block:: bash
    :emphasize-lines: 4

    #!/usr/bin/env bash

    # specify the database name
    DATABASE_NAME=isabell_etesync_server

    # create the backup target
    BACKUP_DIR="${HOME}/backup/etesync_server/$(date '+%Y-%m-%d')"
    mkdir -p "$BACKUP_DIR"

    # backup relevant data
    mysqldump $DATABASE_NAME > "${BACKUP_DIR}/${DATABASE_NAME}.sql"
    cp ${HOME}/etesync_server/secret.txt "$BACKUP_DIR"

Make the file executable:

::

    [isabell@stardust ~]$ chmod +x ~/bin/backup-etesync-server

Set up a cron job by using the ``crontab -e`` command and adding the line:

::

    @daily  $HOME/bin/backup-etesync-server

.. warning:: Your backups should be stored at another location outside your Uberspace!

.. warning:: Keep in mind that the data stored by EteSync server is end-to-end encrypted.
             Therefore, the data from your server backups can not be restored without the encryption password
             which is not included in the backups, because it only exists on your synchronized devices.
             Make sure you keep your encryption password in a safe place, too!

.. _EteSync: https://www.etesync.com/
.. _EteSync Server: https://github.com/etesync/server
.. _Django:  https://www.djangoproject.com/
.. _released: https://github.com/etesync/server/releases/tag/v0.5.0

----

Tested with EteSync server 0.3.0 and Uberspace 7.7.1.2

.. author_list::


