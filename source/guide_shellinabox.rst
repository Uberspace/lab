.. highlight:: console

.. author:: lk3de <web-uberlab@lk3.de>

.. tag:: web
.. tag:: console
.. tag:: ssh
.. tag:: lang-c

.. sidebar:: About

  .. image:: _static/images/shellinabox.svg
      :align: center

##############
Shell In A Box
##############

.. tag_list::

_`Shell In A Box` emulates a terminal in your browser. It implements a web server that works with purely JavaScript and CSS across most modern web browsers. This is helpful if you are e.g. behind a corporate firewall that blocks port 22, which is usually used for :manual:`SSH <basics-ssh>` connections.

----

License
=======

Shell In A Box is released under the `GNU General Public License version 2`_.

Prerequisites
=============

Your page's URL needs to be set up:

.. include:: includes/web-domain-list.rst


Installation
============

Clone Github project
--------------------
Clone the *shellinabox* repository from Github_ into ``~/shellinabox`` and ``cd`` into the newly created directory:

.. code-block:: console

 [isabell@stardust ~]$ git clone https://github.com/shellinabox/shellinabox
 Cloning into 'shellinabox'...
 remote: Enumerating objects: 3073, done.
 remote: Total 3073 (delta 0), reused 0 (delta 0), pack-reused 3073
 Receiving objects: 100% (3073/3073), 4.31 MiB | 6.47 MiB/s, done.
 Resolving deltas: 100% (2418/2418), done.
 [isabell@stardust ~]$ cd ~/shellinabox
 [isabell@stardust shellinabox]$

Build executable
----------------
Run the *autotools*, afterwards build the application with ``configure`` followed by ``make``:

.. code-block:: console

 [isabell@stardust shellinabox]$ autoreconf --install
 [...]
 Makefile.am: installing './INSTALL'
 Makefile.am: installing './depcomp'
 [isabell@stardust shellinabox]$ ./configure --prefix=$HOME
 [...]
 config.status: creating Makefile
 config.status: creating config.h
 config.status: executing depfiles commands
 config.status: executing libtool commands
 [isabell@stardust shellinabox]$ make
 [...]
 make[1]: Leaving directory '/home/isabell/shellinabox'
 [isabell@stardust shellinabox]$ make install
 [...]
 make[1]: Leaving directory `/home/isabell/shellinabox'

This will create a new executable file named ``shellinaboxd`` (notice the *d* at the end of the filename) in your ``~/bin`` directory.

Configuration
=============

Configure web backend
---------------------
.. note:: *shellinabox* is running on port 4200 by default.
.. include:: includes/web-backend.rst

Setup daemon
------------
To run *shellinabox* as a daemon, create a new file ``~/etc/services.d/shellinabox.ini`` with the following content:

.. code-block:: ini

 [program:shellinabox]
 command=shellinaboxd --disable-ssl --verbose
 autostart=yes
 autorestart=yes

We are using two command-line options here:

  * ``--disable-ssl``: Disables the built-in SSL functionality, since this is already enforced by Uberspace's :manual:`HTTPS configuration <web-https>`
  * ``--verbose``: Enables verbose logging which helps troubleshooting (you can safely disable this if you want to)

.. warning: Don't try to run *shellinabox* with the ``--background`` command-line option, as this will confuse

You can find the full reference of command-line options on `Google Code`_.

Refresh supervisord
-------------------
.. include:: includes/supervisord.rst

Finishing installation
======================

Point your browser to https://isabell.uber.space/ (replace ``isabell`` with your username) and enjoy your new browser-based shell.

----

Acknowledgements
================
The icon is made by Freepik_ from Flaticon_.

.. _`GNU General Public License version 2`: https://github.com/shellinabox/shellinabox/blob/master/COPYING
.. _Github: https://github.com/shellinabox/shellinabox
.. _`Google Code`: https://code.google.com/archive/p/shellinabox/wikis/shellinaboxd_man.wiki
.. _Freepik: https://www.flaticon.com/authors/freepik
.. _Flaticon: https://www.flaticon.com/

----

Tested with shellinabox 2.20, Uberspace 7.6.1.2

.. author_list::
