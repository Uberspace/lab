.. highlight:: console

.. author:: Thomas Kammerer <https://kammerer.tk/>

.. tag:: lang-php
.. tag:: web
.. tag:: sync
.. tag:: calendar

.. sidebar:: Logo

  .. image:: _static/images/baikal.png
      :align: center

######
Baïkal
######

.. tag_list::

Baïkal_ is a lightweight CalDAV+CardDAV server.

----

.. note:: For this guide you should be familiar with the basic concepts of

  * :manual:`PHP <lang-php>`
  * :manual:`domains <web-domains>`

Prerequisites
=============

We’re using :manual:`PHP <lang-php>` in the stable version 7.2:

.. code-block:: console

 [isabell@stardust ~]$ uberspace tools version show php
 Using 'PHP' version: '7.2'
 [isabell@stardust ~]$

Your website domain needs to be set up:

.. include:: includes/web-domain-list.rst

Installation
============

Remove your ``html`` directory and download the current version of Baïkal from the github release. Link the Baïkal ``html`` directory as your new 

.. code-block:: console

 [isabell@stardust ~]$ cd /var/www/virtual/$USER/
 [isabell@stardust isabell]$ rmdir html 
 [isabell@stardust isabell]$ wget https://github.com/sabre-io/Baikal/releases/download/0.6.1/baikal-0.6.1.zip
 [isabell@stardust isabell]$ unzip baikal-0.6.1.zip
 [isabell@stardust isabell]$ rm baikal-0.6.1.zip
 [isabell@stardust isabell]$ ln -s baikal/html html
 [isabell@stardust isabell]$ 

Configuration
=============

After the installation you need to open isabell.uber.space in your browser to finish your setup.

Fill out your system settings, admin user and database settings, you can use the included SQLite database or :manual_anchor:`MySQL <database-mysql.html#login-credentials>`.


Updates
=======

Check Baïkal's `stable releases`_ for the latest versions. If a newer version is available, you should manually update your installation.

Backup your ``Specific`` directory, delete everything else in your ``html`` directory.

.. code-block:: console

 [isabell@stardust ~]$ cd /var/www/virtual/$USER/html/
 [isabell@stardust html]$ cp -r Specific ~
 [isabell@stardust html]$ rm -rf * .*

Proceed with the installation steps from here and move back your config file.

.. code-block:: console

 [isabell@stardust html]$ mv ~/Specific ./
 [isabell@stardust html]$

Finish the update by open isabell.uber.space/html in your browser.

.. _Baïkal: http://www.baikal-server.com/
.. _stable releases: https://github.com/sabre-io/Baikal/releases

----

Tested with Baïkal_ 0.6.1 and Uberspace 7.4.3

.. author_list::
