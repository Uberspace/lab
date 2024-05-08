.. highlight:: console

.. author:: Julius Künzel
.. author:: Christian Strauch

.. tag:: web
.. tag:: sso
.. tag:: lang-java

.. spelling::
    Keycloak

.. sidebar:: Logo

  .. image:: _static/images/keycloak.svg
      :align: center

########
Keycloak
########

.. tag_list::

Keycloak is an open source identity and access management system which allows single sign-on for web applications and services.

----

.. note:: For this guide you should be familiar with the basic concepts of

  * :manual:`supervisord <daemons-supervisord>`
  * :manual:`Backends <web-backends>`

License
=======

Keycloak is released under the `Apache 2.0 license`_.

Prerequisites
=============

Your URL needs to be setup:

.. include:: includes/web-domain-list.rst

Installation
============

Download Keycloak
-----------------

Check the Keycloak_ website or `Github Repository`_ for the latest release and copy the download link to the .tar.gz file. Then use ``wget`` to download it. Replace the URL with the one you just got from GitHub.

.. code-block::

 [isabell@stardust ~]$ wget https://github.com/keycloak/keycloak/releases/download/24.0.3/keycloak-24.0.3.tar.gz
 […]
 Saving to: ‘keycloak-24.0.3.tar.gz’

 […]
 [isabell@stardust ~]$

Extract the archive
-------------------

Use ``tar`` to extract the archive and delete the archive. Replace the version in the archive file name with the one you just downloaded.

.. code-block::

 [isabell@stardust ~]$ tar -xvzf keycloak-24.0.3.tar.gz
 keycloak-24.0.3
 [isabell@stardust ~]$ ln -s ~/keycloak-24.0.3 ~/keycloak-current
 [isabell@stardust ~]$



You can now delete the archive:

.. code-block::

 [isabell@stardust ~]$ rm keycloak-24.0.3.tar.gz
 [isabell@stardust ~]$


Configuration
=============

Make sure the SSL certificates have been generated
--------------------------------------------------

After setting up the domain you want to use, access it once using your browser. Even though it won't show anything meaningful, this will make sure uberspace generates the SSL certificates and puts them into ``~/etc/certificates/``. We'll need those certificates to be there in the next step.

Change the configuration
------------------------

Delete everything inside the :file:`~/keycloak-current/conf/keycloak.conf`, and add the following. Replace mydbpassword with the database password output of ``my_print_defaults client`` and, as always, ``isabell`` with your uberspace username. Also replace ``isabell.uber.space`` with the domain name that you are using for keycloak.

.. code-block::

 db=mariadb
 db-username=isabell
 db-password=mydbpassword
 db-url-host=localhost
 db-url-database=isabell_keycloak
 transaction-xa-enabled=false
 http-enabled=true
 http-host=0.0.0.0
 http-port=8080
 hostname-strict=false
 hostname-strict-https=false
 proxy=edge
 https-certificate-file=/home/isabell/etc/certificates/isabell.uber.space.crt
 https-certificate-key-file=/home/isabell/etc/certificates/isabell.uber.space.key


Prepare the admin user
----------------------

Replace ``<username>`` with a user name and ``<password>`` with a password of your choice.

.. code-block::

 [isabell@stardust keycloak-current]$ export KEYCLOAK_ADMIN=<username>
 [isabell@stardust keycloak-current]$ export KEYCLOAK_ADMIN_PASSWORD=<username>
 [isabell@stardust keycloak-current]$

Build keycloak
--------------

.. code-block::

 [isabell@stardust keycloak-current]$ bin/kc.sh build
 […]
 [isabell@stardust keycloak-current]$


Setup daemon
------------

Use your favourite editor to create the file :file:`~/etc/services.d/keycloak.ini` with the following content. Note: it seems there is an issue following symlinks during keycloak startup, so we can't use ``~/keycloak-current`` - in case you downloaded a different version of keycloak, make sure the directory name is correct.

.. code-block:: ini

 [program:keycloak]
 directory=%(ENV_HOME)s/keycloak-24.0.3/
 command=%(ENV_HOME)s/keycloak-24.0.3/bin/kc.sh start --optimized
 autostart=yes
 autorestart=yes
 startsecs=20

.. include:: includes/supervisord.rst



Setup Backend
-------------

.. note::

    Keycloak is running on port 8080.

.. include:: includes/web-backend.rst


Finishing installation
======================

Point your Browser to your installation URL ``https://isabell.uber.space`` and use Keycloak!


A note regarding identity providers
===================================

In case you are intending to use Microsoft as an identity provider with keycloak, they will require you to verify your domain. An easy way to do that is to go through this process:
* temporarily delete the web backend using ``userspace web backend del isabell.uber.space``
* create a directory ``.well-known`` inside your ``/var/www/virtual/isabell/html``
* create a file ``microsoft-identity-association.json`` in that ``.well-known`` directory with the following contents:
.. code-block::

 {
   "associatedApplications": [
     {
       "applicationId": "<your Azure AD application ID>"
     }
   ]
 }

* start the validation in Microsoft's Azure AD console
* delete the ``.well-known`` directory once complete and recreate the web backend with ``uberspace web backend set [...]``


Tuning
======

For further information on configuration and usage read the `Keycloak Documentation`_.


.. author_list::
