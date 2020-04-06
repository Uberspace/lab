.. highlight:: console

.. author:: Gökhan Sirin <g.sirin@gedankengut.de>

.. tag:: lang-php
.. tag:: audience-business
.. tag:: accounting
.. tag:: customer-management

.. sidebar:: Logo

  .. image:: _static/images/gsales2.png
      :align: center


#########
GSALES 2
#########

.. tag_list::

GSALES 2 is a very flexible german billing application specialized for generating recurring invoices.
Equipped with a well documented SOAP API you can easily attach tools and third party apps to GSALES 2 to fit your needs.



----

.. note:: For this guide you should be familiar with the basic concepts of

  * :manual:`PHP <lang-php>`
  * :manual:`MySQL <database-mysql>`



License
=======

GSALES is distributed in a free demo mode where the count of recordsets is limited.
After exceeding the limit GSALES will fall back to a read-only mode requiring you to rent or purchase a licence for the application at `gsales.de <https://www.gsales.de>`_.



Prerequisites
=============

The GSALES 2 download which is used later, is especially for the PHP version 7.1.
So we have to make sure that this PHP version is used on the server. Let's set it with the command:

::

 [isabell@stardust ~]$ uberspace tools version use php 7.1
 Selected PHP version 7.1
 The new configuration is adapted immediately. Patch updates will be applied automatically.
 [isabell@stardust ~]$




After setting the PHP version just make sure we are using the correct version:

::

 [isabell@stardust ~]$ uberspace tools version show php
 Using 'PHP' version: '7.1'
 [isabell@stardust ~]$



The codebase of GSALES 2 is obfuscated and encrypted with the IonCube Encoder. In order to run GSALES 2 on your server you need the so called IonCube Loader. Please follow the guide :lab:`ionCube Loader <guide_ioncube>` to setup the loader for your space.



Installation
============

We are going to install GSALES 2 into a subdirectory called gsales2.

First ``cd`` into your html directory.

::

 [isabell@stardust ~]$ cd html
 [isabell@stardust html]$



Now download the latest release of GSALES 2 for PHP 7.1:

::

 [isabell@stardust html]$ wget https://www.gsales.de/download/latest71.tar.gz
 [isabell@stardust html]$


Extract the downloaded archive

::

 [isabell@stardust html]$ tar -xvzf latest71.tar.gz

After extracting the archive a new subdirectory with ``gsales2-revXXXX`` is created.
For easier access rename this subdirectory to ``gsales2`` with the following command:

::

 [isabell@stardust html]$ mv gsales2-rev1123 gsales2

If you need to lookup the revision number simply list the contents of the directory with ``ls``.



Next get rid of the GSALES 2 download archive:

::

 [isabell@stardust html]$ rm latest71.tar.gz
 [isabell@stardust html]$



Prepare the GSALES 2 configuration file which has to be in place to hold the parameters to access the database later:

::

 [isabell@stardust html]$ cp gsales2/lib/inc.cfg.dist.php gsales2/lib/inc.cfg.php

Create database
===============

Use this command to create a database named ``<username>_gsales2``. In our example this would be ``isabell_gsales2``.

::

 [isabell@stardust ~]$ mysql -e "CREATE  DATABASE ${USER}_gsales2"

Configuration
=============

Now append /gsales2 to your website URL and point your browser to it.
The web based installer will appear asking you to confirm the licence and adding the parameters to connect to the mysql database.

Find out the information for your uberspace mysql database with the command:

.. include:: includes/my-print-defaults.rst

Use ``localhost`` for the Server and your user name for “Benutzer,” the database name ``<username>_gsales2`` for  “Datenbank”. Add the “Passwort” according to the output of the command above.

Click the Button “Datenbankzugang speichern und weiter >>” to continue.

Make sure the boxes on the next page are all green and all requirements for GSALES 2 are set and met.
Click the Button “Installation starten >>”.

Scroll to the very bottom of the page - make sure everything is green again and find your Login information under the Headline “Installation erfolgreich”.
Make sure to save your GSALES 2 Password. Click blue Button “zum GSALES-Login” to Login to your new GSALES 2 Installation.


Updates
=======

GSALES 2 Updates are pretty straightforward.

1. Make sure to have a backup of your files and database.

2. Download the latest release and extract the files over the ones already there.

3. Point your Browser to the Installation and an Updater will guide you through the rest of the process.

A more detailed update instruction can be found on the `gsales website <gsalesupdate_>`_.

.. _gsalesupdate: https://support.gsales.de/hc/de/articles/202105793-gSales-2-richtig-schnell-updaten

----

Tested with GSALES 2 Revision #1123 for PHP 7.1, Uberspace 7.1.16

.. author_list::
