.. highlight:: console

.. author:: Thomas Kammerer <https://kammerer.tk/>

.. tag:: lang-php
.. tag:: web
.. tag:: sync
.. tag:: calendar
.. tag:: audience-family

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

We’re using :manual:`PHP <lang-php>` in the stable version 7.4:

.. code-block:: console

 [isabell@stardust ~]$ uberspace tools version show php
 Using 'PHP' version: '7.4'
 [isabell@stardust ~]$

Your website domain needs to be set up:

.. include:: includes/web-domain-list.rst

Installation
============

Remove your ``html`` directory and download the current version of Baïkal from the github release. Link the Baïkal ``html`` directory as your new

.. code-block:: console

 [isabell@stardust ~]$ cd /var/www/virtual/$USER/
 [isabell@stardust isabell]$ rm -f html/nocontent.html; rmdir html
 [isabell@stardust isabell]$ wget https://github.com/sabre-io/Baikal/releases/download/0.7.2/baikal-0.7.2.zip
 [isabell@stardust isabell]$ unzip baikal-0.7.2.zip
 [isabell@stardust isabell]$ rm baikal-0.7.2.zip
 [isabell@stardust isabell]$ ln -s baikal/html html
 [isabell@stardust isabell]$

You can also choose not to replace your ``html`` directory (and e.g. install Baïkal in a subdirectory or under a subdomain). In that case, you need to perform additional configuration steps.

Configuration
=============

Only if you didn't replace your ``html`` directory (and e.g. installed Baïkal in a subdirectory or under a subdomain), edit the file ``baikal/config/baikal.yaml`` and set the value of ``base_uri`` to ``'/'``.

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

Finish the update by open isabell.uber.space in your browser.

.. _Baïkal: https://sabre.io/baikal/
.. _stable releases: https://github.com/sabre-io/Baikal/releases

----

Tested with Baïkal_ 0.7.2 and Uberspace 7.8.1

.. author_list::
