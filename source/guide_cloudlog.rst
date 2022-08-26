.. author:: Nico Graf DO2NG <hallo@uberspace.de>

.. tag:: lang-php
.. tag:: web

.. highlight:: console

.. sidebar::

  .. image:: _static/images/cloudlog.png
      :align: center


########
Cloudlog
########

.. tag_list::

Cloudlog_ is an open source amateur radio logbook tool written in PHP and distributed under the MIT License. It is developed by Peter Goodhall 2M0SQL.


----

.. note:: For this guide you should be familiar with the basic concepts of

  * PHP_
  * :manual:`MySQL <database-mysql>`
  * :manual:`domains <web-domains>`

Prerequisites
=============

We're using PHP_ in the stable version 7.4:

::

 [isabell@stardust ~]$ uberspace tools version show php
 Using 'PHP' version: '7.4'
 [isabell@stardust ~]$

Your log domain needs to be setup:

.. include:: includes/web-domain-list.rst

Installation
============

First, remove the default ``nocontent.html`` from your :manual:`document root <web-documentroot>` and delete the now empty ``html`` folder:

.. code-block:: console

  [isabell@stardust ~]$ rm /var/www/virtual/$USER/html/nocontent.html
  [isabell@stardust ~]$ rmdir /var/www/virtual/$USER/html
  [isabell@stardust ~]$

Now use ``git`` to clone the Cloudlog repo into a new ``html`` folder:

.. code-block:: console

  [isabell@stardust ~]$ git clone https://github.com/magicbug/Cloudlog.git /var/www/virtual/$USER/html/
  Cloning into '/var/www/virtual/$USER/html'...
  remote: Enumerating objects: 24402, done.
  remote: Counting objects: 100% (370/370), done.
  remote: Compressing objects: 100% (149/149), done.
  remote: Total 24402 (delta 247), reused 320 (delta 219), pack-reused 24032
  Receiving objects: 100% (24402/24402), 16.23 MiB | 23.31 MiB/s, done.
  Resolving deltas: 100% (15879/15879), done.
  [isabell@stardust ~]$

Set up a MySQL database for your Cloudlog installation:

.. code-block:: console

  [isabell@stardust ~]$ mysql -e "CREATE DATABASE ${USER}_cloudlog;"
  [isabell@stardust ~]$

Configuration
=============

Point your browser to Cloudlog's setup wizard at ``https://<yourusername>.uber.space/install`` (in our example, this would be ``https://isabell.uber.space/install``).

.. include:: includes/my-print-defaults.rst

Fill out the web form:

#. Leave the ``Directory`` field blank.
#. The ``Website URL`` field should already be pre-filled with your site's URL, leave it as it is.
#. Optional: Change the ``Default Gridsquare`` if you like.

For the ``Database settings``, use

#. The hostname ``localhost``,
#. Your Uberspace user name as ``Username``,
#. Your MySQL password as ``password``.
#. Enter the ``Database name`` you created in the previous step (in our example this would be ``isabell_cloudlog``).

Once all the required information has been entered, click install. You should now be redirected to your Cloudlog's home page. Log in with the default username ``m0abc`` and default password ``demo``.

Now, you need to set up your own admin user and delete the default user:

#. Open Admin -> User Accounts
#. Create a new user.

In order to delete the default user, log out and then log in again with your newly created Cloudlog user. Then

#. Open Admin -> User Accounts
#. delete ``m0abc``.

For security reasons, you should block web access to the ``.git`` directory. You can do so by setting an intentionally broken web backend:

.. code-block:: console

  [isabell@stardust ~]$ uberspace web backend set /.git --http --port 4711
  Set backend for /.git to port 4711; please make sure something is listening!
  You can always check the status of your backend using "uberspace web backend list".
  [isabell@stardust ~]$

Prettier URLs
=============

In order to hide ``index.php`` from your Cloudlog URLs, rename the provided ``.htaccess.sample`` to ``.htaccess``:

.. code-block:: console

  [isabell@stardust ~]$ mv /var/www/virtual/$USER/html/.htaccess.sample /var/www/virtual/$USER/html/.htaccess
  [isabell@stardust ~]$

Then open Cloudlog's ``application/config/config.php`` in your favourite editor and find the line

.. code-block:: none

  $config['index_page'] = 'index.php';

and change it to

.. code-block:: none

  $config['index_page'] = '';

Updates
=======

The Cloudlog documentation suggests a daily Cronjob to perform the ``git pull`` command to update the code. Run ``crontab -e`` to edit your Crontab and add the following line:

.. code-block:: console

  @daily cd /var/www/virtual/$USER/html && git pull



.. _Cloudlog: https://www.magicbug.co.uk/cloudlog/
.. _PHP: http://www.php.net/

----

Tested with Cloudlog 1.7, Uberspace 7.12.3

.. author_list::
