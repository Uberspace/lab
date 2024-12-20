.. highlight:: console

.. author:: Dominik Kustermann <hilfe@edvstuttgart.de>  
   Translated with ChatGPT

.. tag:: lang-php
.. tag:: web
.. tag:: shop
.. tag:: audience-business

.. sidebar:: Logo

  .. image:: _static/images/shopware.svg
      :align: center

##########
Shopware 6
##########

.. tag_list::

Shopware_ is an open-source e-commerce software powered by Symfony_ and Vue.js_. The community
edition is distributed under the MIT license. It's the successor of Shopware 5.

----

.. note:: For this guide you should be familiar with the basic concepts of

  * :manual:`PHP <lang-php>`
  * :manual:`MySQL <database-mysql>`
  * :manual:`domains <web-domains>`

License
=======

All relevant legal information can be found here

  * https://github.com/shopware/platform/blob/master/LICENSE

Prerequisites
=============

We're using PHP in the stable version 8.1:

::

 [isabell@stardust ~]$ uberspace tools version show php
 Using 'PHP' version: '8.1'
 [isabell@stardust ~]$

.. include:: includes/my-print-defaults.rst

Your shop URL needs to be set up:

.. include:: includes/web-domain-list.rst

Configuration
=============

To configure PHP according to the `Shopware system requirements`_, go to
``$HOME/etc/php.d/``, create ``shopware.ini`` and add the following lines:

::

 memory_limit = 512M
 apc.enable_cli = 1
 opcache.memory_consumption = 256

After setting these PHP parameters, restart PHP to activate the changes

.. code-block:: console

 [isabell@stardust ~]$ uberspace tools restart php
 Your PHP configuration has been loaded.
 [isabell@stardust ~]$

Installation
============

Setup the Environment
----------------------

Switch to your user directory and create a folder for Shopware:

.. code-block:: console

 [isabell@stardust ~]$ cd /var/www/virtual/$USER/
 [isabell@stardust $USER]$ mkdir shopware
 [isabell@stardust $USER]$ cd shopware

Download the Installer
----------------------

Download the Shopware installer script:

.. code-block:: console
 :emphasize-lines: 2

 [isabell@stardust shopware]$ wget https://github.com/shopware/web-recovery/releases/latest/download/shopware-installer.phar.php

Adjust DocumentRoot
-------------------

Move one level up, remove the default ``html`` symlink, and point it to the Shopware installation:

.. code-block:: console

 [isabell@stardust shopware]$ cd ..
 [isabell@stardust $USER]$ rm -f html
 [isabell@stardust $USER]$ ln -s /var/www/virtual/$USER/shopware html

Complete the Installation
-------------------------

Open your browser and navigate to your domain, e.g., ``https://isabell.uber.space``, and follow the installation steps.

.. warning:: When attempting to install the latest version of Shopware directly, I encountered an issue where Shopware requires MariaDB version 10.11. However, Uberspace currently provides only version 10.6.19 on Uberspace 7. According to Uberspace support, this limitation may be resolved with Uberspace 8. Until then, it is mandatory to install Shopware version 6.6.8, as any newer versions will cause issues.  

    If errors occur during the process, refer to the :ref:`Troubleshooting <troubleshooting>` section below.

Post-Installation Configuration
===============================

After installation, follow these steps for further configuration:

1. Perform all available updates via `Shopware > Settings > System > Shopware Updates`.
2. Update the DocumentRoot symlink to the ``public`` directory:

   .. code-block:: console

    [isabell@stardust ~]$ cd /var/www/virtual/$USER/
    [isabell@stardust $USER]$ rm html
    [isabell@stardust $USER]$ ln -s /var/www/virtual/$USER/shopware/public html

3. Adjust the API URL:

   .. code-block:: console

    [isabell@stardust $USER]$ cd /var/www/virtual/$USER/shopware
    [isabell@stardust shopware]$ nano .env.local

    Remove the ``/public`` part from ``APP_URL=[...]``.

4. Upgrade plugins in the Shopware admin.
5. Update the domain under "Sales Channels".

Domain Adjustment
=================

If switching to a custom domain, repeat the steps above to update the symlink and API URL.

.. _troubleshooting:

Troubleshooting
===============

If issues occur during installation, delete the Shopware folder and database to start over:

Follow the steps outlined in the `Download the Installer`_ section to restart the process.

.. code-block:: console

 [isabell@stardust ~]$ rm -rf /var/www/virtual/$USER/shopware
 [isabell@stardust ~]$ mysql -e "DROP DATABASE isabell_shopware"

----

.. _Shopware: https://www.shopware.com
.. _Shopware website: https://www.shopware.com/en/download/
.. _Shopware system requirements: https://docs.shopware.com/en/shopware-6-en/first-steps/system-requirements
.. _Symfony: https://symfony.com
.. _Vue.js: https://vuejs.org
