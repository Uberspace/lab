.. highlight:: console

.. author:: MetroMarv <https://github.com/MetroMarv/>

.. categorize your guide! refer to the current list of tags: https://lab.uberspace.de/tags
.. tag:: lang-python
.. tag:: web
.. tag:: django
.. tag:: monitoring

.. sidebar:: About

  .. image:: _static/images/healthchecks.svg
      :align: center

##########
Healthchecks
##########

.. tag_list::

`Healthchecks <https://github.com/healthchecks/healthchecks>`_ allows you to monitor your periodically run jobs (e.g. CronJobs). It will inform you via different channels (mail, Mattermost,
Slack, Signal, ...) if your job didn't execute on time. To track execution HTTP request or mails may be used.

It offers a web interface to manage your jobs to be monitored.

.. note::
  This guide is based upon the `selfhost documentation`_ of the Healthchecks maintainers.

----

.. note:: For this guide you should be familiar with the basic concepts of

  * :manual:`Python <lang-python>`
  * :manual:`MySQL <database-mysql>` or :manual:`PostgreSQL <database-postgresql>` (not used in this guide)
  * :manual:`supervisord <daemons-supervisord>`
  * :manual:`domains <web-domains>`

License
=======

All relevant legal information can be found here

  * https://github.com/healthchecks/healthchecks/blob/master/LICENSE

Prerequisites
=============

First of all we create a new :manual:`MySQL <database-mysql>` database, that our Healthchecks instance will use:

::

 [isabell@stardust ~]$ mysql -e "CREATE DATABASE isabell_healthchecks"
 [isabell@stardust ~]$

If you'd like to use :manual:`PostgreSQL <database-postgresql>` instead. Please see the respective
:manual:`manual entry <database-postgresql>`.

.. include:: includes/my-print-defaults.rst

Second we create a :manual_anchor:`new mailbox <mail-mailboxes/#setup-a-new-mailbox>`, that we'll use to send alerts to our private email
address if one of our jobs failed to run. You'll have to interactively provide a password. Please choose a secure one and remember the
password, you'll need it later.

::

 [isabell@stardust ~]$ uberspace mail user add healthchecks
 Enter a password for the mailbox:
 Please confirm your password:
 New mailbox created for user: 'healthchecks', it will be live in a few minutes...
 [isabell@stardust ~]$

Third of all your URL needs to be setup:

.. include:: includes/web-domain-list.rst


We're using :manual:`Python <lang-python>` in the currently latest version 3.11:

::

 [isabell@stardust ~]$ python3.11 --version
 Python 3.11.7
 [isabell@stardust ~]$

Installation
============

Download the source
-------------------

In the following steps we'll create a separate folder for this app and future apps, download the :manual:`Python <lang-python>` source code
from GitHub and select the latest version using git tags:

.. code-block:: console
 :emphasize-lines: 21

 [isabell@stardust ~]$ mkdir ~/apps
 [isabell@stardust ~]$ cd ~/apps
 [isabell@stardust ~]$ git clone https://github.com/healthchecks/healthchecks.git
 Cloning into 'healthchecks'...
 remote: Enumerating objects: 28393, done.
 remote: Counting objects: 100% (3677/3677), done.
 remote: Compressing objects: 100% (448/448), done.
 remote: Total 28393 (delta 3420), reused 3349 (delta 3229), pack-reused 24716
 Receiving objects: 100% (28393/28393), 22.57 MiB | 14.09 MiB/s, done.
 Resolving deltas: 100% (22120/22120), done.
 [isabell@stardust ~]$ cd healthchecks
 [isabell@stardust ~]$ git tag
 1.0.2
 v1.0
 v1.0.1
 v1.0.2
 [...]
 v2.9.2
 v3.0
 v3.0.1
 v3.2
 v3.1
 [isabell@stardust ~]$ git checkout v3.2
 Note: switching to 'v3.2'.

 You are in 'detached HEAD' state. You can look around, make experimental
 changes and commit them, and you can discard any commits you make in this
 state without impacting any branches by switching back to a branch.

 If you want to create a new branch to retain commits you create, you may
 do so (now or later) by using -c with the switch command. Example:

   git switch -c <new-branch-name>

 Or undo this operation with:

   git switch -

 Turn off this advice by setting config variable advice.detachedHead to false

 HEAD is now at c99b644a Update CHANGELOG for v3.2 release
 [isabell@stardust ~]$

The note of the ``git checkout`` command can be ignored as we do not plan to do any commits in this git repository.

Set up the virtual environment
-----------------

Next we will setup a :manual:`Python <lang-python>` virtual environment where all dependencies are encapsulated. Then we
install the required dependencies and on top of that also `gunicorn <https://gunicorn.org/>`_ which will be our HTTP server
later.

::

 [isabell@stardust ~]$ python3.11 -m venv venv
 [isabell@stardust ~]$ source venv/bin/activate
 (venv) [isabell@stardust ~]$ pip3.11 install -r requirements.txt
 Collecting aiosmtpd==1.4.4.post2 (from -r requirements.txt (line 1))
   Obtaining dependency information for aiosmtpd==1.4.4.post2 from https://files.pythonhosted.org/packages/ef/b3/f4cce9da53b02aa7d4c0662ca344421023feefc5c8f815b90d1c7514702e/aiosmtpd-1.4.4.post2-py3-none-any.whl.metadata
   Downloading aiosmtpd-1.4.4.post2-py3-none-any.whl.metadata (6.8 kB)
 […]
 [notice] A new release of pip is available: 23.2.1 -> 24.0
 [notice] To update, run: pip install --upgrade pip
 (venv) [isabell@stardust ~]$ pip3.11 install mysql
 Collecting mysql
   Obtaining dependency information for mysql from https://files.pythonhosted.org/packages/9a/52/8d29c58f6ae448a72fbc612955bd31accb930ca479a7ba7197f4ae4edec2/mysql-0.0.3-py3-none-any.whl.metadata
   Downloading mysql-0.0.3-py3-none-any.whl.metadata (746 bytes)
 Collecting mysqlclient (from mysql)
   Using cached mysqlclient-2.2.4-cp311-cp311-linux_x86_64.whl
 […]
 (venv) [isabell@stardust ~]$ pip3.11 install gunicorn
 Collecting gunicorn
   Obtaining dependency information for gunicorn from https://files.pythonhosted.org/packages/0e/2a/c3a878eccb100ccddf45c50b6b8db8cf3301a6adede6e31d48e8531cab13/gunicorn-21.2.0-py3-none-any.whl.metadata
   Using cached gunicorn-21.2.0-py3-none-any.whl.metadata (4.1 kB)
 Collecting packaging (from gunicorn)
   Obtaining dependency information for packaging from https://files.pythonhosted.org/packages/49/df/1fceb2f8900f8639e278b056416d49134fb8d84c5942ffaa01ad34782422/packaging-24.0-py3-none-any.whl.metadata
   Downloading packaging-24.0-py3-none-any.whl.metadata (3.2 kB)
 […]
  (venv) [isabell@stardust ~]$

Configuration
=============

Configure the app
------------------------

Edit the file ``./hc/local_settings.py`` and set your host specific settings:

.. code-block:: python

 DEBUG = False

 SITE_ROOT = 'https://isabell.uber.space'
 SITE_NAME = 'My Monitoring Project'
 PING_ENDPOINT='https://isabell.uber.space/ping/'
 DEFAULT_FROM_EMAIL = 'healthchecks@isabell.uber.space'
 ALLOWED_HOSTS=['isabell.uber.space']
 CSRF_TRUSTED_ORIGINS=['https://isabell.uber.space']
 SECRET_KEY = '<PLACE A RANDOM STRING HERE>'
 REGISTRATION_OPEN = False # True if you'd like to allow user registrations of anyone from the internet

 DATABASES = {
     'default': {
         'ENGINE': 'django.db.backends.mysql',
         'HOST': 'localhost',
         'PORT': '3306',
         'NAME': 'isabell_healthchecks',
         'USER': 'isabell',
         'PASSWORD': 'MySuperSecretPassword',
         'TEST': {'CHARSET': 'UTF8'}
     }
 }

 # Email
 EMAIL_HOST = 'stardust.uberspace.de'
 EMAIL_PORT = 465
 EMAIL_HOST_USER = 'healthchecks@isabell.uber.space'
 EMAIL_HOST_PASSWORD = 'MySuperSecretPassword'
 EMAIL_USE_TLS = False
 EMAIL_USE_SSL = True



Initialize the database
-----------------

Once we set the correct settings we can initialize the database:

.. note:: All commands that start with ``(venv)`` require an activated Python Virtual Environment, you can activate it with ``source venv/bin/activate``.

::

 (venv) [isabell@stardust ~]$ python3.11 ./manage.py migrate
 System check identified some issues:

 WARNINGS:
 ?: (mysql.W002) MariaDB Strict Mode is not set for database connection 'default'
 	HINT: MariaDB's Strict Mode fixes many data integrity problems in MariaDB, such as data truncation upon insertion, by escalating warnings into errors. It is strongly recommended you activate it. See: https://docs.djangoproject.com/en/5.0/ref/databases/#mysql-sql-mode
 api.Check: (models.W037) MariaDB does not support indexes with conditions.
 	HINT: Conditions will be ignored. Silence this warning if you don't care about it.
 api.Flip: (models.W037) MariaDB does not support indexes with conditions.
 	HINT: Conditions will be ignored. Silence this warning if you don't care about it.
 Operations to perform:
   Apply all migrations: accounts, admin, api, auth, contenttypes, logs, payments, sessions
 Running migrations:
   Applying contenttypes.0001_initial... OK
   [...]
   Applying payments.0008_subscription_setup_date... OK
   Applying payments.0009_alter_subscription_user... OK
   Applying sessions.0001_initial... OK

Set up a superuser
-----------------

To access the healthchecks web interface also Django’s admin interface, you need to create a superuser account.

You have to interactively supply a username, email, and password. Usually, you can just accept the suggested (i.e. your) username and skip
the email, if you do not plan to use it inside Django. You should pick a decent password though!

.. code-block:: console
 :emphasize-lines: 2,3,4

 (venv) [isabell@stardust ~]$ python3.11 ./manage.py createsuperuser
 Email address:isabell@uber.space
 Password:
 Password (again):
 Superuser created successfully.
 (venv) [isabell@stardust ~]$

Generate static files
-----------------

Healthchecks uses a couple of static files. We need to generate this as follows:

::

 (venv) [isabell@stardust ~]$ python3.11 ./manage.py collectstatic
 347 static files copied to '/home/isabell/apps/healthchecks/static-collected'.
 (venv) [isabell@stardust ~]$ python3.11 ./manage.py compress
 Compressing... done
 Compressed 26 block(s) from 147 template(s) for 1 context(s).
 (venv) [isabell@stardust ~]$

Set up the daemons
-----------------

Healthchecks requires two daemons to be running. One is for the web interface and another is for the alert. Optionally you can create a
third daemon to send monthly reports. We'll manage this daemons using :manual:`supervisord <daemons-supervisord>`:

Create the file ``~/etc/services.d/healthchecks.ini`` with following content:

.. code-block:: ini

 [program:healthchecks]
 directory=/home/isabell/apps/healthchecks
 command=/bin/bash -c 'venv/bin/gunicorn --bind 0.0.0.0:8000 hc.wsgi:application'
 autostart=true
 autorestart=true
 stopsignal=INT
 # `startsecs` is set by Uberspace monitoring team, to prevent a broken service from looping
 startsecs=30

Then create the file ``~/etc/services.d/healthchecks-sendalert.ini`` with following content:

.. code-block:: ini

 [program:healthchecks-sendalert]
 directory=/home/isabell/apps/healthchecks
 command=/bin/bash -c 'venv/bin/python3.11 manage.py sendalerts'
 autostart=true
 autorestart=true
 stopsignal=INT
 # `startsecs` is set by Uberspace monitoring team, to prevent a broken service from looping
 startsecs=30

Optionally create the third file ``~/etc/services.d/healthchecks-sendreport.ini`` to activate monthly reports with following content:

.. code-block:: ini

 [program:healthchecks-sendreport]
 directory=/home/isabell/apps/healthchecks
 command=/bin/bash -c 'venv/bin/python manage.py sendreports --loop'
 autostart=true
 autorestart=true
 stopsignal=INT
 # `startsecs` is set by Uberspace monitoring team, to prevent a broken service from looping
 startsecs=30

After creating the files ask :manual:`supervisord <daemons-supervisord>` to reload it's config files and start the services:

::

 [isabell@stardust ~]$ supervisorctl reread
 healthchecks: available
 healthchecks-sendalert: available
 healthchecks-sendreport: available
 [isabell@stardust ~]$ supervisorctl update
 healthchecks: updated process group
 healthchecks-sendalert: updated process group
 healthchecks-sendreport: updated process group
 [isabell@stardust ~]$ supervisorctl status
 healthchecks                   RUNNING   pid 13331, uptime 0:03:14
 healthchecks-sendalert         RUNNING   pid 19516, uptime 0:03:14
 healthchecks-sendreport        RUNNING   pid 19517, uptime 0:03:14
 [isabell@stardust ~]$

Configure web backend
-----------------

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

Finishing installation
======================

Point your browser to the configured URL and login with your superuser account.

Best practices
==============

Security
--------

Change all default passwords. Look at folder permissions. Don't get hacked!

Updates
=======

.. note:: Check the `releases feed <https://github.com/healthchecks/healthchecks/releases.atom>`_ regularly to stay informed about the newest
 version. Alternatively check the `releases page <https://github.com/healthchecks/healthchecks/releases>`_ regularly.

If we'd like upgrade to a newer release, we'll first stop the running services, pull the latest source files and basically repeat the
installation process (install latest pip dependencies, migrate the database, generate static files).

::

 [isabell@stardust ~]$ supervisorctl stop healthchecks healthchecks-sendalert healthchecks-sendreport
 [isabell@stardust ~]$ git pull
 remote: Enumerating objects: 286, done.
 remote: Counting objects: 100% (286/286), done.
 remote: Compressing objects: 100% (137/137), done.
 remote: Total 286 (delta 187), reused 241 (delta 149), pack-reused 0
 Receiving objects: 100% (286/286), 337.52 KiB | 14.67 MiB/s, done.
 Resolving deltas: 100% (187/187), completed with 35 local objects.
 From https://github.com/healthchecks/healthchecks
    c99b644a..0a7744c3  master     -> origin/master
 You are not currently on a branch.
 Please specify which branch you want to merge with.
 See git-pull(1) for details.

     git pull <remote> <branch>

 [isabell@stardust ~]$ git checkout <Tag of new version>
 Note: switching to '<Tag of new version>'.

 You are in 'detached HEAD' state. You can look around, make experimental
 changes and commit them, and you can discard any commits you make in this
 state without impacting any branches by switching back to a branch.

 If you want to create a new branch to retain commits you create, you may
 do so (now or later) by using -c with the switch command. Example:

   git switch -c <new-branch-name>

 Or undo this operation with:

   git switch -

 Turn off this advice by setting config variable advice.detachedHead to false

 HEAD is now at <some SHA> <some commit message of new version>
 [isabell@stardust ~]$ source venv/bin/activate
 (venv) [isabell@stardust ~]$ pip3.11 install -r requirements.txt
 Looking in indexes: https://pypi.org/simple/
 Collecting aiosmtpd==1.4.6 (from -r requirements.txt (line 1))
   Obtaining dependency information for aiosmtpd==1.4.6 from https://files.pythonhosted.org/packages/ec/39/d401756df60a8344848477d54fdf4ce0f50531f6149f3b8eaae9c06ae3dc/aiosmtpd-1.4.6-py3-none-any.whl.metadata
   Downloading aiosmtpd-1.4.6-py3-none-any.whl.metadata (6.6 kB)
 [...]
 (venv) [isabell@stardust ~]$ python3.11 ./manage.py migrate
 System check identified some issues:

 WARNINGS:
 ?: (mysql.W002) MariaDB Strict Mode is not set for database connection 'default'
 	HINT: MariaDB's Strict Mode fixes many data integrity problems in MariaDB, such as data truncation upon insertion, by escalating warnings into errors. It is strongly recommended you activate it. See: https://docs.djangoproject.com/en/5.1/ref/databases/#mysql-sql-mode
 api.Check: (models.W037) MariaDB does not support indexes with conditions.
 	HINT: Conditions will be ignored. Silence this warning if you don't care about it.
 api.Flip: (models.W037) MariaDB does not support indexes with conditions.
 	HINT: Conditions will be ignored. Silence this warning if you don't care about it.
 Operations to perform:
   Apply all migrations: accounts, admin, api, auth, contenttypes, logs, payments, sessions
 Running migrations:
   Applying accounts.0049_convert_email_lowercase... OK
   Applying api.0103_check_badge_key... OK
 [...]
 (venv) [isabell@stardust ~]$ python3.11 ./manage.py collectstatic

 You have requested to collect static files at the destination
 location as specified in your settings:

     /home/metro/apps/healthcheck/static-collected

 This will overwrite existing files!
 Are you sure you want to do this?

 Type 'yes' to continue, or 'no' to cancel: yes

 172 static files copied to '/home/metro/apps/healthcheck/static-collected', 182 unmodified.
 (venv) [isabell@stardust ~]$ python3.11 ./manage.py compress
 Compressing... done
 Compressed 26 block(s) from 145 template(s) for 1 context(s).
 [isabell@stardust ~]$ supervisorctl start healthchecks healthchecks-sendalert healthchecks-sendreport
  healthchecks: started
  healthchecks-sendalert: started
  healthchecks-sendreport: started

Debugging
=========

If something fails you can check the :manual:`supervisord <daemons-supervisord>` logs. E.g. for the web interface service you can do this as
follows:

::

 [isabell@stardust ~]$ supervisorctl tail healthchecks stderr
 [2024-03-03 19:05:14 +0100] [13331] [INFO] Starting gunicorn 21.2.0
 [2024-03-03 19:05:14 +0100] [13331] [INFO] Listening at: http://0.0.0.0:8000 (13331)
 [2024-03-03 19:05:14 +0100] [13331] [INFO] Using worker: sync
 [2024-03-03 19:05:14 +0100] [13332] [INFO] Booting worker with pid: 13332
 [2024-03-10 18:11:55 +0100] [13331] [INFO] Handling signal: int
 [2024-03-10 17:11:55 +0000] [13332] [INFO] Worker exiting (pid: 13332)
 [2024-03-10 18:11:56 +0100] [13331] [INFO] Shutting down: Master
 [2024-03-10 18:13:46 +0100] [10587] [INFO] Starting gunicorn 21.2.0
 [2024-03-10 18:13:46 +0100] [10587] [INFO] Listening at: http://0.0.0.0:8000 (10587)
 [2024-03-10 18:13:46 +0100] [10587] [INFO] Using worker: sync
 [2024-03-10 18:13:46 +0100] [10588] [INFO] Booting worker with pid: 10588

Backup
======

All generated data you should backup regularly is saved to the database and the database is regularly backed up by Uberspace.

.. _Selfhost documentation: https://healthchecks.io/docs/self_hosted/

----

Tested with Healthchecks 3.2.0, Python 3.11, Uberspace 7.1.1

.. author_list::
