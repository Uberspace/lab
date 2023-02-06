.. highlight:: console

.. author:: FM <git.fm@mmw9.de>

.. tag:: lang-go
.. tag:: database

.. sidebar:: Logo

  .. image:: _static/images/listmonk.png
      :align: center

########
listmonk
########

.. tag_list::

listmonk_ is a self-hosted newsletter and mailing list manager.

-----

.. note:: For this guide you should be familiar with the basic concepts of

    * :lab:`PostgreSQL <guide_postgresql>`
    * :manual:`domains <web-domains>`
    * :manual:`supervisord <daemons-supervisord>`

License
=======

listmonk is released under the AGPL v3 license.

Installation
============

Create the target directory:

.. code-block:: console

    [isabell@stardust ~]$ mkdir -p ~/opt/listmonk/
    [isabell@stardust ~]$

Jump into the new directory:

.. code-block:: console

    [isabell@stardust ~]$ cd ~/opt/listmonk/
    [isabell@stardust ~]$

.. note:: Please check the Github_ project page for the latest release and copy the archive download link named with listmonk_<version>_linux_amd64.

Download the archive file:

.. code-block:: console

    [isabell@stardust ~]$ wget https://github.com/knadh/listmonk/releases/download/v2.0.0/listmonk_2.0.0_linux_amd64.tar.gz
    [isabell@stardust ~]$

Untar the archive file:

.. code-block:: console

    [isabell@stardust ~]$ tar -xzf listmonk_2.0.0_linux_amd64.tar.gz
    [isabell@stardust ~]$

Delete the archive file:

.. code-block:: console

    [isabell@stardust ~]$ rm listmonk_2.0.0_linux_amd64.tar.gz
    [isabell@stardust ~]$

Database Setup
==============

.. warning:: Your PostgreSQL database environment has to be setup as described in the Lab-Guide_ before you follow the next steps.

Create a new database user (in this example listmonk):

.. code-block:: console

    [isabell@stardust ~]$ createuser listmonk -P
    [isabell@stardust ~]$

Create a new database (in this example listmonk):

.. code-block:: console

    [isabell@stardust ~]$ createdb --encoding=UTF8 --owner=listmonk --template=template0 listmonk
    [isabell@stardust ~]$

.. tip:: Please write down your database info with: ``user``, ``password`` and ``database``.

Configuration
=============

listmonk configuration
----------------------

Jump into the listmonk directory:

.. code-block:: console

    [isabell@stardust ~]$ cd ~/opt/listmonk/
    [isabell@stardust ~]$

Generate the config file:

.. code-block:: console

    [isabell@stardust ~]$ ./listmonk --new-config
    [isabell@stardust ~]$

Edit the config file ``~/opt/listmonk/config.toml`` and change the predefined values of the admin user and database settings:

.. code-block:: console
    :emphasize-lines: 6,12,13,19,20,21

    [app]
    # Interface and port where the app will run its webserver.  The default value
    # of localhost will only listen to connections from the current machine. To
    # listen on all interfaces use '0.0.0.0'. To listen on the default web address
    # port, use port 80 (this will require running with elevated permissions).
    address = "0.0.0.0:9000"

    # BasicAuth authentication for the admin dashboard. This will eventually
    # be replaced with a better multi-user, role-based authentication system.
    # IMPORTANT: Leave both values empty to disable authentication on admin
    # only where an external authentication is already setup.
    admin_username = "listmonk"
    admin_password = "password"

    # Database.
    [db]
    host = "localhost"
    port = 5432
    user = "listmonk"
    password = "password"
    database = "listmonk"
    ssl_mode = "disable"
    max_open = 25
    max_idle = 25
    max_lifetime = "300s"

Create the database structure:

.. code-block:: bash

    [isabell@stardust ~]$ ./listmonk --install
    [isabell@stardust ~]$

Daemon setup
------------

Create ``~/etc/services.d/listmonk.ini`` with the following content:

.. code-block:: ini

    [program:listmonk]
    command=%(ENV_HOME)s/opt/listmonk/listmonk --config %(ENV_HOME)s/opt/listmonk/config.toml
    autostart=yes
    autorestart=yes

.. include:: includes/supervisord.rst

If it's not in state ``RUNNING``, check your configuration.

Webserver setup
----------------

.. note::

    listmonk is running on port 9000.

.. include:: includes/web-backend.rst

Updates
=======

Check the project page on Github_ for new releases. The update approach is similar to the standard installation.

Stop the daemon:

.. code-block:: console

    [isabell@stardust ~]$ supervisorctl stop listmonk
    [isabell@stardust ~]$

Jump into the listmonk directory:

.. code-block:: console

    [isabell@stardust ~]$ cd ~/opt/listmonk/
    [isabell@stardust ~]$

Download the new archive file:

.. code-block:: console

    [isabell@stardust ~]$ wget https://github.com/knadh/listmonk/releases/download/<version>/listmonk_<version>_linux_amd64.tar.gz
    [isabell@stardust ~]$

Rename your existing file-version:

.. code-block:: console

    [isabell@stardust ~]$ mv listmonk listmonk-old
    [isabell@stardust ~]$

Untar the archive file:

.. code-block:: console

    [isabell@stardust ~]$ tar -xzf listmonk_<version>_linux_amd64.tar.gz
    [isabell@stardust ~]$

Delete the archive file:

.. code-block:: console

    [isabell@stardust ~]$ rm listmonk_<version>_linux_amd64.tar.gz
    [isabell@stardust ~]$

And make the binary file executable:

.. code-block:: console

    [isabell@stardust ~]$ chmod +x listmonk
    [isabell@stardust ~]$

Start the update process:

.. code-block:: console

    [isabell@stardust ~]$ ./listmonk --upgrade
    [isabell@stardust ~]$

And start the daemon:

.. code-block:: console

    [isabell@stardust ~]$ supervisorctl start listmonk
    [isabell@stardust ~]$

In case of no problems you can delete your old version:

.. code-block:: console

    [isabell@stardust ~]$ rm listmonk-old
    [isabell@stardust ~]$

----

.. _listmonk: https://github.com/knadh/listmonk
.. _Github: https://github.com/knadh/listmonk/releases
.. _Lab-Guide: https://lab.uberspace.de/guide_postgresql.html

Tested with listmonk 2.0.0 on Uberspace 7.11.5 with PostgreSQL 13

.. author_list::
