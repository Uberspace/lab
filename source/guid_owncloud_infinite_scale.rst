.. highlight:: console

.. author:: TPhilipp Bielefeldt <philipp@bielefeldt.online>

.. tag:: golang
.. tag:: web
.. tag:: groupware
.. tag:: file-storage
.. tag:: sync
.. tag:: photo-management

#####
ownCloud Infinite Scale
#####

.. tag_list::

ownCloud Infinite Scale is a File Storage and Collaboration software written in Go.
It is distributed under the Apache-2.0 license by ownCloud GmbH.

----

.. note:: For this guide you should be familiar with the basic concepts of

  * :manual:`domains <web-domains>`

Prerequisites
=============

Before installing oCIS, make sure you have a domain ready.
Also, note that oCIS expects port 9200 to be available, which by default is blocked on uberspace.
Hence, you have to configures nginX to forward all requests to port 9200 of the local machine.

.. code-block:: console

 [isabell@stardust ~]$ uberspace web domain add myowncloud.isabell.uber.space
 [isabell@stardust ~]$ uberspace web backend set myowncloud.isabell.uber.space --http --port 9200

.. include:: includes/web-domain-list.rst

Since there is no local service running to answer port 9200, the "NOT OK" status you'll receive is to be expected here.

Now, download the latest version of oCIS from `ownCloud's website <https://download.owncloud.com/ocis/ocis/stable/?sort=time&order=desc>`_.

.. code-block:: console

 [isabell@stardust ~]$ curl https://download.owncloud.com/ocis/ocis/stable/4.0.1/ocis-4.0.1-linux-amd64 --output ocis
 [isabell@stardust ~]$ chmod +x ocis


Init
====

You need to set some parameters in order to get oCIS running:

.. code-block:: console

 [isabell@stardust ~]$ export OCIS_URL=https://myowncloud.isabell.uber.space
 [isabell@stardust ~]$ export PROXY_TLS=false
 [isabell@stardust ~]$ export PROXY_HTTP_ADDR=0.0.0.0:9200
 [isabell@stardust ~]$ export PROXY_LOG_LEVEL=warn

(This is for an inital trial set-up; later, add these to your .bashrc for instance.)
For information on the available settings, have a look at `the documentation <https://doc.owncloud.com/ocis/next/deployment/services/s-list/proxy.html#configuration>`_. 

Now, you can initialise your oCIS.

.. code-block:: console

 [isabell@stardust ~]$ ./ocis init
 Do you want to configure Infinite Scale with certificate checking disabled?
  This is not recommended for public instances! [yes | no = default] no
 
 =========================================
  generated OCIS Config
 =========================================
  configpath : /home/isabell/.ocis/config/ocis.yaml
  user       : admin
  password   : ***<you'll get your own here :-)>***

Safe the admin password you received.


Run Server
==========

Now, you should be ready to fire up the ownCloud Infinite Scale server.
You can do that by running

.. code-block:: console

 [isabell@stardust ~]$ ./ocis server &

Go to the URL you entered above (i.e. myowncloud.isabell.uber.space in this example).

You should be presented with the ownCloud login mask.
Enter the user ("admin") and password you got from the init step.

You should now be logged in as an administrator.
From here, you can use the Application Switcher to get to the Administration Settings.
There, create a new user as you like.
Use this user account to investigate the you own ownCloud.
