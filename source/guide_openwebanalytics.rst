.. highlight:: console

.. spelling::
    owa

.. author:: Thomas Johnson <https://johnson.tj/>

.. tag:: lang-php
.. tag:: web
.. tag:: analytics

.. sidebar:: Logo

  .. image:: _static/images/openwebanalytics.png
      :align: center
      
.. error::

  This guide seems to be **broken** for the current versions of open web analytics, we would be
  happy if you want to work on a solution and create a Pull Request.
  See also the related issue: https://github.com/Uberspace/lab/issues/1427

##################
Open Web Analytics
##################

.. tag_list::

`Open Web Analytics`_ is an open source web analytics software framework that you can use to track and analyze how people use your websites and applications.

----

.. note:: For this guide you should be familiar with the basic concepts of

  * :manual:`PHP <lang-php>`
  * :manual:`MySQL <database-mysql>`
  * :manual:`domains <web-domains>`

Prerequisites
=============

We’re using :manual:`PHP <lang-php>` in the stable version 7.2:

.. code-block:: console

 [isabell@stardust ~]$ uberspace tools version show php
 Using 'PHP' version: '7.2'
 [isabell@stardust ~]$

.. include:: includes/my-print-defaults.rst

Your website domain needs to be set up:

.. include:: includes/web-domain-list.rst

Installation
============

Create the database and download the `latest version`_ into the subdirectory ``owa`` under your :manual:`DocumentRoot <web-documentroot>`.

.. code-block:: console

 [isabell@stardust ~]$ mysql -e "CREATE DATABASE ${USER}_owa"
 [isabell@stardust ~]$ cd /var/www/virtual/$USER/html/
 [isabell@stardust html]$ mkdir owa && cd owa
 [isabell@stardust owa]$ wget https://github.com/Open-Web-Analytics/Open-Web-Analytics/releases/download/1.6.8/owa_1.6.8_packaged.tar
 (...)
 [isabell@stardust owa]$ tar -xvf owa_1.6.8_packaged.tar
 (...)
 [isabell@stardust owa]$

Configuration
=============

After the installation you need to open isabell.uber.space/owa in your browser to finish your setup.

Fill out your configuration settings:
 * Database Host: ``localhost``
 * Database Name: ``isabell_owa``
 * Database User: ``isabell``
 * Database Password: :manual_anchor:`credentials <database-mysql.html#login-credentials>`

Updates
=======

.. note:: Check the update feed_ regularly to stay informed about the newest version.

Check Open Web Analytics's `stable releases`_ for the latest versions. If a newer version is available, replace the version number ``1.6.8`` with the latest one.

Backup your ``owa/owa-config.php`` file, delete everything else in your ``owa`` directory.

.. code-block:: console

 [isabell@stardust ~]$ cd /var/www/virtual/$USER/html/owa/
 [isabell@stardust owa]$ cp owa/owa-config.php ~
 [isabell@stardust owa]$ rm -rf * .*
 [isabell@stardust owa]$ wget https://github.com/Open-Web-Analytics/Open-Web-Analytics/releases/download/1.6.8/owa_1.6.8_packaged.tar
 (...)
 [isabell@stardust owa]$ tar -xvf owa_1.6.8_packaged.tar
 (...)
 [isabell@stardust owa]$ mv ~/owa-config.php ./
 [isabell@stardust owa]$

Finish the update by open isabell.uber.space in your browser.

.. _Open Web Analytics: http://www.openwebanalytics.com/
.. _latest version: https://github.com/Open-Web-Analytics/Open-Web-Analytics/releases
.. _feed: https://github.com/Open-Web-Analytics/Open-Web-Analytics/releases.atom
.. _stable releases: https://github.com/Open-Web-Analytics/Open-Web-Analytics/releases

----

Tested with Open Web Analytics 1.6.8 and Uberspace 7.5.1

.. author_list::
