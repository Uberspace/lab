.. highlight:: console

.. author:: Nico Graf <hallo@uberspace.de>

.. tag:: lang-c
.. tag:: database
.. tag:: audience-developers

.. sidebar:: Logo

  .. image:: _static/images/redis.svg
      :align: center

##########
Redis
##########

.. tag_list::

Redis_ is a key-value store NoSQL database. It is primarily used because of its high read and write rates. Redis uses two columns, storing pairs of one key and one corresponding value.

----

.. note:: For this guide you should be familiar with the basic concepts of :manual:`supervisord <daemons-supervisord>`.


License
=======

Redis is distributed under the `BSD license`_.

Configuration
=============

Create the folder ``~/.redis/``:

.. code-block:: bash

 [isabell@stardust ~]$ mkdir ~/.redis/
 [isabell@stardust ~]$

Now create the config file ``~/.redis/conf`` with an editor of your choice and enter these settings. Replace ``<user>`` with your user name.

.. code-block:: none
 :emphasize-lines: 1

 unixsocket /home/<user>/.redis/sock
 daemonize no
 port 0
 save ""

Setup daemon
------------

Use your favourite editor to create ``~/etc/services.d/redis.ini`` with the following content:

.. code-block:: ini

 [program:redis]
 command=redis-server %(ENV_HOME)s/.redis/conf
 directory=%(ENV_HOME)s/.redis
 autostart=yes
 autorestart=yes

.. include:: includes/supervisord.rst

If it’s not in state RUNNING, check your configuration.

Accessing redis
---------------

Use the Unix socket ``~/.redis/sock`` to access redis with other applications. You can also use the ``redis-cli`` client to access the Redis shell:

.. code-block:: bash

 [isabell@stardust ~]$ redis-cli -s ~/.redis/sock
 redis /home/isabell/.redis/sock>

.. _Redis: https://redis.io/
.. _BSD license: https://github.com/antirez/redis/blob/unstable/COPYING

----

Tested with Redis 5.0.3, Uberspace 7.2.1.0

.. author_list::
