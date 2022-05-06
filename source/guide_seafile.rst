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

Download
--------

Check the `Seafile website`_ for the latest ``Server for generic Linux`` release, copy the download link and replace the URL in the following command with the one you just copied.

.. _Seafile website: https://www.seafile.com/en/download/

::

 [isabell@stardust ~]$ mkdir seafile
 [isabell@stardust ~]$ cd seafile/
 [isabell@stardust seafile]$ curl https://download.seadrive.org/seafile-server_8.0.7_x86-64.tar.gz | tar xzf -
 [isabell@stardust seafile]$

Install dependencies
--------------------

.. note:: Parts of Seafile call ``python3``, but don't work with Python 3.6, which is the version the default alias on Uberspace resolves to. A local symlink to ``python3.8`` and using ``pip3.8`` instead of just ``pip3`` remedy this. (Make sure that no other service depends on ``python3`` pointing to ``python3.6``!)

First, create a symlink to ``python3``.

::

 [isabell@stardust seafile]$ ln -s /usr/bin/python3.8 $HOME/bin/python3

Install the required python libraries.

::

 [isabell@stardust seafile]$ pip3.8 install --upgrade pip Pillow captcha jinja2 sqlalchemy==1.4.3 django-simple-captcha python3-ldap mysqlclient --user
 [isabell@stardust seafile]$

.. note:: Two depencies, ``pylibmc`` and ``django-pylibmc`` cannot be installed because they would require the system packages ``memcached`` and ``libmemcached-devel`` to be installed on Uberspace. This is okay because memcached support in Seafile is `optional <https://manual.seafile.com/deploy/add_memcached/>`_ and only recommended for installations with more than 50 users.

Create databases
----------------

Create the needed MySQL databases as the installer file won't work on uberspace.

::

 [isabell@stardust seafile]$ mysql -e "create database ${USER}_ccnet character set = 'utf8';"
 [isabell@stardust seafile]$ mysql -e "create database ${USER}_seafile character set = 'utf8';"
 [isabell@stardust seafile]$ mysql -e "create database ${USER}_seahub character set = 'utf8';"
 [isabell@stardust seafile]$

Run installer
-------------

Run the seafile installer script.

::

 [isabell@stardust seafile]$ cd ~/seafile/seafile-server-*
 [isabell@stardust seafile-server-8.0.7]$  ./setup-seafile-mysql.sh

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

Configure
---------

Enter your domain name in config, if you haven't already done that when running the installer script above; Edit ``~/seafile/conf/ccnet.conf``

.. warning:: Replace ``isabell`` with your username, and if you are using a custom domain, use it in place of ``isabell.user.space``!

.. code-block:: console

  SERVICE_URL = https://isabell.uber.space/


Change gunicorn config; Edit ``~/seafile/conf/gunicorn.conf.py`` and change the ``bind =`` line to:

.. code-block:: console

  bind = "0.0.0.0:8000"

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

Expose
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

 [isabell@stardust ~]$ cd ~/seafile/seafile-server-latest
 [isabell@stardust seafile-server-latest]$ ./seafile.sh restart
 [isabell@stardust seafile-server-latest]$ ./seahub.sh restart
 [isabell@stardust seafile-server-latest]$

With starting seahub for the first time, you have to create an admin account.

Now you can point your browser to your domain and login with your admin account.


Updates
=======

Updating seafile is pretty easy. First update the pip3 packages, then download the new version and untar the new package into the "seafile" directory you created during the installation, recreate the symlink to the latest version and restart seafile and seahub after that.

::

 [isabell@stardust ~]$ pip3.8 install --upgrade pip Pillow captcha jinja2 sqlalchemy==1.4.3 django-simple-captcha python3-ldap mysqlclient --user
 [isabell@stardust ~]$ cd ~/seafile/
 [isabell@stardust seafile]$ curl https://download.seadrive.org/seafile-server_8.0.7_x86-64.tar.gz | tar xzf -
 [isabell@stardust seafile]$ ln -sfn /home/seafile/seafile/seafile-server-8.0.7 /home/seafile/seafile/seafile-server-latest
 [isabell@stardust seafile]$ cd seafile-server-latest
 [isabell@stardust seafile-server-latest]$ ./seafile.sh restart
 [isabell@stardust seafile-server-latest]$ ./seahub.sh restart

----

Tested with seafile-server-8.0.7, Uberspace 7.11.3.0

.. author_list::
