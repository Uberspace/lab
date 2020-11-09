.. highlight:: console

.. author:: Direnc <direnc99@gmail.com>

.. categorize your guide! refer to the current list of tags: https://lab.uberspace.de/tags
.. tag:: web
.. tag:: self-hosting


.. sidebar:: About

  .. image:: _static/images/teamcity.svg
      :align: center
      :target: https://www.jetbrains.com/company/brand/logos/


##########
TeamCity
##########

.. tag_list::

TeamCity_ is a build management tool by JetBrains. It is not open source and requires a license, though it offers a freemium model with up to 100 build configurations and 3 build agents. TeamCity makes it possible to attach a server to your projects in different Version Control Systems so that it runs build steps on pre-configured triggers.

----

.. note:: For this guide you should be familiar with the basic concepts of

  * :manual:`MySQL <database-mysql>`
  * :manual:`domains <web-domains>`

License
=======

All relevant legal information can be found here

  * https://www.jetbrains.com/teamcity/buy/license.html

Logo source: https://www.jetbrains.com/company/brand/logos/

Prerequisites
=============

We're using Java in the stable version 14.0.2:

::

 [isabell@stardust ~]$ java --version
 openjdk 14.0.2 2020-07-14
 OpenJDK Runtime Environment 20.3 (build 14.0.2+12)
 OpenJDK 64-Bit Server VM 20.3 (build 14.0.2+12, mixed mode, sharing)
 [isabell@stardust ~]$

MySQL
-----

.. include:: includes/my-print-defaults.rst

We will create a separate database for TeamCity:

::

 [isabell@stardust ~]$ mysql -e "CREATE DATABASE ${USER}_teamcity"
 [isabell@stardust ~]$

Your URL needs to be setup:

.. include:: includes/web-domain-list.rst

You can also setup your own :manual_anchor:`domain <web-domains.html>`. TeamCity will run as a backend serving HTML files.

Installation
============

Step 1
------
First, we're going to download TeamCity and extract it.

Download the latest version (TeamCity-Download_ page) of the tgz archive and extract it. Note that the download link on the page is actually a redirect. So instead of the link behind the button, use the direct link e.g.: ``https://download.jetbrains.com/teamcity/TeamCity-2020.1.5.tar.gz``.

::

 [isabell@stardust ~]$ wget -O teamcity.tgz https://download.jetbrains.com/teamcity/TeamCity-2020.1.5.tar.gz
 [isabell@stardust ~]$ tar --gzip --extract --file=teamcity.tgz
 [isabell@stardust ~]$ rm teamcity.tgz
 [isabell@stardust ~]$

Step 2
------
Start the TeamCity Server. The startup scripts lie in TeamCity/bin

::

 [isabell@stardust ~]$ ./TeamCity/bin/runAll.sh start
 Spawning TeamCity restarter in separate process
 TeamCity restarter running with PID XXXXX
 Starting TeamCity build agent...
 Java executable is found: '/usr/lib/jvm/java-1.8.0-openjdk-1.8.0.262.b10-0.el7_8.x86_64/jre/bin/java'
 Starting TeamCity Build Agent Launcher...
 Agent home directory is /home/isabell/TeamCity/buildAgent
 Agent Launcher Java runtime version is 1.8
 Lock file: /home/isabell/TeamCity/buildAgent/logs/buildAgent.properties.lock
 Using no lock
 Done [28997], see log at /home/isabell/TeamCity/buildAgent/logs/teamcity-agent.log
 [isabell@stardust ~]$

Step 3
------
Now we should configure a web backend for TeamCity.

::

 [isabell@stardust bin]$ uberspace web backend set --http --port 8111 isabell.uber.space
 Set backend for isabell.uber.space/ to port 8111; please make sure something is listening!
 You can always check the status of your backend using "uberspace web backend list".
 [isabell@stardust bin]$


Step 4
------
We visit the page in the browser of our choice on isabell.uber.space.

1. Type in the data directory. You can also use the default one at /home/isabell/.BuildServer
2. Wait for the Data Directory to be initialized
3. For the Database select ``MySQL``
4. Download the JDBC Driver by clicking on the download button
5. For the Database Settings, we enter our information:

  1. ``Database name``: ``isabell_teamcity``
  2. ``User name``: ``isabell``
  3. ``Database password``: ``MySuperSecretPassword``

6. Wait for the initialization to complete. This could take a while.
7. In the License Agreement page scroll down, tick the Accept license Agreement checkbox and uncheck the usage statistics. Click on continue.
8. Choose a username and password and click on ``Create Account``
9. TeamCity is now up and running. You can configure your first build configuration under ``Projects``

Best practices
==============

Documentation
-------------

TeamCity has extensive documentation. Check it out under TeamCity-Docs_.

Tuning
======

You can add extra functionalities of TeamCity with plugins. Check out the TeamCity-Plugins_ page.

.. _TeamCity: https://www.jetbrains.com/teamcity/
.. _TeamCity-Download: https://www.jetbrains.com/teamcity/download/#section=get
.. _TeamCity-Docs: https://www.jetbrains.com/help/teamcity/teamcity-documentation.html
.. _TeamCity-Plugins: https://plugins.jetbrains.com/teamcity


----

Tested with TeamCity version 1.5 Build 78938, Uberspace 7.7.9.0

.. author_list::
