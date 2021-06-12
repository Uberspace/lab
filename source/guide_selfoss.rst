.. highlight:: console

.. author:: Nico Graf <hallo@uberspace.de>

.. tag:: lang-php
.. tag:: web
.. tag:: rss

.. sidebar:: Logo

  .. image:: _static/images/selfoss.png
      :align: center

#######
selfoss
#######

.. tag_list::

.. abstract::
  selfoss_ is a free and open source web-based news feed reader and
  aggregator.

----

.. note:: For this guide you should be familiar with the basic concepts of

  * :manual:`MySQL <database-mysql>`
  * :manual:`domains <web-domains>`
  * :manual:`PHP <lang-php>`
  * :manual:`cron <daemons-cron>`

License
=======

The software is licensed under GPLv3_. All relevant information can be found in the repository of the project.

Prerequisites
=============

We're using :manual:`PHP <lang-php>` in the stable version 7.1:

::

 [isabell@stardust ~]$ uberspace tools version show php
 Using 'PHP' version: '7.1'
 [isabell@stardust ~]$

.. include:: includes/my-print-defaults.rst

The domain you want to use must be set up:

.. include:: includes/web-domain-list.rst

Installation
============

Download and extract ZIP archive
--------------------------------

Check the selfoss_ website or `GitHub repo`_ for the `latest release`_ and copy the download link to the ZIP file. Then ``cd`` to your :manual:`DocumentRoot <web-documentroot>` and use ``wget`` to download it. Replace the URL with the one you just copied.

.. code-block:: console
 :emphasize-lines: 2

 [isabell@stardust ~]$ cd /var/www/virtual/$USER/
 [isabell@stardust isabell]$ wget https://github.com/SSilence/selfoss/releases/download/47.11/selfoss-47.11.zip
 […]
 Saving to: ‘selfoss-47.11.zip’

 100%[========================================================================================================================>] 2,881,068    819KB/s   in 3.7s

 2018-09-24 10:49:50 (766 KB/s) - ‘selfoss-47.11.zip’ saved [2881068/2881068]

Unzip the archive to the ``html`` folder and then delete it. Replace the version in the file name with the one you downloaded.

.. code-block:: console
 :emphasize-lines: 1,6

 [isabell@stardust isabell]$ unzip -d html/ selfoss-47.11.zip
 […]
   inflating: html/common.php
   inflating: html/run.php
   inflating: html/cliupdate.php
 [isabell@stardust isabell]$ rm selfoss-47.11.zip
 [isabell@stardust isabell]$

Configuration
=============

Setup your database
-------------------

We recommend setting up a new database for selfoss.

.. code-block:: console
 :emphasize-lines: 1

 [isabell@stardust ~]$ mysql -e "CREATE DATABASE ${USER}_selfoss"

Configuration
-------------

Copy the ``default.ini`` to ``config.ini``:

::

 [isabell@stardust isabell]$ cd html
 [isabell@stardust html]$ cp default.ini config.ini
 [isabell@stardust html]$

Now edit ``config.ini`` file, change the database type to ``mysql`` and provide your MySQL credentials.

.. code-block:: ini
 :emphasize-lines: 4,5,6

 [globals]
 db_type=mysql
 db_host=localhost
 db_database=isabell_selfoss
 db_username=isabell
 db_password=MySuperSecretPassword
 db_port=3306

We also recommend password protection for your installation. First, generate a random string to use as salt_.

::

 [isabell@stardust html]$ pwgen 32 1

Copy the output and set it as salt in your ``config.ini``.

.. code-block:: ini
 :emphasize-lines: 1

 salt=FqFvsGWABfpPK6zQnVzD

Save the file and visit ``https://isabell.uber.space/password`` in your browser. Replace ``isabell.uber.space`` with your domain. Use the web form to generate a hash of your password and copy the hash.

Edit ``config.ini`` again and insert your user name and password hash:

.. code-block:: ini
 :emphasize-lines: 1,2

 username=isabell
 password=c6d064709111ff0a689f206524cec8952417b9f16121a06b4ec8c58a11b570cdb7df4d6912e49415d6c615c2961c35166f0ed98eb027425100a1ebdd55a97906
 salt=FqFvsGWABfpPK6zQnVzD

You can now log in to your installation and start adding and reading feeds.

Check out the official `selfoss documentation`_ for explanation of further configuration parameters.

Cron job
========

It is recommended to set up a cron job to automatically update your feeds. Edit your cron tab using the ``crontab -e`` command and insert this cron job to update every 15 minutes. Make sure to replace ``/home/isabell/html/cliupdate.php`` with the path to the ``cliupdate.php`` script inside the selfoss folder.

::

 */15 * * * * php /home/isabell/html/cliupdate.php > /dev/null 2>&1

.. _selfoss: https://selfoss.aditu.de/
.. _latest release: https://github.com/SSilence/selfoss/releases/latest
.. _GPLv3: https://www.gnu.org/licenses/gpl-3.0.html
.. _salt: https://en.wikipedia.org/wiki/Salt_(cryptography)
.. _selfoss documentation: https://selfoss.aditu.de/#configuration_params
.. _Github repo: https://github.com/SSilence/selfoss

----

Tested with selfoss 2.18, Uberspace 7.1.12.0

.. author_list::
