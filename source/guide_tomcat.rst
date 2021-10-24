.. highlight:: console

.. author:: Christian Macht <https://github.com/cmacht/>

.. tag:: lang-java
.. tag:: web

.. sidebar:: Logo

  .. image:: _static/images/tomcat.png
      :align: center

######
Tomcat
######

.. tag_list::

Tomcat_ is a free and open-source web server and servlet container in which Java code can run. It consists of several components: Catalina (a servlet container), Coyote (an HTTP connector) and Jasper (a Jakarta Server Pages engine). Tomcat is released under the `Apache 2.0 License <http://www.apache.org/licenses/LICENSE-2.0>`_.

----

.. note:: For this guide you should be familiar with the basic concepts of

  * :manual_anchor:`supervisord <daemons-supervisord>`
  * :manual_anchor:`web backends <web-backends>`



Prerequisites
=============

After logging in :manual_anchor:`with ssh <basics-ssh>`, check which Java version you are running and where it is located:

::

 [isabell@stardust ~]$ java --version
 openjdk 17 2021-09-14
 OpenJDK Runtime Environment 21.9 (build 17+35)
 OpenJDK 64-Bit Server VM 21.9 (build 17+35, mixed mode, sharing)
 [isabell@stardust ~]$ which java
 /usr/bin/java
 [isabell@stardust ~]$

Also check your URL and, if you like, set up :manual_anchor:`additional domains <web-domains>`:

.. include:: includes/web-domain-list.rst


Installation
============

Create application directory and files
--------------------------------------

First create a folder called ``tomcat``:

::

 [isabell@stardust ~]$ mkdir ~/tomcat
 [isabell@stardust ~]$


Next, download the `current version <https://tomcat.apache.org/download-10.cgi>`_ of Tomcat and unpack it into your new folder:

::

 [isabell@stardust ~]$ wget https://dlcdn.apache.org/tomcat/tomcat-10/v10.0.12/bin/apache-tomcat-10.0.12.tar.gz
 Resolving dlcdn.apache.org (dlcdn.apache.org)... 151.101.2.132, 2a04:4e42::644
 Connecting to dlcdn.apache.org (dlcdn.apache.org)|151.101.2.132|:443... connected.
 HTTP request sent, awaiting response... 200 OK
 Length: 11890640 (11M) [application/x-gzip]
 Saving to: ‘apache-tomcat-10.0.12.tar.gz’
 [isabell@stardust ~]$ tar --extract --file=apache-tomcat-10.0.12.tar.gz --directory=tomcat/ --strip-components=1
 [isabell@stardust ~]$


Configuration
==============

Set up service
--------------

Create the service file ``~/etc/services.d/tomcat.ini`` and fill it with:

::

 [program:tomcat]
 environment=CATALINA_HOME=%(ENV_HOME)s/tomcat
 command=%(ENV_HOME)s/tomcat/bin/catalina.sh run

You could explicitely set further environment variables like ``JAVA_HOME`` (required for debugging) or ``CATALINA_BASE`` (specify directories for multiple instances). These are documented in the initial comment block of ``~/tomcat/bin/catalina.sh`` but are not required for a minimal installation.

.. include:: includes/supervisord.rst

For your convenience, you may also want to create a symbolic link to the log file. Note the differences between ``catalina.out`` and ``catalina.YYYY-MM-DD.log`` explained `here <https://stackoverflow.com/questions/51985958/what-is-the-difference-between-catalina-out-and-catalina-yyyy-mm-dd-log-log>`_ .

::

 [isabell@stardust ~]$ ln -s ~/tomcat/logs/catalina.out ~/logs/tomcat.log


Tomcat is now up and running as a service. To make it accessible from the outside, we need to configure a web backend.



Set up web backend
------------------

.. note::

    Tomcat is running on port 8080. This is only relevant for the server but can nevertheless be changed in ``~/tomcat/conf/server.xml``.

.. include:: includes/web-backend.rst


At this point, Tomcat should be visible at ``https://isabell.uber.space``. However, to really make use of the management interface you still need to give yourself access.


Set up web management users
---------------------------

To make the management interface usable, edit ``~/tomcat/conf/tomcat-users.xml``. You will find several blocks of comments that you may want to delete or simply uncomment. Make sure to add this line and set an appropriate password:

::

 <tomcat-users>
     <user username="admin" password="SET-YOUR-PASSWORD" roles="manager-gui,admin-gui"/>
 </tomcat-users>

By default, Tomcat only allows connections coming from the server itself to access the Manager and Host Manager apps. Since it is installed on a remote machine, you will probably want to remove this restriction. Open the files at ``~/tomcat/webapps/manager/META-INF/context.xml`` and ``~/tomcat/webapps/host-manager/META-INF/context.xml`` and comment out the IP restrictions in **both** of them by adding ``<!-- ... -->`` like this:

::

 <Context antiResourceLocking="false" privileged="true" >
   <!--<Valve className="org.apache.catalina.valves.RemoteAddrValve"
         allow="127\.\d+\.\d+\.\d+|::1|0:0:0:0:0:0:0:1" />-->
 </Context>

Afterwards, restart the ``supervisord`` service:

::

 [isabell@stardust ~]$ supervisorctl restart tomcat
 [isabell@stardust ~]$


Tomcat should now be fully usable!

----

Tested with Uberspace 7.11.5 and Tomcat 10.0.12 on OpenJDK 17.


.. _Tomcat: http://tomcat.apache.org/
.. author_list::
