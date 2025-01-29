.. highlight:: console

.. author:: Thomas Johnson <https://johnson.tj/>

.. tag:: lang-php
.. tag:: web
.. tag:: cms

.. sidebar:: Logo

  .. image:: _static/images/concrete_cms.png
      :align: center

############
Concrete CMS
############

.. tag_list::

`Concrete CMS`_  is an open-source content management system for publishing content on the World Wide Web and intranets. Concrete CMS is designed for ease of use, for users with a minimum of technical skills. It enables users to edit site content directly from the page. It provides version management for every page, similar to wiki software, another type of web site development software. Concrete CMS allows users to edit images through an embedded editor on the page.

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

 [isabell@stardust ~]$ mysql -e "CREATE DATABASE ${USER}_concrete_cms"
 [isabell@stardust ~]$ cd /var/www/virtual/$USER/
 [isabell@stardust isabell]$ wget https://github.com/concretecms/concretecms/releases/download/9.3.9/concrete-cms-9.3.9.zip
 [isabell@stardust isabell]$ unzip concrete-cms-9.3.9.zip
 [isabell@stardust isabell]$ rm -f html/nocontent.html; rmdir html
 [isabell@stardust isabell]$ mv concrete-cms-9.3.9 html
 [isabell@stardust isabell]$ rm concrete-cms-9.3.9.zip
 [isabell@stardust isabell]$

Configuration
=============

Point your browser to your domain (e.g. isabell.uber.space) to set up and configure your Concrete CMS installation.

Enter the following information into the installer:

  * your MySQL hostname, username and password: the hostname is ``localhost`` you should have your MySQL :manual_anchor:`credentials <database-mysql.html#login-credentials>` ready.
  * the name of your newly created Concrete CMS database (e.g. ``isabell_concrete_cms``)

Usage
=====

There is a user manual available on how to use Concrete CMS.

    * https://documentation.concretecms.org/


Updates
=======

.. note:: Check the update feed_ regularly to stay informed about the newest version.

Navigate to Dashboard > System and Settings > Update Concrete.


.. _Concrete CMS: https://www.concretecms.org/
.. _feed: https://github.com/concretecms/concretecms/releases.atom
.. _PHP: http://www.php.net/


----

Tested with Concrete CMS 9.3.9, Uberspace 7.16.3, PHP 8.3

.. author_list::
