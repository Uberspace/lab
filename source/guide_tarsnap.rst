. highlight:: console

.. author:: Torsten Meyer <https://knodderdachs.de>

.. tag:: backup

.. sidebar:: Logo

  .. image:: _static/images/tarsnap.png
      :align: center

#######
Tarsnap
#######

.. tag_list::

Tarsnap is a secure online backup service for UNIX-like operating systems, including BSD, Linux, and OS X. It was created in 2008 by Colin Percival. Tarsnap encrypts data, and then stores it on Amazon S3.
The service is designed for efficiency, only uploading and storing data that has directly changed since the last backup. Its security keys are known only to the user.

----

.. note:: For this guide you should be familiar with the basic concepts of

  * :manual:`SSH <basics-ssh>`
  * :manual:`Shell <basics-shell>`
  * :manual:`Cronjobs <daemons-cron>`


Installation
============

.. hint:: You find a list of some of the commandline parameters at the end of this tutorial.


Download GPG keys and the source and verify it
----------------------------------------------

.. code-block:: console

 [isabell@stardust ~]$ wget https://www.tarsnap.com/tarsnap-signing-key-2021.asc
 [isabell@stardust ~]$ gpg --list-packets tarsnap-signing-key-2021.asc | grep signature
 [isabell@stardust ~]$ gpg --import tarsnap-signing-key-2021.asc
 [isabell@stardust ~]$ rm tarsnap-signing-key-2021.asc
 [isabell@stardust ~]$

.. code-block:: console

 [isabell@stardust ~]$ wget https://www.tarsnap.com/download/tarsnap-autoconf-1.0.39.tgz
 [isabell@stardust ~]$ wget https://www.tarsnap.com/download/tarsnap-sigs-1.0.39.asc
 [isabell@stardust ~]$ gpg --decrypt tarsnap-sigs-1.0.39.asc
 [isabell@stardust ~]$ shasum -a 256 tarsnap-autoconf-1.0.39.tgz
 [isabell@stardust ~]$ rm tarsnap-sigs-1.0.39.asc
 [isabell@stardust ~]$


Extract and compile the code
----------------------------

.. code-block:: console

 [isabell@stardust ~]$ tar -xzf tarsnap-autoconf-1.0.39.tgz
 [isabell@stardust ~]$ cd tarsnap-autoconf-1.0.39/
 [isabell@stardust tarsnap-autoconf-1.0.39]$ ./configure --prefix=/home/$USER
 [isabell@stardust tarsnap-autoconf-1.0.39]$ make
 [isabell@stardust tarsnap-autoconf-1.0.39]$ make install
 [isabell@stardust tarsnap-autoconf-1.0.39]$ cd ..
 [isabell@stardust ~]$ rm -rf tarsnap-autoconf-1.0.39
 [isabell@stardust ~]$ rm tarsnap-autoconf-1.0.39.tgz
 [isabell@stardust ~]$

Configuration
=============

Create a working directory
--------------------------

.. code-block:: console

 [isabell@stardust ~]$ mkdir /home/$USER/tarsnap
 [isabell@stardust ~]$
 

Create a user account and preload money to it
---------------------------------------------

Go to https://www.tarsnap.com/register.cgi and register an account. After that load some money to it. At least $5.


Create some keyfiles
--------------------

.. code-block:: console

 [isabell@stardust ~]$ tarsnap-keygen \
							--keyfile /home/$USER/tarsnap/tarsnap.key \
							--user your_registered_email_from_the_account_registration \
							--machine some_nifty_name
							--passphrased
 [isabell@stardust ~]$

As this key has all rights to manage your backups, you have to create a key with write-only access to do backups automatically per cronjob.

.. code-block:: console

 [isabell@stardust ~]$ tarsnap-keymgmt \
							--outkeyfile /home/$USER/tarsnap/tarsnapwrite.key \
							-w /home/$USER/tarsnap/tarsnap.key``
 [isabell@stardust ~]$

.. warning:: Please copy your keyfiles to a safe place! Without the keys you cannot access your backups anymore.


Set up the config file
----------------------

.. code-block:: console

 [isabell@stardust ~]$ cp /home/$USER/etc/tarsnap.conf.sample /home/$USER/etc/tarsnap.conf
 [isabell@stardust ~]$

Now edit ``/home/$USER/etc/tarsnap.conf`` with the editor of your choice. The config file is already commented by the author.
Make sure to use your write-only keyfile under keyfile in the config file.


Create a backup script
----------------------

Create a script ``/home/$USER/tarsnap-backup.sh`` using the editor of your choice with the following content:

``!/bin/sh
/home/$USER/bin/tarsnap -c \
	-f "BACKUP-$(date +%d-%m-%Y_%H-%M-%S)" \
	/var/www/virtual/$USER``

Now make it executable.

.. code-block:: console

 [isabell@stardust ~]$ chmod u+x /home/$USER/tarsnap-backup.sh
 [isabell@stardust ~]$


Setup automatic backups per cronjob
-----------------------------------

.. code-block:: console

 [isabell@stardust ~]$ crontab -e
 [isabell@stardust ~]$

Enter ``0 02 * * * /home/$USER/tarsnap-backup.sh`` to let the backup run every night at 2 am.

.. hint:: For help setting up cronjobs go to https://crontab.guru/


Test your backup
----------------

Start a backup using

.. code-block:: console

 [isabell@stardust ~]$ /home/$USER/tarsnap-backup.sh
 [isabell@stardust ~]$

To show all your existing backups use

.. code-block:: console

 [isabell@stardust ~]$ tarsnap --list-archives --keyfile /home/$USER/tarsnap/tarsnap.key | sort
 [isabell@stardust ~]$

You should see one backup at the moment.

To restore this backup, create another directory as a testing destination using

.. code-block:: console

 [isabell@stardust ~]$ mkdir /home/$USER/restoretest
 [isabell@stardust ~]$
 
Then use

.. code-block:: console

 [isabell@stardust ~]$ tarsnap -x -v -f BACKUP --keyfile /home/$USER/tarsnap/tarsnap.key -C /home/$USER/restoretest
 [isabell@stardust ~]$

to restore your backed up files to the testing directory.

.. note:: BACKUP has to be replaced by the name listed by --list-archives in the step above.


Commandline parameters
----------------------

Here is a list of all parameters used in this tutorial if not obvious by its name.

  * ``-c``: create a backup
  * ``-x``: restore a backup
  * ``-f``: specifies the backup to create or restore
  * ``-t``: list the contents of a backup archive
  * ``-v``: shows the filenames during backup or restor
  * ``-C``: changes the directory


Finish
======

Now everything should work.

To get additional help use the manpages or read the documentation at https://www.tarsnap.com/documentation.html

----

Tested with Tarsnap 1.0.39, Uberspace 7.9.0.0

.. author_list::
