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

Installation
============

Step 1
------

Download the seafile server and extract it to a folder called seafile.

::

 [isabell@stardust ~]$ wget https://download.seadrive.org/seafile-server_6.3.4_x86-64.tar.gz
 [isabell@stardust ~]$ mkdir seafile
 [isabell@stardust ~]$ mv seafile-server_* seafile
 [isabell@stardust ~]$ cd seafile/
 [isabell@stardust ~]$ tar -xzf seafile-server_*
 [isabell@stardust ~]$ mkdir installed
 [isabell@stardust ~]$ mv seafile-server_* installed/
 [isabell@stardust ~]$

Step 2
------

Install the required python libraries.

::

 [isabell@stardust ~]$ curl --silent http://effbot.org/media/downloads/Imaging-1.1.7.tar.gz | tar -xzf -
 [isabell@stardust ~]$ cd Imaging-1.1.7
 [isabell@stardust ~]$ perl -pi -e 's|/usr/lib|/usr/lib64|g' setup.py
 [isabell@stardust ~]$ python2.7 setup.py install --user
 [isabell@stardust ~]$ cd ..
 [isabell@stardust ~]$ rm -rf Imaging-1.1.7
 [isabell@stardust ~]$

Step 3
------

Create the needed MySQL databases as the installer file won't work on uberspace.

.. warning:: Replace ``isabell`` with your username!

::

 [isabell@stardust ~]$ mysql
 MariaDB [(none)]>     create database `isabell_ccnet-db` character set = 'utf8';
 MariaDB [(none)]>     create database `isabell_seafile-db` character set = 'utf8';
 MariaDB [(none)]>     create database `isabell_seahub-db` character set = 'utf8';
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
  [ ccnet database ] isabell_ccnet-db

  verifying user "isabell" access to database isabell_ccnet-db ...  done

  Enter the existing database name for seafile:
  [ seafile database ] isabell_seafile-db

  verifying user "isabell" access to database isabell_seafile-db ...  done

  Enter the existing database name for seahub:
  [ seahub database ] isabell_seahub-db

  verifying user "isabell" access to database isabell_seahub-db ...  done

Configure port
--------------

Since seafile uses its own webserver and fileserver, you need to find 2 free ports. Run this command 2 times and write down the 2 ports.

.. include:: includes/generate-port.rst

Step 5
------

Enter your domain name in config; Edit ``~/seafile/conf/ccnet.conf``

.. warning:: Replace ``isabell`` with your username!

.. code-block:: console
  :emphasize-lines: 1

  SERVICE_URL = https://isabell.uber.space/

Step 6
------

Change seahub port in config; Edit ``~/seafile/conf/gunicorn.conf``

.. warning:: Replace ``<yourport>`` with your first port!

.. code-block:: console
  :emphasize-lines: 1

  bind = "0.0.0.0:<yourport>"

Step 7
------

Change seafile port in config; Edit ``~/seafile/conf/seafile.conf``

.. warning:: Replace ``<yoursecondport>`` with your second port!

.. code-block:: console
  :emphasize-lines: 2

  [fileserver]
  port = <yoursecondport>

Step 8
------

Change seahub config; Edit ``~/seafile/conf/seahub_settings.py``
Add the following lines:

.. warning:: Replace ``isabell`` with your username!

.. code-block:: console
  :emphasize-lines: 1,2,6,8

  SITE_BASE = 'https://isabell.uber.space'
  SITE_NAME = 'isabell.uber.space'

  SECURE_PROXY_SSL_HEADER = ('HTTP_X_FORWARDED_PROTO', 'https')

  FILE_SERVER_ROOT = 'https://isabell.uber.space/seafhttp'

  CSRF_TRUSTED_ORIGINS = ['isabell.uber.space']

Step 9 - Setup .htaccess
------------------------

Create a ``~/html/.htaccess`` file with the following content:

.. warning:: Replace ``<yourport>`` with your first port!
.. warning:: Replace ``<yoursecondport>`` with your second port!

.. code-block:: apache
  :emphasize-lines: 6,7

  RewriteEngine On
  RewriteCond %{REQUEST_FILENAME} !-f
  DirectoryIndex disabled
  RewriteBase /

  RewriteRule ^seafhttp/(.*) http://localhost:<yoursecondport>/$1 [P]
  RewriteRule ^(.*)$ http://localhost:<yourport>/$1 [P]


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


.. _Python: https://manual.uberspace.de/en/lang-python.html
.. _MySQL: https://manual.uberspace.de/en/database-mysql.html
.. _domains: https://manual.uberspace.de/en/web-domains.html
.. _credentials: https://manual.uberspace.de/en/database-mysql.html#login-credentials

----

Tested with seafile-server-6.3.4, Uberspace 7.1.13.0

.. authors::
