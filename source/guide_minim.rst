.. author:: minim <https://minim.one/>
.. highlight:: console

.. sidebar:: Logo

  .. image:: _static/images/minim.png
      :align: center

#####
minim
#####

minim_ offers a super simple PHP Content Management System. The code is Open Source and you're free to modify, distribute and use it for private and commercial projects.

It'is ideal for simple travel blogs or publishing news. It has an easy administration interface and an automatic generated RSS feed. Themes and other modifications are fully customisable.

----

.. note:: For this guide you should be familiar with the basic concepts of

  * :manual:`PHP <lang-php>`
  * :manual:`domains <web-domains>`

Prerequisites
=============

We're using :manual:`PHP <lang-php>` in the stable version 7.2:

::

 [isabell@stardust ~]$ uberspace tools version use php 7.2
 Selected PHP version 7.2
 The new configuration is adapted immediately. Patch updates will be applied automatically.
 [isabell@stardust ~]$ uberspace tools version show php
 Using 'PHP' version: '7.2'
 [isabell@stardust ~]$

Your URL needs to be setup:

.. include:: includes/web-domain-list.rst

Installation
============

Download minim
--------------

Use ``wget`` to download the latest release_.

.. code-block:: console

 [isabell@stardust ~]$ cd ~/html
 [isabell@stardust html]$ wget https://minim.one/downloads/?latest -O minim-latest.zip
 [isabell@stardust html]$ unzip minim-latest.zip
 [isabell@stardust html]$ rm minim-latest.zip
 [isabell@stardust html]$

Configuration
=============

Customization
-------------

You can leave the configuration_ in ``config/config.php`` or do changes as you want to.

Create your own theme in ``themes``. Just copy the default theme or create one from scratch.

Finishing installation
======================

Point your browser to URL.

Best practices
==============

Security
--------

The admin interface is disabled by default. If you enable it, you should change the standard password in ``addons/admin.php``.

Updates
=======

.. note:: Check the update feed_ regularly to stay informed about the newest version.

Check minim's feed_ for the latest version.

.. code-block:: console

 [isabell@stardust ~]$ cd ~/html
 [isabell@stardust html]$ wget https://minim.one/downloads/?latest -O minim-latest.zip
 [isabell@stardust html]$ cp -r minim minim-backup
 [isabell@stardust html]$ unzip minim-latest.zip -d minim-latest
 [isabell@stardust html]$ mv minim-latest/minim/config minim-latest/minim/config-new
 [isabell@stardust html]$ cp -r minim-latest/minim ./
 [isabell@stardust html]$ rm -rf minim-latest*
 [isabell@stardust html]$

Check if the configuration_ changed in ``config-new/config.php`` and your ``config/config.php`` (happens very rarely).
If everything works alright you can delete the ``config-new`` directory.

.. _minim: https://minim.one/
.. _configuration: https://minim.one/docs/
.. _feed: https://minim.one/rss/
.. _release: https://minim.one/downloads/

----

Tested with minim 0.9.2, Uberspace 7.1.14

.. authors::
