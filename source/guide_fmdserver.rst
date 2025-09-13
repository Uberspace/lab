.. author:: andyi-cpu

.. tag:: lang-go
.. tag:: web
.. tag:: findmydevice
.. tag:: smartfon
.. tag:: lineageos
.. highlight:: console

.. sidebar:: Logo

  .. image:: https://gitlab.com/uploads/-/system/project/avatar/24557720/favicon.ico?width=18
      :align: center

####################
FindMyDevice-Server
####################

.. tag_list::


FMD-Server_  is a web interface to locate your android device and send commands to it, take photos, lock or delete it.
A general Installation guide can be found on Gitlab-FMD-Server_ . (Mainpage)



----

Prerequisites
=============

A domain or subdomain, like $USER.uber.space to connect to your FMD-Server via web backend, the FMD-Server package from GitLab.



Installation
============

Download FMD Server:

Gitlab-FMD-Server_ (mainpage), download Link_ (releases): 


Rename the downloaded .zip to fmd-server.zip, unzip and copy the folder ``fmd-server`` to fmd-foss (you have the create this folder) into your ``/home/isabell/fmd-foss/``

Use any sftp programm like filezilla or use the shell to copy the servers source code to your webhost.

Start the FMD-Server:

.. code-block:: bash

     [isabell@stardust ~]$cd /home/isabell/fmd-foss/fmd-server/
     [isabell@stardust ~]$go run main.go serve
     # or
     [isabell@stardust ~]$go build
     [isabell@stardust ~]$./fmd-server serve
   
should result in:
   
.. code-block:: bash   

  atimestamp:  WRN no config found, using defaults
  atimestamp:  using config configFile=
  atimestamp:  INF starting FMD Server dbDir=./db/ version=v0.11.0 webDir=./web/
  atimestamp:  INF loading database
  atimestamp:  INF no SQLite DB found, creating one
  atimestamp:  INF listening on insecure port PortInsecure=8080


Bind the server, which shouĺd be running now (message above), to your domain via a web backend:

.. include:: includes/web-backend.rst

Now it should already work. You can try with your webbrowser. Before, you still have to restart your FMD-Server manually again. 
If your server is not running you will get a 502 Bad Gateway response.
Final step will be to let your system know about howto start fmd-server on it's own:

We have to create a new service with supervisord and a fmd-server.ini in  ``/home/isabell/etc/services.d/supervisord-fmd.ini``, 
with the following entries:

.. code-block:: ini

  [program:fmd-foss]
    directory=home/isabell/fmd-foss/fmd-server/
    command=home/isabell/fmd-foss/fmd-server/fmd-server serve
    autostart=yes
    autorestart=yes
    startsecs=30

In General:

.. include:: includes/supervisord.rst

You can use any sftp programm or your shell to copy your supervisord-fmd.ini. 
Afterwards, ask ``supervisord`` to look for the new ``supervisord-fmd.ini`` file, in your case it will look like this:

.. code-block:: bash

 [isabell@stardust ~]$ supervisorctl reread
 fmd-foss: available

Next step is to start your daemon:

.. code-block:: bash

 [isabell@stardust ~]$ supervisorctl update
 fmd-foss: added process group


Further Information about supervisord_ :


Ready, now you might want to prepare your android device/smartfon for login and testing:
On GitLab_ or F-Droid_ you will find the fmd-android packages.


Configuration
=============
Auto


Updates
=======
Should be ok. just to replace the code in your fmd-server folder and rebuild, read changelog.

Download Link_ (releases):


Rename the downloaded .zip to fmd-server.zip, unzip and replace the files and folders in  your  `/home/isabell/fmd-foss/``

Use any sftp programm like filezilla or use the shell to copy the servers source code to your webhost.

Start the FMD-Server:

.. code-block:: bash

     [isabell@stardust ~]$cd /home/isabell/fmd-foss/fmd-server/
     [isabell@stardust ~]$go run main.go serve
     # or
     [isabell@stardust ~]$go build
     [isabell@stardust ~]$./fmd-server serve
   
should result in:
   
.. code-block:: bash   

  atimestamp:  WRN no config found, using defaults
  atimestamp:  using config configFile=
  atimestamp:  INF starting FMD Server dbDir=./db/ version=v0.11.0 webDir=./web/
  atimestamp:  INF loading database
  atimestamp:  INF no SQLite DB found, creating one
  atimestamp:  INF listening on insecure port PortInsecure=8080




----

Backup
======
no backup

Remove
======
.. code-block:: bash

  [isabell@stardust ~]$ supervisorctl stop fmd-foss
  [isabell@stardust ~]$ supervisorctl remove fmd-foss
  [isabell@stardust ~]$ uberspace web backend del allcolorsarebeautiful.example
   
   Delete the fmd-foss folder and the supervisord-fmd.ini file.

.. _GitLab: https://gitlab.com/fmd-foss/fmd-android/ 
.. _F-Droid: https://f-droid.org/packages/de.nulide.findmydevice/
.. _Gitlab-FMD-Server: https://gitlab.com/fmd-foss/fmd-server/
.. _Link: https://gitlab.com/fmd-foss/fmd-server/-/releases/
.. _supervisord: https://manual.uberspace.de/daemons-supervisord/
.. _FMD-Server: https://gitlab.com/fmd-foss/fmd-server/

.. author_list::
