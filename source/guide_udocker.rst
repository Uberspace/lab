.. highlight:: console

.. author:: katakombi <katakombi@gmail.com>

.. sidebar:: About

  .. image:: _static/images/udocker.png
      :align: center

####################
Qt5WebApp in UDocker
####################

UDocker is a python-based command line tool which allows to run docker containers in unprivileged user environments. Under the hood it can utilize a variety of container runtime engines.

----

.. note:: Since UDocker has a similar syntax as docker it is helpful to have some practical experience with docker

Short Description
=================

We will utilize UDocker to pull the official ubuntu container image. 
Then, we will install Qt5 and QtWebApp to run an example web application.

Installation
============

UDocker
-------

::

 [isabell@stardust ~] mkdir -p ~/.udocker
 [isabell@stardust ~] wget https://raw.githubusercontent.com/indigo-dc/udocker/019e4d663d226aaa0caa3b173da6d1ce8264a0ab/udocker.py -O ~/.udocker/udocker.py
 [isabell@stardust ~] chmod u+x ~/.udocker/udocker.py
 [isabell@stardust ~] ln -sf ~/.udocker/udocker.py ~/bin/udocker

Ubuntu 18:04
------------

::

 [isabell@stardust ~] udocker pull ubuntu:bionic
 [isabell@stardust ~] udocker create --name=Ubuntu_Qt5 ubuntu:bionic

Prepare the installation script (Qt5,g++,make,vim)

::

 [isabell@stardust ~] cat << EOF > ~/install.sh
 #!/bin/bash
 apt-get update && apt-get -y upgrade
 apt-mark hold dbus # dbus creates new groups upon installation which is not possible in udocker
 apt-get install -y vim make g++ qt5-default
 EOF
 [isabell@stardust ~] chmod a+x ~/install.sh

Execute the script as super user inside the container using a fakeroot-like environment

:: 

 [isabell@stardust ~] udocker run --user=root -v ~/install.sh -i -t Ubuntu_Qt5 ~/install.sh


Setup Qt5 WebApp
================

::

 [isabell@stardust ~] wget http://stefanfrings.de/qtwebapp/QtWebApp.zip -O ~/QtWebApp.zip
 [isabell@stardust ~] cd ~ && unzip ./QtWebApp.zip

Adapt port
----------

Find a free port

::

 [isabell@stardust ~] WWW_PORT=$(( $RANDOM % 4535 + 61000)); netstat -tulpen | grep $WWW_PORT && echo "try again"

Usually this gives you a free port on first try. If you see `try again` repeat the previous command.
Now we adapt the settings so that the external port 443 is being mapped to the local port.

::

 [isabell@stardust ~] cat << EOF > ~/html/.htaccess
 RewriteEngine On
 RewriteRule ^(.*)$ http://localhost:$WWW_PORT/$1 [P]
 EOF
 [isabell@stardust ~] sed -i 's/^port=8080/port='$WWW_PORT'/' ~/QtWebApp/Demo1/etc/Demo1.ini


Compile
-------

::

 [isabell@stardust ~] udocker run --user=$USER --hostauth --hostenv --bindhome -i -t Ubuntu_Qt5 /bin/sh -c 'cd ~/QtWebApp/Demo1/ && qmake && make'


Run
---

::

 [isabell@stardust ~] udocker run --user=$USER --hostauth --hostenv --bindhome Ubuntu_Qt5 /bin/sh -c 'cd ~/QtWebApp/Demo1/ && ./Demo1'&

Test installation
-----------------

::

 [isabell@stardust ~] wget http://localhost:$WWW_PORT/index.html/form

This command should retrieve the html form containing `city` and `name`.
Repeat this command using your uberspace account name

::

 [isabell@stardust ~] wget https://myuber.uber.space/index.html/form

Final words
-----------

This is just one of many examples where running an entire docker image in user space comes in handy.
UDocker allows manipulation of the container contents and hence very flexible setups can be performed rapidly.
However, not all docker images will run properly as some restrictions apply (e.g. privileged ports cannot be used).

Sources
=======

  * https://github.com/indigo-dc/udocker/
  * https://proot-me.github.io/
  * http://stefanfrings.de/qtwebapp/index.html

.. authors::
