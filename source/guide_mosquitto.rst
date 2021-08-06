.. highlight:: console

.. author:: André Birke <https://github.com/abirke>
.. author:: Tim Hetkämper <https://github.com/transistortim>

.. tag:: iot
.. tag:: lang-c
.. tag:: protocol-mqtt
.. tag:: publish-subscribe

.. sidebar:: About

  .. image:: _static/images/mosquitto.png
      :align: center

#########
Mosquitto
#########

.. tag_list::

Mosquitto_ is an open source MQTT message broker written in C. It also provides the tools ``mosquitto_sub`` and ``mosquitto_pub`` for subscription and publication.

----

License
=======

All relevant legal information can be found here

  * https://github.com/eclipse/mosquitto/blob/master/LICENSE.txt


Prerequisites
=============

If you want to use Mosquitto with a custom domain you need to set it up first:

.. include:: includes/web-domain-list.rst


Installation
============

Luckily, Mosquitto is preinstalled on Uberspace hosts.
We just need to configure it (see below).


Configuration
=============
We're setting up the broker to be reachable via a dedicated TCP port (as opposed to MQTT over WebSockets).
The communication will be secured using TLS encryption and password authentication.

Copy default config
-------------------

Copy the default (preinstalled) configuration to ``~/etc/mosquitto``.

.. code-block:: console
 :emphasize-lines: 1,2

 [isabell@stardust ~]$ mkdir -p ~/etc/mosquitto/
 [isabell@stardust ~]$ cp /etc/mosquitto/mosquitto.conf ~/etc/mosquitto/
 [isabell@stardust ~]$

Open firewall port
------------------

.. include:: includes/open-port.rst

Update config
-------------

Uncomment and update the following configuration values in ``~/etc/mosquitto/mosquitto.conf``.
Update ``certfile`` and ``keyfile`` to match the domain certificates you want to use Mosquitto with.
The last two values ensure that only registered users are allowed.

::

 cafile /etc/ssl/certs/ca-bundle.crt
 certfile /home/isabell/etc/certificates/isabell.uber.space.crt
 keyfile /home/isabell/etc/certificates/isabell.uber.space.key
 port 40132
 allow_anonymous false
 password_file /home/isabell/etc/mosquitto/passwd

Create user(s)
--------------

Create a password file for the first user. To add more users, omit ``-c``, which creates (overwrites) the given file.

.. code-block:: console
 :emphasize-lines: 1,2,3

 [isabell@stardust ~]$ mosquitto_passwd -c ~/etc/mosquitto/passwd isabell
 Password: [hidden]
 Reenter password: [hidden]
 [isabell@stardust ~]$


Finishing installation
======================

Setup daemon
------------

Create the file ``~/etc/services.d/mosquitto.ini`` with the following content:

.. code-block:: ini

  [program:mosquitto]
  command=mosquitto -c %(ENV_HOME)s/etc/mosquitto/mosquitto.conf
  autostart=yes
  autorestart=yes

.. include:: includes/supervisord.rst


Automate certificate reloading
------------------------------

To ensure Mosquitto uses the latest certificates, restart the service monthly, e.g. by creating a cron job via ``crontab -e``.

.. code-block:: none

 @monthly supervisorctl restart mosquitto > /dev/null


Test
====

.. note:: Note that the following commands expose your password to anyone who can view running processes, so use only with test data!

Subscription
------------

After successful subscription, incoming messages as well as pings are printed to the command line. Quit with ``CTRL+C``.

.. code-block:: console
 :emphasize-lines: 1,9

 [isabell@stardust ~]$ mosquitto_sub --host isabell.uber.space --port 40132 --topic isabellstesttopic --tls-version tlsv1.2 --cafile /etc/ssl/certs/ca-bundle.crt --username isabell --pw yoursecretpassword --debug
 Client mosq-XXXXXXXXXXXXXXXXXX sending CONNECT
 Client mosq-XXXXXXXXXXXXXXXXXX received CONNACK (0)
 Client mosq-XXXXXXXXXXXXXXXXXX sending SUBSCRIBE (Mid: 1, Topic: isabellstesttopic/, QoS: 0, Options: 0x00)
 Client mosq-XXXXXXXXXXXXXXXXXX received SUBACK
 Subscribed (mid: 1): 0
 Client mosq-XXXXXXXXXXXXXXXXXX sending PINGREQ
 Client mosq-XXXXXXXXXXXXXXXXXX received PINGRESP
 ^C
 [isabell@stardust ~]$

Publication
-----------

.. code-block:: console
 :emphasize-lines: 1

 [isabell@stardust ~]$ mosquitto_pub --message "Hello world" --host isabell.uber.space --port 40132 --topic isabellstesttopic --tls-version tlsv1.2 --cafile /etc/ssl/certs/ca-bundle.crt --username isabell --pw yoursecretpassword --debug
 Client mosq-XXXXXXXXXXXXXXXXXX sending CONNECT
 Client mosq-XXXXXXXXXXXXXXXXXX received CONNACK (0)
 Client mosq-XXXXXXXXXXXXXXXXXX sending PUBLISH (d0, q0, r0, m1, 'isabellstesttopic/', ... (11 bytes))
 Client mosq-XXXXXXXXXXXXXXXXXX sending DISCONNECT
 [isabell@stardust ~]$


.. _Mosquitto: https://mosquitto.org/

----

Tested with Mosquitto_ 1.6.10, Uberspace 7.7.9.0

.. author_list::
