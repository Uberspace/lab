.. highlight:: console

.. author:: Thomas Johnson <https://johnson.tj/>

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

We’re using :manual:`PHP <lang-php>` in the stable version 8.1:

.. code-block:: console

 [isabell@stardust ~]$ uberspace tools version show php
 Using 'PHP' version: '8.5'
 [isabell@stardust ~]$

Your website domain needs to be set up:

.. include:: includes/web-domain-list.rst

Installation
============

Remove your ``html`` directory and download the current version of Baïkal from the github release. Link the Baïkal ``html`` directory as your new

.. code-block:: console

 [isabell@stardust ~]$ cd /var/www/virtual/$USER/
 [isabell@stardust isabell]$ rm -f html/nocontent.html; rmdir html
 [isabell@stardust isabell]$ wget https://github.com/sabre-io/Baikal/releases/download/0.11.1/baikal-0.11.1.zip
 [isabell@stardust isabell]$ unzip baikal-0.11.1.zip
 [isabell@stardust isabell]$ rm baikal-0.11.1.zip
 [isabell@stardust isabell]$ ln -s baikal/html html
 [isabell@stardust isabell]$

You can also choose not to replace your ``html`` directory (and e.g. install Baïkal in a subdirectory or under a subdomain). In that case, you need to perform additional configuration steps.

Configuration
=============

After the installation you need to open isabell.uber.space in your browser to finish your setup.

Fill out your system settings, admin user and database settings, you can use the included SQLite database or :manual_anchor:`MySQL <database-mysql.html#login-credentials>`.


Updates
=======

Check Baïkal's `stable releases`_ for the latest versions. You might want to use the `baikal_updates`_ script for doing these checks. If a newer version is available, you should manually update your installation.

Backup your ``Specific`` directory and the ``baikal.yaml`` config file, delete everything else in your ``html`` directory.

.. code-block:: console

 [isabell@stardust ~]$ cd /var/www/virtual/$USER/html/
 [isabell@stardust html]$ cp -r Specific ~
 [isabell@stardust html]$ cp baikal.yaml ~
 [isabell@stardust html]$ rm -rf * .*

Proceed with the installation steps from here and move back your config files.

.. code-block:: console

 [isabell@stardust html]$ mv ~/Specific ./
 [isabell@stardust html]$ mv ~/baikal.yaml ./config/
 [isabell@stardust html]$

Finish the update by open isabell.uber.space in your browser.

.. _Baïkal: https://sabre.io/baikal/
.. _stable releases: https://github.com/sabre-io/Baikal/releases
.. _baikal_updates: https://github.com/fl3a/baikal_updates

Troubleshooting
===============
If you get a server error 500 when accessing the dav.php, cal.php or card.php then you possibly need to specify the base uri explicitly. Edit the baikal.yaml file in the config directory and set ``base_uri`` to ``'/'`` if you chosen to replace your ``html`` directory or to the subdirectory you chosen (e.g. ``'/baikal/'``) to instal baikal to. The trailing slash is not optional and needs to present.

----

Tested with Baïkal_ 0.11.1, PHP 8.5 and Uberspace 7.17.2

.. author_list::
