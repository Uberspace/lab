.. highlight:: console

.. author:: Yannick Ihmels <yannick@ihmels.org>

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

Shopware_ is a open source e-commerce software powered by Symfony_ and Vue.js_. The community
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

We're using PHP in the stable version 7.2:

::

 [isabell@stardust ~]$ uberspace tools version show php
 Using 'PHP' version: '7.2'
 [isabell@stardust ~]$

.. include:: includes/my-print-defaults.rst

Your shop URL needs to be setup:

.. include:: includes/web-domain-list.rst

Installation
============

Download
--------

Check the `Shopware website`_ for the latest release and copy the URL to the ZIP file. Replace the
URL with the one you just copied.

.. code-block:: console
 :emphasize-lines: 2

 [isabell@stardust ~]$ cd /var/www/virtual/$USER/
 [isabell@stardust isabell]$ curl -o shopware.zip https://releases.shopware.com/sw6/install_6.0.0_ea2_1571125323.zip
 [isabell@stardust isabell]$ unzip -d shopware shopware.zip
 [isabell@stardust isabell]$ rm shopware.zip
 [isabell@stardust isabell]$

Since Shopware uses the sub directory public/ as the :manual:`DocumentRoot <web-documentroot>`,
you need to remove your DocumentRoot and create a symlink to the shopware/public/ directory:

.. warning:: Make sure ``html`` is empty before deleting it. If there are any files you want to keep
   in ``html``, you can also rename the folder instead of deleting it.

.. code-block:: console

 [isabell@stardust isabell]$ rm -rf html
 [isabell@stardust isabell]$ ln -s /var/www/virtual/$USER/shopware/public html
 [isabell@stardust isabell]$

Setup
------

Point your browser to your domain, e.g. ``https://isabell.uber.space`` and follow the instructions
to set up Shopware. We suggest you use an
:manual_anchor:`additional database <database-mysql.html#additional-databases>`. For example:
isabell_shopware.

Configuration
=============

PHP Memory
----------

In order to increase the memory limit of php to the recommended value of 512 MB, go to
``$HOME/etc/php.d/``, create ``memory_limit.ini`` and add the following line:

::

 memory_limit = 512M

Updates
=======

.. note:: Check the update feed_ regularly to stay informed about the newest version.


.. _Shopware: https://www.shopware.com
.. _Shopware website: https://www.shopware.com/en/download/
.. _Symfony: https://symfony.com
.. _Vue.js: https://vuejs.org
.. _feed: https://github.com/shopware/platform/releases.atom

----

Tested with Shopware 6.0.0-ea2 , Uberspace 7.3.8.1

.. author_list::
