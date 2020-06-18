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

  [isabell@stardust ~]$ python3 -m pip install --user --upgrade radicale bcrypt passlib
  Collecting radicale
  Using cached https://files.pythonhosted.org/packages/be/50/b5094950d53f11e56eb17932469e0e313275da0c5e633590c939863f3c37/Radicale-2.1.11.tar.gz
  Requirement already up-to-date: bcrypt in ./.local/lib/python3.4/site-packages
  Requirement already up-to-date: vobject>=0.9.6 in ./.local/lib/python3.4/site-packages (from radicale)
  Collecting python-dateutil>=2.7.3 (from radicale)
    Using cached https://files.pythonhosted.org/packages/74/68/d87d9b36af36f44254a8d512cbfc48369103a3b9e474be9bdfe536abfc45/python_dateutil-2.7.5-py2.py3-none-any.whl
  Requirement already up-to-date: six>=1.4.1 in ./.local/lib/python3.4/site-packages (from bcrypt)
  Requirement already up-to-date: cffi>=1.1 in ./.local/lib/python3.4/site-packages (from bcrypt)
  Collecting pycparser (from cffi>=1.1->bcrypt)
    Using cached https://files.pythonhosted.org/packages/68/9e/49196946aee219aead1290e00d1e7fdeab8567783e83e1b9ab5585e6206a/pycparser-2.19.tar.gz
  Installing collected packages: python-dateutil, radicale, pycparser
    Found existing installation: python-dateutil 2.7.3
      Uninstalling python-dateutil-2.7.3:
        Successfully uninstalled python-dateutil-2.7.3
    Found existing installation: Radicale 2.1.10
      Uninstalling Radicale-2.1.10:
        Successfully uninstalled Radicale-2.1.10
    Running setup.py install for radicale ... done
    Found existing installation: pycparser 2.18
      Uninstalling pycparser-2.18:
        Successfully uninstalled pycparser-2.18
    Running setup.py install for pycparser ... done
  Successfully installed pycparser-2.19 python-dateutil-2.7.5 radicale-2.1.11
  You are using pip version 9.0.1, however version 18.1 is available.
  You should consider upgrading via the 'pip install --upgrade pip' command.
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

In order for your Radicale instance to be reachable from the web, you need to put a file called ``.htaccess`` into your ``~/html`` folder (or any other DocumentRoot, see the :manual:`document root <web-documentroot>` for details), with the following content:

.. code-block:: ini
  :emphasize-lines: 3,9

  AuthType      Basic
  AuthName      "Radicale - Password Required"
  AuthUserFile  "/var/www/virtual/<username>/htpasswd"
  Require       valid-user

  DirectoryIndex disabled

  RewriteEngine On
  RewriteRule ^(.*) http://<username>.local.uberspace.de:8000/$1 [P]

Again, don't forget to fill in your username!


Start Service
-------------

.. include:: includes/supervisord.rst

And you're done!


Updates
=======
.. note:: Check the changelog_ regularly to stay informed about new updates and releases.

.. code-block:: console

  [isabell@stardust ~]$ python3 -m pip install --upgrade radicale
  [isabell@stardust ~]$ supervisorctl restart radicale
  radicale: stopped
  radicale: started
  [isabell@stardust ~]$

.. _Radicale: https://radicale.org/
.. _Changelog: https://github.com/Kozea/Radicale/releases/
.. _Config: https://radicale.org/3.0.html#documentation

----

Tested with Radicale 2.1.11, Uberspace 7.1.17

.. author_list::
