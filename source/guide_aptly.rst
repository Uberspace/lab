.. highlight:: console

.. author:: Thomas S. <https://github.com/Thomas--S/>

.. tag:: package-management

#####
aptly
#####

.. tag_list::

aptly_ is described on its website like this:
    *aptly is a swiss army knife for Debian repository management: it allows you to mirror remote repositories, manage local package repositories, take snapshots, pull new versions of packages along with dependencies, publish as Debian repository.*

----


License
=======

License information can be found here

  * https://github.com/aptly-dev/aptly/blob/master/LICENSE

Prerequisites
=============

First of all, you'll need to install Homebrew_. This tool will be used to install aptly.

.. code-block:: console
 :emphasize-lines: 28

 [isabell@stardust ~]$ sh -c "$(curl -fsSL https://raw.githubusercontent.com/Linuxbrew/install/master/install.sh)"
 ==> This script will install:
 /home/isabell/.linuxbrew/bin/brew
 /home/isabell/.linuxbrew/share/doc/homebrew
 /home/isabell/.linuxbrew/share/man/man1/brew.1
 /home/isabell/.linuxbrew/share/zsh/site-functions/_brew
 /home/isabell/.linuxbrew/etc/bash_completion.d/brew
 /home/isabell/.cache/Homebrew/
 /home/isabell/.linuxbrew/Homebrew
 ==> The following new directories will be created:
 /home/isabell/.linuxbrew/bin
 /home/isabell/.linuxbrew/etc
 /home/isabell/.linuxbrew/include
 /home/isabell/.linuxbrew/lib
 /home/isabell/.linuxbrew/sbin
 /home/isabell/.linuxbrew/share
 /home/isabell/.linuxbrew/var
 /home/isabell/.linuxbrew/opt
 /home/isabell/.linuxbrew/share/zsh
 /home/isabell/.linuxbrew/share/zsh/site-functions
 /home/isabell/.linuxbrew/var/homebrew
 /home/isabell/.linuxbrew/var/homebrew/linked
 /home/isabell/.linuxbrew/Cellar
 /home/isabell/.linuxbrew/Caskroom
 /home/isabell/.linuxbrew/Homebrew
 /home/isabell/.linuxbrew/Frameworks

 Press RETURN to continue or any other key to abort

 [...]

 [isabell@stardust ~]$

To be able to use the ``brew`` command, you can add the following line to ``~/.bash_profile``:

.. warning:: Replace ``isabell`` with your username!

::

 eval $(/home/isabell/.linuxbrew/bin/brew shellenv)

To make this change effective for the current session, you can use:

::

 [isabell@stardust ~]$ source ~/.bash_profile
 [isabell@stardust ~]$

Installation
============

To install aptly, you can simply use brew:

::

 [isabell@stardust ~]$ brew install aptly

 [...]

 [isabell@stardust ~]$

Basic Configuration and Usage
=============================

This guide only shows a basic configuration and a very simple example of how aptly can be used.
For more advanced use cases please consult the official documentation of aptly.

Create default config file
--------------------------

Aptly automatically generates ``~/.aptly.conf`` with default contents as soon as you tell aptly to show the default configuration:

::

 [isabell@stardust ~]$ aptly config show
 Config file not found, creating default config at /home/isabell/.aptly.conf

 {
     "rootDir": "/home/isabell/.aptly",
     "downloadConcurrency": 4,
     "downloadSpeedLimit": 0,
     "architectures": [],
     "dependencyFollowSuggests": false,
     "dependencyFollowRecommends": false,
     "dependencyFollowAllVariants": false,
     "dependencyFollowSource": false,
     "dependencyVerboseResolve": false,
     "gpgDisableSign": false,
     "gpgDisableVerify": false,
     "gpgProvider": "gpg",
     "downloadSourcePackages": false,
     "skipLegacyPool": true,
     "ppaDistributorID": "ubuntu",
     "ppaCodename": "",
     "skipContentsPublishing": false,
     "FileSystemPublishEndpoints": {},
     "S3PublishEndpoints": {},
     "SwiftPublishEndpoints": {}
 }
 [isabell@stardust ~]$


Configure Filesystem Endpoint
-----------------------------

To configure a filesystem endpoint for publishing the packets, you can add the following entry to ``~/.aptly.conf``:

.. warning:: Replace ``isabell`` with your username!

::

 {
   ...,
   "FileSystemPublishEndpoints": {
     "public": {
       "rootDir": "/var/www/virtual/isabell/html/repo",
       "linkMethod": "copy",
       "verifyMethod": "md5"
     }
   }
 }

Configure Repository
--------------------

You can create a new repository with the following command:

::

 [isabell@stardust ~]$ aptly -distribution="stable" -architectures=amd64 repo create IsabellsRepo

 Local repo [IsabellsRepo] successfully added.
 You can run 'aptly repo add IsabellsRepo ...' to add packages to repository.
 [isabell@stardust ~]$

Now you need to generate a GPG key. This can be achieved with the following commands:

.. code-block:: console
 :emphasize-lines: 16, 18, 26, 28, 32, 33, 34, 38, 39

 [isabell@stardust ~]$ gpg --gen-key
 gpg (GnuPG) 2.0.22; Copyright (C) 2013 Free Software Foundation, Inc.
 This is free software: you are free to change and redistribute it.
 There is NO WARRANTY, to the extent permitted by law.

 gpg: Verzeichnis `/home/isabell/.gnupg' erzeugt
 gpg: Neue Konfigurationsdatei `/home/isabell/.gnupg/gpg.conf' erstellt
 gpg: WARNUNG: Optionen in `/home/isabell/.gnupg/gpg.conf' sind während dieses Laufes noch nicht wirksam
 gpg: Schlüsselbund `/home/isabell/.gnupg/secring.gpg' erstellt
 gpg: Schlüsselbund `/home/isabell/.gnupg/pubring.gpg' erstellt
 Bitte wählen Sie, welche Art von Schlüssel Sie möchten:
    (1) RSA und RSA (voreingestellt)
    (2) DSA und Elgamal
    (3) DSA (nur signieren/beglaubigen)
    (4) RSA (nur signieren/beglaubigen)
 Ihre Auswahl? 1
 RSA-Schlüssel können zwischen 1024 und 4096 Bit lang sein.
 Welche Schlüssellänge wünschen Sie? (2048) 4096
 Die verlangte Schlüssellänge beträgt 4096 Bit
 Bitte wählen Sie, wie lange der Schlüssel gültig bleiben soll.
          0 = Schlüssel verfällt nie
       <n>  = Schlüssel verfällt nach n Tagen
       <n>w = Schlüssel verfällt nach n Wochen
       <n>m = Schlüssel verfällt nach n Monaten
       <n>y = Schlüssel verfällt nach n Jahren
 Wie lange bleibt der Schlüssel gültig? (0)
 Schlüssel verfällt nie
 Ist dies richtig? (j/N) j

 GnuPG erstellt eine User-ID um Ihren Schlüssel identifizierbar zu machen.

 Ihr Name ("Vorname Nachname"): Isabell Stardust
 Email-Adresse: isabell@uber.space
 Kommentar:
 Sie haben diese User-ID gewählt:
     "Isabell Stardust <isabell@uber.space>"

 Ändern: (N)ame, (K)ommentar, (E)-Mail oder (F)ertig/(A)bbrechen? f
 Sie benötigen eine Passphrase, um den geheimen Schlüssel zu schützen.

 Wir müssen eine ganze Menge Zufallswerte erzeugen.  Sie können dies
 unterstützen, indem Sie z.B. in einem anderen Fenster/Konsole irgendetwas
 tippen, die Maus verwenden oder irgendwelche anderen Programme benutzen.
 Wir müssen eine ganze Menge Zufallswerte erzeugen.  Sie können dies
 unterstützen, indem Sie z.B. in einem anderen Fenster/Konsole irgendetwas
 tippen, die Maus verwenden oder irgendwelche anderen Programme benutzen.
 gpg: /home/isabell/.gnupg/trustdb.gpg: trust-db erzeugt
 gpg: Schlüssel 807C769E ist als uneingeschränkt vertrauenswürdig gekennzeichnet
 Öffentlichen und geheimen Schlüssel erzeugt und signiert.

 gpg: "Trust-DB" wird überprüft
 gpg: 3 marginal-needed, 1 complete-needed, PGP Vertrauensmodell
 gpg: Tiefe: 0  gültig:   1  signiert:   0  Vertrauen: 0-, 0q, 0n, 0m, 0f, 1u
 pub   4096R/A01A2680 2020-01-09
   Schl.-Fingerabdruck = AB2B 5151 5041 48D7 104F  8A9C 9414 BE64 A01A 2680
 uid                  Isabell Stardust <isabell@uber.space>
 sub   4096R/B748CEA8 2020-01-09

 [isabell@stardust ~]$

Upload the package
------------------

You can now put the ``.deb`` package you want to publish in the home directory, for example via SFTP.
For the rest of this guide, ``example-1.deb`` will be assumed as file name.

Add the package to the repository
---------------------------------

::

 [isabell@stardust ~]$ aptly repo add IsabellsRepo example-1.deb
 Loading packages...
 [+] example_1.0-1_all added
 [isabell@stardust ~]$

Create a snapshot
-----------------

::

 [isabell@stardust ~]$ aptly snapshot create IsabellsRepo2020-01-09 from repo IsabellsRepo

 Snapshot IsabellsRepo2020-01-09 successfully created.
 You can run 'aptly publish snapshot IsabellsRepo2020-01-09' to publish snapshot as Debian repository.
 [isabell@stardust ~]$

Publish the snapshot
--------------------

.. code-block:: console
 :emphasize-lines: 11, 19

 [isabell@stardust ~]$ aptly -architectures=all publish snapshot IsabellsRepo2020-01-09 filesystem:public:
 Loading packages...
 Generating metadata files and linking package files...
 Finalizing metadata files...
 Signing file 'Release' with gpg, please enter your passphrase when prompted:

 Sie benötigen eine Passphrase, um den geheimen Schlüssel zu entsperren.
 Benutzer: "Isabell Stardust <isabell@uber.space>"
 4096-Bit RSA Schlüssel, ID A01A2680, erzeugt 2020-01-09

 Geben Sie die Passphrase ein:

 Clearsigning file 'Release' with gpg, please enter your passphrase when prompted:

 Sie benötigen eine Passphrase, um den geheimen Schlüssel zu entsperren.
 Benutzer: "Isabell Stardust <isabell@uber.space>"
 4096-Bit RSA Schlüssel, ID A01A2680, erzeugt 2020-01-09

 Geben Sie die Passphrase ein:


 Snapshot IsabellsRepo2020-01-09 has been successfully published.
 Please setup your webserver to serve directory '/var/www/virtual/isabell/html/repo' with autoindexing.
 Now you can add following line to apt sources:
   deb http://your-server/ stable main
 Don't forget to add your GPG key to apt with apt-key.

 You can also use `aptly serve` to publish your repositories over HTTP quickly.
 [isabell@stardust ~]$

Publish GPG Key
---------------

.. warning:: Replace ``isabell`` with your username and ``A01A2680`` with your public key ID!

::

 [isabell@stardust ~]$ mkdir /var/www/virtual/isabell/html/key
 [isabell@stardust ~]$ gpg --output /var/www/virtual/isabell/html/key/key.gpg --armor --export A01A2680
 [isabell@stardust ~]$

Using the repository
--------------------

On your local Debian-based system you can now add the repository by adding the following line to your local ``sources.list``:

::

 deb https://isabell.uber.space/repo stable main

You can add the key to your local system with:

::

 [john@doe ~]$ curl -sSL https://isabell.uber.space/key/key.gpg | sudo apt-key add -

Updates
=======

.. note:: Check the update feed_ regularly to stay informed about the newest version.

You can use ``brew upgrade`` to update aptly.


.. _aptly: https://aptly.info
.. _Homebrew: https://docs.brew.sh/Homebrew-on-Linux
.. _feed: https://github.com/aptly-dev/aptly/releases.atom

----

Tested with aptly 1.4.0, Uberspace 7.3.10

.. author_list::
