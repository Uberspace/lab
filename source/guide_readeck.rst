.. highlight:: console

.. author:: no-one <https://github.com/no-one>

.. tag:: lang-go
.. tag:: read-later
.. tag:: reading-list

.. sidebar:: Logo

  .. image:: _static/images/readeck.png
      :align: center

#######
Readeck
#######

.. tag_list::

Readeck_ is an open source bookmark manager and a read later tool. It allows you to save the content of websites that you like and that you want to keep for as long as possible.

----

.. note:: For this guide you should be familiar with the basic concepts of

  * :manual:`supervisord <daemons-supervisord>`
  * :manual:`web backends <web-backends>`

License
=======

All relevant legal information can be found here:

  * https://codeberg.org/readeck/readeck/src/branch/main/LICENSE

Installation
============

Create a new directory, enter the directory you just created, download the latest version, rename the file and make the binary executable:

.. note:: Replace ``0.17.1`` with the version of the `latest release`_.

.. code-block:: console

 [isabell@stardust ~]$ mkdir ~/readeck
 [isabell@stardust ~]$ cd ~/readeck
 [isabell@stardust readeck]$ wget "https://codeberg.org/readeck/readeck/releases/download/0.17.1/readeck-0.17.1-linux-amd64"
 [isabell@stardust readeck]$ mv readeck-0.17.1-linux-amd64 readeck
 [isabell@stardust readeck]$ chmod +x readeck
 [isabell@stardust readeck]$

To create all the necessary files, you should start Readeck for a moment:
  
.. code-block:: console

 [isabell@stardust readeck]$ ./readeck serve
 INFO[0000] workers started
 INFO[0000] server started          url="http://localhost:8000/"

Now press ``Ctrl+C`` to stop it again:

.. code-block:: console
  
 ^CINFO[0174] shutting down...
 INFO[0174] stopping server...
 INFO[0174] server stopped
 INFO[0174] stopping workers...
 INFO[0174] workers stopped
 [isabell@stardust readeck]$

The directory ``data`` (with further content) and the file ``config.toml`` have now been created in the directory ``~/readeck``.
  
Configuration
=============

Configure Readeck
-----------------

.. note:: Visit the `official documentation`_ to see all available settings.

The following setting must be adjusted in the ``~/readeck/config.toml``:

::

 host = "0.0.0.0"

Just underneath that line, add

::

 use_x_forwarded_proto = true

As a lot of data is written to the log in the standard configuration, it may be sufficient to select a different setting here:

::

 log_level = "warn"

Readeck has a "forgot password" function, but this will only appear if the email section has been configured in the ``config.toml`` file. So if you want this, add the following:

.. warning:: Replace ``stardust`` with your hostname, ``isabell`` with your username and insert the correct values for ``username`` and ``password``!

::

 [email]
 host = "stardust.uberspace.de"
 port = 587
 username = "Your email address, including the domain"
 password = "Your password for the email address"
 encryption = "starttls"
 from = "isabell@uber.space"


Setup daemon
------------

Create ``~/etc/services.d/readeck.ini`` with the following content:

::

 [program:readeck]
 directory=%(ENV_HOME)s/readeck/
 command=%(ENV_HOME)s/readeck/readeck serve
 autostart=yes
 autorestart=yes
 startsecs=30
             
.. include:: includes/supervisord.rst

If it's not in state RUNNING, check your configuration.

Setup web backend
-----------------

.. note:: The default port for Readeck is ``8000``.

.. include:: includes/web-backend.rst

.. warning:: Replace ``isabell`` with your username!

If Readeck is running, you can now find the website at ``https://isabell.uber.space``.

Updates
=======

.. note:: Check the `Codeberg release page <latest release_>`_ regularly to stay informed about the newest version.

To update the software, download the latest version, replace the executable file and restart the daemon (``supervisorctl restart readeck``).

.. _Readeck: https://readeck.org
.. _latest release: https://codeberg.org/readeck/readeck/releases
.. _official documentation: https://readeck.org/en/docs/configuration

----

Tested with Readeck 0.17.1, Uberspace 7.16.4

.. author_list::
