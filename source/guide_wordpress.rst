.. sectionauthor:: Uberspace <hallo@uberspace.de>
.. highlight:: console

.. sidebar:: Logo
  
  .. image:: _static/images/wordpress.png 
      :align: center

#########
WordPress
#########

WordPress_ is an open source blogging platform written in PHP and distributed under the GPLv2 licence.

WordPress was released in 2003 by Matt Mullenweg and Mike Little as a fork of b2/cafelog. It is maintained by the WordPress foundation.

----

.. note:: For this guide you should be familiar with the basic concepts of 

  * PHP_
  * MySQL_ 
  * domains_

Prerequisites
=============

We're using PHP_ in the stable version 7.1:

::

 [isabell@stardust ~]$ uberspace tools version show php
 Using 'PHP' version: '7.1'
 [isabell@stardust ~]$

.. include:: includes/my-print-defaults.rst

Your blog domain needs to be setup:

.. include:: includes/web-domain-list.rst

Installation
============

``cd`` to your `document root`_, then download and extract the latest release of the WordPress installer:

::

 [isabell@stardust ~]$ cd /var/www/virtual/$USER/html/
 [isabell@stardust html]$ curl https://wordpress.org/latest.tar.gz | tar -xzf - --strip-components=1
   % Total    % Received % Xferd  Average Speed   Time    Time     Time  Current
                                  Dload  Upload   Total   Spent    Left  Speed
 100 8364k  100 8364k    0     0  4448k      0  0:00:01  0:00:01 --:--:-- 4449k
 [isabell@stardust html]$

Now point your browser to your blog URL and follow the instructions.

You will need to enter the following information:

  * your MySQL hostname, username and password: the hostname is ``localhost`` and you should know your MySQL credentials_ by now. If you don't, start reading again at the top.
  * your WordPress database name: we suggest you use an additional_ database. For example: isabell_wordpress


Updates
=======

By default, WordPress `automatically updates`_ itself to the latest stable minor version. 

.. warning:: Plugins and themes are **not** updated automatically, so make sure to regularly check the updates section in your WordPress installation's settings. Unpatched plugins or themes are a commonly abused to gain control of WordPress installations, e.g. to send spam mails.


.. _Wordpress: https://wordpress.org
.. _PHP: http://www.php.net/
.. _credentials: https://manual.uberspace.de/en/database-mysql.html#login-credentials
.. _MySQL: https://manual.uberspace.de/en/database-mysql.html
.. _domains: https://manual.uberspace.de/en/web-domains.html
.. _document root: https://manual.uberspace.de/en/web-documentroot.html
.. _additional: https://manual.uberspace.de/en/database-mysql.html#additional-databases
.. _automatically updates: https://codex.wordpress.org/Configuring_Automatic_Background_Updates

