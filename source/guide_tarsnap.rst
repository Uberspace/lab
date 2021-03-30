.. highlight:: console

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

Import GPG key:

.. code-block:: console

 [isabell@stardust ~]$ wget https://www.tarsnap.com/tarsnap-signing-key-2021.asc
 (...)
 2021-03-30 14:52:12 (157 MB/s) - ‘tarsnap-signing-key-2021.asc’ saved [1810/1810]
 [isabell@stardust ~]$ gpg --import tarsnap-signing-key-2021.asc
 gpg: /home/tsnap/.gnupg/trustdb.gpg: trustdb created
 gpg: key 171F041B: public key "Tarsnap source code signing key (Tarsnap Backup Inc.) <cperciva@tarsnap.com>" imported
 gpg: Total number processed: 1
 gpg:               imported: 1  (RSA: 1)
 gpg: no ultimately trusted keys found
 [isabell@stardust ~]$ rm tarsnap-signing-key-2021.asc
 [isabell@stardust ~]$

Download and unpack tarsnap source:

.. code-block:: console
 :emphasize-lines: 10

 [isabell@stardust ~]$ wget https://www.tarsnap.com/download/tarsnap-autoconf-1.0.39.tgz
 (...)
 2021-03-30 22:49:04 (667 KB/s) - ‘tarsnap-autoconf-1.0.39.tgz.1’ saved [641089/641089]
 [isabell@stardust ~]$ wget https://www.tarsnap.com/download/tarsnap-sigs-1.0.39.asc
 (...)
 2021-03-30 22:49:28 (97.8 MB/s) - ‘tarsnap-sigs-1.0.39.asc’ saved [972/972]
 [isabell@stardust ~]$ gpg --decrypt tarsnap-sigs-1.0.39.asc
 SHA256 (tarsnap-autoconf-1.0.39.tgz) = 5613218b2a1060c730b6c4a14c2b34ce33898dd19b38fb9ea0858c5517e42082
 gpg: Signature made Wed 27 Jan 2021 02:40:40 CET using RSA key ID 171F041B
 gpg: Good signature from "Tarsnap source code signing key (Tarsnap Backup Inc.) <cperciva@tarsnap.com>"
 gpg: WARNING: This key is not certified with a trusted signature!
 gpg:          There is no indication that the signature belongs to the owner.
 Primary key fingerprint: CAEE 7C6B 11B1 7F77 D72F  E3A9 F6DD 38B1 171F 041B
 [isabell@stardust ~]$ rm tarsnap-sigs-1.0.39.asc
 [isabell@stardust ~]$


Extract and compile the code
----------------------------

.. code-block:: console

 [isabell@stardust ~]$ tar -xzf tarsnap-autoconf-1.0.39.tgz
 [isabell@stardust ~]$ cd tarsnap-autoconf-1.0.39/
 [isabell@stardust tarsnap-autoconf-1.0.39]$ ./configure --prefix=/home/$USER
 [isabell@stardust tarsnap-autoconf-1.0.39]$ make -j2
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

 [isabell@stardust ~]$ mkdir ~/tarsnap
 [isabell@stardust ~]$ mkdir ~/tarsnap/cache
 [isabell@stardust ~]$
 

Create a user account and preload money to it
---------------------------------------------

Go to https://www.tarsnap.com/register.cgi and register an account. After that load some money to it. At least $5.


Create some keyfiles
--------------------

.. code-block:: console
 :emphasize-lines: 3,4

 [isabell@stardust ~]$ tarsnap-keygen \
                         --keyfile ~/tarsnap/tarsnap.key \
                         --user your_registered_email_from_the_account_registration \
                         --machine some_nifty_name \
                         --passphrased
 [isabell@stardust ~]$

As this key has all rights to manage your backups, you have to create a key with write-only access to do backups automatically per cronjob.

.. code-block:: console

 [isabell@stardust ~]$ tarsnap-keymgmt \
                         --outkeyfile ~/tarsnap/tarsnapwrite.key \
                         -w ~/tarsnap/tarsnap.key
 [isabell@stardust ~]$

.. warning:: Please copy your keyfiles to a safe place! Without the keys you cannot access your backups anymore.


Set up the config file
----------------------

.. code-block:: console

 [isabell@stardust ~]$ cp ~/etc/tarsnap.conf.sample ~/etc/tarsnap.conf
 [isabell@stardust ~]$

Now edit ``~/etc/tarsnap.conf`` with the editor of your choice. The config file is already commented by the author.
Make sure to use your write-only keyfile under keyfile in the config file:

.. code-block::
 :emphasize-lines: 4,7,10,13,16,21

 ### Recommended options
 
 # Tarsnap cache directory
 cachedir ~/tarsnap/cache
 
 # Tarsnap key file
 keyfile ~/tarsnap/tarsnapwrite.key
 
 # Don't archive files which have the nodump flag set.
 nodump
 
 # Print statistics when creating or deleting archives.
 print-stats
 
 # Create a checkpoint once per GB of uploaded data.
 checkpoint-bytes 1G
 
 ### Commonly useful options
 
 # Use SI prefixes to make numbers printed by --print-stats more readable.
 humanize-numbers


Create a backup script
----------------------

Create a script ``~/bin/tarsnap-backup.sh`` using the editor of your choice with the following content:

.. code-block:: bash

 #!/bin/sh
 ~/bin/tarsnap -c \
    -f "BACKUP-$(date +%d-%m-%Y_%H-%M-%S)" \
    /var/www/virtual/$USER

Now make it executable.

.. code-block:: console

 [isabell@stardust ~]$ chmod u+x ~/bin/tarsnap-backup.sh
 [isabell@stardust ~]$


Setup automatic backups per cronjob
-----------------------------------

.. code-block:: console

 [isabell@stardust ~]$ crontab -e
 [isabell@stardust ~]$

Enter ``0 02 * * * tarsnap-backup.sh`` to let the backup run every night at 2 am.

.. hint:: For help setting up cronjobs go to https://crontab.guru/


Test your backup
----------------

Start a backup using

.. code-block:: console

 [isabell@stardust ~]$ tarsnap-backup.sh
 Directory /home/isabell/tarsnap/cache created for "--cachedir /home/isabell/tarsnap/cache"
 tarsnap: Removing leading '/' from member names
                                        Total size  Compressed size
 All archives                                 7751             2797
   (unique data)                              7751             2797
 This archive                                 7751             2797
 New data                                     7751             2797
 [isabell@stardust ~]$

To show all your existing backups use

.. code-block:: console

 [isabell@stardust ~]$ tarsnap --list-archives --keyfile ~/tarsnap/tarsnap.key | sort
 [isabell@stardust ~]$

You should see one backup at the moment.

To restore this backup, create another directory as a testing destination using

.. code-block:: console

 [isabell@stardust ~]$ mkdir ~/restoretest
 [isabell@stardust ~]$
 
Then use

.. code-block:: console

 [isabell@stardust ~]$ tarsnap -x -v -f BACKUP --keyfile ~/tarsnap/tarsnap.key -C ~/restoretest
 [isabell@stardust ~]$

to restore your backed up files to the testing directory.

.. note:: BACKUP has to be replaced by the name listed by ``--list-archives`` in the step above.


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
