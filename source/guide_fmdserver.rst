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


`FMD-Server`_ is a web interface to locate your android device and send commands to it, take photos, lock or delete it.
A general Installation guide can be found on Gitlab. 
https://gitlab.com/fmd-foss/fmd-server (Mainpage)


----

Prerequisites
=============

A domain or subdomain to connect to your FMD-Server via web backend, The FMD-Server package from GitLab.



Installation
============

Download FMD Server:

https://gitlab.com/fmd-foss/fmd-server (Mainpage)

Download Link (11.9.2025)
https://gitlab.com/fmd-foss/fmd-server/-/archive/v0.11.0/fmd-server-v0.11.0.zip

Rename to fmd-server, unzip and copy the new folder fmd-server to fmd-foss (you have the create this folder) into your /home/isabell/fmd-foss/

Use any sftp programm like filezilla or use the shell to copy the servers source code to your webhost.

Start the FMD-Server:

.. code-block:: bash

    cd /home/isabell/fmd-foss/fmd-server/
    go run main.go serve
    # or
    go build
   ./fmd-server serve
   
should result in:
   
.. code-block:: bash   

   WRN no config found, using defaults
   using config configFile=
   INF starting FMD Server dbDir=./db/ version=v0.11.0 webDir=./web/
   INF loading database
   INF no SQLite DB found, creating one
   INF listening on insecure port PortInsecure=8080


Bind the server which shouĺd be running now to your domain via a web backend:

.. code-block:: bash

   [isabell@stardust ~]$ uberspace web backend set allcolorsarebeautiful.example --http --port 8080
   Set backend for allcolorsarebeautiful.example/ to port 8080; please make sure something is listening!
   You can always check the status of your backend using "uberspace web backend list".

Further informations about ubers web-backends: 
https://manual.uberspace.de/web-backends/

Now should already work. You can try with your browser. But before you still have to restart your FMD-Server manually again. 
If your server is not running you will get a 502 Bad Gateway response.
Final Step will be to let your system know abou howto start fmd-server on it's own:

We have to create a new service with supervisord and a fmd-server.ini in  ``/home/isabell/etc/services.d/supervisord-fmd.ini``, 
with the following entries:

.. code-block:: ini

  [program:fmd-foss]
    directory=home/isabell/fmd-foss/fmd-server/
    command=home/isabell/fmd-foss/fmd-server/fmd-server serve
    autostart=yes
    autorestart=yes
    startsecs=30

You can user any sftp programm or your shell to copy your supervisord-fmd.ini. 
Afterwards, ask ``supervisord`` to look for the new ``supervisord-fmd.ini`` file:

.. code-block:: bash

 [isabell@stardust ~]$ supervisorctl reread
 fmd-foss: available

Next step is to start your daemon:

.. code-block:: bash

 [isabell@stardust ~]$ supervisorctl update
 fmd-foss: added process group


Further Information about supervisord:
https://manual.uberspace.de/daemons-supervisord/

Ready, it's the time you might want to prepare a android device/smartfon for login and testing:

https://gitlab.com/fmd-foss/fmd-android or https://f-droid.org/packages/de.nulide.findmydevice/

Configuration
=============
Auto


Updates
=======
Should be ok. just to replace the code in your fmd-server folder and rebuid, read changelog.

----

Backup
======
no backup

Remove
======
.. code-block:: bash

   supervisorctl stop fmd-foss
   supervisorctl remove fmd-foss
   uberspace web backend del allcolorsarebeautiful.example
   
   Delete the fmd-foss folder and the supervisord-fmd.ini file.


.. author_list::
