.. highlight:: console

.. spelling::
    sbt

.. author:: Raphael Höser <raphael@hoeser.info>

.. tag:: lang-java
.. tag:: continuous-integration
.. tag:: automation

.. sidebar:: Logo

  .. image:: _static/images/Jenkins_logo_with_title.svg
      :align: center

########
Jenkins
########

.. tag_list::

Jenkins_ is an open source automation server written in Java. Jenkins helps to automate the non-human part of the software development process, with continuous integration and facilitating technical aspects of continuous delivery. It is a server-based system that runs in servlet containers such as Apache Tomcat. It supports version control tools, including AccuRev, CVS, Subversion, Git, Mercurial, Perforce, TD/OMS, ClearCase and RTC, and can execute Apache Ant, Apache Maven and sbt based projects as well as arbitrary shell scripts and Windows batch commands. The creator of Jenkins is Kohsuke Kawaguchi. Released under the MIT License, Jenkins is free software.

Builds can be triggered by various means, for example by commit in a version control system, by scheduling via a cron-like mechanism and by requesting a specific build URL. It can also be triggered after the other builds in the queue have completed. Jenkins functionality can be extended with plugins.

----

.. note:: For this guide you should be familiar with the basic concepts of

  * :manual_anchor:`supervisord <daemons-supervisord>`
  * :manual_anchor:`web backends <web-backends>`

License
=======

Jenkins is released under the `MIT License <https://github.com/jenkinsci/jenkins/blob/master/LICENSE.txt>`_.

Prerequisites
=============

We're using Java version 17, check the version to confirm:

::

 [isabell@stardust ~]$ $ java -version
 openjdk version "17.0.2" 2022-01-18
 OpenJDK Runtime Environment 21.9 (build 17.0.2+8)
 OpenJDK 64-Bit Server VM 21.9 (build 17.0.2+8, mixed mode, sharing)
 [isabell@stardust ~]$

Your URL needs to be setup:

.. include:: includes/web-domain-list.rst


Installation
============

Create Workspace
----------------

First create a folder called ``Jenkins`` and a subfolder called ``Jenkins_home``.
Jenkins_home will hold all your Jenkins's data.

::

 [isabell@stardust ~]$ mkdir ~/Jenkins/Jenkins_home -p
 [isabell@stardust ~]$


Download Jenkins
-----------------

Next we download the current version of Jenkins:

::

 [isabell@stardust ~]$ wget -O Jenkins/jenkins.war http://mirrors.jenkins.io/war/latest/jenkins.war
 --2019-05-24 15:33:32--  http://mirrors.jenkins.io/war/latest/jenkins.war
 Resolving mirrors.jenkins.io (mirrors.jenkins.io)... 52.202.51.185
 Connecting to mirrors.jenkins.io (mirrors.jenkins.io)|52.202.51.185|:80... connected.
 HTTP request sent, awaiting response... 302 Found
 Location: http://ftp-nyc.osuosl.org/pub/jenkins/war/2.178/jenkins.war [following]
 --2019-05-24 15:33:32--  http://ftp-nyc.osuosl.org/pub/jenkins/war/2.178/jenkins.war
 Resolving ftp-nyc.osuosl.org (ftp-nyc.osuosl.org)... 64.50.233.100, 2600:3404:200:237::2
 Connecting to ftp-nyc.osuosl.org (ftp-nyc.osuosl.org)|64.50.233.100|:80... connected.
 HTTP request sent, awaiting response... 200 OK
 Length: 77273755 (74M) [application/x-java-archive]
 Saving to: ‘Jenkins/jenkins.war’

 100%[====================================================>]  77,273,755  21.4MB/s   in 3.7s

 2019-05-24 15:33:36 (20.1 MB/s) - ‘Jenkins/jenkins.war’ saved [77273755/77273755]
 [isabell@stardust ~]$


At this point you would already be able to run Jenkins, but you wouldn't be able to connect to it and it would not run as a service.

Configuration
==============

Install service
---------------

We create the service file ``~/etc/services.d/jenkins.ini`` and fill it with:

.. code-block:: ini

 [program:jenkins]
 directory=%(ENV_HOME)s/Jenkins/Jenkins_home
 environment=JENKINS_HOME="%(ENV_HOME)s/Jenkins/Jenkins_home"
 command=java -jar %(ENV_HOME)s/Jenkins/jenkins.war --httpPort=8080 --enable-future-java

.. include:: includes/supervisord.rst

Your Jenkins is now up and running as a service.

Finally we'll setup our connection to the rest of the world.

Setup Web backend
-----------------

.. note::

    Jenkins is running on port 8080.

.. include:: includes/web-backend.rst

Finishing Installation
======================

First connect and initial password
----------------------------------

Now you can go to ``https://isabell.uber.space`` and see the Jenkins asking for your initial password. It will tell you the path where it is stored, most probably it should be in a file in ``~/Jenkins/Jenkins_home/secrets/initialAdminPassword``:

::

 [isabell@stardust ~]$ cat ~/Jenkins/Jenkins_home/secrets/initialAdminPassword
 SOMEHEXTHATIWONTTELLYOU
 [isabell@stardust ~]$

Copy and paste that and you'll be good to go. Just follow the setup and everything should work out.

Updates
=======

To jump to a new version just replace the old war with the new version.

.. note:: Recommended reading to follow along and go beyond this guide:

  * `Official Jenkins Manual <https://jenkins.io/doc/>`_
  * `Official Jenkins WAR guide <https://jenkins.io/doc/book/installing/#war-file>`_

.. _Jenkins: https://jenkins.io
.. author_list::
