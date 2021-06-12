.. highlight:: console

.. author:: Thomas Kammerer <https://kammerer.tk/>

.. tag:: lang-php
.. tag:: web
.. tag:: audience-business

.. sidebar:: Logo

  .. image:: _static/images/osticket.png
      :align: center

#########
osTicket
#########

.. tag_list::

.. abstract::
  osTicket_ is a widely-used open source support ticket system. It seamlessly integrates inquiries created via email, phone and web-based forms into a simple easy-to-use multi-user web interface. Manage, organize and archive all your support requests and responses in one place while providing your customers with accountability and responsiveness they deserve.

----

.. note:: For this guide you should be familiar with the basic concepts of

  * :manual:`PHP <lang-php>`
  * :manual:`MySQL <database-mysql>`
  * :manual:`domains <web-domains>`

License
=======

osTicket is released under the `GPL2 license`_.

Prerequisites
=============

We’re using :manual:`PHP <lang-php>` in the stable version 7.2. Since new Uberspaces are currently setup with PHP 7.1 by default you need to set this version manually:

::

 [isabell@stardust ~]$ uberspace tools version use php 7.2
 Selected PHP version 7.2
 The new configuration is adapted immediately. Patch updates will be applied automatically.
 [isabell@stardust ~]$

.. include:: includes/my-print-defaults.rst

Your website domain needs to be set up:

.. include:: includes/web-domain-list.rst

Installation
============

To install osTicket we clone the current version using Git. ``cd`` to your :manual:`DocumentRoot <web-documentroot>` so the cloned folder will be under your ``html``.

.. code-block:: console
 :emphasize-lines: 2

 [isabell@stardust ~]$ cd /var/www/virtual/$USER/html/
 [isabell@stardust html]$ git clone https://github.com/osTicket/osTicket.git .
 Cloning into '.'...
 (...)
 [isabell@stardust ~]$

Configuration
=============

Copy the configuration template.

::

 [isabell@stardust html]$ cp include/ost-sampleconfig.php include/ost-config.php
 [isabell@stardust html]$

After the installation you need to open isabell.uber.space in your browser to finish your setup.

Fill out your system settings, admin user and edit the following database settings:
 * MySQL Database: ``isabell_osticket``
 * MySQL Username: ``isabell``
 * MySQL Password from your MySQL :manual_anchor:`credentials <database-mysql.html#login-credentials>`

::

 [isabell@stardust html]$ chmod 0444 include/ost-config.php
 [isabell@stardust html]$

Best practices
==============

Security
--------

Remove the setup directory.

::

 [isabell@stardust html]$ rm -rf setup/
 [isabell@stardust html]$

Updates
=======

.. note:: Check the update feed_ regularly to stay informed about the newest version.

Check osTicket's `stable releases`_ for the latest versions. If a newer version is available, you should manually update your installation.

Backup your ``config/ost-config.php`` file, delete everything else in your ``html`` directory.

::

 [isabell@stardust ~]$ cd /var/www/virtual/$USER/html/
 [isabell@stardust html]$ cp config/ost-config.php ~
 [isabell@stardust html]$ rm -rf * .*
 [isabell@stardust html]$ git clone https://github.com/osTicket/osTicket.git .
 Cloning into '.'...
 (...)
 [isabell@stardust html]$ mv ~/ost-config.php config/
 [isabell@stardust html]$

Finish the update by open isabell.uber.space in your browser.

.. _osTicket: https://osticket.com/
.. _feed: https://github.com/osTicket/osTicket/releases.atom
.. _GPL2 license: https://opensource.org/licenses/GPL-2.0
.. _stable releases: https://github.com/osTicket/osTicket/releases

----

Tested with osTicket 1.14.1 and Uberspace 7.4

.. author_list::
