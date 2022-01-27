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
Shopware 5
##########

.. tag_list::

Shopware_ is a open source e-commerce software written in PHP. The community edition is distributed
under the AGPLv3  license.

----

.. note:: For this guide you should be familiar with the basic concepts of

  * :manual:`PHP <lang-php>`
  * :manual:`MySQL <database-mysql>`
  * :manual:`domains <web-domains>`
  * :manual:`cronjobs <daemons-cron>`

License
=======

All relevant legal information can be found here

  * https://github.com/shopware/shopware/blob/5.6/license.txt

Prerequisites
=============

We're using PHP in the stable version 7.4:

::

 [isabell@stardust ~]$ uberspace tools version show php
 Using 'PHP' version: '7.4'
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
 [isabell@stardust isabell]$ wget -O shopware.zip https://www.shopware.com/en/Download/redirect/version/sw5/file/install_5.7.6_32510831fc10df11821cf6de6aa03de47fd40255.zip
 [isabell@stardust isabell]$ unzip -d html shopware.zip
 [isabell@stardust isabell]$ rm shopware.zip
 [isabell@stardust isabell]$

Setup
------

Point your browser to your domain, e.g. ``https://isabell.uber.space`` and follow the instructions
to set up Shopware. For more information see the `installation guide`_. We suggest you use an
:manual_anchor:`additional database <database-mysql.html#additional-databases>`. For example:
``isabell_shopware``.

Configuration
=============

Cronjob
-------

Add the following cronjob to your :manual:`crontab <daemons-cron>`:

::

 */15  *  *  *  * php /var/www/virtual/$USER/html/bin/console sw:cron:run > $HOME/logs/shopware-cron.log 2>&1

Updates
=======

Shopware can be updated via AutoUpdate_. If an update is available you will be notified in the
backend. From there you can start the update.

.. note:: Check the update feed_ or `changelog page`_ regularly to stay informed about the newest
 version.


.. _Shopware: https://www.shopware.com
.. _Shopware website: https://www.shopware.com/en/download/
.. _installation guide: https://docs.shopware.com/en/shopware-5-en/first-steps/installing-shopware
.. _AutoUpdate: https://docs.shopware.com/en/shopware-5-en/update-guides/updating-shopware#update-via-autoupdate
.. _feed: https://github.com/shopware/shopware/releases.atom
.. _changelog page: https://www.shopware.com/en/changelog-sw5/

----

Tested with Shopware 5.7.6 , Uberspace 7.11.5

.. author_list::
