.. highlight:: console

.. author:: lk3de <web-uberlab@lk3.de>

.. tag:: web
.. tag:: console
.. tag:: ssh

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

Your blog URL needs to be setup:

.. code-block:: console

 [isabell@stardust ~]$ uberspace web domain list
 isabell.uber.space
 [isabell@stardust ~]$

Installation
============

Clone Github project
-------------
Clone the shellinabox repository from Github_ into ``~/shellinabox`` and ``cd`` into the newly created directory:

.. code-block:: console

 [isabell@stardust ~]$ git clone https://github.com/shellinabox/shellinabox
 Cloning into 'shellinabox'...
 TODO here
 [isabell@stardust ~]$ cd ~/shellinabox
 [isabell@stardust ~/shellinabox]$
 TODO check this & paste code block
 
Build executable
----------------
Run the autotools, afterwards build the application with configure and make:

.. code-block:: console

 [isabell@stardust ~/shellinabox]$ autoreconf --install
 TODO output
 [isabell@stardust ~/shellinabox]$ ./configure
 TODO output
 [isabell@stardust ~/shellinabox]$ make
 TODO output
 [isabell@stardust ~/shellinabox]$

This will create a new executable file ``shellinaboxd`` in the same directory.

Configuration
=============

Open port
---------
.. include:: includes/open-port.rst

Configure web backend
---------------------
.. include:: includes/web-backend.rst

Setup daemon
------------
Create a new file ``~/etc/services.d/shellinabox.ini`` with the following content:

.. warning:: Replace ``isabell`` with your username and ``<port>`` with the port that you have opened in the firewall!

.. code-block:: ini

 [program:shellinabox]
 command=/home/isabell/shellinabox/shellinaboxd --background --disable-ssl --port <port> --verbose
 autostart=yes
 autorestart=yes

We are using a few command-line options here:

  * ``--background``: Tells shellinaboxd to run as daemon in the background
  * ``--disable-ssl``: Disables the built-in SSL function, since this is covered by the :manual:`web backend <web-backends>`
  * ``--port``: Overrides the default port with the one that you have opened in the firewall
  * ``--verbose``: Enables verbose logging which helps troubleshooting (can be safely disabled as well)
  
You can find the full reference on `Google Code`_.

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
.. _Flaticon: https://www.flaticon.com/
.. _Freepik: https://www.flaticon.com/authors/freepik

Tested with shellinabox 2.20, Uberspace TODO

.. author_list::
