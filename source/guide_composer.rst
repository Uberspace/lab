.. author:: Tede Mehrtens <kontakt@tedemehrtens.de>
.. highlight:: console

.. sidebar:: Logo

  .. image:: _static/images/composer-satis.png
      :align: center

#########
Composer
#########

Composer_ is a modern dependency manager for php. 

It allows you to easily set up dependencies for the software you develop, update them and resolve any conflicts between packages.

----

.. note:: For this guide you should be familiar with the basic concepts of

  * PHP_
  * CLI_

Prerequisites
=============

As composer requires at least PHP version 5.3.2, you can use it with each version available in your uberspace.

Installation
============

Download the composer setup file to your current directory and run it.
After installing composer, you may delete the installer.

Since we want composer to be installed into our ~/bin directory and be available using the command "composer", we need to tell the installer:

  * ``--install-dir``: Tells the installer in which directory composer should be installed
  * ``--filename``: Sets the filename of the executable


.. code-block:: console
 :emphasize-lines: 2

 [isabell@stardust html]$ wget -qO composer-setup.php https://getcomposer.org/installer
 [isabell@stardust html]$ php composer-setup.php --install-dir=/home/$USER/bin --filename=composer
 All settings correct for using Composer
 Downloading...

 Composer (version 1.8.4) successfully installed to: /home/isabell/bin/composer
 Use it: php bin/composer
 [isabell@stardust html]$ rm composer-setup.php
 [isabell@stardust html]$ 

Updates
=======

You can easily update composer to the latest version using ``composer self-update``

.. code-block:: console

 [isabell@stardust html]$ composer self-update
 You are already using composer version 1.8.4 (stable channel).
 [isabell@stardust html]$ 

.. _Composer: https://getcomposer.org/
.. _PHP: http://www.php.net/
.. _CLI: https://manual.uberspace.de/basics-shell.html

----

Tested with Composer 1.8.4, Uberspace 7.2.3

.. authors::
