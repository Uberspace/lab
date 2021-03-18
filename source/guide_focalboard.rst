.. highlight:: console

.. author:: Thomas Kammerer <https://kammerer.tk/>

.. tag:: web
.. tag:: project-management

.. sidebar:: Logo

  .. image:: _static/images/focalboard.svg
      :align: center

##########
Focalboard
##########

.. tag_list::

Focalboard_ is an open source, self-hosted alternative to Trello, Notion, and Asana. 

----

.. note:: For this guide you should be familiar with the basic concepts of

  * :manual:`supervisord <daemons-supervisord>`
  * :manual:`domains <web-domains>`

Prerequisites
=============

Your website domain needs to be set up:

.. include:: includes/web-domain-list.rst

Installation
============

Download the latest release_ to your home directory and extract the application.

.. code-block:: console

 [isabell@stardust ~]$ wget https://github.com/mattermost/focalboard/releases/download/v0.6.1/focalboard-linux.tar.gz
 [isabell@stardust ~]$ tar xzfv focalboard-linux.tar.gz
 [isabell@stardust ~]$


Configuration
=============

You need to change ``"localOnly": true`` to ``"localOnly": false`` in ``~/focalboard-app/config.json``

Setup daemon
------------

Create ``~/etc/services.d/focalboard.ini`` with the following content:

.. code-block:: ini

 [program:focalboard]
 directory=%(ENV_HOME)s/focalboard-app
 command=/home/focal/focalboard-app/focalboard-server
 autostart=yes
 autorestart=yes

.. include:: includes/supervisord.rst

Configure web server
--------------------

.. note::

    Focalboard is running on port 8088.

.. include:: includes/web-backend.rst

Configure application
---------------------

Open a browser and point it to the domain and you should be redirected to the login screen. Click the link to register a new user instead, and complete the registration.

The first user registration will always be permitted, but subsequent registrations will require an invite link which includes a code. You can invite additional users by clicking on your username in the top left, then selecting "Invite users".

Updates
-------

.. note:: Check the git repository_ regularly to stay informed about changes.

To update the application, stop the daemon and repeat the installation step.

.. _Focalboard: https://focalboard.com/
.. _release: https://github.com/mattermost/focalboard/releases/
.. _repository: https://github.com/mattermost/focalboard/

----

Tested with Focalboard 0.6.1 and Uberspace 7.10.0

.. author_list::
