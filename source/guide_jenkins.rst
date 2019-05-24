.. highlight:: console

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

Jenkins_ is an open source automation server written in Java. Jenkins_ helps to automate the non-human part of the software development process, with continuous integration and facilitating technical aspects of continuous delivery. It is a server-based system that runs in servlet containers such as Apache Tomcat. It supports version control tools, including AccuRev, CVS, Subversion, Git, Mercurial, Perforce, TD/OMS, ClearCase and RTC, and can execute Apache Ant, Apache Maven and sbt based projects as well as arbitrary shell scripts and Windows batch commands. The creator of Jenkins_ is Kohsuke Kawaguchi. Released under the MIT License, Jenkins_ is free software.

Builds can be triggered by various means, for example by commit in a version control system, by scheduling via a cron-like mechanism and by requesting a specific build URL. It can also be triggered after the other builds in the queue have completed. Jenkins_ functionality can be extended with plugins.

----

.. note:: For this guide you should be familiar with the basic concepts of

  * :manual_anchor:`supervisord <daemons-supervisord>`
  * :manual_anchor:`web backends <web-backends>`

.. note:: Recommended reading to follow along and go beyond this guide:

  * `Official Jenkins Manual <https://jenkins.io/doc/>`_
  * `Official Jenkins WAR guide <https://jenkins.io/doc/book/installing/#war-file>`_

License
=======

Jenkins_ is released under the `MIT License <https://github.com/jenkinsci/jenkins/blob/master/LICENSE.txt>`_.

Prerequisites
=============

We're using java version 8 or 11 (9, 10 and 12 are currently not supported) `Supported Java Versions <https://jenkins.io/doc/administration/requirements/java/>`_.

::

 [isabell@stardust ~]$ java -version
 openjdk version "1.8.0_212"
 OpenJDK Runtime Environment (build 1.8.0_212-b04)
 OpenJDK 64-Bit Server VM (build 25.212-b04, mixed mode)
 [isabell@stardust ~]$

Your URL needs to be setup:

.. include:: includes/web-domain-list.rst


Installation
============

Create Workspace
----------------

First create a folder called ``Jenkins`` and a subfolder called ``jenkins_home``.
jenkins_home will hold all your Jenkins's data.

::

 [isabell@stardust ~]$ mkdir ~/Jenkins/jenkins_home -p
 [isabell@stardust ~]$


Download Jenkins_
-----------------

Next we download the current version of Jenkins:

::

 [isabell@stardust ~]$ wget -O Jenkins/jenkins.war http://mirrors.jenkins.io/war/latest/jenkins.war
 [isabell@stardust ~]$


At this point you would already be able to run Jenkins, but you wouldn't be able to connect to it and it would not run as a service.

Speaking of service:

Configurtation
==============

Install service
---------------

We create the service file ``~/etc/services.d/jenkins.ini`` and fill it with:

::

 [program:jenkins]
 directory=%(ENV_HOME)s/Jenkins/jenkins_home
 command=java -jar ../jenkins.war


After that refresh and update the daemons and check if everything worked out:

::

 [isabell@stardust ~]$ supervisorctl reread
 jenkins: available
 [isabell@stardust ~]$ supervisorctl update
 jenkins: added process group
 [isabell@stardust ~]$ supervisorctl status
 jenkins                          RUNNING   pid 4711, uptime 0:47:11
 [isabell@stardust ~]$

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

Now you can go to ``https://isabell.uber.space`` and see the Jenkins asking for your initial password. It is stored in ``~/Jenkins/jenkins_home/secrets/initialAdminPassword``.

::

 [isabell@stardust ~]$ cat jenkins_home/secrets/initialAdminPassword
 SOMEHEXTHATIWONTTELLYOU
 [isabell@stardust ~]$

Just copy and paste that and you'll be good to go. Just follow the setup and everything should work out.

Updates
=======

Do jump to a new version just replace the old war with the new version.

.. _Jenkins: https://jenkins.io
.. author_list::
