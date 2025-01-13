.. highlight:: console

.. author:: Thomas Johnson <https://johnson.tj/>

.. tag:: lang-php
.. tag:: web
.. tag:: cms
.. tag:: membership-management

.. sidebar:: Logo

  .. image:: _static/images/admidio.svg
      :align: center

#######
Admidio
#######

.. tag_list::

Admidio_  is a free online membership management, which is optimized for associations, groups and organizations. In addition to classic user management it consists of a variety of modules that can be installed and adjusted on a new or existing homepage.

----

.. note:: For this guide you should be familiar with the basic concepts of

  * PHP_
  * :manual:`MySQL <database-mysql>`
  * :manual:`domains <web-domains>`

Prerequisites
=============

.. include:: includes/my-print-defaults.rst

We’re using :manual:`PHP <lang-php>` in the stable version 8.3:

.. code-block:: console

 [isabell@stardust ~]$ uberspace tools version show php
 Using 'PHP' version: '8.3'
 [isabell@stardust ~]$

Your website domain needs to be set up:

.. include:: includes/web-domain-list.rst

Installation
============

We create the Database, download the latest version and unzip the file.

.. code-block:: console

 [isabell@stardust ~]$ mysql -e "CREATE DATABASE ${USER}_admidio"
 [isabell@stardust ~]$ cd ~/html
 [isabell@stardust html]$ wget https://github.com/Admidio/admidio/archive/refs/tags/v4.3.13.zip
 [isabell@stardust html]$ unzip v4.3.13.zip
 [isabell@stardust html]$ mv admidio-4.3.13/* ./
 [isabell@stardust html]$ rmdir admidio-4.3.13
 [isabell@stardust html]$ rm v4.3.13.zip
 [isabell@stardust html]$

Configuration
=============

Point your browser to your domain (e.g. isabell.uber.space) to set up and configure your Admidio installation.

Enter the following information into the installer:

  * your MySQL hostname, username and password: the hostname is ``localhost`` you should have your MySQL :manual_anchor:`credentials <database-mysql.html#login-credentials>` ready.
  * the name of your newly created Admidio database (e.g. ``isabell_admidio``)

Usage
=====

There is a user manual available on how to use Admidio.

    * https://www.admidio.org/dokuwiki/


Updates
=======

.. note:: Check the update feed_ regularly to stay informed about the newest version.

1. Download the latest version to your :manual:`DocumentRoot <web-documentroot>` and unzip the file.
2. Remove the ``adm_program`` directory and ``index.php`` file.
3. Copy the new ``adm_program`` directory and ``index.php`` from the new version into your :manual:`DocumentRoot <web-documentroot>`
4. Check the update process if you have any plugins or customized themes.
5. Point your browser to your domain (e.g. isabell.uber.space) to finalize the update.

The update process is described here:

    * https://www.admidio.org/dokuwiki/doku.php?id=en:2.0:update


.. _Admidio: https://www.admidio.org/
.. _feed: https://github.com/Admidio/admidio/releases.atom
.. _PHP: http://www.php.net/


----

Tested with Admidio 4.3.13, Uberspace 7.16.3, PHP 8.3

.. author_list::
