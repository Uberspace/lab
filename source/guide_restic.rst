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

  * :manual:`Go <lang-go>`
  * :manual:`SSH <basics-ssh>`
  * :manual:`cronjobs <daemons-cron>`

License
=============

Restic is an open source software distributed under the BSD-2-Clause License. All relevant legal information can be found here

  * https://github.com/restic/restic/blob/master/LICENSE


Prerequisites
=============

We're using :manual:`Go <lang-golang>` version go1.12.5 to compile the software.

::

 [isabell@stardust ~]$ go version
 go version go1.12.5 linux/amd64
 [isabell@stardust ~]$

If you want to back up to a remote server, you should set up a bucket a or user first. Restic currently supports backup with:

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

``cd`` to your ``/$HOME`` home directory before fetching Restic.

We're building restic from source with the following steps:

::

 [isabell@stardust ~]$ git clone https://github.com/restic/restic.git
 [...]
 [isabell@stardust ~]$ cd restic
 [isabell@stardust restic]$ go run build.go
 [...]
 [isabell@stardust restic]$


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
  [isabell@stardust ~]$ ~/restic/restic -r b2:bucketname:path/to/repo init
  enter password for new repository:
  enter password again:
  created restic repository eefee03bbd at b2:bucketname:path/to/repo
  Please note that knowledge of your password is required to access the repository.
  Losing your password means that your data is irrecoverably lost.
  [isabell@stardust ~]$

Automation
----------
It is recommended to create a bash script to automate the backups. Please edit this template to fit your needs.

.. note:: Remember to set the ``B2_ACCOUNT_ID``, ``B2_ACCOUNT_KEY`` and repository to your service, details on environment variables can be read `here <https://restic.readthedocs.io/en/latest/040_backup.html#environment-variables>`__.

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
  EXCLUDED_FILES='superSecretFile.txt'

  # Run restic backup
  ~/restic/restic -r b2:bucketname:path/to/repo backup $FILES --exclude-if-present=$EXCLUDED_FILES

  #set +x # Stop printing

  # Remove restic details from current shell
  export -n B2_ACCOUNT_ID B2_ACCOUNT_KEY RESTIC_PASSWORD

Save the content into the file ``~/resticBackup.sh``

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

 [isabell@stardust ~]$ ~/restic/restic -r /srv/restic-repo key add
 enter password for repository:
 enter password for new key:
 enter password again:
 saved new key as <Key of isabell@stardust, created on 2020-01-01 12:00:00.000000000 +0200 CEST>
 [isabell@stardust ~]$

Current keys can now be listed with

::

 [isabell@stardust ~]$ ~/restic/restic -r /srv/restic-repo key list
 enter password for repository:
 ID          User        Host        Created
 ----------------------------------------------------------------------
 5c657874    isabell    stardust   2020-01-01 10:30:00
 *eb78040b   isabell    stardust   2020-01-01 12:00:00
 [isabell@stardust ~]$

Restoring from backup
---------------------

Please follow the Restic documentation on how to resore the files

  * https://restic.readthedocs.io/en/latest/050_restore.html

Updates
=======

.. note:: Releases can be followed on the Github repository: https://github.com/restic/restic/releases or with the update feed_.

The binaries can be updated by using the ``~/restic/restic self-update`` command or by building from source again.


.. _feed: https://github.com/restic/restic/releases.atom
.. _Restic: https://restic.net/

----

Tested with Restic 0.9.6, Uberspace 7.7.4.0, Go 1.12.5 and Git 2.24.3

.. author_list::
