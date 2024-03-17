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

Next we will setup a :manual:`Python <lang-python>` virtual environment where all dependencies are encapsulated:

::

 [isabell@stardust ~]$ python3.11 -m venv venv
 [isabell@stardust ~]$ source venv/bin/activate
 [isabell@stardust ~]$ pip3.11 install -r requirements.txt
 Collecting aiosmtpd==1.4.4.post2 (from -r requirements.txt (line 1))
   Obtaining dependency information for aiosmtpd==1.4.4.post2 from https://files.pythonhosted.org/packages/ef/b3/f4cce9da53b02aa7d4c0662ca344421023feefc5c8f815b90d1c7514702e/aiosmtpd-1.4.4.post2-py3-none-any.whl.metadata
   Downloading aiosmtpd-1.4.4.post2-py3-none-any.whl.metadata (6.8 kB)
 Collecting cronsim==2.5 (from -r requirements.txt (line 2))
   Using cached cronsim-2.5-py3-none-any.whl
 Collecting Django==5.0.2 (from -r requirements.txt (line 3))
   Obtaining dependency information for Django==5.0.2 from https://files.pythonhosted.org/packages/50/1b/7536019fd20654919dcd81b475fee1e54f21bd71b2b4e094b2ab075478b2/Django-5.0.2-py3-none-any.whl.metadata
   Using cached Django-5.0.2-py3-none-any.whl.metadata (4.1 kB)
 Collecting django-compressor==4.4 (from -r requirements.txt (line 4))
   Obtaining dependency information for django-compressor==4.4 from https://files.pythonhosted.org/packages/a0/b5/3c000d6d7b8ffa8831d2ef5bcbbe5780de172024e226ec89391853d4b759/django_compressor-4.4-py2.py3-none-any.whl.metadata
   Using cached django_compressor-4.4-py2.py3-none-any.whl.metadata (5.0 kB)
 Collecting django-stubs-ext==4.2.7 (from -r requirements.txt (line 5))
   Obtaining dependency information for django-stubs-ext==4.2.7 from https://files.pythonhosted.org/packages/21/be/e87631afa766a101877758495bec4108fdaa20ba65a2e80bc02cfa874985/django_stubs_ext-4.2.7-py3-none-any.whl.metadata
   Using cached django_stubs_ext-4.2.7-py3-none-any.whl.metadata (3.6 kB)
 Collecting fido2==1.1.2 (from -r requirements.txt (line 6))
   Obtaining dependency information for fido2==1.1.2 from https://files.pythonhosted.org/packages/e3/99/68bab31fbb49e8b3a58ce31cfde5ed9aede6efe5eebbece2eaf93ade75c0/fido2-1.1.2-py3-none-any.whl.metadata
   Using cached fido2-1.1.2-py3-none-any.whl.metadata (1.4 kB)
 Collecting oncalendar==1.0 (from -r requirements.txt (line 7))
   Using cached oncalendar-1.0-py3-none-any.whl
 Collecting psycopg2==2.9.9 (from -r requirements.txt (line 8))
   Using cached psycopg2-2.9.9-cp311-cp311-linux_x86_64.whl
 Collecting pycurl==7.45.2 (from -r requirements.txt (line 9))
   Using cached pycurl-7.45.2-cp311-cp311-linux_x86_64.whl
 Collecting pydantic==2.5.3 (from -r requirements.txt (line 10))
   Obtaining dependency information for pydantic==2.5.3 from https://files.pythonhosted.org/packages/dd/b7/9aea7ee6c01fe3f3c03b8ca3c7797c866df5fecece9d6cb27caa138db2e2/pydantic-2.5.3-py3-none-any.whl.metadata
   Using cached pydantic-2.5.3-py3-none-any.whl.metadata (65 kB)
 Collecting pyotp==2.9.0 (from -r requirements.txt (line 11))
   Obtaining dependency information for pyotp==2.9.0 from https://files.pythonhosted.org/packages/c3/c0/c33c8792c3e50193ef55adb95c1c3c2786fe281123291c2dbf0eaab95a6f/pyotp-2.9.0-py3-none-any.whl.metadata
   Using cached pyotp-2.9.0-py3-none-any.whl.metadata (9.8 kB)
 Collecting segno==1.6.0 (from -r requirements.txt (line 12))
   Obtaining dependency information for segno==1.6.0 from https://files.pythonhosted.org/packages/f7/06/3613899162a62ff307c07ad3214e6a1772f946c34f25ccd79f6549dd2e69/segno-1.6.0-py3-none-any.whl.metadata
   Using cached segno-1.6.0-py3-none-any.whl.metadata (9.7 kB)
 Collecting statsd==4.0.1 (from -r requirements.txt (line 13))
   Obtaining dependency information for statsd==4.0.1 from https://files.pythonhosted.org/packages/f4/d0/c9543b52c067a390ae6ae632d7fd1b97a35cdc8d69d40c0b7d334b326410/statsd-4.0.1-py2.py3-none-any.whl.metadata
   Downloading statsd-4.0.1-py2.py3-none-any.whl.metadata (2.9 kB)
 Collecting whitenoise==6.6.0 (from -r requirements.txt (line 14))
   Obtaining dependency information for whitenoise==6.6.0 from https://files.pythonhosted.org/packages/67/16/bb488ac8230f1bce94943b6654f2aad566d18aae575c8b6d8a99c78c489e/whitenoise-6.6.0-py3-none-any.whl.metadata
   Using cached whitenoise-6.6.0-py3-none-any.whl.metadata (3.7 kB)
 Collecting atpublic (from aiosmtpd==1.4.4.post2->-r requirements.txt (line 1))
   Obtaining dependency information for atpublic from https://files.pythonhosted.org/packages/42/d5/f3c7110d3763af646150203b8bfe6932ab05a9b3e228c27d138babeb92ae/atpublic-4.0-py3-none-any.whl.metadata
   Using cached atpublic-4.0-py3-none-any.whl.metadata (1.8 kB)
 Collecting attrs (from aiosmtpd==1.4.4.post2->-r requirements.txt (line 1))
   Obtaining dependency information for attrs from https://files.pythonhosted.org/packages/e0/44/827b2a91a5816512fcaf3cc4ebc465ccd5d598c45cefa6703fcf4a79018f/attrs-23.2.0-py3-none-any.whl.metadata
   Using cached attrs-23.2.0-py3-none-any.whl.metadata (9.5 kB)
 Collecting asgiref<4,>=3.7.0 (from Django==5.0.2->-r requirements.txt (line 3))
   Obtaining dependency information for asgiref<4,>=3.7.0 from https://files.pythonhosted.org/packages/9b/80/b9051a4a07ad231558fcd8ffc89232711b4e618c15cb7a392a17384bbeef/asgiref-3.7.2-py3-none-any.whl.metadata
   Using cached asgiref-3.7.2-py3-none-any.whl.metadata (9.2 kB)
 Collecting sqlparse>=0.3.1 (from Django==5.0.2->-r requirements.txt (line 3))
   Obtaining dependency information for sqlparse>=0.3.1 from https://files.pythonhosted.org/packages/98/5a/66d7c9305baa9f11857f247d4ba761402cea75db6058ff850ed7128957b7/sqlparse-0.4.4-py3-none-any.whl.metadata
   Downloading sqlparse-0.4.4-py3-none-any.whl.metadata (4.0 kB)
 Collecting django-appconf>=1.0.3 (from django-compressor==4.4->-r requirements.txt (line 4))
   Obtaining dependency information for django-appconf>=1.0.3 from https://files.pythonhosted.org/packages/c0/98/1cb3d9e8b1c6d0a74539b998474796fc5c0c0888b6201e5c95ba2f7a0677/django_appconf-1.0.6-py3-none-any.whl.metadata
   Using cached django_appconf-1.0.6-py3-none-any.whl.metadata (5.4 kB)
 Collecting rcssmin==1.1.1 (from django-compressor==4.4->-r requirements.txt (line 4))
   Obtaining dependency information for rcssmin==1.1.1 from https://files.pythonhosted.org/packages/70/61/3f129d34981d1d7eb46cd9ba20a73720d99a64bfa0cf10c4dbddd1b9c2b7/rcssmin-1.1.1-cp311-cp311-manylinux1_x86_64.whl.metadata
   Downloading rcssmin-1.1.1-cp311-cp311-manylinux1_x86_64.whl.metadata (4.5 kB)
 Collecting rjsmin==1.2.1 (from django-compressor==4.4->-r requirements.txt (line 4))
   Obtaining dependency information for rjsmin==1.2.1 from https://files.pythonhosted.org/packages/29/be/427af5875f63e6ca4f717285a36fd3f377665dacc0a57d3ea68a937296a4/rjsmin-1.2.1-cp311-cp311-manylinux1_x86_64.whl.metadata
   Downloading rjsmin-1.2.1-cp311-cp311-manylinux1_x86_64.whl.metadata (4.3 kB)
 Collecting typing-extensions (from django-stubs-ext==4.2.7->-r requirements.txt (line 5))
   Obtaining dependency information for typing-extensions from https://files.pythonhosted.org/packages/f9/de/dc04a3ea60b22624b51c703a84bbe0184abcd1d0b9bc8074b5d6b7ab90bb/typing_extensions-4.10.0-py3-none-any.whl.metadata
   Downloading typing_extensions-4.10.0-py3-none-any.whl.metadata (3.0 kB)
 Collecting cryptography!=35,<44,>=2.6 (from fido2==1.1.2->-r requirements.txt (line 6))
   Obtaining dependency information for cryptography!=35,<44,>=2.6 from https://files.pythonhosted.org/packages/d4/fa/057f9d7a5364c86ccb6a4bd4e5c58920dcb66532be0cc21da3f9c7617ec3/cryptography-42.0.5-cp39-abi3-manylinux_2_17_x86_64.manylinux2014_x86_64.whl.metadata
   Downloading cryptography-42.0.5-cp39-abi3-manylinux_2_17_x86_64.manylinux2014_x86_64.whl.metadata (5.3 kB)
 Collecting annotated-types>=0.4.0 (from pydantic==2.5.3->-r requirements.txt (line 10))
   Obtaining dependency information for annotated-types>=0.4.0 from https://files.pythonhosted.org/packages/28/78/d31230046e58c207284c6b2c4e8d96e6d3cb4e52354721b944d3e1ee4aa5/annotated_types-0.6.0-py3-none-any.whl.metadata
   Using cached annotated_types-0.6.0-py3-none-any.whl.metadata (12 kB)
 Collecting pydantic-core==2.14.6 (from pydantic==2.5.3->-r requirements.txt (line 10))
   Obtaining dependency information for pydantic-core==2.14.6 from https://files.pythonhosted.org/packages/e7/84/2dc88180fc6f0d13aab2a47a53b89c2dbc239e2a87d0a58e31077e111e82/pydantic_core-2.14.6-cp311-cp311-manylinux_2_17_x86_64.manylinux2014_x86_64.whl.metadata
   Using cached pydantic_core-2.14.6-cp311-cp311-manylinux_2_17_x86_64.manylinux2014_x86_64.whl.metadata (6.5 kB)
 Collecting cffi>=1.12 (from cryptography!=35,<44,>=2.6->fido2==1.1.2->-r requirements.txt (line 6))
   Obtaining dependency information for cffi>=1.12 from https://files.pythonhosted.org/packages/9b/89/a31c81e36bbb793581d8bba4406a8aac4ba84b2559301c44eef81f4cf5df/cffi-1.16.0-cp311-cp311-manylinux_2_17_x86_64.manylinux2014_x86_64.whl.metadata
   Using cached cffi-1.16.0-cp311-cp311-manylinux_2_17_x86_64.manylinux2014_x86_64.whl.metadata (1.5 kB)
 Collecting pycparser (from cffi>=1.12->cryptography!=35,<44,>=2.6->fido2==1.1.2->-r requirements.txt (line 6))
   Obtaining dependency information for pycparser from https://files.pythonhosted.org/packages/62/d5/5f610ebe421e85889f2e55e33b7f9a6795bd982198517d912eb1c76e1a53/pycparser-2.21-py2.py3-none-any.whl.metadata
   Downloading pycparser-2.21-py2.py3-none-any.whl.metadata (1.1 kB)
 Using cached aiosmtpd-1.4.4.post2-py3-none-any.whl (154 kB)
 Using cached Django-5.0.2-py3-none-any.whl (8.2 MB)
 Using cached django_compressor-4.4-py2.py3-none-any.whl (148 kB)
 Using cached django_stubs_ext-4.2.7-py3-none-any.whl (8.9 kB)
 Using cached fido2-1.1.2-py3-none-any.whl (203 kB)
 Using cached pydantic-2.5.3-py3-none-any.whl (381 kB)
 Using cached pyotp-2.9.0-py3-none-any.whl (13 kB)
 Using cached segno-1.6.0-py3-none-any.whl (74 kB)
 Using cached statsd-4.0.1-py2.py3-none-any.whl (13 kB)
 Using cached whitenoise-6.6.0-py3-none-any.whl (19 kB)
 Using cached pydantic_core-2.14.6-cp311-cp311-manylinux_2_17_x86_64.manylinux2014_x86_64.whl (2.1 MB)
 Using cached rcssmin-1.1.1-cp311-cp311-manylinux1_x86_64.whl (48 kB)
 Using cached rjsmin-1.2.1-cp311-cp311-manylinux1_x86_64.whl (31 kB)
 Using cached annotated_types-0.6.0-py3-none-any.whl (12 kB)
 Using cached asgiref-3.7.2-py3-none-any.whl (24 kB)
 Downloading cryptography-42.0.5-cp39-abi3-manylinux_2_17_x86_64.manylinux2014_x86_64.whl (4.6 MB)
    ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━ 4.6/4.6 MB 42.2 MB/s eta 0:00:00
 Using cached django_appconf-1.0.6-py3-none-any.whl (6.4 kB)
 Using cached sqlparse-0.4.4-py3-none-any.whl (41 kB)
 Downloading typing_extensions-4.10.0-py3-none-any.whl (33 kB)
 Using cached atpublic-4.0-py3-none-any.whl (4.9 kB)
 Using cached attrs-23.2.0-py3-none-any.whl (60 kB)
 Using cached cffi-1.16.0-cp311-cp311-manylinux_2_17_x86_64.manylinux2014_x86_64.whl (464 kB)
 Using cached pycparser-2.21-py2.py3-none-any.whl (118 kB)
 Installing collected packages: statsd, rjsmin, rcssmin, whitenoise, typing-extensions, sqlparse, segno, pyotp, pycurl, pycparser, psycopg2, oncalendar, cronsim, attrs, atpublic, asgiref, annotated-types, pydantic-core, Django, cffi, aiosmtpd, pydantic, django-stubs-ext, django-appconf, cryptography, fido2, django-compressor
 Successfully installed Django-5.0.2 aiosmtpd-1.4.4.post2 annotated-types-0.6.0 asgiref-3.7.2 atpublic-4.0 attrs-23.2.0 cffi-1.16.0 cronsim-2.5 cryptography-42.0.5 django-appconf-1.0.6 django-compressor-4.4 django-stubs-ext-4.2.7 fido2-1.1.2 oncalendar-1.0 psycopg2-2.9.9 pycparser-2.21 pycurl-7.45.2 pydantic-2.5.3 pydantic-core-2.14.6 pyotp-2.9.0 rcssmin-1.1.1 rjsmin-1.2.1 segno-1.6.0 sqlparse-0.4.4 statsd-4.0.1 typing-extensions-4.10.0 whitenoise-6.6.0

 [notice] A new release of pip is available: 23.2.1 -> 24.0
 [notice] To update, run: pip install --upgrade pip
 [isabell@stardust ~]$ pip3.11 install mysql
 Collecting mysql
   Obtaining dependency information for mysql from https://files.pythonhosted.org/packages/9a/52/8d29c58f6ae448a72fbc612955bd31accb930ca479a7ba7197f4ae4edec2/mysql-0.0.3-py3-none-any.whl.metadata
   Downloading mysql-0.0.3-py3-none-any.whl.metadata (746 bytes)
 Collecting mysqlclient (from mysql)
   Using cached mysqlclient-2.2.4-cp311-cp311-linux_x86_64.whl
 Downloading mysql-0.0.3-py3-none-any.whl (1.2 kB)
 Installing collected packages: mysqlclient, mysql
 Successfully installed mysql-0.0.3 mysqlclient-2.2.4

 [notice] A new release of pip is available: 23.2.1 -> 24.0
 [notice] To update, run: pip install --upgrade pip
 [isabell@stardust ~]$ pip3.11 install gunicorn
 Collecting gunicorn
   Obtaining dependency information for gunicorn from https://files.pythonhosted.org/packages/0e/2a/c3a878eccb100ccddf45c50b6b8db8cf3301a6adede6e31d48e8531cab13/gunicorn-21.2.0-py3-none-any.whl.metadata
   Using cached gunicorn-21.2.0-py3-none-any.whl.metadata (4.1 kB)
 Collecting packaging (from gunicorn)
   Obtaining dependency information for packaging from https://files.pythonhosted.org/packages/49/df/1fceb2f8900f8639e278b056416d49134fb8d84c5942ffaa01ad34782422/packaging-24.0-py3-none-any.whl.metadata
   Downloading packaging-24.0-py3-none-any.whl.metadata (3.2 kB)
 Using cached gunicorn-21.2.0-py3-none-any.whl (80 kB)
 Downloading packaging-24.0-py3-none-any.whl (53 kB)
    ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━ 53.5/53.5 kB 2.9 MB/s eta 0:00:00
 Installing collected packages: packaging, gunicorn
 Successfully installed gunicorn-21.2.0 packaging-24.0

 [notice] A new release of pip is available: 23.2.1 -> 24.0
 [notice] To update, run: pip install --upgrade pip
 [isabell@stardust ~]$

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

::

 [isabell@stardust ~]$ python3.11 ./manage.py migrate
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
   Applying auth.0001_initial... OK
   Applying accounts.0001_initial... OK
   Applying accounts.0002_profile_ping_log_limit... OK
   Applying accounts.0003_profile_token... OK
   Applying accounts.0004_profile_api_key... OK
   Applying accounts.0005_auto_20160509_0801... OK
   Applying accounts.0006_profile_current_team... OK
   Applying accounts.0007_profile_check_limit... OK
   Applying accounts.0008_profile_bill_to... OK
   Applying accounts.0009_auto_20170714_1734... OK
   Applying accounts.0010_profile_team_limit... OK
   Applying accounts.0011_profile_sort... OK
   Applying accounts.0012_auto_20171014_1002... OK
   Applying accounts.0013_remove_profile_team_access_allowed... OK
   Applying accounts.0014_auto_20171227_1530... OK
   Applying accounts.0015_auto_20181029_1858... OK
   Applying accounts.0016_remove_profile_bill_to... OK
   Applying accounts.0017_auto_20190112_1426... OK
   Applying accounts.0018_auto_20190112_1426... OK
   Applying accounts.0019_project_badge_key... OK
   Applying accounts.0020_auto_20190112_1950... OK
   Applying accounts.0021_auto_20190112_2005... OK
   Applying accounts.0022_auto_20190114_0857... OK
   Applying accounts.0023_auto_20190117_1419... OK
   Applying accounts.0024_auto_20190119_1540... OK
   Applying accounts.0025_remove_member_team... OK
   Applying accounts.0026_auto_20190204_2042... OK
   Applying accounts.0027_profile_deletion_notice_date... OK
   Applying accounts.0028_auto_20191119_1346... OK
   Applying accounts.0029_remove_profile_current_project... OK
   Applying accounts.0030_member_transfer_request_date... OK
   Applying accounts.0031_auto_20200803_1413... OK
   Applying accounts.0032_auto_20200819_0757... OK
   Applying accounts.0033_member_rw... OK
   Applying accounts.0034_credential... OK
   Applying accounts.0035_profile_reports... OK
   Applying accounts.0036_fill_profile_reports... OK
   Applying accounts.0037_profile_tz... OK
   Applying accounts.0038_profile_theme... OK
   Applying accounts.0039_remove_profile_reports_allowed... OK
   Applying accounts.0040_auto_20210722_1244... OK
   Applying accounts.0041_fill_role... OK
   Applying accounts.0042_remove_member_rw... OK
   Applying accounts.0043_add_role_manager... OK
   Applying accounts.0044_auto_20210730_0942... OK
   Applying accounts.0045_auto_20210908_1257... OK
   Applying accounts.0046_profile_deletion_scheduled_date... OK
   Applying accounts.0047_profile_over_limit_date... OK
   Applying accounts.0048_alter_profile_user... OK
   Applying admin.0001_initial... OK
   Applying admin.0002_logentry_remove_auto_add... OK
   Applying admin.0003_logentry_add_action_flag_choices... OK
   Applying api.0001_initial... OK
   Applying api.0002_auto_20150616_0732... OK
   Applying api.0003_auto_20150616_1249... OK
   Applying api.0004_auto_20150616_1319... OK
   Applying api.0005_auto_20150630_2021... OK
   Applying api.0006_check_grace... OK
   Applying api.0007_ping... OK
   Applying api.0008_auto_20150801_1213... OK
   Applying api.0009_auto_20150801_1250... OK
   Applying api.0010_channel... OK
   Applying api.0011_notification... OK
   Applying api.0012_auto_20150930_1922... OK
   Applying api.0013_auto_20151001_2029... OK
   Applying api.0014_auto_20151019_2039... OK
   Applying api.0015_auto_20151022_1008... OK
   Applying api.0016_auto_20151030_1107... OK
   Applying api.0017_auto_20151117_1032... OK
   Applying api.0018_remove_ping_body... OK
   Applying api.0019_check_tags... OK
   Applying api.0020_check_n_pings... OK
   Applying api.0021_ping_n... OK
   Applying api.0022_auto_20160130_2042... OK
   Applying api.0023_auto_20160131_1919... OK
   Applying api.0024_auto_20160203_2227... OK
   Applying api.0025_auto_20160216_1214... OK
   Applying api.0026_auto_20160415_1824... OK
   Applying api.0027_auto_20161213_1059... OK
   Applying api.0028_auto_20170305_1907... OK
   Applying api.0029_auto_20170507_1251... OK
   Applying api.0030_check_last_ping_body... OK
   Applying api.0031_auto_20170509_1320... OK
   Applying api.0032_auto_20170608_1158... OK
   Applying api.0033_auto_20170714_1715... OK
   Applying api.0034_auto_20171227_1530... OK
   Applying api.0035_auto_20171229_2008... OK
   Applying api.0036_auto_20180116_2243... OK
   Applying api.0037_auto_20180127_1215... OK
   Applying api.0038_auto_20180318_1306... OK
   Applying api.0039_remove_check_last_ping_body... OK
   Applying api.0040_auto_20180517_1336... OK
   Applying api.0041_check_desc... OK
   Applying api.0042_auto_20181029_1522... OK
   Applying api.0043_channel_name... OK
   Applying api.0044_auto_20181120_2004... OK
   Applying api.0045_flip... OK
   Applying api.0046_auto_20181218_1245... OK
   Applying api.0047_auto_20181225_2315... OK
   Applying api.0048_auto_20190102_0737... OK
   Applying api.0049_auto_20190102_0743... OK
   Applying api.0050_ping_kind... OK
   Applying api.0051_auto_20190104_0908... OK
   Applying api.0052_auto_20190104_1122... OK
   Applying api.0053_check_subject... OK
   Applying api.0054_auto_20190112_1427... OK
   Applying api.0055_auto_20190112_1427... OK
   Applying api.0056_auto_20190114_0857... OK
   Applying api.0057_auto_20190118_1319... OK
   Applying api.0058_auto_20190312_1716... OK
   Applying api.0059_auto_20190314_1744... OK
   Applying api.0060_tokenbucket... OK
   Applying api.0061_webhook_values... OK
   Applying api.0062_auto_20190720_1350... OK
   Applying api.0063_auto_20190903_0901... OK
   Applying api.0064_auto_20191119_1346... OK
   Applying api.0065_auto_20191127_1240... OK
   Applying api.0066_channel_last_error... OK
   Applying api.0067_last_error_values... OK
   Applying api.0068_auto_20200117_1023... OK
   Applying api.0069_auto_20200117_1227... OK
   Applying api.0070_auto_20200411_1310... OK
   Applying api.0071_check_manual_resume... OK
   Applying api.0072_auto_20200701_1007... OK
   Applying api.0073_auto_20200721_1000... OK
   Applying api.0074_auto_20200803_1411... OK
   Applying api.0075_auto_20200805_1004... OK
   Applying api.0076_auto_20201128_0951... OK
   Applying api.0077_auto_20210506_0755... OK
   Applying api.0078_sms_values... OK
   Applying api.0079_auto_20210907_0918... OK
   Applying api.0080_fill_slug... OK
   Applying api.0081_channel_last_notify... OK
   Applying api.0082_fill_last_notify... OK
   Applying api.0083_channel_disabled... OK
   Applying api.0084_ping_body_raw... OK
   Applying api.0085_ping_object_size... OK
   Applying api.0086_remove_check_last_ping_was_fail_and_more... OK
   Applying api.0087_check_failure_kw_check_filter_body_and_more... OK
   Applying api.0088_fill_kw... OK
   Applying api.0089_remove_check_subject_remove_check_subject_fail... OK
   Applying api.0090_alter_check_filter_subject... OK
   Applying api.0091_alter_check_filter_body... OK
   Applying api.0092_alter_check_success_kw... OK
   Applying api.0093_alter_check_failure_kw... OK
   Applying api.0094_ping_rid_alter_channel_kind... OK
   Applying api.0095_check_last_start_rid... OK
   Applying api.0096_check_start_kw_alter_channel_kind... OK
   Applying api.0097_alter_channel_kind... OK
   Applying api.0098_channel_last_notify_duration... OK
   Applying api.0099_alter_channel_disabled... OK
   Applying api.0100_opsgenie_values... OK
   Applying api.0101_alter_channel_kind... OK
   Applying api.0102_alter_check_kind... OK
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
   Applying logs.0001_initial... OK
   Applying payments.0001_initial... OK
   Applying payments.0002_subscription_plan_id... OK
   Applying payments.0003_subscription_address_id... OK
   Applying payments.0004_subscription_send_invoices... OK
   Applying payments.0005_subscription_plan_name... OK
   Applying payments.0006_subscription_invoice_email... OK
   Applying payments.0007_auto_20200727_1430... OK
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

 [isabell@stardust ~]$ python3.11 ./manage.py createsuperuser
 Email address:isabell@uber.space
 Password:
 Password (again):
 Superuser created successfully.
 [isabell@stardust ~]$

Generate static files
-----------------

Healthchecks uses a couple of static files. We need to generate this as follows:

::

 [isabell@stardust ~]$ python3.11 ./manage.py collectstatic
 347 static files copied to '/home/isabell/apps/healthchecks/static-collected'.
 [isabell@stardust ~]$ python3.11 ./manage.py compress
 Compressing... done
 Compressed 26 block(s) from 147 template(s) for 1 context(s).
 [isabell@stardust ~]$

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

.. include:: includes/my-print-defaults.rst

Your backend should now point to the service; let's check it:

.. code-block:: console

    [isabell@stardust ~]$ uberspace web backend list
    / http:8000 => OK, listening: listening: PID 13332, /home/isabell/apps/healthcheck/venv/bin/python3.11 venv/bin/gunicorn --bind 0.0.0.0:8000 hc.wsgi:application
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

If we'd like upgrade to a newer release, we'll first stop the running services, pull the latest source files and repeat the database
migration and static file generation steps before we start the services again.

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
 [isabell@stardust ~]$ python3.11 ./manage.py migrate
 [isabell@stardust ~]$ python3.11 ./manage.py collectstatic
 [isabell@stardust ~]$ python3.11 ./manage.py compress
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

----

Tested with Healthchecks 3.2.0, Python 3.11, Uberspace 7.1.1

.. author_list::
