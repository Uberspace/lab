.. highlight:: console

.. author:: revilowaldow <oliver@warlow.engineer>
.. author:: Glumbosch <glumbosch.home.blog>

.. tag:: self-hosting
.. tag:: web

.. sidebar:: Logo

  .. image:: _static/images/foundryvtt.png
      :align: center

############
Foundry VTT
############

.. tag_list::

`Foundry Virtual Tabletop <https://foundryvtt.com/>`_ is an alternative to Roll20 and many other platforms that enable you to play tabletop role playing games online.

Prerequisites
==============

Foundry VTT License
--------------------

Foundry is not free software, but you can host it on your own server.

The first step is to purchase a license from their `website <https://foundryvtt.com/>`_.
  
If you pay by SEPA transfer the payment can take up to a week, faster payment methods are available.

Set the node js version
--------------------------

Connect to your Uberspace server with :manual:`ssh <basics-ssh>`.

Foundry uses something called :manual:`Node.js <lang-nodejs>`; we need to tell our Uberspace server to use version 14.


Paste the following command into your ssh window:

::

 [isabell@stardust ~]$ uberspace tools version use node 14
 Selected Node.js version 14
 [isabell@stardust ~]$

To verify the change you can enter:

::

 [isabell@stardust ~]$ uberspace tools version show node
 Using 'Node.js' version: '14'
 [isabell@stardust ~]$

Installation
======================

Prepare installation folders
-----------------------------

Create the required directories:

::

[isabell@stardust ~]$ mkdir ~/foundryvtt
[isabell@stardust ~]$ mkdir ~/foundrydata
[isabell@stardust ~]$

To check that you did this correctly you can type ``ls`` which will show you a list of what is in the folder.


Downloading and Unpacking
-----------------------------

We will now download the software to the server. 

First change the folder you are in from the home folder to **foundryvtt** by using the following command:

::

[isabell@stardust ~]$ cd foundryvtt
[isabell@stardust foundryvtt]$

You will need to get a link from the Foundry VTT website, the link expires after a few minutes.

Copy the link for the linux version that you can find on your purchased licenses page.

Then use the following command with your link:

::

[isabell@stardust foundryvtt]$ wget -O foundryvtt.zip "https://foundryvtt.s3.amazonaws.com/longlink-xxxxxxxxxxxxxxxxxxxxxxxxxx"
[isabell@stardust foundryvtt]$

After the download has completed, unzip the package with this command:

::

[isabell@stardust foundryvtt]$ unzip foundryvtt.zip
[isabell@stardust foundryvtt]$

Once you have done this, change back to the home folder with:

::

[isabell@stardust foundryvtt]$ cd ..
[isabell@stardust ~]$


Configuration
=============

Open Port 30000
---------------

So that you and your players can connect to Foundry you need to run the following command to open a port:

::

[isabell@stardust ~]$ uberspace web backend set / --http --port 30000
[isabell@stardust ~]$

Set Foundry to Autorun
----------------------

So that Foundry is automatically started we need to create a service.

To do this create a config file in the folder ``etc/services.d/foundry.ini`` with the following contents.

.. code-block:: ini

 [program:foundry]
 command=node %(ENV_HOME)s/foundryvtt/resources/app/main.js –dataPath=%(ENV_HOME)s/foundrydata
 autostart=yes
 autorestart=yes


.. include:: includes/supervisord.rst

Finishing installation
======================

Your Foundry server can now be visited at https://isabell.uber.space


Best practices
==============

Security
--------

When you open Foundry for the first time you will have to provide your license key and accept the Service Agreement.
**Immediately after doing this set an administrator password in the Config tab.**

As of version ``0.8.7`` Foundry has greatly improved password security for world users. **It is strongly reccomended to use 0.8.7 or higher for this reason.**

When you create a world in Foundry it does not have a password by default, please immediately create one and do not reuse the Foundry admin password.


----
Tested with Foundry 0.8.7, Uberspace 7.1.1

.. author_list::
