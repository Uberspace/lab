.. highlight:: console

.. author:: Kim Diallo  <mail@diallo.kim>

.. tag:: lang-nodejs
.. tag:: audience-admins
.. tag:: web
.. tag:: console

.. sidebar:: Logo

  .. image:: _static/images/olivetin.png
      :align: center

##########
OliveTin
##########

.. tag_list::

OliveTin gives safe and simple access to predefined shell commands from a web interface.

----

.. note:: For this guide you should be familiar with the uberspace basic concepts of

  * supervisord_
  * domains_
  * `web backends`_

License
=======

OliveTin is released under the `AGPL-3.0 License`_.


Installation
============

Download OliveTin
------------------

Check Github_ for the `latest release`_ and copy the download link to the linux-amd64.tar.gz file.

.. code-block:: console

 [isabell@stardust ~]$ wget --quiet https://github.com/OliveTin/OliveTin/releases/download/2022-04-07/OliveTin-2022-04-07-linux-amd64.tar.gz --output-document ~/olivetin.tar.gz
 [isabell@stardust ~]$


Extract OliveTin
--------------------------

Create a directory and unpack the archive into it.

.. code-block:: console

 [isabell@stardust ~]$ mkdir ~/OliveTin
 [isabell@stardust ~]$ tar -zxf olivetin.tar.gz --directory=$HOME/OliveTin --strip-components 1
 [isabell@stardust ~]$


Cleaning up
-----------

.. code-block:: console

 [isabell@stardust ~]$ rm olivetin.tar.gz
 [isabell@stardust ~]$


Configuration
=============

Configure OliveTin
------------------

Create a directory for the config file and copy the ``~/OliveTin/config.yaml`` into it.

.. code-block:: ini

 [isabell@stardust ~]$ mkdir ~/etc/OliveTin
 [isabell@stardust ~]$ cp ~/OliveTin/config.yaml ~/etc/OliveTin/config.yaml

Now you can add scripts and shell commands in '~/etc/OliveTin/config.yaml' which should be executed via the web interface. Use the examples in the file and the configdoc_ for orientation.

Setup daemon
------------

Use your favourite editor to create ``~/etc/services.d/olivetin.ini`` with the following content:

.. code-block:: ini

 [program:olivetin]
 directory=%(ENV_HOME)s/OliveTin
 command=%(ENV_HOME)s/OliveTin/OliveTin --configdir %(ENV_HOME)s/etc/OliveTin
 autostart=yes
 autorestart=yes

.. include:: includes/supervisord.rst

If it’s not in state RUNNING, check your configuration.

Configure web backend
---------------------

.. note::

    OliveTin is running on port 1337 in the default configuration. If you want or need to use another port, you can change that in the ``~/OliveTin/config.yaml``..

.. include:: includes/web-backend.rst


Updates
=======

Periodically check the releases page_ to learn about new versions.

To update OliveTin, stop the daemon:

.. code-block:: console

 [isabell@stardust ~]$ supervisorctl stop olivetin
 olivetin: stopped
 [isabell@stardust ~]$

Rename the OliveTRin directory:

.. code-block:: console

 [isabell@stardust ~]$ mv OliveTin old_OliveTin

Now repeat the Installation steps followed by a restart using ``supervisorctl start olivetin``.

When the daemon regains RUNNING status, you can now dispose of the old directory:

.. code-block:: console

 [isabell@stardust ~]$ rm -r ~/old_OliveTin
 [isabell@stardust ~]$

.. _Github: https://github.com/OliveTin/OliveTin
.. _Revised BSD license: https://github.com/OliveTin/OliveTin/blob/main/LICENSE
.. _documentation: https://docs.olivetin.app
.. _configdoc: https://docs.olivetin.app/config.html#config
.. _releases page: https://github.com/OliveTin/OliveTin/releases

----

Tested with OliveTin 2022-04-07, Uberspace 7.12.2

.. author_list::
