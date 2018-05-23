.. author:: minim <https://github.com/minim-one>
.. highlight:: console

.. sidebar:: Logo

  .. image:: _static/images/minim.png
      :align: center

#####
minim
#####

minim_ offers a super simple PHP Content Management System. The code is Open Source and you're free to modify, distribute and use it for private and commercial projects.

It'is ideal for simple travel blogs or publishing news. It has an easy administration interface and a automatic generated RSS feed. Themes and other modifications are fully customisable.

----

.. note:: For this guide you should be familiar with the basic concepts of

  * PHP_
  * domains_

Prerequisites
=============

We're using PHP_ in the stable version 7.2:

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

Use ``wget`` to download the latest release_. Copy the path to the ``.zip`` archive to your wget command. Change the URL to the latest version.

.. code-block:: console
 :emphasize-lines: 2,3,4

 [isabell@stardust ~]$ cd ~/html
 [isabell@stardust html]$ wget https://minim.one/downloads/minim-23.42.1.zip
 [isabell@stardust html]$ unzip minim-23.42.1
 [isabell@stardust html]$ rm minim-23.42.1
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

The admin interface is disabled by default. If you enable it, you should change the standard password.

Updates
=======

.. note:: Check the update feed_ regularly to stay informed about the newest version.

Check minim's feed_ for the latest version and copy the link to the ``.zip`` archive. In this example the version is 23.42.1, which of course does not exist. Change the version to the latest one in the highlighted lines.

.. code-block:: console
 :emphasize-lines: 2,4,5,6,7

 [isabell@stardust ~]$ cd ~/html
 [isabell@stardust html]$ wget https://minim.one/downloads/minim-23.42.1.zip
 [isabell@stardust html]$ cp -r minim minim-backup
 [isabell@stardust html]$ unzip minim-23.42.1.zip -d minim-23.42.1
 [isabell@stardust html]$ mv minim-23.42.1/minim/config minim-23.42.1/minim/config-new
 [isabell@stardust html]$ cp -r minim-23.42.1/minim ./
 [isabell@stardust html]$ rm -rf minim-23.42.1*
 [isabell@stardust html]$

Check if the configuration_ changed in ``config-new/config.php`` and your ``config/config.php`` (happens very rarely).
If everything works alright you can delete your ``minim-backup`` and the ``config-new`` directories.

.. _minim: https://minim.one/
.. _domains: https://manual.uberspace.de/en/web-domains.html
.. _PHP: https://manual.uberspace.de/en/lang-php.html#show-available-versions
.. _configuration: https://minim.one/docs/
.. _feed: https://minim.one/rss/
.. _release: https://minim.one/downloads/

----

Tested with minim 0.5.0.1, Uberspace 7.1.6

.. authors::
