.. highlight:: console

.. author:: Thomas Johnson <https://johnson.tj/>

.. tag:: file-storage
.. tag:: lang-go
.. tag:: privacy

###
ots
###

.. tag_list::

ots_  is a one-time-secret sharing platform. The secret is encrypted with a symmetric 256bit AES encryption in the browser before being sent to the server. Afterwards an URL containing the ID of the secret and the password is generated. The password is never sent to the server so the server will never be able to decrypt the secrets it delivers with a reasonable effort. Also the secret is immediately deleted on the first read.

----

.. note:: For this guide you should be familiar with the basic concepts of

  * :manual:`domains <web-domains>`
  * :manual:`supervisord <daemons-supervisord>`
  * :manual:`web backends <web-backends>`

Installation
============

We create the working directory, download the latest version and extract the file.

.. code-block:: console

 [isabell@stardust ~]$ mkdir ots
 [isabell@stardust ~]$ cd ots
 [isabell@stardust ots]$ wget https://github.com/Luzifer/ots/releases/download/v1.15.1/ots_linux_amd64.tgz
 [isabell@stardust ots]$ tar -xzf ots_linux_amd64.tgz
 [isabell@stardust ots]$ rm ots_linux_amd64.tgz
 [isabell@stardust ots]$

Customization
=============

.. note::
    This step is optional.
    
In order to be adjustable to your needs there are some ways to customize your OTS setup. All of those require you to create a YAML file containing the definitions of your customizations and to load this file through the ``--customize=~/ots/customize.yaml``. Check out customization_  for more information and add this option to your service command in the next step.

Service
=======

Now you should set up a service that keeps ots alive while you are gone. Create the file ``~/etc/services.d/ots.ini`` with the following content:

.. code-block:: ini

 [program:ots]
 command=%(ENV_HOME)s/ots/ots
 autostart=yes
 autorestart=yes
 startsecs=30

.. include:: includes/supervisord.rst

Web Backend
===========

.. note::

    ots should now be running on port 3000.

.. include:: includes/web-backend.rst

Updates
=======

.. note:: Check the update feed_ regularly to stay informed about the newest version.

Change the version and repeat the installation step.


.. _ots: https://github.com/Luzifer/ots/
.. _customization: https://github.com/Luzifer/ots/wiki/Customization/
.. _feed: https://github.com/Luzifer/ots/releases.atom


----

Tested with ots 1.15.1, Uberspace 7.16.4

.. author_list::
