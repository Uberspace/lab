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

First download the tarball from `conan.io <https://conan.io/downloads.html>`_ to your local computer and transfer it to your uberspace (e.g. by scp or :manual:`sftp <basics-sftp>`).

Create the target directory:

::

 [isabell@stardust ~]$ mkdir -p ~/jfrog/artifactory
 [isabell@stardust ~]$

To ease navigation save the jfrog folder path into an environment variable:

::

 [isabell@stardust ~]$ cd ~/jfrog
 [isabell@stardust ~]$ export JFROG_HOME=$(pwd)
 [isabell@stardust ~]$


Installation
============

The following guide is based on the `Linux Archive Installation <https://www.jfrog.com/confluence/display/JFROG/Installing+Artifactory#InstallingArtifactory-LinuxArchiveInstallation>`_.


Untar the tarball:

::

 [isabell@stardust ~]$ cd to/where/you/saved/the/artifactory/tarball
 [isabell@stardust ~]$ tar -xvf jfrog-artifactory-cpp-ce-<version>-linux.tar.gz
 [isabell@stardust ~]$ mv artifactory-cpp-ce-<version> $JFROG_HOME/artifactory
 [isabell@stardust ~]$

Replace ``<version>`` with the version you downloaded.

Database Setup
--------------

Uberspace provides you a :manual:`mariadb <database-mysql>` instance. So we need to create the database and install the driver.

To create a new database for Artifactory execute:

::

 [isabell@stardust ~]$ mysql -e "CREATE DATABASE isabell_artifactory CHARACTER SET utf8 COLLATE utf8_bin;"
 [isabell@stardust ~]$

The name ``isabell_artifactory`` is later needed for the configuration.

To download the mariadb driver run:

::

 [isabell@stardust ~]$ pushd $JFROG_HOME/artifactory/var/bootstrap/artifactory/tomcat/lib
 [isabell@stardust ~]$ wget https://repo1.maven.org/maven2/org/mariadb/jdbc/mariadb-java-client/2.7.6/mariadb-java-client-2.7.6.jar
 [isabell@stardust ~]$ popd
 [isabell@stardust ~]$

Other versions of the maria db driver can be found at `mvnrepository.com <https://mvnrepository.com/artifact/org.mariadb.jdbc/mariadb-java-client>`_.

Cleanup
=======

You can delete the Artifactory tarball.

Configuration
=============

Configure Artifactory
---------------------

Find out your uberspace virtual ip:

::

 [isabell@stardust ~]$ ifconfig -a
 [isabell@stardust ~]$

Find the ``veth_isabell`` section and note down the ``inet`` address.

Find your database password by looking into ``~/.my.cnf``.

Create a config file from the basic template:

::

 [isabell@stardust ~]$ cp $JFROG_HOME/artifactory/var/etc/system.basic-template.yaml $JFROG_HOME/artifactory/var/etc/system.yaml
 [isabell@stardust ~]$

Edit ``$JFROG_HOME/artifactory/var/etc/system.yaml``.

Under the ``shared -> node`` key insert your virtual uberspace ip (e.g. 100.64.154.65)

.. code-block:: yaml

  shared:
      node:
          ip: 100.64.154.65

Under the ``shared -> database`` key insert the following database configuration:

.. code-block:: yaml

  shared:
      database:
          type: mariadb
          driver: org.mariadb.jdbc.Driver
          url: "jdbc:mariadb://localhost/isabell_artifactory?characterEncoding=UTF-8&elideSetAutoCommits=true&useSSL=false&useMysqlMetadata=true"
          username: isabell
          password: <your db password>

Domain Setup
------------

    Artifactory will be running on port 8082.

.. include:: includes/web-backend.rst

Setup daemon
------------

Create the file ``~/etc/services.d/artifactory.ini`` with the following content:

.. code-block:: ini

  [program:artifactory]
  command=/home/isabell/jfrog/artifactory/app/bin/artifactoryctl
  environment=JFROG_HOME="/home/mwdev/jfrog"
  autostart=yes
  autorestart=yes


Finishing installation
======================

Start Artifactory
-----------------

.. include:: includes/supervisord.rst

Now point your browser to your uberspace and you should see the Artifactory webinterface.

The default user is ``admin`` and the corresponding password ``password``. At first login you are prompted to change the password.

----

Tested with Artifactory CE 7.41.12, Uberspace 7.13.0

.. author_list::
