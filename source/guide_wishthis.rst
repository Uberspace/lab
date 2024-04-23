.. highlight:: console

.. author:: Kevin Jost <https://github.com/systemsemaphore>

.. tag:: JavaScript
.. tag:: lang-php
.. tag:: web

.. sidebar:: Logo

  .. image:: _static/images/wishthis.svg
      :align: center

#######
wishthis
#######

.. tag_list::

`wishthis`_ is a self-hosted platform to create, manage and view your wishes for any kind of occasion.

----

.. note:: For this guide you should be familiar with the basic concepts of

  * :manual:`PHP <lang-php>`
  * :manual:`MySQL <database-mysql>`
  * :manual:`domains <web-domains>`

Prerequisites
=============

We’re using :manual:`PHP <lang-php>` in the stable version 8.2:

.. code-block:: console
 :emphasize-lines: 1

 [isabell@stardust ~]$ uberspace tools version use php 8.2
 Selected PHP version 8.2
 [isabell@stardust ~]$

.. include:: includes/my-print-defaults.rst

Your website domain needs to be set up:

.. include:: includes/web-domain-list.rst

Installation
============

.. note:: Make sure wishthis is setup via a domain directly and not running inside a sub-folder.

``cd`` to your :manual:`DocumentRoot <web-documentroot>`, then clone the wishthis repository. You can find the latest stable version on the `release notes`_.

.. code-block:: console
 :emphasize-lines: 1,2,3,6

 [isabell@stardust ~]$ cd /var/www/virtual/$USER/html
 [isabell@stardust html]$ rm -f nocontent.html
 [isabell@stardust html]$ git clone -b stable https://github.com/wishthis/wishthis.git .
 [isabell@stardust html]$

After cloning the repository, you need to create an additional folder:

.. code-block:: console
 :emphasize-lines: 1,2,3

 [isabell@stardust ~]$ cd /var/www/virtual/$USER/html/src/
 [isabell@stardust src]$ mkdir cache
 [isabell@stardust src]$

Create database
---------------

While not technically necessary, it is recommended to create a single-purpose MySQL database for whishthis:

.. code-block:: console

 [isabell@stardust ~]$ mysql --verbose --execute="CREATE DATABASE ${USER}_wishthis"
 --------------
 CREATE DATABASE isabell_wishthis
 --------------

 [isabell@stardust ~]$

Finishing installation
======================

Point your browser to ``https://isabell.uber.space/`` The built-in setup should start. Follow the instructions, enter your database credentials and the name of the database you just created, and register your user account.

Updates
=======

.. note:: Check the `release notes`_ regularly to stay informed about the newest version.

Run ``git pull`` in the wishthis directory to pull the latest changes from upstream.

.. code-block:: console
 :emphasize-lines: 1,2

 [isabell@stardust ~]$ cd ~/html
 [isabell@stardust html]$ git pull origin stable
 [isabell@stardust html]$

Optional steps
==============

Disabling registration
----------------------
By default, registration is open to anyone. If you have registered an account for yourself and want to disable registration, you need to change the value in the config file:

.. code-block:: console
 :emphasize-lines: 1

 [isabell@stardust ~]$ nano ~/html/src/config/config.php
 [isabell@stardust config]$

.. code-block:: yaml
  :emphasize-lines: 4
  
  /**
   * Miscellaneous
   */
  define('DISABLE_USER_REGISTRATION', true);
::

Acknowledgements
================

.. warning:: wishthis v.1.1.1 still has a bug where German special letters (umlauts) are not correctly displayed: https://github.com/wishthis/wishthis/issues/80

This guide is based on the official `wishthis readme`_.

.. _wishthis: https://wishthis.online/
.. _release notes: https://github.com/wishthis/wishthis/releases
.. _wishthis readme: https://github.com/wishthis/wishthis/blob/develop/README.md

----

Tested with wishthis v1.1.1 and Uberspace 7.15.14

.. author_list::
