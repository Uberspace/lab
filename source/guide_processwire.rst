.. highlight:: console

.. author:: Marco Krage <marco@my-azur.de>

.. sidebar:: Logo

  .. image:: _static/images/processwire.svg
      :align: center

###########
ProcessWire 
###########

Processwire_ is a free content management system (CMS) and framework (CMF) written in PHP.

----

.. note:: For this guide you should be familiar with the basic concepts of

  * :manual:`MySQL <database-mysql>`
  * :manual:`Domains <web-domains>`
  * :manual:`PHP <lang-php>`

License
=======

ProcessWire is distributed under the `MPL 2.0`_ license, but also designates some files as using the MIT_ license.

Prerequisites
=============

::

 [isabell@stardust ~]$ my_print_defaults client
 --default-character-set=utf8mb4
 --user=isabell
 --password=MySuperSecretPassword
 [isabell@stardust ~]$

Your blog URL needs to be setup:

::

 [isabell@stardust ~]$ uberspace web domain list
 isabell.uber.space
 [isabell@stardust ~]$

Installation
============

``cd`` to your :manual:`document root <web-documentroot>`, then download the latest release and extract it:

.. code-block:: console

 [isabell@stardust ~]$ cd /var/www/virtual/$USER/html/
 [isabell@stardust html]$ wget https://github.com/processwire/processwire/archive/master.tar.gz
 --2019-03-31 12:01:53--  https://github.com/processwire/processwire/archive/master.tar.gz
 [...]
 2019-03-31 12:01:57 (7.32 MB/s) - 'master.tar.gz' saved [13867981]
 [isabell@stardust html]$ tar xfz master.tar.gz
 [isabell@stardust html]$ rm master.tar.gz
 [isabell@stardust html]$

In this guide we are using the document root rather than an subfolder.

::

 [isabell@stardust html]$ mv processwire-master/* .
 [isabell@stardust html]$ rm -r processwire-master/
 [isabell@stardust html]$

.. important:: Edit ``htaccess.txt`` and comment out the line ``Options +FollowSymLinks``. This option is not allowed on a Uberspace an will lead to a Internal Server Error.

Configuration
=============

Point your browser to your domain, e.g. ``https://isabell.uber.space``. This will initiate the ProcessWire installer.

You will need to enter the following information:

  * Site Installation Profile: Use "Default (Beginner Edition)" to start with some example data or use "Blank" if you already know what you are doing.
  * your MySQL username and password: you should know your MySQL :manual_anchor:`credentials <database-mysql.html#login-credentials>` by now. If you don't, start reading again at the top.
  * your database name: we suggest you use an :manual_anchor:`additional <database-mysql.html#additional-databases>` database. For example: ``isabell_processwire``
  * Admin User: The name, email address and password of the admin user.


Finishing installation
======================

If not changed during the installation open ``https://isabell.uber.space/processwire/`` and login to the backend.

Now that the installation is complete, make you familiar with the basics of ProcessWire's structure, API and read the `getting started`_ pages.


Best practices
==============

Security
--------

Make your ``/config.php`` file non-writable.



Updates
=======

.. note:: Check the blog_ regularly to stay informed about the newest version.


.. _Processwire: https://processwire.com
.. _MPL 2.0: https://www.mozilla.org/en-US/MPL/2.0/
.. _MIT: https://opensource.org/licenses/MIT
.. _getting started: https://processwire.com/docs/start/
.. _blog: https://processwire.com/blog/

----

Tested with ProcessWire 3.0.123, Uberspace 7.2.7.0

.. authors::
