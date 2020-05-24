.. highlight:: console

.. author:: Lukas Bockstaller <lukas.bockstaller@posteo.de>

.. tag:: lang-c
.. tag:: database
.. tag:: audience-developers

.. sidebar:: Logo

  .. image:: _static/images/memcached.svg
      :align: center

##########
Memcached
##########

.. tag_list::

Memcached is an in-memory key-value store for small chunks of arbitrary data (strings, objects) from results of database calls, API calls, or page rendering.

----

.. note:: For this guide you should be familiar with the basic concepts of :manual:`supervisord <daemons-supervisord>`.


License
=======

Memcached is distributed under the `Revised BSD license`_.

Installation
============

Download memcached
------------------

.. code-block:: console

 [isabell@stardust ~]$ wget https://memcached.org/latest -O ~/memcached-latest.tar.gz
 --2020-01-17 17:41:28--  https://memcached.org/latest
 Resolving memcached.org (memcached.org)... 107.170.231.145
 Connecting to memcached.org (memcached.org)|107.170.231.145|:443... connected.
 HTTP request sent, awaiting response... 302 Moved Temporarily
 Location: https://www.memcached.org/files/memcached-1.5.20.tar.gz [following]
 --2020-01-17 17:41:29--  https://www.memcached.org/files/memcached-1.5.20.tar.gz
 Resolving www.memcached.org (www.memcached.org)... 107.170.231.145
 Connecting to www.memcached.org (www.memcached.org)|107.170.231.145|:443... connected.
 HTTP request sent, awaiting response... 200 OK
 Length: 531035 (519K) [application/octet-stream]
 Saving to: '/home/isabell/memcached-latest.tar.gz'

 100%[================================================>] 531,035      810KB/s   in 0.6s

 2020-01-17 17:41:31 (810 KB/s) - '/home/isabell/memcached-latest.tar.gz' saved [531035/531035]


Extract memcached
--------------------------
.. code-block:: console

 [isabell@stardust ~]$ tar -zxvf memcached-latest.tar.gz
 memcached-1.5.20/
 memcached-1.5.20/m4/
 […]
 memcached-1.5.20/sasl_defs.c
 memcached-1.5.20/Makefile.am
 memcached-1.5.20/jenkins_hash.c
 [isabell@stardust ~]$


Build memcached
---------------

.. code-block:: console

 [isabell@stardust ~]$ cd memcached-1.x.x/
 [isabell@stardust memcached-1.x.x]$ ./configure && make && make test
 checking build system type... x86_64-pc-linux-gnu
 checking host system type... x86_64-pc-linux-gnu
 checking for a BSD-compatible install... /usr/bin/install -c
 […]
 File 'slabs.c' Lines executed:86.53% of 616 Creating 'slabs.c.gcov' File '/usr/include/stdlib.h' Lines executed:50.00% of 2 Creating 'stdlib.h.gcov'
 File 'stats.c' Lines executed:90.36% of 83 Creating 'stats.c.gcov'
 File 'thread.c' Lines executed:81.43% of 377 Creating 'thread.c.gcov'
 File 'util.c' Lines executed:87.96% of 108 Creating 'util.c.gcov'
 [isabell@stardust memcached-1.x.x]$

Try running ``memcached`` to make sure everything works:

.. code-block:: console

 [isabell@stardust memcached-1.x.x]$ ./memcached -vvvv
 slab class   1: chunk size        96 perslab   10922
 slab class   2: chunk size       120 perslab    8738
 slab class   3: chunk size       152 perslab    6898
 slab class   4: chunk size       192 perslab    5461
 […]
 Nothing left to crawl for 251
 Nothing left to crawl for 252
 Nothing left to crawl for 253
 Nothing left to crawl for 254
 Nothing left to crawl for 255
 LRU crawler thread sleeping

If no errors occur, then everything should be fine and you can exit the program with ``Ctrl`` + ``C``.

Copy the ``memcached`` binary to your `~/bin` folder:

.. code-block:: console

 [isabell@stardust memcached-1.x.x]$ cp memcached ~/bin/
 [isabell@stardust memcached-1.x.x]$

Configuration
=============

Setup daemon
------------

Use your favourite editor to create ``~/etc/services.d/memcached.ini`` with the following content:

.. code-block:: ini

 [program:memcached]
 command=memcached --port 11211 --listen=127.0.0.1
 autostart=yes
 autorestart=yes

.. include:: includes/supervisord.rst

If it’s not in state RUNNING, check your configuration.

Testing memcached
-----------------

Test if memcached is responding on it's assigned port by issuing the following command to display the current configuration parameters.

.. code-block:: console

 [isabell@stardust ~]$ echo "stats settings" | nc localhost 11211
 STAT maxbytes 67108864
 STAT maxconns 1024
 STAT tcpport 2021
 […]
 STAT worker_logbuf_size 65536
 STAT track_sizes no
 STAT inline_ascii_response no
 END
 [isabell@stardust ~]$

Alternative configurations
--------------------------

Memcached can be configured to listen for connections using TCP, UDP or Unix sockets and tuned to maximize performance.
The official documentation_ lists the possible options.

Updates
=======

To update memcached, repeat the Installation steps followed by a restart using ``supervisorctl restart memcached``. Periodically check the changelog_ to learn about new versions.


.. _memcached: https://memcached.org/
.. _Revised BSD license: https://github.com/memcached/memcached/blob/master/LICENSE
.. _documentation: https://github.com/memcached/memcached/wiki/ConfiguringServer
.. _changelog: https://github.com/memcached/memcached/wiki/ReleaseNotes


----

Tested with memcached 1.5.20, Uberspace 7.3.10.0

.. author_list::

