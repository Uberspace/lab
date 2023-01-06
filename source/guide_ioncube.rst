.. _guide_ioncube:

.. highlight:: console

.. author:: Gökhan Sirin <g.sirin@gedankengut.de>

.. tag:: lang-php
.. tag:: lang-c
.. tag:: proprietary

.. sidebar:: Logo

  .. image:: _static/images/ioncube.png
      :align: center


##############
ionCube Loader
##############

.. tag_list::

Using ionCube encoded and secured PHP files requires a file called the ionCube Loader to be installed on the web server and made available to PHP.

----

.. note:: For this guide you should be familiar with the basic concepts of

  * :manual:`PHP <lang-php>`


Installation
============

The installation of the ionCube Loader is pretty straightforward.

First we have to download and extract it:

::

  [isabell@stardust ~]$ wget https://downloads.ioncube.com/loader_downloads/ioncube_loaders_lin_x86-64.tar.gz
  [isabell@stardust ~]$ tar -xvzf ioncube_loaders_lin_x86-64.tar.gz
  [isabell@stardust ~]$



Tidy up your space if you want by removing the downloaded archive:

::

  [isabell@stardust ~]$ rm ioncube_loaders_lin_x86-64.tar.gz
  [isabell@stardust ~]$



Now we have to make sure that our PHP installation is loading this extension.
Create the php.early.d directory which is holding custom configuration directives for PHP:

::

  [isabell@stardust ~]$ mkdir etc/php.early.d
  [isabell@stardust ~]$


As you know, your Uberspace supports multiple PHP versions. The ionCube Loader depends on the used PHP version. So let's find out which version is in place:

::

 [isabell@stardust ~]$ uberspace tools version show php
 Using 'PHP' version: '8.1'
 [isabell@stardust ~]$



ionCube Loader for PHP 8.1
==========================

Create the following configuration directive if you are using PHP 8.1.

::

  [isabell@stardust ~]$ echo "zend_extension=$HOME/ioncube/ioncube_loader_lin_8.1.so" > etc/php.early.d/ioncube.ini
  [isabell@stardust ~]$



Changes to the PHP configuration will take effect after reloading PHP:

::

  [isabell@stardust ~]$ uberspace tools restart php
  Your php configuration has been loaded.
  [isabell@stardust ~]$


----

Tested with IonCube 12.0.2, Uberspace 7.13, PHP 8.1

.. author_list::
