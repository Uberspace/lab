.. highlight:: console

.. author:: Finn <mail@f1nn.eu>

.. tag:: lang-python
.. tag:: web
.. tag:: file-storage
.. tag:: sync
.. tag:: collaborative-editing

.. sidebar:: Logo

  .. image:: _static/images/seafile.png
      :align: center

##########
Seafile
##########

.. tag_list::

Seafile is an enterprise file hosting platform with high reliability and performance. Put files on your own server. Sync and share files across different devices, or access all the files as a virtual disk.

----

.. note:: For this guide you should be familiar with the basic concepts of

  * :manual:`Python <lang-python>` and its package manager pip
  * :manual:`MySQL <database-mysql>`
  * :manual:`domains <web-domains>`

License
=======

All relevant legal information can be found here

  * https://www.seafile.com/en/product/private_server/

Prerequisites
=============

You'll need your MySQL :manual_anchor:`credentials <database-mysql.html#login-credentials>`. Get them with ``my_print_defaults``:

::

 [isabell@stardust ~]$ my_print_defaults client
 --default-character-set=utf8mb4
 --user=isabell
 --password=MySuperSecretPassword
 [isabell@stardust ~]$

Your URL needs to be setup:

::

 [isabell@stardust ~]$ uberspace web domain list
 isabell.uber.space
 [isabell@stardust ~]$

Installation
============

Step 1
------

Download the seafile server and extract it to a folder called seafile.

::

 [isabell@stardust ~]$ mkdir seafile
 [isabell@stardust ~]$ cd seafile/
 [isabell@stardust ~]$ curl https://download.seadrive.org/seafile-server_6.3.4_x86-64.tar.gz | tar xzf -
 [isabell@stardust ~]$

Step 2
------

Install the required python libraries.

::

 [isabell@stardust ~]$ pip install 'Pillow==3.*' --user
 [isabell@stardust ~]$

Step 3
------

Create the needed MySQL databases as the installer file won't work on uberspace.

.. warning:: Replace ``isabell`` with your username!

::

 [isabell@stardust ~]$ mysql -e "create database ${USER}_ccnet character set = 'utf8';"
 [isabell@stardust ~]$ mysql -e "create database ${USER}_seafile character set = 'utf8';"
 [isabell@stardust ~]$ mysql -e "create database ${USER}_seahub character set = 'utf8';"
 [isabell@stardust ~]$

Step 4
------

Run the seafile installer script.

::

 [isabell@stardust ~]$ cd ~/seafile/seafile-server-*
 [isabell@stardust ~]$ ./setup-seafile-mysql.sh
 [isabell@stardust ~]$

Important answers:

.. warning:: Replace ``isabell`` with your username!

.. code-block:: console
  :emphasize-lines: 8,11,14,19,24

  -------------------------------------------------------
  Please choose a way to initialize seafile databases:
  -------------------------------------------------------

  [1] Create new ccnet/seafile/seahub databases
  [2] Use existing ccnet/seafile/seahub databases

  [ 1 or 2 ] 2

  Which mysql user to use for seafile?
  [ mysql user for seafile ] isabell

  Enter the existing database name for ccnet:
  [ ccnet database ] isabell_ccnet

  verifying user "isabell" access to database isabell_ccnet ...  done

  Enter the existing database name for seafile:
  [ seafile database ] isabell_seafile

  verifying user "isabell" access to database isabell_seafile ...  done

  Enter the existing database name for seahub:
  [ seahub database ] isabell_seahub

  verifying user "isabell" access to database isabell_seahub ...  done

Step 5
------

Enter your domain name in config; Edit ``~/seafile/conf/ccnet.conf``

.. warning:: Replace ``isabell`` with your username!

.. code-block:: console

  SERVICE_URL = https://isabell.uber.space/

Step 6
------

Change seahub config; Edit ``~/seafile/conf/seahub_settings.py`` and  add the following lines:

.. warning:: Replace ``isabell`` with your username!

.. code-block:: console

  SITE_BASE = 'https://isabell.uber.space'
  SITE_NAME = 'isabell.uber.space'

  SECURE_PROXY_SSL_HEADER = ('HTTP_X_FORWARDED_PROTO', 'https')

  FILE_SERVER_ROOT = SITE_BASE + '/seafhttp'
  CSRF_TRUSTED_ORIGINS = [SITE_NAME]

  #redirect to $USER tmp, avoid conflict with other users
  CACHE_DIR = "/home/isabell/seafile/tmp/logs"

  import os

  CACHES = {
    'default': {
      'BACKEND': 'django.core.cache.backends.filebased.FileBasedCache',
      'LOCATION': os.path.join(CACHE_DIR, 'seahub_cache'),
      'OPTIONS': {
        'MAX_ENTRIES': 1000000
      }
    }
  }

Step 7
------

.. note::

    Seafile is running on multiple ports. You'll need a backed at ``/`` for
    gunicorn on port ``8000`` and another backend on ``/seafhttp`` for the
    fileserver on port ``8082``. The latter also needs the parameter ``--remove-prefix``.

.. include:: includes/web-backend.rst

Finishing installation
======================

Restart seafile and seahub
--------------------------

::

 [isabell@stardust ~]$ cd ~/seafile/seafile-server-*
 [isabell@stardust ~]$ ./seafile.sh restart
 [isabell@stardust ~]$ ./seahub.sh restart
 [isabell@stardust ~]$

With starting seahub for the first time, you have to create an admin account.

Now you can point your browser to your domain and login with your admin account.


Updates
=======

Updating seafile is pretty easy. Just untar the new package into the "seafile" directory you created during the installation. Restart seafile and seahub after that.

::

 [isabell@stardust ~]$ cd ~/seafile/
 [isabell@stardust ~]$ curl https://download.seadrive.org/seafile-server_6.3.4_x86-64.tar.gz | tar xzf -
 [isabell@stardust ~]$


----

Tested with seafile-server-6.3.4, Uberspace 7.1.13.0

.. author_list::
