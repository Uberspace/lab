.. _upgrade_node_apps:

#####
Dealing with applications when upgrading the node.js version
#####

.. warning:: First, please check the source of the application to see if there is a separate guide for this case and follow it if so.

.. note::

  The following steps assume that the application is installed account-wide, not in a separate directory,
  so npm is called with the flag ``--global``. If your application is installed to a specific
  directory, omit the ``--global`` from the following steps and enter your application's directory
  before running the npm commands.

Upgrade Node.js App
================

Preparation
-----------

If your application runs as a service, stop it:

.. code-block:: console

  [isabell@stardust ~]$ supervisorctl stop <app>
  <app>: stopped
  [isabell@stardust ~]$



Now the application including all packages should be updated to the latest version.

.. code-block:: console

 [isabell@stardust ~]$ npm --global update
 ...
 added 2 packages and updated 9 packages in 10.521s
 [isabell@stardust ~]$



Perform Upgrades
--------------------------

Set the new node.js version:

.. code-block:: console

 [isabell@stardust ~]$ uberspace tools version use node <xy>
 Selected node version <xy>
 The new configuration is adapted immediately. Patch updates will be applied automatically.
 [isabell@stardust ~]$


Under the new version all installed packages should be rebuilt once:

.. code-block:: console

 [isabell@stardust ~]$ npm rebuild --global
 rebuilt dependencies successfully
 [isabell@stardust ~]$


And then be provided with the available updates for the new version:

.. code-block:: console

 [isabell@stardust ~]$ npm update --global
 ...
 added 9 packages and updated 22 packages in 33.211s
 [isabell@stardust ~]$


Restart Service
--------------------------

Now you can start the service again:

.. code-block:: console

  [isabell@stardust ~]$ supervisorctl start <app>
  <app>: started
  [isabell@stardust ~]$
