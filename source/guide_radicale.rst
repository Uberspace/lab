.. highlight:: console
.. author:: stunkymonkey <http://stunkymonkey.de>
.. tag:: lang-python
.. tag:: web
.. tag:: groupware
.. tag:: sync

.. sidebar:: Logo

  .. image:: _static/images/radicale.svg
      :align: center

########
Radicale
########

.. tag_list::

Radicale_ is a Free and Open-Source CalDAV and CardDAV Server.

* Shares calendars through CalDAV, WebDAV and HTTP.
* Shares contacts through CardDAV, WebDAV and HTTP.
* Supports events, todos, journal entries and business cards.
* Works out-of-the-box, no installation nor configuration required.
* Can warn users on concurrent editing.
* Can limit access by authentication.
* Can secure connections.
* Works with many CalDAV and CardDAV clients.
* Is GPLv3-licensed free software.


----

.. note:: For this guide you should be familiar with the basic concepts of

  * :manual:`Python <lang-python>`
  * :manual:`supervisord <daemons-supervisord>`
  * :manual:`domains <web-domains>`


Prerequisites
=============

Your radicale URL needs to be setup:

.. include:: includes/web-domain-list.rst

The configuration directory needs to be created:

::

 [isabell@stardust ~] mkdir -p ~/.config/radicale/

Installation
============


Download Sources
----------------

download the latest version and install bcrypt for storing hashed passwords.

.. code-block:: console

  [isabell@stardust ~]$ python3.9 -m pip install --user --upgrade radicale bcrypt passlib
  Collecting radicale
    Downloading Radicale-3.1.8-py3-none-any.whl (138 kB)
       ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━ 138.1/138.1 KB 12.8 MB/s eta 0:00:00
  Collecting bcrypt
    Downloading bcrypt-4.0.0-cp36-abi3-manylinux_2_17_x86_64.manylinux2014_x86_64.whl (594 kB)
       ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━ 594.1/594.1 KB 26.9 MB/s eta 0:00:00
  Collecting passlib
    Downloading passlib-1.7.4-py2.py3-none-any.whl (525 kB)
       ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━ 525.6/525.6 KB 52.0 MB/s eta 0:00:00
  Collecting defusedxml
    Downloading defusedxml-0.7.1-py2.py3-none-any.whl (25 kB)
  Collecting python-dateutil>=2.7.3
    Downloading python_dateutil-2.8.2-py2.py3-none-any.whl (247 kB)
       ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━ 247.7/247.7 KB 38.0 MB/s eta 0:00:00
  Collecting vobject>=0.9.6
    Downloading vobject-0.9.6.1.tar.gz (58 kB)
       ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━ 58.6/58.6 KB 12.0 MB/s eta 0:00:00
    Preparing metadata (setup.py) ... done
  Collecting six>=1.5
    Downloading six-1.16.0-py2.py3-none-any.whl (11 kB)
  Using legacy 'setup.py install' for vobject, since package 'wheel' is not installed.
  Installing collected packages: passlib, six, defusedxml, bcrypt, python-dateutil, vobject, radicale
    Running setup.py install for vobject ... done
  Successfully installed bcrypt-4.0.0 defusedxml-0.7.1 passlib-1.7.4 python-dateutil-2.8.2 radicale-3.1.8 six-1.16.0 vobject-0.9.6.1
  WARNING: You are using pip version 22.0.4; however, version 22.2.2 is available.
  You should consider upgrading via the '/bin/python3.9 -m pip install --upgrade pip' command.
  ...
  [isabell@stardust ~]$

Configuration
=============


Create config files
-------------------

Save the following as your radicale configuration in ``~/.config/radicale/config``.

.. code-block:: ini
  :emphasize-lines: 2,6

  [server]
  hosts = 0.0.0.0:8000

  [auth]
  type = htpasswd
  htpasswd_filename = /var/www/virtual/<username>/htpasswd
  htpasswd_encryption = bcrypt

  [storage]
  filesystem_folder = ~/.var/lib/radicale/collections

For a more detailed configuration look `here <Config_>`_.


Setup daemon
------------

Create a file ``~/etc/services.d/radicale.ini`` and put the following in it:

.. code-block:: ini

  [program:radicale]
  command=radicale


Finishing installation
======================



Add a user
----------

For the generation of the file with the user use this command:

.. code-block:: console

  [isabell@stardust ~]$ htpasswd -B -c /var/www/virtual/$USER/htpasswd isabell
  New password:
  Re-type new password:
  [isabell@stardust ~]$

It will prompt you for a password now.

For every following user use it without ``-c``:

.. code-block:: console

  [isabell@stardust ~]$ htpasswd -B /var/www/virtual/$USER/htpasswd isabell
  New password:
  Re-type new password:
  [isabell@stardust ~]$


Configure web server
--------------------

In order for your Radicale instance to be reachable from the web, you need to connect it to the uberspace frontend using a web backend (:manual:`web backends <web-backends>`):

.. code-block:: console

  [isabell@stardust ~]$ uberspace web backend set / --http --port 8000
  Set backend for / to port 8000; please make sure something is listening!
  You can always check the status of your backend using "uberspace web backend list".
  [isabell@stardust ~]$ uberspace web backend list
  / http:8000 => OK, listening: PID 9947, /usr/bin/python3 /home/isabell/.local/bin/radicale


Start Service
-------------

.. include:: includes/supervisord.rst

And you're done!


Updates
=======
.. note:: Check the changelog_ regularly to stay informed about new updates and releases.

.. code-block:: console

  [isabell@stardust ~]$ python3 -m pip install --user --upgrade radicale
  [isabell@stardust ~]$ supervisorctl restart radicale
  radicale: stopped
  radicale: started
  [isabell@stardust ~]$

.. _Radicale: https://radicale.org/
.. _Changelog: https://github.com/Kozea/Radicale/releases/
.. _Config: https://radicale.org/3.0.html#documentation

----

Tested with Radicale 3.0.6, Uberspace 7.11.1

.. author_list::
