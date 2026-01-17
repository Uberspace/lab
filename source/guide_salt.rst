.. author:: ctr49 <https://github.com/ctr49>

.. tag:: automation
.. tag:: lang-python

.. highlight:: console

.. sidebar:: Logo

  .. image:: _static/images/saltstack.png
      :align: center

##########
SaltStack
##########

.. tag_list::

`SaltStack <https://saltstack.com/>`_ (or simply `Salt`) is Python-based, open-source software for event-driven IT automation, remote task execution, and configuration management. Supporting the "Infrastructure as Code" approach to data center system and network deployment and management, configuration automation, SecOps orchestration, vulnerability remediation, and hybrid cloud control.

The ``salt-master`` controls so called ``salt-minions`` through formulae, pillars and grains. The scope of this guide is to install a ``salt-master`` (without a co-located minion) on an Uberspace.

Source code for SaltStack is available for review `on GitHub <https://github.com/saltstack/salt>`_ and `distributed under the Apache License 2.0 <https://github.com/saltstack/salt/blob/master/LICENSE>`_.

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

Installing Salt 3007.8 in a ``virtualenv`` using python 3.10. If you want to install a later version of salt look up the correct python version `here <https://docs.saltproject.io/salt/install-guide/en/latest/topics/salt-python-version-support.html>`)_ and replace the version numbers in the commands. Also installing pygit2 (because it is a dependency for any gitfs in Salt which is very common). Packages are installed in multiple steps as updated setuptools, pip and wheel may be needed for others to install. Download latest sample config as last step.

.. code-block:: console

 [isabell@stardust ~]$ python3.10 -m venv ~/salt_venv
 [isabell@stardust ~]$ source ~/salt_venv/bin/activate
 (salt_venv) [isabell@stardust ~]$ pip3.10 install -U setuptools pip wheel
 (salt_venv) [isabell@stardust ~]$ pip3.10 install -U pygit2
 (salt_venv) [isabell@stardust ~]$ pip3.10 install -r https://github.com/saltstack/salt/raw/refs/tags/v3007.8/requirements/base.txt
 (salt_venv) [isabell@stardust ~]$ pip3.10 install salt==3007.8
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


Setup daemon
------------

Create ``~/etc/services.d/salt-master.ini`` with the following content:

.. code-block:: ini

 [program:salt-master]
 process_name=salt-master
 command=%(ENV_HOME)s/salt_venv/bin/salt-master
 directory=%(ENV_HOME)s/salt_venv
 autostart=yes
 autorestart=yes

.. include:: includes/supervisord.rst

If it's not in state ``RUNNING``, check the logs.

Finishing installation
======================

Connect minions
---------------

Now you can connect a minion to the salt master. The minion configuration needs the IP address of your Uberspace (or a hostname resolving to it) and the following minimal configuration:

.. code-block:: yaml

 master: <IP or hostname of Uberspace>:<high-port2>
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
 (salt_venv) [isabell@stardust ~]$ pip3.10 install <any additional dependencies from newer version>
 (salt_venv) [isabell@stardust ~]$ pip3.10 install -U salt
 (salt_venv) [isabell@stardust ~]$ deactivate
 [isabell@stardust ~]$ supervisorctl restart salt-master



Tested with SaltStack 3001, Uberspace 7.7

.. author_list::
