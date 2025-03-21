.. highlight:: console

.. author:: Julius Künzel
.. author:: Yannick Ihmels <yannick@ihmels.org>

.. tag:: web
.. tag:: sso
.. tag:: lang-java

.. spelling:word-list::
    Keycloak

.. sidebar:: Logo

  .. image:: _static/images/keycloak.svg
    :align: center

########
Keycloak
########

.. tag_list::

`Keycloak`_ is an open source identity and access management system which allows single sign-on for web applications and services.

----

.. note:: For this guide you should be familiar with the basic concepts of

  * :manual:`supervisord <daemons-supervisord>`
  * :manual:`Backends <web-backends>`

License
=======

Keycloak is released under the `Apache 2.0 license`_.

Prerequisites
=============

.. include:: includes/my-print-defaults.rst

You can use the domains that are currently configured:

.. include:: includes/web-domain-list.rst

If you want to use Keycloak with a domain not shown here, such as your own domain, :manual:`setup your domain <web-domains>` for use with your Asteroid.

Installation
============

Download
--------

Download the latest version of Keycloak release from the `GitHub release page`_:

::

  [isabell@stardust ~]$ curl -L https://github.com/keycloak/keycloak/releases/download/26.1.2/keycloak-26.1.2.tar.gz | tar -xzf -
    % Total    % Received % Xferd  Average Speed   Time    Time     Time  Current
                                   Dload  Upload   Total   Spent    Left  Speed
    0     0    0     0    0     0      0      0 --:--:-- --:--:-- --:--:--     0
  100  141M  100  141M    0     0  52.6M      0  0:00:02  0:00:02 --:--:-- 62.6M
  [isabell@stardust ~]$

Create symlink
--------------

Next create a symlink to point to the latest version:

::

  [isabell@stardust ~]$ ln -sfn ~/keycloak-26.1.2 ~/keycloak
  [isabell@stardust ~]$

Configuration
=============

Create database
---------------

Create a database for Keycloak:

.. code-block:: console

  [isabell@stardust ~]$ mysql --execute "CREATE DATABASE ${USER}_keycloak"
  [isabell@stardust ~]$

Configure Keycloak
------------------

Update the config file ``~/keycloak/conf/keycloak.conf`` with the following content:

.. note:: Replace ``isabell`` with your username and fill the database password ``db-password`` with yours.

.. code-block:: ini
  :emphasize-lines: 5,8,11,14

  # The database vendor.
  db=mariadb

  # The username of the database user.
  db-username=isabell

  # The password of the database user.
  db-password=MySuperSecretPassword

  # The full database JDBC URL. If not provided, a default URL is set based on the selected database vendor.
  db-url=jdbc:mariadb://localhost/isabell_keycloak

  # Hostname for the Keycloak server.
  hostname=isabell.uber.space

  # Enables the HTTP listener.
  http-enabled=true

  # The proxy headers that should be accepted by the server.
  proxy-headers=xforwarded

Create initial admin user
-------------------------

To create a temporary admin user, execute the following command:

::

  [isabell@stardust ~]$ ~/keycloak/bin/kc.sh bootstrap-admin user
  Changes detected in configuration. Updating the server image.
  Updating the configuration and installing your custom providers, if any. Please wait.

  [...]

  Enter username [temp-admin]:
  Enter password: [hidden]
  Enter password again: [hidden]

  [...]
  [isabell@stardust ~]$


This command will prompt for a username and a password.

.. warning:: The created admin user is temporary and should be replaced with a new user using the Administration Console.

Set up web backend
------------------

.. note::

    Keycloak will run on port 8080.

.. include:: includes/web-backend.rst

Set up daemon
-------------

Use your favourite editor to create the file :file:`~/etc/services.d/keycloak.ini` with the following content.

.. code-block:: ini

  [program:keycloak]
  command=%(ENV_HOME)s/keycloak/bin/kc.sh start
  autostart=yes
  autorestart=yes
  startsecs=60

.. include:: includes/supervisord.rst

You can check the service’s log file using ``supervisorctl tail -f keycloak``.


Finishing installation
======================

Point your browser to your installation URL ``https://isabell.uber.space`` and use Keycloak. As mentioned earlier, you should create a new admin user for the master realm and delete the temporary admin user afterwards.

Updates
=======

.. note:: Check the update feed_ regularly to stay informed about the newest version.

Before keycloak can be updated, it needs to be shutdown first:

::

 [isabell@stardust ~]$ supervisorctl stop keycloak
 [isabell@stardust ~]$

Next, install the new version as described in the :lab_anchor:`installation <guide_keycloak.html#installation>` chapter.

Then copy ``conf/``, ``providers/`` and ``themes/`` from the previous installation to the new installation.

Please have a look at the `Upgrading Guide`_ and perform any manual migration steps.

After that start Keyclock again:

::

 [isabell@stardust ~]$ supervisorctl start keycloak
 [isabell@stardust ~]$

Keycloak performs database migrations automatically.

.. _Keycloak: https://www.keycloak.org
.. _Apache 2.0 License: https://github.com/gohugoio/hugo/blob/master/LICENSE
.. _Github release page: https://github.com/keycloak/keycloak/releases
.. _feed: https://github.com/keycloak/keycloak/releases.atom
.. _Upgrading Guide: https://www.keycloak.org/docs/latest/upgrading/index.html

----

Tested with Keycloak 26.2.1, Uberspace 7.16.1

.. author_list::
