.. highlight:: console

.. author:: Nico Graf <hallo@uberspace.de>

.. sidebar:: Logo

  .. image:: _static/images/redis.svg
      :align: center

##########
Redis
##########

Redis_ is a key-value store NoSQL database. It is primarily used because of its high read and write rates. Redis uses two columns, storing pairs of one key and one corresponding value.

----

.. note:: For this guide you should be familiar with the basic concepts of supervisord_.


License
=======

Redis is distributed under the `BSD license`_.

Installation
============

Download Redis
--------------

.. code-block:: bash

 [isabell@stardust ~]$ wget http://download.redis.io/redis-stable.tar.gz -O ~/redis-stable.tar.gz
 --2019-01-03 13:51:21--  http://download.redis.io/redis-stable.tar.gz
 Resolving download.redis.io (download.redis.io)... 109.74.203.151
 Connecting to download.redis.io (download.redis.io)|109.74.203.151|:80... connected.
 HTTP request sent, awaiting response... 200 OK
 Length: 1999982 (1.9M) [application/x-gzip]
 Saving to: ‘/home/isabell/redis-stable.tar.gz’

 100%[======================================>] 1,999,982   --.-K/s   in 0.07s

 2019-01-03 13:51:21 (27.3 MB/s) - ‘redis-stable.tar.gz’ saved [1999982/1999982]


Extract Redis
--------------------------
.. code-block:: bash

 [isabell@stardust ~]$ tar xfv redis-stable.tar.gz
 redis-stable/
 redis-stable/INSTALL
 […]
 redis-stable/CONTRIBUTING
 redis-stable/redis.conf
 redis-stable/runtest-cluster
 [isabell@stardust ~]$ 


Build Redis
-----------

.. code-block:: bash

 [isabell@stardust ~]$ cd redis-stable/
 [isabell@stardust ~]$ make
 cd src && make all
 make[1]: Entering directory `/home/isabell/redis-stable/src'
     CC Makefile.dep
 make[1]: Leaving directory `/home/isabell/redis-stable/src'
 […]
     LINK redis-benchmark
     INSTALL redis-check-rdb
     INSTALL redis-check-aof

 Hint: It's a good idea to run 'make test' ;)

 make[1]: Leaving directory `/home/isabell/redis-stable/src'
 [isabell@stardust redis-stable]$ 

Try running ``src/redis-server`` to make sure everything works:

.. code-block:: bash

 [isabell@stardust redis-stable]$ src/redis-server --unixsocket ~/tmp/redis.sock
 16813:C 03 Jan 2019 14:02:49.774 # oO0OoO0OoO0Oo Redis is starting oO0OoO0OoO0Oo
 16813:C 03 Jan 2019 14:02:49.774 # Redis version=5.0.3, bits=64, commit=00000000, modified=0, pid=16813, just started
 16813:C 03 Jan 2019 14:02:49.774 # Warning: no config file specified, using the default config. In order to specify a config file use src/redis-server /path/to/re
 dis.conf
 16813:M 03 Jan 2019 14:02:49.775 # You requested maxclients of 10000 requiring at least 10032 max file descriptors.
 16813:M 03 Jan 2019 14:02:49.775 # Server can't set maximum open files to 10032 because of OS error: Operation not permitted.
 16813:M 03 Jan 2019 14:02:49.775 # Current maximum open files is 4096. maxclients has been reduced to 4064 to compensate for low ulimit. If you need higher maxcli
 ents increase 'ulimit -n'.
                 _._
            _.-``__ ''-._
       _.-``    `.  `_.  ''-._           Redis 5.0.3 (00000000/0) 64 bit
   .-`` .-```.  ```\/    _.,_ ''-._
  (    '      ,       .-`  | `,    )     Running in standalone mode
  |`-._`-...-` __...-.``-._|'` _.-'|     Port: 6379
  |    `-._   `._    /     _.-'    |     PID: 16813
   `-._    `-._  `-./  _.-'    _.-'
  |`-._`-._    `-.__.-'    _.-'_.-'|
  |    `-._`-._        _.-'_.-'    |           http://redis.io
   `-._    `-._`-.__.-'_.-'    _.-'
  |`-._`-._    `-.__.-'    _.-'_.-'|
  |    `-._`-._        _.-'_.-'    |
   `-._    `-._`-.__.-'_.-'    _.-'
       `-._    `-.__.-'    _.-'
           `-._        _.-'
               `-.__.-'

 16813:M 03 Jan 2019 14:02:49.776 # WARNING: The TCP backlog setting of 511 cannot be enforced because /proc/sys/net/core/somaxconn is set to the lower value of 128.
 16813:M 03 Jan 2019 14:02:49.776 # Server initialized
 16813:M 03 Jan 2019 14:02:49.776 # WARNING overcommit_memory is set to 0! Background save may fail under low memory condition. To fix this issue add 'vm.overcommit_memory = 1' to /etc/sysctl.conf and then reboot or run the command 'sysctl vm.overcommit_memory=1' for this to take effect.
 16813:M 03 Jan 2019 14:02:49.776 # WARNING you have Transparent Huge Pages (THP) support enabled in your kernel. This will create latency and memory usage issues with Redis. To fix this issue run the command 'echo never > /sys/kernel/mm/transparent_hugepage/enabled' as root, and add it to your /etc/rc.local in order to retain the setting after a reboot. Redis must be restarted after THP is disabled.
 16813:M 03 Jan 2019 14:02:49.776 * DB loaded from disk: 0.000 seconds
 16813:M 03 Jan 2019 14:02:49.776 * Ready to accept connections

If the last line reads ``Ready to accept connections``, everything looks good and you can exit the program with ``Ctrl`` + ``C``.

Copy the ``redis-server`` and ``redis-cli`` binaries to your `~/bin` folder:

.. code-block:: bash

 [isabell@stardust ~]$ cp ~/redis-stable/src/redis-server ~/bin/
 [isabell@stardust ~]$ cp /redis-stable/src/redis-cli ~/bin/
 [isabell@stardust ~]$ 

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

Setup daemon
------------

Use your favourite editor to create ``~/etc/services.d/redis.ini`` with the following content:

.. code-block:: ini

 [program:redis]
 command=%(ENV_HOME)s/bin/redis-server %(ENV_HOME)s/.redis/conf
 autostart=yes
 autorestart=yes

Tell supervisord_ to refresh its configuration and start the service:

.. code-block:: bash

 [isabell@stardust ~]$ supervisorctl reread
 redis: available
 [isabell@stardust ~]$ supervisorctl update
 redis: added process group
 [isabell@stardust ~]$ supervisorctl status
 redis                            RUNNING   pid 18943, uptime 0:00:47
 [isabell@stardust ~]$

If it's not inIf it’s not in state RUNNING, check your configuration.

Accessing redis
---------------

Use the Unix socket ``~/.redis/sock`` to access redis with other applications. You can also use the ``redis-cli`` client to access the Redis shell:

.. code-block:: bash

 [isabell@stardust ~]$ redis-cli -s ~/.redis/sock
 redis /home/isabell/.redis/sock>

.. _Redis: https://redis.io/
.. _BSD license: https://github.com/antirez/redis/blob/unstable/COPYING
.. _supervisord: https://manual.uberspace.de/en/daemons-supervisord.html

----

Tested with Redis 5.0.3, Uberspace 7.2.1.0

.. authors::

