.. highlight:: console

.. author:: Sascha Groetzner <https://groetzner.net>

.. categorize your guide! refer to the current list of tags: https://lab.uberspace.de/tags
.. tag:: lang-php

.. sidebar:: Logo

  .. image:: _static/images/xdebug.svg
      :align: center

######
Xdebug
######


.. tag_list::

`Xdebug <https://xdebug.org>`_ is an extension for PHP, and provides a range of features to improve the PHP development experience.

----

.. note:: For this guide you should be familiar with the basic concepts of

  * :manual:`PHP <lang-php>`

License
=======

Xdebug is released under `The Xdebug License
<https://github.com/xdebug/xdebug/blob/master/LICENSE>`_, which is based on
`The PHP License <https://github.com/php/php-src/blob/master/LICENSE>`_. It is
an Open Source license (though not explicitly endorsed by the Open Source
Initiative).

Prerequisites
=============

We're using :manual:`PHP <lang-php>` in the stable version 8:

.. code-block:: console

 [isabell@stardust ~]$ uberspace tools version show php
 Using 'PHP' version: '8.0'
 [isabell@stardust ~]$

Installation
============

export PHP Path
---------------

.. code-block:: console

 [isabell@stardust ~]$ export PATH="/opt/remi/php80/root/bin:$PATH"

Create install directory
------------------------

.. code-block:: console

 [isabell@stardust ~]$ mkdir -p $HOME/lib/php/modules
 [isabell@stardust ~]$ cd $(mktemp --directory --tmpdir xdebug.XXX)
 [isabell@stardust xdebug.wgZ]$

Download
--------

.. code-block:: console

 [isabell@stardust xdebug.wgZ]$ wget -qO- https://xdebug.org/files/xdebug-3.0.4.tgz |tar -zxvf -

Make PHP Module
---------------

.. code-block:: console

 [isabell@stardust xdebug.wgZ]$ cd xdebug-3.0.4
 [isabell@stardust xdebug-3.0.4]$ phpize && ./configure --prefix="$HOME" --enable-xdebug
 Configuring for:
 PHP Api Version:         20200930
 Zend Module Api No:      20200930
 Zend Extension Api No:   420200930
 checking for grep that handles long lines and -e... /usr/bin/grep
 ...
 [isabell@stardust xdebug-3.0.4]$ sed -i "s|/opt/remi/php80/root/usr/lib64/php/modules|$HOME/lib/php/modules|g" Makefile
 [isabell@stardust xdebug-3.0.4]$ make && make install
 Makefile:245: warning: overriding recipe for target 'test'
 Makefile:132: warning: ignoring old recipe for target 'test'
 /bin/sh /tmp/xdebug.tYY/xdebug-3.0.4/libtool --mode=compile cc -I. ...
 ...

Cleanup install directory
-------------------------

.. code-block:: console

 [isabell@stardust xdebug-3.0.4]$ cd && rm -rf /tmp/xdebug*
 [isabell@stardust ~]$

Configuration
=============

Configure PHP-Module
--------------------

.. code-block:: console

 [isabell@stardust xdebug-3.0.4]$ echo "zend_extension=$HOME/lib/php/modules/xdebug.so;" >> $HOME/etc/php.d/xdebug.ini
 [isabell@stardust xdebug-3.0.4]$ uberspace tools restart php

Finishing installation
======================

Configure PHP Settings
----------------------

Most features in Xdebug have to be opted in into. Each feature has a specific opt-in. For example to use the debugger you need to set xdebug.mode=debug in your configuration file.

Modify ``~/etc/php.d/xdebug.ini`` to your own individual needs.

.. code-block:: ini

 zend_extension=/home/isabell/lib/php/modules/xdebug.so;
 xdebug.mode=debug
 xdebug.client_host=123.123.123.123
 xdebug.client_port=9000

.. tip:: You need to reload PHP whenever you change your configuration files: ``uberspace tools restart php`` checks your configuration for sanity and restarts your PHP instance.

Tuning
======

Disable Xdebug for Production-Environment because it have a big impact on performance and can also disclose internal data.

Updates
=======

.. note:: Check the website_ regularly to stay informed about the newest version.


.. _website: https://xdebug.org/announcements

----

Tested with  Xdebug 3.0.4, Uberspace 7.10.0

.. author_list::
