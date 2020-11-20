.. highlight:: console

.. author:: Kevin Jost <https://github.com/systemsemaphore>

.. tag:: lang-go
.. tag:: web

.. sidebar:: Logo

  .. image:: _static/images/shiori.svg
      :align: center

######
Shiori
######

.. tag_list::

Shiori_ is a simple bookmarks manager written in Go and distributed under the MIT License. It can be used as a `command line application <https://github.com/go-shiori/shiori/wiki/Usage#using-command-line-interface>`_ or via the built-in web-ui.

----

.. note:: For this guide you should be familiar with the basic concepts of

  * :manual:`supervisord <daemons-supervisord>`
  * :manual:`web backends <web-backends>`

Prerequisites
=============

.. note:: Shiori won't work with a subpath (e.g. https://isabell.uber.space/shiori/).

By default, Shiori runs on port 8080.
To reach it, you need to configure a `web backend <webbackend_>`_.

::

  [isabell@stardust ~]$ uberspace web backend set / --http --port 8080
  Set backend for / to port 8080; please make sure something is listening!
  You can always check the status of your backend using "uberspace web backend list".
  [isabell@stardust ~]$

.. _webbackend: https://manual.uberspace.de/web-backends.html

Installation
============

Like a lot of Go software, Shiori is distributed as a single binary. Download Shiori's latest `release <https://github.com/go-shiori/shiori/releases/latest>`_ and make sure that the file can be executed.

::

  [isabell@stardust ~]$ mkdir ~/shiori && cd ~/shiori
  [isabell@stardust shiori]$ wget https://github.com/go-shiori/shiori/releases/download/v1.5.0/shiori-linux-amd64-stretch
  Resolving github.com (github.com)... 140.82.121.3
  Connecting to github.com (github.com)|140.82.121.3|:443... connected.
  HTTP request sent, awaiting response... 302 Found
  Length: 19735216 (19M) [application/octet-stream]
  Saving to: ‘shiori-linux-amd64-stretch’

 100%[======================================>] 19,735,216  12.2MB/s

  2020-11-11 22:04:39 (12.2 MB/s) - ‘shiori-linux-amd64-stretch’ saved [19735216/19735216]
  [isabell@stardust shiori~]$ chmod u+x shiori-linux-amd64-stretch
  [isabell@stardust shiori]$

Configuration
=============

Setup daemon
-----------

.. note:: To use a different port instead of 8080, you need to add ``-p <portnumber>`` to the command in your ``shiori.ini`` file. Remember to adjust the port for the web backend as well.

Create ``~/etc/services.d/shiori.ini`` with the following content.

.. code-block:: ini

  [program:shiori]
  command=/home/isabell/shiori/shiori-linux-amd64-stretch serve
  autostart=yes
  autorestart=yes

.. include:: includes/supervisord.rst

If it's not in state RUNNING, check your configuration.

Finishing installation
======================

The default user and password is ``shiori`` and ``gopher``.
Once logged in you will be able to use the web interface. To add a new account,
open the settings page and click on "Add new account".
With this, the default user will be deactivated automatically.

Updates
=======

.. note:: Check the update feed_ regularly to stay informed about the newest version.

Check Shiori's `releases <https://github.com/go-shiori/shiori/release>`_ for the latest version. If a newer
version is available, stop daemon by ``supervisorctl stop shiori`` and repeat the "Installation" step followed by ``supervisorctl start shiori`` to restart Shiori.

.. _Shiori: https://github.com/go-shiori/shiori#readme
.. _Documentation: https://github.com/go-shiori/shiori/tree/master/docs/
.. _feed: https://github.com/go-shiori/shiori/releases/
.. _Dashboard: https://uberspace.de/dashboard/authentication

----

Tested with Shiori 1.5.0, Uberspace 7.7.9.0

.. author_list::
