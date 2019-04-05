.. highlight:: console

.. author:: pvitt <pvitt@posteo.de>

########
GoAccess
########

GoAccess is an open source real-time web log analyzer and interactive viewer that runs in a terminal or through your browser. It provides fast and valuable HTTP statistics for system administrators that require a visual server report on the fly.

Its core idea is to quickly analyze and view web server statistics in real time without needing to use your browser (great if you want to do a quick analysis of your access log via SSH, or if you simply love working in the terminal). While the terminal output is the default output, it has the capability to generate a complete, self-contained real-time HTML report (great for analytics, monitoring and data visualization), as well as a JSON, and CSV report.

Installation
============

Step 1
------

Choose one of the installation methods from the `GoAccess Installation page`_. This guide installs GoAccess by cloning the latest testing version from the `GitHub repository`_.

::

  [isabell@stardust ~]$ git clone https://github.com/allinurl/goaccess.git
  [...]
  [isabell@stardust ~]$ cd goaccess
  [isabell@stardust goaccess]$

Alternatively, download the latest version via wget:

::

  [isabell@stardust ~]$ wget https://tar.goaccess.io/goaccess-1.3.tar.gz
  [isabell@stardust ~]$ tar -xzvf goaccess-1.3.tar.gz
  [isabell@stardust ~]$ cd goaccess-1.3/
  [isabell@stardust goaccess-1.3]$

.. warning:: This guide is created using Github, thus the path of the downloaded files is ``goaccess``. If you downloaded the tar archive, please note that this extracts to a folder containing the version number, currently being 1.3, so that the folder is ``goaccess-1.3``.

Step 2
------

After downloading the sources, we need to build the executable.

::

  [isabell@stardust goaccess]$ autoreconf --force --install
  [...]
  [isabell@stardust goaccess]$

autoreconf adapts the build environment to your uberspace:

  * ``--force``: consider all files obsolete
  * ``--install``: copy missing auxiliary files

::

  [isabell@stardust goaccess]$ ./configure --enable-geoip --enable-utf8 --prefix=$HOME
  [...]
  [isabell@stardust goaccess]$

The ``--prefix`` option tells make to install GoAccess_ to your home directory. The other two flags ``--enable-geoip`` and ``--enable-utf8`` are suggested by GoAccess_ and enable support for UTF-8 formatted files as well as support for trying to locate users according to their IP addresses.

::

  [isabell@stardust goaccess]$ make
  [...]
  [isabell@stardust goaccess]$ make install
  [...]
  [isabell@stardust goaccess]$

Configuration
=============

Now GoAccess_ is already available. To use it, the configuration needs to be adjusted to the local environment. This is done by editing the configuration file ``~/etc/goaccess/goaccess.conf``.

1. Activate the time format ``time-format %H:%M:%S``
2. Activate the date format ``date-format %d/%b/%Y``
3. Activate the log format ``log-format COMBINED``

All other settings can be configured to your liking. See the man page for more information.

Usage
=====

To use GoAccess_, it has to know which log file to parse. Your uberspace web server log is in ``~/logs/webserver/access_log``, thus we need to call GoAccess_ with this path:

::

  [isabell@stardust ~]$ goaccess ~/logs/webserver/access_log


.. _GoAccess: https://goaccess.io/
.. _GoAccess Installation page: https://goaccess.io/download#installation
.. _GitHub repository: https://goaccess.io/download#build

.. authors::
