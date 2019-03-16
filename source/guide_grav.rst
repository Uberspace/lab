.. highlight:: console

.. author:: Daniel Kratz <uberlab@danielkratz.com>

.. sidebar:: Logo

  .. image:: _static/images/grav.svg
      :align: center

##########
Grav
##########

Grav_ is an open source flat-file (no database) content management system written in PHP.

It was developed with a focus on speed, simplicity, and flexibility. Content can be managed by easily editing folders and markdown files or using an admin panel (GUI).

----

.. note:: For this guide you should be familiar with the basic concepts of

  * PHP_
  * :manual:`domains <web-domains>`

License
=======

Grav is released under the `MIT License`_. All relevant information can be found in the LICENSE.txt_ file in the repository of the project.

Prerequisites
=============

We're using PHP_ in the stable version 7.1:

::

 [isabell@stardust ~]$ uberspace tools version show php
 Using 'PHP' version: '7.1'
 [isabell@stardust ~]$

Your website domain needs to be set up:

.. include:: includes/web-domain-list.rst

Installation
============

To install Grav we use Composer_ to create a new project in our :manual:`document root <web-documentroot>`.

.. code-block:: console
 :emphasize-lines: 1,2

 [isabell@stardust ~]$ cd /var/www/virtual/$USER
 [isabell@stardust isabell]$ composer create-project getgrav/grav html
 Installing getgrav/grav (42.2.1)
  - Installing getgrav/grav (42.2.1): Downloading (100%)
 Created project in /var/www/virtual/isabell/html
 Loading composer repositories with package information
 Installing dependencies (including require-dev) from lock file
 Package operations: 67 installs, 0 updates, 0 removals
 [...]
 [isabell@stardust isabell]$

Visit your previously set up domain isabell.uber.space and you will see a page confirming that the installation was successfull.

Install admin panel
-------------------

You can optionally install the Grav admin panel. To do so we use the integrated Grav Package Manager (GPM).
Navigate to your installation directory and install the admin plugin. The package manager will ask you to confirm the installation.

.. code-block:: console
 :emphasize-lines: 1,2,8

 [isabell@stardust ~]$ cd ~/html
 [isabell@stardust html]$ bin/gpm install admin
 GPM Releases Configuration: Stable
 The following dependencies need to be installed...
  |- Package form
  |- Package login
  |- Package email
 Install these packages? [Y|n] Y
 [...]
 [isabell@stardust isabell]$

After the installation you need to open isabell.uber.space/admin in your browser to create an admin account (please don't use ``admin`` as your username).

Tuning
======

Grav turns on caching out of the box to improve the performance of your site. It will automatically use the best cache driver available. You can find more information in the Grav Documentation under `Performance & Caching`_.

Updates
=======

.. note:: Check the update feed_ regularly to stay informed about the newest version.

To update Grav you can use the integrated Grav Package Manager (GPM).
To update the Grav core navigate to your :manual:`document root <web-documentroot>` and use the ``selfupgrade`` command.

.. code-block:: console
 :emphasize-lines: 1,2

 [isabell@stardust ~]$ cd ~/html
 [isabell@stardust html]$ bin/gpm selfupgrade --force
 [isabell@stardust isabell]$

After updating the Grav core use the ``update`` command to update all plugins and themes.

.. warning:: Please make sure to always update the Grav core first before updating plugins and themes.

.. code-block:: console
 :emphasize-lines: 1,2

 [isabell@stardust ~]$ cd ~/html
 [isabell@stardust html]$ bin/gpm update --force
 [isabell@stardust isabell]$

.. _Grav: https://getgrav.org/
.. _PHP: http://www.php.net/
.. _Composer: https://getcomposer.org/
.. _feed: https://github.com/getgrav/grav/releases.atom
.. _MIT License: https://opensource.org/licenses/MIT
.. _LICENSE.txt: https://github.com/getgrav/grav/blob/develop/LICENSE.txt
.. _GitHub: https://github.com/getgrav/grav
.. _Performance & Caching: https://learn.getgrav.org/advanced/performance-and-caching

----

Tested with Grav 1.5.2, Uberspace 7.1.13

.. authors::
