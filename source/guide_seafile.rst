.. highlight:: console

.. author:: Finn <mail@f1nn.eu>

.. sidebar:: Logo

  .. image:: _static/images/seafile.png
      :align: center

##########
Seafile
##########

Seafile is an enterprise file hosting platform with high reliability and performance. Put files on your own server. Sync and share files across different devices, or access all the files as a virtual disk.

----

.. note:: For this guide you should be familiar with the basic concepts of

  * Python_ and its package manager pip
  * MySQL_
  * domains_

License
=======

All relevant legal information can be found here

  * https://www.seafile.com/en/product/private_server/

Prerequisites
=============

You'll need your MySQL credentials_. Get them with ``my_print_defaults``:

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

Configure port
--------------

Since seafile uses its own webserver and fileserver, you need to find 2 free ports. Run this command 2 times and write down the 2 ports.

.. code-block:: console

 [isabell@stardust ~]$ FREEPORT=$(( $RANDOM % 4535 + 61000 )); ss -ln src :$FREEPORT | grep $FREEPORT && echo "try again" || echo $FREEPORT
 9000
 [isabell@stardust ~]$ FREEPORT=$(( $RANDOM % 4535 + 61000 )); ss -ln src :$FREEPORT | grep $FREEPORT && echo "try again" || echo $FREEPORT
 9001
 [isabell@stardust ~]$

Write the ports down. In our example we use 9000 as gunicorn-port and 9001 as fileserver-port. In reality you'll get free ports between 61000 and 65535.

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

 [isabell@stardust ~]$ mysql
 MariaDB [(none)]>     create database `isabell_ccnet` character set = 'utf8';
 MariaDB [(none)]>     create database `isabell_seafile` character set = 'utf8';
 MariaDB [(none)]>     create database `isabell_seahub` character set = 'utf8';
 MariaDB [(none)]>     exit;
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

Change seahub (gunicorn) port in config; Edit ``~/seafile/conf/gunicorn.conf``

.. warning:: Replace ``<gunicorn-port>`` with your gunicorn port!

.. code-block:: console

  bind = "0.0.0.0:<gunicorn-port>"

Step 7
------

Change seafile port in config; Edit ``~/seafile/conf/seafile.conf``

.. warning:: Replace ``<fileserver-port>`` with your fileserver port!

.. code-block:: console

  [fileserver]
  port = <fileserver-port>

Step 8
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

Step 9 - Setup .htaccess
------------------------

Create a ``~/html/.htaccess`` file with the following content:

.. warning:: Replace ``<gunicorn-port>`` with your gunicorn port!
.. warning:: Replace ``<fileserver-port>`` with your fileserver port!

.. code-block:: apache
  :emphasize-lines: 6,7

  RewriteEngine On
  RewriteCond %{REQUEST_FILENAME} !-f
  DirectoryIndex disabled
  RewriteBase /

  RewriteRule ^seafhttp/(.*) http://localhost:<fileserver-port>/$1 [P]
  RewriteRule ^(.*)$ http://localhost:<gunicorn-port>/$1 [P]


In our example this would be:

.. code-block:: apache

  RewriteEngine On
  RewriteCond %{REQUEST_FILENAME} !-f
  DirectoryIndex disabled
  RewriteBase /

  RewriteRule ^seafhttp/(.*) http://localhost:9001/$1 [P]
  RewriteRule ^(.*)$ http://localhost:9000/$1 [P]


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


.. _Python: https://manual.uberspace.de/en/lang-python.html
.. _MySQL: https://manual.uberspace.de/en/database-mysql.html
.. _domains: https://manual.uberspace.de/en/web-domains.html
.. _credentials: https://manual.uberspace.de/en/database-mysql.html#login-credentials


----

Tested with seafile-server-6.3.4, Uberspace 7.1.13.0

.. authors::
