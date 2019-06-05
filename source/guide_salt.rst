.. author:: ctr49 <https://github.com/ctr49>

.. tag:: automation

.. highlight:: console

.. sidebar:: Logo

  .. image:: _static/images/saltstack.png
      :align: center

##########
SaltStack
##########

.. tag_list::

`SaltStack`_ (or simply `Salt`) is Python-based, open-source software for event-driven IT automation, remote task execution, and configuration management. Supporting the "Infrastructure as Code" approach to data center system and network deployment and management, configuration automation, SecOps orchestration, vulnerability remediation, and hybrid cloud control.

The `salt-master` controls so called `salt-minions` through formulae, pillars and grains. The scope of this guide is to install a `salt-master`(without a co-located minion) on an Uberspace.

----

.. note:: For this guide you should be familiar with the basic concepts of

  * :manual:`Opening ports <basics-ports>`
  * :manual:`supervisord <daemons-supervisord>`

Prerequisites
=============

We need two open TCP ports for minions to communicate with the Salt master.

::

 [user@host ~]$ uberspace port add
 Port <high-port1> will be open for TCP and UDP traffic in a few minutes.
 [user@host ~]$ uberspace port add
 Port <high-port2> will be open for TCP and UDP traffic in a few minutes.
 [user@host ~]$ uberspace port list
 <high-port1>
 <high-port2>

Take note of the high ports, you will need them for salt master configuration later.

Installation
============

Install salt-master
-------------------

The `salt` installation script requires root privileges and only supports virtualenv installation for Ubuntu. So we'll follow the `Developer installation` guide to install the salt master manually. However, we don't want the latest head development version, but the latest stable/tagged version. As of writing this guide, the latest stable version is 2019.2.1

::

 [user@host ~]$ mkdir -p ~/salt/src
 [user@host ~]$ cd ~/salt/src
 [user@host ~]$ git clone https://github.com/saltstack/salt
 [user@host ~]$ cd salt
 [user@host ~]$ git remote add upstream https://github.com/saltstack/salt
 [user@host ~]$ git fetch --tags upstream
 [user@host ~]$ git branch 2019.2.1
 [user@host ~]$ virtualenv ~/salt/virtualenv
 [user@host ~]$ source ~/salt/virtualenv/bin/activate
 [user@host ~]$ pip install pyzmq PyYAML pycrypto msgpack-python jinja2 psutil futures tornado
 [user@host ~]$ MIMIC_SALT_INSTALL=1 pip install --global-option='--salt-root-dir=~/salt/virtualenv/' -e ~/salt/src/salt
 [user@host ~]$ cp ~/salt/src/salt/conf/master ~/salt/virtualenv/etc/salt/


Configuration
=============

Edit `~/salt/virtualenv/etc/salt/master` and make at least the following changes:

::

 user: <your-user>
 publish_port: <first port the was added above>
 ret_port: <second port the was added above>
 root_dir: /home/<username>/salt/virtualenv


Setup daemon
------------

Create ``~/etc/services.d/salt-master.ini`` with the following content:

.. code-block:: ini

 [program:salt-master]
 process_name=salt-master
 command=/home/<username>/salt/virtualenv/bin/salt-master
 autostart=yes
 autorestart=yes

Tell ``supervisord`` to refresh its configuration and start the service:

::

 [user@host ~]$ supervisorctl reread
 salt-master: available
 [user@host ~]$ supervisorctl update
 salt-master: added process group
 [user@host ~]$ supervisorctl status
 salt-master                      RUNNING   pid 24968, uptime 0:00:05

If it's not in state RUNNING, check your configuration.

Finishing installation
======================

Connect minions
---------------

Now you can connect a minion to the salt master. The minion configuration needs the IP address of your Uberspace (or a hostname resolving to it) and the high-port you used as `ret_port` in the master configuration. An initial minion run will upload the minion private key to the master and you view and accept this key to establish communication:

.. code-block:: console

 [user@host ~]$ salt-key -L
 Accepted Keys:
 Denied Keys:
 Unaccepted Keys:
 <your-new-minion>
 Rejected Keys:


 [user@host ~]$ salt-key -a <your-new-minion>

Salt master is now setup with the first minion connected.


Tested with SaltStack 2019.2.1, Uberspace 7.3

.. author_list::
