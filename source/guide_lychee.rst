.. highlight:: console

.. sidebar:: Logo
  
  .. image:: _static/images/lychee.png 
      :align: center

#########
Lychee
#########

Lychee_ is a open source photo-management software written in PHP and distributed under the MIT license. It allows you to easily upload, sort and manage your photos, all while presenting those with a beautiful web interface.

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

Also, the domain you want to use for Lychee must be set up as well:

.. include:: includes/web-domain-list.rst

Installation
============

``cd`` to your `document root`_, then clone the latest release of the Lychee installer and move the files to the document root:

::

 [isabell@stardust ~]$ cd /var/www/virtual/$USER/html/
 [isabell@stardust html]$ git clone https://github.com/electerious/Lychee.git
 Cloning into 'Lychee'...
 remote: Counting objects: 10458, done.
 remote: Compressing objects: 100% (8/8), done.
 remote: Total 10458 (delta 3), reused 7 (delta 2), pack-reused 10448
 Receiving objects: 100% (10458/10458), 5.74 MiB | 8.85 MiB/s, done.
 Resolving deltas: 100% (7144/7144), done.
 [isabell@stardust html]$ mv Lychee/* Lychee/.[!.]* . && rmdir Lychee
 [isabell@stardust html]$

Now point your browser to your Lychee URL and follow the instructions.

You will need to enter the following information:

  * your MySQL hostname, username and password: the hostname is ``localhost`` and you should know your MySQL credentials_ by now. If you don't, start reading again at the top.
  * your Lychee database name: we suggest you use an additional_ database. For example: isabell_lychee. Enter that, you can leave the prefix field empty.

For the last step you have to enter the username/password you want to use for the Lychee user.

Updates
=======

You can regularly check the release section of Lychees GitHub_ for any new releases. 

If a new version is available, ``cd`` to your `document root` and do a simple ``git pull``:

::

 [isabell@stardust ~]$ cd /var/www/virtual/$USER/html/
 [isabell@stardust html]$ git pull
 Already up to date.
 [isabell@stardust html]$


.. _Lychee: https://lychee.electerious.com/
.. _GitHub: https://github.com/electerious/Lychee/releases
.. _PHP: http://www.php.net/
.. _credentials: https://manual.uberspace.de/en/database-mysql.html#login-credentials
.. _MySQL: https://manual.uberspace.de/en/database-mysql.html
.. _domains: https://manual.uberspace.de/en/web-domains.html
.. _document root: https://manual.uberspace.de/en/web-documentroot.html
.. _additional: https://manual.uberspace.de/en/database-mysql.html#additional-databases
