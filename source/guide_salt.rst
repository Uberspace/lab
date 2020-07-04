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

The ``salt-master`` controls so called ``salt-minions`` through formulae, pillars and grains. The scope of this guide is to install a ``salt-master``(without a co-located minion) on an Uberspace.

----

.. note:: For this guide you should be familiar with the basic concepts of

  * :manual:`Opening ports <basics-ports>`
  * :manual:`supervisord <daemons-supervisord>`

Prerequisites
=============

We need two open TCP ports for minions to communicate with the Salt master.

.. code-block:: console

 [isabell@stardust ~]$ uberspace port add
 Port <high-port1> will be open for TCP and UDP traffic in a few minutes.
 [isabell@stardust ~]$ uberspace port add
 Port <high-port2> will be open for TCP and UDP traffic in a few minutes.
 [isabell@stardust ~]$ uberspace port list
 <high-port1>
 <high-port2>

Take note of the high ports, you will need them for salt master configuration later.

Installation
============

Install
-------

Installing salt in a a ``virtualenv`` using python 3.8 (latest available python on Uberspace). Also installing pygit2 as it is a dependency for any gitfs in Salt (which is very common).

.. code-block:: console

 [isabell@stardust ~]$ virtualenv -p python3.8 ~/salt_venv
 [isabell@stardust ~]$ source ~/salt_venv/bin/activate
 (salt_venv) [isabell@stardust ~]$ pip3.8 install -U setuptools pip wheel 
 (salt_venv) [isabell@stardust ~]$ pip3.8 install salt pygit2
 (salt_venv) [isabell@stardust ~]$ deactivate
 [isabell@stardust ~]$ mkdir -p ~/salt_venv/etc/salt ~/salt_venv/var/log/salt
 [isabell@stardust ~]$ curl https://raw.githubusercontent.com/saltstack/salt/master/conf/master -o ~/salt_venv/etc/salt/master
 

Configuration
=============

Edit ``~/salt_venv/etc/salt/master`` and make at least the following changes:

.. code-block:: yaml

 user: <your-user i.e. isabell>
 publish_port: <high-port1>
 ret_port: <high-port2>
 root_dir: <absolute path to venv i.e. /home/isabell/salt_venv>


Setup daemon
------------

Create ``~/etc/services.d/salt-master.ini`` with the following content:

.. code-block:: ini

 [program:salt-master]
 process_name=salt-master
 command=%(ENV_HOME)s/salt_venv/bin/salt-master -c ~/salt_venv/etc/salt
 directory=%(ENV_HOME)s/salt_venv
 autostart=yes
 autorestart=yes

Tell ``supervisord`` to refresh its configuration and start the service:

::

 [isabell@stardust ~]$ supervisorctl reread
 salt-master: available
 [isabell@stardust ~]$ supervisorctl update
 salt-master: added process group
 [isabell@stardust ~]$ supervisorctl status
 salt-master                      RUNNING   pid 24968, uptime 0:00:05

If it's not in state RUNNING, check your configuration.

Finishing installation
======================

Connect minions
---------------

Now you can connect a minion to the salt master. The minion configuration needs the IP address of your Uberspace (or a hostname resolving to it) and the following minimal configuration:

.. code-block:: yaml

 master: <IP or hostname of UberSpace>:<high-port2>
 publish_port: <high-port1>

An initial minion run will upload the minion public key to the master and you view and accept this key to establish communication:

.. code-block:: console

 [isabell@stardust ~]$ source ~/salt_venv/bin/activate
 (salt_venv) [isabell@stardust ~]$ salt-key -L
 Accepted Keys:
 Denied Keys:
 Unaccepted Keys:
 <your-new-minion>
 Rejected Keys:


 (salt_venv) [isabell@stardust ~]$ salt-key -a <your-new-minion>
 (salt_venv) [isabell@stardust ~]$ deactivate

Salt master is now setup with the first minion connected.

Updating Salt
=============

Update Salt in ``virtualenv``:

.. code-block:: console

 [isabell@stardust ~]$ source ~/salt_venv/bin/activate
 (salt_venv) [isabell@stardust ~]$ pip3.8 install -U salt
 (salt_venv) [isabell@stardust ~]$ deactivate
 [isabell@stardust ~]$ supervisorctl restart salt-master




Tested with SaltStack 3001, Uberspace 7.7

.. author_list::
