.. highlight:: console
.. author:: Hafnium <haf@hafnium.me>

.. tag:: lang-go
.. tag:: file-storage
.. tag:: backup
.. tag:: sync
.. tag:: bash

.. sidebar:: About

  .. image:: _static/images/restic.png
      :align: center

#########
Restic
#########

.. tag_list::

Restic_ is a fast and secure backup program, which have compatibility with multiple cloud providers.

----

.. note:: For this guide you should be familiar with the basic concepts of

  * :manual:`SSH <basics-ssh>`
  * :manual:`cronjobs <daemons-cron>`

License
=============

Restic is an open source software distributed under the BSD-2-Clause License. All relevant legal information can be found here

  * https://github.com/restic/restic/blob/master/LICENSE


Prerequisites
=============

If you want to backup files to a remote server, you should set up a bucket a or user first. Restic currently supports backup with:

  - `Local directory <https://restic.readthedocs.io/en/latest/030_preparing_a_new_repo.html#local>`__
  - `sftp server (via SSH) <https://restic.readthedocs.io/en/latest/030_preparing_a_new_repo.html#sftp>`__
  - `HTTP REST server <https://restic.readthedocs.io/en/latest/030_preparing_a_new_repo.html#rest-server>`__ (`protocol <doc/100_references.rst#rest-backend>`__ `rest-server <https://github.com/restic/rest-server>`__)
  - `AWS S3 <https://restic.readthedocs.io/en/latest/030_preparing_a_new_repo.html#amazon-s3>`__ (either from Amazon or using the `Minio <https://minio.io>`__ server)
  - `OpenStack Swift <https://restic.readthedocs.io/en/latest/030_preparing_a_new_repo.html#openstack-swift>`__
  - `BackBlaze B2 <https://restic.readthedocs.io/en/latest/030_preparing_a_new_repo.html#backblaze-b2>`__
  - `Microsoft Azure Blob Storage <https://restic.readthedocs.io/en/latest/030_preparing_a_new_repo.html#microsoft-azure-blob-storage>`__
  - `Google Cloud Storage <https://restic.readthedocs.io/en/latest/030_preparing_a_new_repo.html#google-cloud-storage>`__
  - And many other services via the `rclone <https://rclone.org>`__ `Backend <https://restic.readthedocs.io/en/latest/030_preparing_a_new_repo.html#other-services-via-rclone>`__

Installation
============

You can find and download the latest stable release versions of restic from the `restic
release page <https://github.com/restic/restic/releases/latest>`__. SHA256 checksums and `GPG <https://restic.readthedocs.io/en/latest/090_participating.html#security>`__ signed files can also be found there.

We're installing a compiled restic binary for a 64-bit machine, and making it executable with the following steps:

::

 [isabell@stardust ~]$ wget https://github.com/restic/restic/releases/download/v0.12.1/restic_0.12.1_linux_amd64.bz2
 [isabell@stardust ~]$ bzip2 -d restic_0.12.1_linux_amd64.bz2
 [isabell@stardust ~]$ mv restic_0.12.1_linux_amd64 ~/bin/restic
 [isabell@stardust ~]$ chmod 700 ~/bin/restic
 [isabell@stardust ~]$


Configuration
=============

Login details
-------------
Now it's time to get you login/API details from you remote server. This differs from service to service, but usually boils down to a key id (username) and a key (password).

Setup repository
----------------
.. note:: The service or protocol used, needs to be specified, when communicating with a repository. Please read in the restic documentation: https://restic.readthedocs.io/en/latest/030_preparing_a_new_repo.html

.. warning:: Restic repositories are encrypted, and losing the password means losing access to all the files. So please save the password somewhere safe.

Here we're initializing a repository on a Backblaze B2 bucket

::

  [isabell@stardust ~]$ export B2_ACCOUNT_ID=<MY_APPLICATION_KEY_ID>
  [isabell@stardust ~]$ export B2_ACCOUNT_KEY=<MY_APPLICATION_KEY>
  [isabell@stardust ~]$ restic -r b2:bucketname:path/to/repo init
  enter password for new repository:
  enter password again:
  created restic repository eefee03bbd at b2:bucketname:path/to/repo
  Please note that knowledge of your password is required to access the repository.
  Losing your password means that your data is irrecoverably lost.
  [isabell@stardust ~]$

Automation
----------
It is recommended to create a script to automate the backups. Please edit this template to fit your needs.

.. note:: Remember to set the ``B2_ACCOUNT_ID``, ``B2_ACCOUNT_KEY`` and repository to your service, details on environment variables can be read `here <https://restic.readthedocs.io/en/latest/040_backup.html#environment-variables>`__.
.. tip:: If you need to backup a folder but want to exclude some files from backup withing that folder, you can use the flag ``--exclude-if-present='superSecretFile.txt'`` while calling restic. Be aware that this flag will create an error if the list of excluded files is empty.

::

  #!/bin/bash

  # Restic API keys
  export B2_ACCOUNT_ID='[hidden]'
  export B2_ACCOUNT_KEY='[hidden]'
  export RESTIC_PASSWORD='[hidden]'

  # Print commands for debugging
  #set -x

  #Files to include/exclude
  FILES='/var/www/virtual/isabell/html/ /home/isabell/myImportantDocument.md'

  # Run restic backup
  ~/bin/restic -r b2:bucketname:path/to/repo backup $FILES

  #set +x # Stop printing

  # Remove restic details from current shell
  export -n B2_ACCOUNT_ID B2_ACCOUNT_KEY RESTIC_PASSWORD

Save the content into the file ``~/resticBackup.sh`` and make executable ``chmod +x ~/resticBackup.sh``.

Cronjob
-------
We do not want to login every day to backup our files. So a cronjob can be set up, to run the bash script at 00:05:00 (5 AM).

Insert the following into your :manual:`crontab <daemons-cron>`:

::

  0 5 * * * sh $HOME/resticBackup.sh > $HOME/logs/restic-cron.log 2>&1

Best practices
==============

Security
--------
Make sure only your user account can run the script by changing file permissions

::

  [isabell@stardust ~]$ chmod 700 ~/resticBackup.sh
  [isabell@stardust ~]$

You should use a strong password for the repository.

Another consideration is to find a solution to distribute the API keys and repository password. If you followed the guide, the details are in plaintext right now, but if someone (including root user) can read the bash script, they can possibly also read the files you are trying backing up.

Managing keys
-------------
Restic allows for creation of multiple keys. this can be done with

::

 [isabell@stardust ~]$ restic -r /srv/restic-repo key add
 enter password for repository:
 enter password for new key:
 enter password again:
 saved new key as <Key of isabell@stardust, created on 2020-01-01 12:00:00.000000000 +0200 CEST>
 [isabell@stardust ~]$

Current keys can now be listed with

::

 [isabell@stardust ~]$ restic -r /srv/restic-repo key list
 enter password for repository:
 ID          User        Host        Created
 ----------------------------------------------------------------------
 5c657874    isabell    stardust   2020-01-01 10:30:00
 *eb78040b   isabell    stardust   2020-01-01 12:00:00
 [isabell@stardust ~]$

Restoring from backup
---------------------

Please follow the Restic documentation on how to restore the files

  * https://restic.readthedocs.io/en/latest/050_restore.html

Updates
=======

.. note:: Releases can be followed on the Github repository: https://github.com/restic/restic/releases or with the update feed_.

The binaries can be updated by using the ``restic self-update`` command or by building from source again.


.. _feed: https://github.com/restic/restic/releases.atom
.. _Restic: https://restic.net/

----

Tested with Restic 0.12.1, Uberspace 7.11.4

.. author_list::
