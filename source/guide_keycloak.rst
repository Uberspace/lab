.. highlight:: console

.. author:: Julius Künzel

.. tag:: web
.. tag:: sso

.. spelling::
    Keycloak

.. sidebar:: Logo

  .. image:: _static/images/keycloak.svg
      :align: center

########
Keycloak
########

.. tag_list::

Keycloak is an open source identity and access management system which allows single sign-on for web applications and services.

----

.. note:: For this guide you should be familiar with the basic concepts of

  * :manual:`supervisord <daemons-supervisord>`
  * :manual:`Backends <web-backends>`

License
=======

Keycloak is released under the `Apache 2.0 license`_.

Prerequisites
=============

Your URL needs to be setup:

.. include:: includes/web-domain-list.rst

Installation
============

Download Keycloak
-----------------

Check the Keycloak_ website or `Github Repository`_ for the latest release and copy the download link to the .tar.gz file. Then use ``wget`` to download it. Replace the URL with the one you just got from GitHub.

::

 [isabell@stardust ~]$ wget https://github.com/keycloak/keycloak/releases/download/15.0.2/keycloak-15.0.2.tar.gz
 […]
 Saving to: ‘keycloak-15.0.2.tar.gz’

 100%[======================================>] 253,994,058 51,5MB/s   in 4,8s

 2021-11-19 22:36:18 (50,7 MB/s) - ‘keycloak-15.0.2.tar.gz’ saved [253994058/253994058]
 [isabell@stardust ~]$

Extract the archive
-------------------

Use ``tar`` to extract the archive and delete the archive. Replace the version in the archive file name with the one you just downloaded.

::

 [isabell@stardust ~]$ tar -xvzf keycloak-15.0.2.tar.gz
 keycloak-15.0.2
 [isabell@stardust ~]$

You can now delete the archive:

::

 [isabell@stardust ~]$ rm keycloak-15.0.2.tar.gz
 [isabell@stardust ~]$

Configuration
=============

Change the configuration
------------------------

Find the following block in file :file:`standalone/configuration/standalone.xml` and add the ``proxy-address-forwarding="true"`` attribute to ``<http-listener>`` element under ``<server>``.

.. code-block:: xml
 :emphasize-lines: 4

 <subsystem xmlns="urn:jboss:domain:undertow:10.0" default-server="default-server" default-virtual-host="default-host" default-servlet-container="default" default-security-domain="other" statistics-enabled="${wildfly.undertow.statistics-enabled:${wildfly.statistics-enabled:false}}">
     <buffer-cache name="default"/>
     <server name="default-server">
         <http-listener name="default" socket-binding="http" redirect-socket="https" enable-http2="true" read-timeout="30000" proxy-address-forwarding="true"/>
         <https-listener name="https" socket-binding="https" security-realm="ApplicationRealm" enable-http2="true" read-timeout="30000"/>
         <host name="default-host" alias="localhost">
             <location name="/" handler="welcome-content"/>
             <http-invoker security-realm="ApplicationRealm"/>
         </host>
     </server>
     ...
 </subsystem>


Create an admin user
--------------------

Replace ``<username>`` with a user name of your choice and enter a password when your a asked to

.. code-block::
 :emphasize-lines: 2

 [isabell@stardust ~]$ cd ~/keycloak-15.0.2/bin
 [isabell@stardust keycloak-15.0.2]$ ./add-user-keycloak.sh -u <username>
 Press ctrl-d (Unix) or ctrl-z (Windows) to exit
 Password:
 [isabell@stardust keycloak-15.0.2]$

Setup daemon
------------

Use your favourite editor to create the file :file:`~/etc/services.d/keycloak.ini` with the following content. Replace the version in the archive file name with the one you just downloaded.

.. code-block:: ini
 :emphasize-lines: 2

 [program:keycloak]
 command=/home/smartlab/keycloak-15.0.2/bin/standalone.sh -b 0.0.0.0
 autostart=yes
 autorestart=yes

.. include:: includes/supervisord.rst



Setup Backend
-------------

.. note::

    Keycloak is running on port 8080.

.. include:: includes/web-backend.rst

Link Logs
---------

Since Keycloak writes logs to :file:`standalone/logs` we want to create a symlink to :file:`~/logs`:


::

 [isabell@stardust ~]$ ln -s ~/keycloak-15.0.2/standalone/log ~/logs/keycloak-15.02
 [isabell@stardust ~]$


Finishing installation
======================

Point your Browser to your installation URL ``https://isabell.uber.space`` and use Keycloak!

Tuning
======

For further information on configuration and usage go to https://www.keycloak.org/documentation.

Updates
=======

.. note:: Check the update feed_ regularly to stay informed about the newest version.

To update Keycloak install the new version as described under :lab_anchor:`Installation <guide_keycloak.html#installation>`, but without the configuration steps.

Migrate data
------------

Copy the :file:`standalone` directory from the previous installation over the directory in the new installation:

::

 [isabell@stardust ~]$ cp -r keycloak-12.0.0/standalone keycloak-15.0.2
 keycloak: stopped
 [isabell@stardust ~]$

You also need to copy any custom modules that have been added to the :file:`modules` directory in the same way.

For some versions manual migration steps are needed: https://www.keycloak.org/docs/latest/upgrading/index.html#migration-changes

Stop the process of the previous version
----------------------------------------


First stop the daemon:

::

 [isabell@stardust ~]$ supervisorctl stop keycloak
  keycloak: stopped
 [isabell@stardust ~]$

Unfortunately stopping the daemon is not enough so you need to identify the running Keycloak process. The command starts with ``java -D[Standalone]``.

.. code-block::
 :emphasize-lines: 4

 [isabell@stardust ~]$ ps aux
 USER       PID %CPU %MEM    VSZ   RSS TTY      STAT START   TIME COMMAND
 isabell   1138  0.0  0.0 219848 17536 ?        Ss   Nov02  11:40 /opt/uberspace/python-venv/bin/python /usr/bin/supervisord -c /etc/supervisord.conf
 isabell   1786  0.4  1.5 1659844 477116 ?      Sl   Nov02 116:23 java -D[Standalone] -server -Xms64m -Xmx512m -XX:MetaspaceSize=96M -XX:MaxMetaspaceSize=256m -Djava.net.preferIPv4Stack=true - Djboss.modules.system.pkgs=org.jboss.byteman
 isabell  23108  0.0  0.0 116912  3556 pts/6    Ss   22:25   0:00 -bash
 isabell  26803  0.0  0.0 155452  1844 pts/6    R+   23:18   0:00 ps aux
 isabell  32155  0.0  0.0 737800 27388 ?        Ss   Nov18   0:11 php-fpm: master process (/opt/uberspace/etc/smartlab/php-fpm.conf)
 [isabell@stardust ~]$

And kill the process. Replace ``PID`` by the PID identified in the previous step.

::

 [isabell@stardust ~]$ kill -SIGKILL PID
 [isabell@stardust ~]$

Run the upgrade script
----------------------

.. note:: If you are using a different configuration file than the default one, edit the migration script to specify the new file name.

Now run the script:

::

 [isabell@stardust ~]$ cd keycloak-15.0.2
 [isabell@stardust keycloak-15.0.2]$ bin/jboss-cli.sh --file=bin/migrate-standalone.cli
 *** WARNING ***

 ** If the following embed-server command fails, manual intervention is needed.
 ** In such case, remove any <extension> and <subsystem> declarations referring
 ** to the removed smallrye modules from the standalone.xml file and rerun this script.
 ** For details, see Migration Changes section in the Upgrading guide.
 ** We apologize for this inconvenience.

 *** Begin Migration ***
 [...]
 *** End Migration ***
 [isabell@stardust keycloak-15.0.2]$

Update and restart the daemon
-----------------------------

Edit :file:`~/etc/services.d/keycloak.ini` with your favourite editor to point to the directory of the new version.

After updating the configuration reread and start the daemon as described under :lab_anchor:`Setup daemon <guide_keycloak.html#setup-daemon>`.

Clean up
--------

Once you made sure had success and everything works as expected you can delete the previous version:

::

 [isabell@stardust ~]$ rm -r keycloak-12.0.0 logs/keycloak-15.02
 [isabell@stardust ~]$



.. _Keycloak: https://www.keycloak.org/downloads
.. _feed: https://github.com/keycloak/keycloak/releases.atom
.. _Apache 2.0 License: https://github.com/gohugoio/hugo/blob/master/LICENSE
.. _Github Repository: https://github.com/keycloak/keycloak/releases

----

Tested with Keycloak 15.0.2, Uberspace 7.11.5

.. author_list::
