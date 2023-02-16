.. highlight:: console

.. spelling::
    Artifactory

.. author:: Martin Wudenka <http://martin.wudenka.de>

.. tag:: conan
.. tag:: artifactory
.. tag:: lang-c
.. tag:: lang-cpp
.. tag:: audience-developers

.. sidebar:: About

  .. image:: _static/images/artifactorycecpp.svg
      :align: center

############################
Artifactory CE for C and C++
############################

.. tag_list::

Created to speed up C/C++ development cycles using binary repositories, Artifactory CE for C/C++ lets you host private packages on your server, giving you the power of JFrog Artifactory for Conan and generic binaries.

----

.. note:: For this guide you should be familiar with the basic concepts of

  * :manual:`supervisord <daemons-supervisord>`

License
=======

The EULA for Artifactory CE can be found `here <https://jfrog.com/de/artifactory-community-edition-c-c-eula/>`_.

Prerequisites
=============

Download the tarball from `conan.io <https://conan.io/downloads.html>`_.

::

 [isabell@stardust ~]$ wget https://releases.jfrog.io/artifactory/bintray-artifactory/org/artifactory/cpp/ce/jfrog-artifactory-cpp-ce/[RELEASE]/jfrog-artifactory-cpp-ce-[RELEASE]-linux.tar.gz
 […]
 Saving to: ‘jfrog-artifactory-cpp-ce-[RELEASE]-linux.tar.gz’
 100%[===============================>] 677,895,184 46.8KB/s   in 16m 49s

 2022-12-15 17:50:07 (656 KB/s) - ‘jfrog-artifactory-cpp-ce-[RELEASE]-linux.tar.gz’ saved [677895184/677895184]

Create the target directory:

::

 [isabell@stardust ~]$ mkdir ~/jfrog
 [isabell@stardust ~]$

Installation
============

The following guide is based on the `Linux Archive Installation <https://www.jfrog.com/confluence/display/JFROG/Installing+Artifactory#InstallingArtifactory-LinuxArchiveInstallation>`_.


Untar the tarball:

.. code-block:: console
 :emphasize-lines: 3

 [isabell@stardust ~]$ cd ~
 [isabell@stardust ~]$ tar xvf jfrog-artifactory-cpp-ce-\[RELEASE\]-linux.tar.gz
 artifactory-cpp-ce-7.47.12
 […]
 artifactory-cpp-ce-7.47.12/app/artifactory/tomcat/webapps/artifactory.war
 artifactory-cpp-ce-7.47.12/app/misc/tomcat/mc.war
 [isabell@stardust ~]$ mv artifactory-cpp-ce-<version> ~/jfrog/artifactory
 [isabell@stardust ~]$

Replace ``<version>`` with the version you downloaded.

Database Setup
--------------

Uberspace provides you a :manual:`mariadb <database-mysql>` instance. So we need to create the database and install the driver.

To create a new database for Artifactory execute:

::

 [isabell@stardust ~]$ mysql -e "CREATE DATABASE ${USER}_artifactory CHARACTER SET utf8 COLLATE utf8_bin;"
 [isabell@stardust ~]$

The name ``isabell_artifactory`` is later needed for the configuration.

To download the mariadb driver run:

::

 [isabell@stardust ~]$ cd ~/jfrog/artifactory/var/bootstrap/artifactory/tomcat/lib
 [isabell@stardust lib]$ wget https://repo1.maven.org/maven2/org/mariadb/jdbc/mariadb-java-client/2.7.6/mariadb-java-client-2.7.6.jar
 [isabell@stardust lib]$ cd ~
 [isabell@stardust ~]$

Other versions of the maria db driver can be found at `mvnrepository.com <https://mvnrepository.com/artifact/org.mariadb.jdbc/mariadb-java-client>`_.

Cleanup
=======

You can delete the Artifactory tarball.

Configuration
=============

Configure Artifactory
---------------------

.. include:: includes/my-print-defaults.rst

Create a config file from the basic template:

::

 [isabell@stardust ~]$ cp ~/jfrog/artifactory/var/etc/system.basic-template.yaml ~/jfrog/artifactory/var/etc/system.yaml
 [isabell@stardust ~]$

Edit ``~/jfrog/artifactory/var/etc/system.yaml``.

Under the ``shared -> node`` key replace the listening address:

.. code-block:: yaml

  shared:
      node:
          ip: 0.0.0.0

Under the ``shared -> database`` key insert the following database configuration:

.. code-block:: yaml
  :emphasize-lines: 5-7

  shared:
      database:
          type: mariadb
          driver: org.mariadb.jdbc.Driver
          url: "jdbc:mariadb://localhost/<username>_artifactory?characterEncoding=UTF-8&elideSetAutoCommits=true&useSSL=false&useMysqlMetadata=true"
          username: <username>
          password: <your db password>

Replace ``<username>`` and ``<password>`` with your user name and MySQL password.

Domain Setup
------------

    Artifactory will be running on port 8082.

.. include:: includes/web-backend.rst

Setup daemon
------------

Create the file ``~/etc/services.d/artifactory.ini`` with the following content:

.. code-block:: ini

  [program:artifactory]
  command=%(ENV_HOME)s/jfrog/artifactory/app/bin/artifactoryctl
  environment=JFROG_HOME=%(ENV_HOME)s/jfrog
  autostart=yes
  autorestart=yes
  startsecs=30


Finishing installation
======================

Start Artifactory
-----------------

.. include:: includes/supervisord.rst

Now point your browser to your uberspace and you should see the Artifactory webinterface.

The default user is ``admin`` and the corresponding password ``password``. At first login you are prompted to change the password.

Debugging
=========

Logs are saved at ``~/jfrog/artifactory/var/log/console.log``.

----

Tested with Artifactory CE 7.41.12, Uberspace 7.13.0

.. author_list::
