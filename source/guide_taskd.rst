.. highlight:: console

.. author:: seeq

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

Taskd_ is a Free and Open-Source Taskwarrior Server for synchronization between multiple Taskwarrior clients.
Taskwarrior is Free and Open Source Software that manages your TODO list from the command line. It is flexible, fast, and unobtrusive. It does its job then gets out of your way. 

* Multiple clients
* TLS secured
* Andorid App available (also in FDroid)
* Is MIT-licensed free software.

.. _Taskd: https://taskwarrior.org/

----

.. note:: For this guide you should be familiar with the basic concepts of

  * :manual:`supervisord <daemons-supervisord>`
  * :manual:`domains <web-domains>`
  * The taskwarrior application which is available in almost all packet managers. On Android look for the taskwarrior app (also available at FDroid).

Prerequisites
=============

Before you sync anything, make a backup of your local task data. You never know what might happen.
::

 [isabell@othermachine ~]$ tar czf task-backup-$(date +'%Y%m%d').tar.gz *
 [isabell@othermachine ~]$

Move this file somewhere safe.

Your taskd domain needs to be setup:

.. include:: includes/web-domain-list.rst

Taskd listens on a port (by default ``53589``). We need to open a port in the firewall that our client can connect to the task server.

::

 [isabell@stardust ~]$ uberspace port add
 Port 40200 will be open for TCP and UDP treffic in a few minutes.
 [isabell@stardust ~]$

remember this port. To connect later, we'll also need to know the hostname:

::

 [isabell@stardust ~]$ hostname -f
 stardust.uberspace.de
 [isabell@stardust ~]$


We need a directory where the taskd files are stored.
::

 [isabell@stardust ~]$ export TASKDDATA=/home/isabell/.var/taskddata
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

Install Required taskd Binaries
-------------------------------
::

 [isabell@stardust ~]$ cp /home/isabell/taskd-1.1.0/src/taskd /home/isabell/bin
 [isabell@stardust ~]$ cp /home/isabell/taskd-1.1.0/src/taskdctl /home/isabell/bin
 [isabell@stardust ~]$

Verify installation:
::

 [isabell@stardust ~]$ taskd -v
 [isabell@stardust ~]$ taskdctl status
 /usr/local/bin/taskdctl status: daemon not running
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

The taskd bundles scripts for generating reuqired keys and certificates for everything in the pki directory. We can set all required information in the vars file. But first we follow the recommended step andy copy the pki directory to the TASKDDATA directory so we have everything in one place.
::

 [isabell@stardust ~]$ cp -r /home/isabell/taskd-1.1.0/pki $TASKDDATA
 [isabell@stardust ~]$ cd $TASKDDATA/pki
 [isabell@stardust ~]$

Now edit the vars file in $TASKDDATA/pki/vars as required. E.g.:

.. code-block:: ini

 BITS=4096
 EXPIRATION_DAYS=365
 ORGANIZATION="isabellorganization"
 CN=stardust.uberspace.de
 COUNTRY=DE
 STATE="Saxony"
 LOCALITY="Dresden"

Note: Make sure the CN matches the domain you are going to use for synchronization! Taskwarrior clients are strict with that if you do not switch off certificate checking.
In our case isabell.uber.space will not work and lead to a certificate error in the client. User whatever hostname -f yields!

::

 [isabell@stardust ~]$ ./generate
 ...
 [isabell@stardust ~]$


Note that the client.* files are not used for the clients connecting to the server! We will generate coresponding files in the next section. The client files here are for the API.
But first we move the required files to the TASKDDATA directory:
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

Configure the rest. Insert your firewall port here!
::

 [isabell@stardust ~]$ cd $TASKDDATA/
 [isabell@stardust ~]$ taskd config --force log $PWD/taskd.log
 [isabell@stardust ~]$ taskd config --force pid.file $PWD/taskd.pid
 [isabell@stardust ~]$ taskd config --force server 0.0.0.0:40200

 $ taskd config
 ....
 [isabell@stardust ~]$


Setup daemon
------------

Create a file ``~/etc/services.d/taskd.ini`` and put the following in it:

.. code-block:: ini

  [program:taskd]
  command=taskd server --data $(ENV_HOME)s/.var/taskddata

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

Remember the user key! This identifies the user (as the name is not neccessary unique).
Let's put this information in a file just to make things easier especially on Android where you can then copy paste the information. Create a file ``~/Isabell_task_info`` and put this in:

::

 org Public
 key cf31f287-ee9e-43a8-843e-e8bbd5de4294
 name Isabell Smith
 server stardust.uberspace.de:40200



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
* Genererate an ID (see 'Setup Clients')
* Generate key and cert

Configuring the Client
----------------------

Now Isabell wants to sync all her devices. Copy four files to all her divices:
::

 [isabell@othermachine ~]$ scp /home/isabell/.var/taskddata/pki/ca.cert.pem isabell@othermachine:~/.task/
 [isabell@othermachine ~]$ scp /home/isabell/.var/taskddata/pki/Isabell_Smith.cert.pem isabell@othermachine:~/.task/
 [isabell@othermachine ~]$ scp /home/isabell/.var/taskddata/pki/Isabell_Smith.key.pem isabell@othermachine:~/.task/
 [isabell@othermachine ~]$ scp /home/isabell/.var/taskddata/pki/Isabell_task_info isabell@othermachine:~/.task/
 [isabell@othermachine ~]$ 


On your linux machine configure taskwarrior
::

 [isabell@othermachine ~]$ task config taskd.certificate -- ~/.task/Isabell_Smith.cert.pem
 [isabell@othermachine ~]$ task config taskd.key -- ~/.task/Isabell_Smith.key.pem
 [isabell@othermachine ~]$ task config taskd.ca -- ~/.task/ca.cert.pem
 [isabell@othermachine ~]$ task config taskd.server      -- stardust.uberspace.de:40200
 [isabell@othermachine ~]$ task config taskd.credentials -- Public/Isabell Smith/cf31f287-ee9e-43a8-843e-e8bbd5de4294
 [isabell@othermachine ~]$ 


Android:
Edit the configuration on Android in settings in the menu and add some lines (of course adopt the respective fields like the port of your server and the user-id). Also it may be neccessary to escapt slashes.

::

 taskd.server=stardust.uberspace.de:40200 
 taskd.credentials=Public\/isabell smith\/a472ac30-137d-4a6f-aee1-7da6ca10c8da
 taskd.certificate=\/home\/you\/.task\/isabell_smith.cert.pem                              
 taskd.key=\/path\/to\/isabell_smith.key.pem                                       
 taskd.ca=\/home\/you\/.task\/ca.cert.pem                                                    



Sync
=====

Initial sync (upload current task status):
::

 [isabell@othermachine ~]$ task sync init
 Please confirm that you wish to upload all your pending tasks to the Task Server (yes/no) yes
 Syncing with stardust.uberspace.de:40200 Sync successful.  2 changes uploaded.


After that:
::

 [isabell@othermachine ~]$ task sync
 [isabell@othermachine ~]$ 

Hint:
I added a function to my ~/.bashrc:

::

 function tas() {
 	task "$@"
 	task sync
  }

Then from now on use like this:
::

 [isabell@othermachine ~]$ tas add write guide for uberlab prio:M due:3d
 [isabell@othermachine ~]$ 


Updates
=======

To update taskd, repeat the Installation steps followed by a restart using ``supervisorctl restart taskd``. Periodically check the changelog_ to learn about new versions.

.. _changelog: https://github.com/GothenburgBitFactory/taskserver/blob/master/ChangeLog

.. author_list:: seeq
