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

.. note:: For this guide you should be familiar with the basic concepts of

  * :manual:`Python <lang-python>` and its package manager pip
  * :lab:`Django-Framework <guide_django>`
  * :manual:`web backends <web-backends>`
  * :manual:`supervisord <daemons-supervisord>`
  * :manual:`domains <web-domains>`

License
=======

All relevant legal information can be found here

  * https://github.com/etesync/server/blob/master/LICENSE

Prerequisites
=============

Your URL needs to be setup:

.. include:: includes/web-domain-list.rst

Install uWSGI
-------------

.. include:: includes/install-uwsgi.rst

Installation
============

Step 1
------

Clone the source code from Github to ``~/etesync_server``.
Make sure to replace the release number ``v0.3.0`` in the command with the latest release
which can be found at the release_ page on GitHub:

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
 [isabell@stardust etesync_server]$

Step 3
------

Apply database migrations:

::

 [isabell@stardust etesync_server]$ python3.6 manage.py migrate
 [isabell@stardust etesync_server]$

Install the static files:

::

 [isabell@stardust etesync_server]$ mkdir /var/www/virtual/$USER/html/static/
 [isabell@stardust etesync_server]$ ln -s /var/www/virtual/$USER/html/static/
 [isabell@stardust etesync_server]$ python3.6 manage.py collectstatic

 152 static files copied to '/home/isabell/etesync_server/static'.
 [isabell@stardust etesync_server]$

Configuration
=============

Configure Webserver
-------------------

Open ``~/etesync_server/etesync_server/settings.py`` and edit the line ``ALLOWED_HOSTS = []`` to add your host name (e.g. ``isabell.uber.space``):

.. code-block:: ini

 ALLOWED_HOSTS = ['isabell.uber.space']

Security configuration
----------------------

Perform a Django deployment check, which will give some configuration recommendations:

::

 [isabell@stardust ~]$ cd ~/etesync_server
 [isabell@stardust etesync_server]$ python3.6 manage.py check --deploy
 System check identified some issues:

 WARNINGS:
 ...
 [isabell@stardust etesync_server]$ 

Open ``~/etesync_server/etesync_server/settings.py`` and add the recommanded configuration at the end:

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


Configure web backend
---------------------

.. note::

    EteSync server is running on port 8000 in the default configuration.

.. include:: includes/web-backend.rst

And for the static files:

::

  [isabell@stardust ~]$ uberspace web backend set --apache /static
  Set backend for /static to apache.
  [isabell@stardust ~]$

Setup daemon
------------

To deploy your application with ``uwsgi``, create a file at ``~/uwsgi/apps-enabled/etesync_server.ini`` with the following content:

.. warning:: Replace ``<username>`` with your username! (3 times)

.. code-block:: ini
  :emphasize-lines: 2,15,16

  [uwsgi]
  chdir = /home/<username>/etesync_server
  base = %(chdir)/etesync_server

  http = :8000
  master = true
  wsgi-file = %(base)/wsgi.py
  touch-reload = %(wsgi-file)
  static-map = /static=%(base)/static

  app = wsgi

  plugin = python

  uid = <username>
  gid = <username>

Restart ``uwsgi``:

::

 [isabell@stardust etesync_server]$ supervisorctl restart uwsgi

Test installation
-----------------

Perform a CURL request to your URL (e.g. ``https://isabell.uber.space``) to see if your installation succeeded:

::

 [isabell@stardust ~]$ curl -I https://isabell.uber.space
 HTTP/2 200 
 ...
 [isabell@stardust ~]$

If you don't see ``HTTP/2 200 OK`` check your installation.

Usage
=====

First, you have to create an admin user:

.. warning:: Set your own username, email and password (twice).
             Select a secure password which should differ from the password used for your Uberspace account.

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
             and create a non-privileged user that you can use.

Now you can install the EteSync_ app on your device(s), and log into your account
using your EteSync Server (e.g. ``https://isabell.uber.space``) to be used for syncing.

Backup
======

.. warning:: Do not (solely) rely on the :manual:`Uberspace backups <basics-backup>`.

Relevant data to be backed up is the SQLite database (which is located at ``~/etesync_server/db.sqlite3``)
and the file ``~/etesync_server/secret.txt``.
Both files are included in the :manual:`backups <basics-backup>` of your whole Uberspace.
But the SQLite database should be backed up with SQLite itself to avoid inconsistant state due to concurrent read/writes.

To set up an automatic backup, create a file ``~/bin/backup-etesync-server`` with the following content:

.. code-block:: bash

 #!/usr/bin/env bash

 # create the backup target
 BACKUP_DIR="$HOME/backup/etesync_server/$(date)"
 mkdir -p "$BACKUP_DIR"

 # backup relevant data
 sqlite3 ~/etesync_server/db.sqlite3 ".backup '$BACKUP_DIR/db.sqlite3'"
 cp ~/etesync_server/secret.txt "$BACKUP_DIR"

Make the file executable:

.. code-block:: console

 [isabell@stardust ~]$ chmod +x ~/bin/backup-etesync-server

Set up a cron job by using the ``crontab -e`` command and adding the line:

::

 @daily  $HOME/bin/backup-etesync-server

.. warning:: Your backup should be stored at another location outside your Ubersapce!

             Depending on the size of your SQLite database you should probably think about deleting
             old backups from your Uberspace, too.

.. warning:: Keep in mind that the data stored by EteSync server is end-to-end encrypted.
             Therefore the data from your server backups can not be restored without the encryption password
             which is not included in the backups, because it only exists on your syncronized devices.
             Make sure you keep your encryption password in a safe place, too!

Updates
=======

.. note:: Check the release_ page on GitHub regularly or follow the feed_ to stay informed about the newest version.

If there is a new version available, update your EteSync server installation.
To get the latest release with ``git``, you first have to commit the changes you made to ``~/etesync_server/etesync_server/settings.py``:

.. code-block:: console

 [isabell@stardust ~]$ cd ~/etesync_server
 [isabell@stardust etesync_server]$ git add etesync_server/settings.py
 [isabell@stardust etesync_server]$ git commit -m "adjust django application settings"
 [isabell@stardust etesync_server]$ 

Then you can install the latest release (make sure to replace ``v0.3.x`` in the second command with the latest version number):

.. code-block:: console
 :emphasize-lines: 1

 [isabell@stardust etesync_server]$ git pull --rebase origin v0.3.x
 [isabell@stardust etesync_server]$ pip3.6 install -U -r requirements.txt
 [isabell@stardust etesync_server]$ python3.6 manage.py migrate
 [isabell@stardust etesync_server]$ python3.6 manage.py collectstatic
 [isabell@stardust etesync_server]$ 


.. _EteSync: https://www.etesync.com/
.. _EteSync Server: https://github.com/etesync/server
.. _Django:  https://www.djangoproject.com/
.. _release: https://github.com/etesync/server/releases
.. _feed: https://github.com/etesync/server/releases.atom

----

Tested with EteSync server 0.3.0 and Uberspace 7.7.1.2

.. author_list::


