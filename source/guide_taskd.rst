.. highlight:: console

.. author:: seeq

.. tag:: lang-cpp
.. tag:: lang-python
.. tag:: activity-tracking
.. tag:: console
.. tag:: sync

.. sidebar:: Logo

  .. image:: _static/images/taskwarrior.png
      :align: center

########
Taskd
########

.. tag_list::

.. abstract::
  Taskd_ is a free and open-source Taskwarrior server for synchronization between multiple Taskwarrior clients.
  Taskwarrior is free and Open Source Software that manages your TODO list from the command line. It is flexible, fast, and unobtrusive. It does its job then gets out of your way.

  * Multiple clients
  * TLS secured
  * Android-App available (also in FDroid)
  * MIT-licensed free software.

----

.. note:: For this guide you should be familiar with the basic concepts of

  * :manual:`supervisord <daemons-supervisord>`
  * :manual:`domains <web-domains>`
  * The taskwarrior application which is available in almost all packet managers. On Android look for the taskwarrior app (also available at FDroid).

.. note:: Take care as this guide switches between your local machine (indicated by isabell@local) and your uberspace (isabell@stardust).

Prerequisites
=============

Before you sync anything, make a backup of your local task data. You never know what might happen.
::

 [isabell@local ~]$ cd ~/.task/
 [isabell@local .task]$ tar czf ~/task-backup-$(date +'%Y%m%d').tar.gz *
 [isabell@local .task]$

Move this file somewhere safe, it was created in your local home directory.

Now switch to your uberspace account.

Your taskd domain needs to be setup:

.. include:: includes/web-domain-list.rst

Taskd listens on a port (by default ``53589``). We need to open a port in the firewall that our client can connect to the task server.

::

 [isabell@stardust ~]$ uberspace port add
 Port 40200 will be open for TCP and UDP treffic in a few minutes.
 [isabell@stardust ~]$

.. note:: Remember this opened port, you'll need it in the following configuration. Always replace the example port 40200 in the following.

We need a directory where the taskd files are stored.
::

 [isabell@stardust ~]$ export TASKDDATA=~/.var/taskddata
 [isabell@stardust ~]$ mkdir -p $TASKDDATA
 [isabell@stardust ~]$

The ``$TASKDDATA`` environment variable is expected by the taskdctl binary we are going to install now.


Installation
============


Download Sources
----------------

Download the latest version and build it.

.. code-block:: console

  [isabell@stardust ~]$ curl -LO https://taskwarrior.org/download/taskd-1.1.0.tar.gz
  ...
  [isabell@stardust ~]$ tar xzf taskd-1.1.0.tar.gz
  [isabell@stardust ~]$ cd taskd-1.1.0
  [isabell@stardust ~]$ cmake -DCMAKE_BUILD_TYPE=release .
  ...
  [isabell@stardust ~]$ make
  ...
  [isabell@stardust ~]$

Now install the required taskd binaries ...
::

 [isabell@stardust ~]$ cp ~/taskd-1.1.0/src/taskd ~/bin
 [isabell@stardust ~]$ cp ~/taskd-1.1.0/src/taskdctl ~/bin
 [isabell@stardust ~]$

... and verify the installation:
::

 [isabell@stardust ~]$ taskd -v

 taskd 1.1.0 built for linux
 Copyright (C) 2010 - 2015 Göteborg Bit Factory.
 ...
 [isabell@stardust ~]$ taskdctl status
 /home/isabell/bin/taskdctl status: daemon not running
 [isabell@stardust ~]$


Configuration
=============

Initialization of taskd
-----------------------
::

 [isabell@stardust ~]$ taskd init
 You must specify the 'server' variable, for example:
 taskd config server localhost:53589

 Created /home/isabell/.var/taskddata/config

 [isabell@stardust ~]$

Create Server PKI Certificates and key
--------------------------------------

The taskd bundles scripts for generating required keys and certificates for everything in the pki directory. We can set all required information in the vars file. But first we follow the recommended step and copy the pki directory to the ``$TASKDDATA`` directory so we have everything in one place.
::

 [isabell@stardust ~]$ cp -r ~/taskd-1.1.0/pki $TASKDDATA
 [isabell@stardust ~]$ cd $TASKDDATA/pki
 [isabell@stardust ~]$

Now edit the vars file in ``$TASKDDATA/pki/vars`` as required. Set the domain to be used as CN.

.. note:: This leads to certificates being valid for one year. After this time you need to manually renew all certificates. These are not automatically updated.

.. code-block:: ini

 BITS=4096
 EXPIRATION_DAYS=365
 ORGANIZATION="isabellorganization"
 CN=isabell.uber.space
 COUNTRY=DE
 STATE="Saxony"
 LOCALITY="Dresden"

Note: Make sure the CN matches the domain you are going to use for synchronization! Taskwarrior clients are strict with that if you do not switch off certificate checking.


::

 [isabell@stardust ~]$ ./generate
 ...
 [isabell@stardust ~]$


Note that the ``client.*`` files are not used for the clients connecting to the server! We will generate corresponding files in the next section. The client files here are for the API.
But first we move the required files to the ``$TASKDDATA`` directory:
::

 [isabell@stardust ~]$ cp client.cert.pem $TASKDDATA
 [isabell@stardust ~]$ cp client.key.pem  $TASKDDATA
 [isabell@stardust ~]$ cp server.cert.pem $TASKDDATA
 [isabell@stardust ~]$ cp server.key.pem  $TASKDDATA
 [isabell@stardust ~]$ cp server.crl.pem  $TASKDDATA
 [isabell@stardust ~]$ cp ca.cert.pem     $TASKDDATA
 [isabell@stardust ~]$


Configure the server
--------------------

Make the crypto files known to the server:
::

 [isabell@stardust ~]$ taskd config --force client.cert $TASKDDATA/client.cert.pem
 [isabell@stardust ~]$ taskd config --force client.key  $TASKDDATA/client.key.pem
 [isabell@stardust ~]$ taskd config --force server.cert $TASKDDATA/server.cert.pem
 [isabell@stardust ~]$ taskd config --force server.key  $TASKDDATA/server.key.pem
 [isabell@stardust ~]$ taskd config --force server.crl  $TASKDDATA/server.crl.pem
 [isabell@stardust ~]$ taskd config --force ca.cert     $TASKDDATA/ca.cert.pem
 [isabell@stardust ~]$

Configure the rest. Insert the port number you've opened at the beginning.
::

 [isabell@stardust ~]$ cd $TASKDDATA/
 [isabell@stardust ~]$ taskd config --force log ~/logs/taskd.log
 [isabell@stardust ~]$ taskd config --force pid.file $TASKDDATA/taskd.pid
 [isabell@stardust ~]$ taskd config --force server 0.0.0.0:40200

 $ taskd config
 ....
 [isabell@stardust ~]$


Setup daemon
------------

Create a file ``~/etc/services.d/taskd.ini`` and put the following in it:

.. code-block:: ini

  [program:taskd]
  command=taskd server --data %(ENV_HOME)s/.var/taskddata

.. include:: includes/supervisord.rst

If it's not in state RUNNING, check your logs.


Setup Clients
-------------------------------------
Clients are gathered in organizations. In general one organization will suffice (in our case we call it "Public"). But if you want to big feel free to add more.
::

 [isabell@stardust ~]$ taskd add org Public
 Created organization 'Public'
 [isabell@stardust ~]$

Now add as many users as you like. Spaces are ok as long you quote the name.

::

 [isabell@stardust ~]$ taskd add user 'Public' 'Isabell Smith'
 New user key: cf31f287-ee9e-43a8-843e-e8bbd5de4294
 Created user 'First Last' for organization 'Public'
 [isabell@stardust ~]$

Remember the user key! This identifies the user (as the name is not necessary unique).
Let's put this information in a file just to make things easier especially on Android where you can then copy paste the information. Create a file ``$TASKDDATA/pki/Isabell_task_info`` and put this in:

::

 org Public
 key cf31f287-ee9e-43a8-843e-e8bbd5de4294
 name Isabell Smith
 server isabell.uber.space:40200



Generate Client Certificates and Keys
-------------------------------------
As we have a user, we need a key and a cert. The correctness of the name is not important. It is only used for the output file names and ignored in authentication.
::

 [isabell@stardust ~]$ cd $TASKDDATA/pki
 [isabell@stardust ~]$ ./generate.client Isabell_Smith
 ...
 [isabell@stardust ~]$

We now have two file more in the directory:
::

 Isabell_Smith.cert.pem
 Isabell_Smith.key.pem


For every new user the steps to take are:

* Generate an ID (see 'Setup Clients')
* Generate key and cert

Configuring the Client
----------------------

Now Isabell wants to sync her devices. Get all four files to the .task directory at her local devices. These commands are executed on your local machine again:
::

 [isabell@local ~]$ scp isabell@stardust.uberspace.de:~/.var/taskddata/pki/ca.cert.pem ~/.task/
 [isabell@local ~]$ scp isabell@stardust.uberspace.de:~/.var/taskddata/pki/Isabell_Smith.cert.pem ~/.task/
 [isabell@local ~]$ scp isabell@stardust.uberspace.de:~/.var/taskddata/pki/Isabell_Smith.key.pem ~/.task/
 [isabell@local ~]$ scp isabell@stardust.uberspace.de:~/.var/taskddata/pki/Isabell_task_info ~/.task/
 [isabell@local ~]$


Now configure taskwarrior. Update the values according to your settings.
::

 [isabell@local ~]$ task config taskd.certificate -- ~/.task/Isabell_Smith.cert.pem
 Are you sure you want to add 'taskd.certificate' with a value of '/home/isabell/.task/Isabell_Smith.cert.pem'? (yes/no) y
 Config file /home/isabell/.taskrc modified.
 [isabell@local ~]$ task config taskd.key -- ~/.task/Isabell_Smith.key.pem
 (...)
 [isabell@local ~]$ task config taskd.ca -- ~/.task/ca.cert.pem
 (...)
 [isabell@local ~]$ task config taskd.server -- isabell.uber.space:40200
 (...)
 [isabell@local ~]$ task config taskd.credentials -- Public/Isabell Smith/cf31f287-ee9e-43a8-843e-e8bbd5de4294
 (...)
 [isabell@local ~]$


Configure Android (optional)
............................
Edit the configuration on Android in settings in the menu and add some lines (of course adopt the respective fields like the port of your server and the user-id). Also it may be necessary to escape slashes.

::

 taskd.server=isabell.uber.space:40200
 taskd.credentials=Public\/isabell smith\/a472ac30-137d-4a6f-aee1-7da6ca10c8da
 taskd.certificate=\/home\/you\/.task\/isabell_smith.cert.pem
 taskd.key=\/path\/to\/isabell_smith.key.pem
 taskd.ca=\/home\/you\/.task\/ca.cert.pem



Sync your tasks
===============

Initial sync (upload current task status):
::

 [isabell@local ~]$ task sync init
 Please confirm that you wish to upload all your pending tasks to the Task Server (yes/no) yes
 Syncing with isabell.uber.space:40200 Sync successful.  2 changes uploaded.
 [isabell@local ~]$


After that you can always sync your tasks by. If you run it directly you get the following as you haven't changed any task.
::

 [isabell@local ~]$ task sync
 Syncing with isabell.uber.space:40200

 Sync successful.  No changes.
 [isabell@local ~]$

.. note:: To sync your changes on the close of your shell you can use the following commands in your ``~/.bashrc.local`` (line 1) or for zsh in your ``~/.zshrc.local`` (line 2) respectively.


  .. code-block:: bash

	trap "task sync" exit   # does not work on zsh correctly
	zshexit() { task sync } # only zsh


.. note:: To automatically sync your changes on each action you might add the following to your ``~/.bashrc.local`` or ``~/.zshrc.local``:

	.. code-block:: bash

	 function tas() {
		task "$@"
		task sync
	  }

	Then from now on use taskwarrior like this:
	::

	 [isabell@local ~]$ tas add write guide for uberlab prio:M due:3d
	 [isabell@local ~]$



Updates
=======

To update taskd, repeat the Installation steps followed by a restart using ``supervisorctl restart taskd``. Periodically check the changelog_ to learn about new versions.

.. _changelog: https://github.com/GothenburgBitFactory/taskserver/blob/master/ChangeLog
.. _Taskd: https://taskwarrior.org/

----

Tested with taskd 1.1.0, Uberspace 7.7.9.0

.. author_list::
