.. highlight:: console

.. author:: Sebastian Burschel <https://github.com/SeBaBu/>

.. tag:: lang-python
.. tag:: web
.. tag:: file-storage
.. tag:: webdav

.. sidebar:: About

  .. image:: _static/images/wsgidav.png
      :align: center

############
WsgiDAV
############

.. tag_list::

A generic and extendable WebDAV server written in Python and based on WSGI. It can be used to share files between across your various devices or with friends.

----

.. note:: For this guide you should be familiar with the basic concepts of

  * :manual:`supervisord <daemons-supervisord>`
  * :manual:`domains <web-domains>`

License
=======

MIT license.

  * https://github.com/mar10/wsgidav/blob/master/LICENSE

Installation
============

Use pip3 to install wsgidav:

::

 [isabell@stardust ~]$ pip3 install wsgidav cheroot --user

Create the data folder:

::

 [isabell@stardust ~]$ mkdir ~/webdav


Add additional folders you want to access via webdav with:

::

 [isabell@stardust ~]$ mkdir ~/webdav/<newfoldername>

Config file
======================

.. note::

    Only use spaces to indent in the config file! No tabs!


We will modify this example config (YAML): https://wsgidav.readthedocs.io/en/latest/user_guide_configure.html#sample-wsgidav-yaml

Define which folder should be accessible:

::

 mount_path: null
 provider_mapping:
     "/": "/home/isabell/webdav/"
     "/firstpath": "/home/isabell/webdav/<newpath>"
 # Adds folder "/home/isabell/webdav/<newpath>" to URL https://isabell.uber.space/firstpath


Add user and password for every path:

::

 simple_dc:
     user_mapping:
         "*":  # default (used for all shares that are not explicitly listed). Keep this one!
             "isabell":
                 password: "<password>" # Change it!
                 roles: ["editor"]
         "/firstpath": # The mount_path this user has access to.
             "isabellscousin": # Username
                 password: "<password>" # Password. Change it!
 # You can add multiple users for every path.

Save the file here:

::

~/etc/wsgidav.yaml

Configure web server
====================

To make the web server available as a web backend you have to explicitly set the host ip address in the configuration file ``~/etc/wsgidav.yaml``.

::

host: 0.0.0.0

.. note::

    wsgidav is running on port 8080.

.. include:: includes/web-backend.rst

Configure ``supervisord``
=========================

Create ``~/etc/services.d/wsgidav.ini`` with the following content:

.. code-block:: ini

 [program:wsgidav]
 command=wsgidav -c %(ENV_HOME)s/etc/wsgidav.yaml
 directory = %(ENV_HOME)s/webdav
 autostart=yes
 autorestart=yes

Start Service
=============

.. include:: includes/supervisord.rst

Now go to ``https://<username>.uber.space`` (would be ``https://isabell.uber.space`` in our example) and see if it works. Enjoy!


----

Tested with wsgidav 3.1.0, Uberspace 7.8.1.0

.. author_list::
