.. highlight:: console

.. author:: FM <git.fm@mmw9.de>

########
GoAccess
########

GoAccess_ is an open source realtime web log analyzer and viewer. It use the standard web server log file as source to build a readable graphical HTML output as web page (dashboard) or an overview in the shell. 

This documentation describe the way to let create a static web page as overview, which will be updated every hour with a cron job. More details are on the `man page`_ and on GitHub_ available.

License
=======

GoAccess is released under the `MIT License`_

Installation
============

Step 1 - Download and Extract the Source Code
---------------------------------------------

Create a working directory.

::

 [isabell@stardust ~]$ mkdir ~/filebase/
 [isabell@stardust ~]$ cd ~/filebase/
 [isabell@stardust ~]$

Download the actual source code from GitHub. 

::

 [isabell@stardust ~]$ git clone https://github.com/allinurl/goaccess.git
 [isabell@stardust ~]$

Step 2 - Source Code Configuration, Compiling and Installation
--------------------------------------------------------------

Prepare the compile environment.

::

 [isabell@stardust ~]$ cd ~/filebase/goaccess/
 [isabell@stardust ~]$ autoreconf -fiv
 [isabell@stardust ~]$

Configure and compile the source code with the commands ``configure``, ``make`` and finally install it with ``make install``.

.. note:: Please use single steps instead of combining all three in one process to see and identify possible errors.

Before we start, we have to consider some aspects, especially a shared hosting environment like Uberspace:

 * ``--prefix=/home/isabell``: Installation target for your personal Uberspace.
 * ``--enable-utf8``: Compile with wide character support.
 * ``--enable-geoip=legacy``: Compile with GeoLocation support, legacy will utilize the original GeoIP databases.

Other options can be found in the GoAccess `installation documentation`_.

.. warning:: Replace ``isabell`` with your Uberspace name!

::

 [isabell@stardust ~]$ cd ~/filebase/goaccess/
 [isabell@stardust ~]$ ./configure --enable-utf8 --enable-geoip=legacy --prefix=/home/isabell
 [isabell@stardust ~]$ make
 [isabell@stardust ~]$ make install
 [isabell@stardust ~]$

Configuration
=============

After the installation of GoAccess, it is necessary to enable the web server logs and to configure GoAccess with the right log format.

Step 1 - Enable the Web Server Log
----------------------------------

Please follow the instructions by the Uberspace manual_ to enable the web server logs.

.. note:: Please consider, after the web server log enabling, it needs some time to have some entries in your new log files. Depends on the web traffic.

Step 2 - GoAccess Configuration
-------------------------------

Edit the configuration file ``~/etc/goaccess/goaccess.conf`` and reach out for the following parameters to uncomment these.

.. code-block:: bash
 :emphasize-lines: 2,4,6,8
 
 # Time Format Options (required)
 time-format %H:%M:%S
 
 # Date Format Options (required)
 date-format %d/%b/%Y
 
 # NCSA Combined Log Format (is in use by Uberspace)
 log-format %h %^[%d:%t %^] "%r" %s %b "%R" "%u"
 
 # Set HTML report page title and header.
 html-report-title My Uberspace

Launch
======

Step 1 - First Try (or Realtime Analysis in the Shell)
------------------------------------------------------

To get first results, to check that everthing is maintained, please enter:

::

 [isabell@stardust ~]$ goaccess -a -p ~/etc/goaccess/goaccess.conf -f ~/logs/webserver/access_log

Scroll with your cursor keys up and down. With "q" you can quit GoAccess.

The used parameters are:

 * ``-a``: Enable a list of user-agents by hosts.
 * ``-p``: Config file location.
 * ``-f``: Web server log file location.

Step 2 - HTML Output
--------------------

This is the graphical variant as static HTML web page. I consider a new folder inside the html location, that you have access from outside on your statistics.

::

 [isabell@stardust ~]$ cd ~/html/
 [isabell@stardust ~]$ mkdir statistics
 [isabell@stardust ~]$

The command to create a static file with GoAccess is:

::

 [isabell@stardust ~]$ goaccess -a -p ~/etc/goaccess/goaccess.conf -f ~/logs/webserver/access_log -o ~/html/statistics/report.html

The additional parameter is:

 * ``-o``: To define the output file.

.. note:: The target folder ``statistics`` and file name ``report.html`` are examples. If you want more privacy after this publication, please use other names for boths.

To visit your new file, please use your browser (https://your-uberspace/statistics/report.html).

Step 3 - Script File
--------------------

To create a GoAccess file with a cron job every hour as example, a script is helpful. The location and name for the script file is: ~/bin/script_goaccess.sh

.. code-block:: bash
 
 #!/bin/bash
 
 goaccess -a -p ~/etc/goaccess/goaccess.conf -f ~/logs/webserver/access_log -o ~/html/statistics/report.html

Make your script file executable with:

::

 [isabell@stardust ~]$ chmod 0774 ~/bin/script_goaccess.sh
 [isabell@stardust ~]$

Step 4 - Cron Job
-----------------

`Cron jobs`_ are described in detail in the Uberspace manual. In this case i consider the following task:

::

 [isabell@stardust ~]$ crontab -e
 [isabell@stardust ~]$

and content:

.. code-block:: bash
 
 0 * * * * $HOME/bin/script_goaccess.sh >/dev/null 2>&1

Best Practices
==============

The actual readable web log file is valid for one day. Uberspace consider a rolling aspect and create archives of the last seven days. With other words, a long term statistics is not possible, otherwise the next script level consider the archives per day too.

.. _GoAccess: https://goaccess.io/
.. _man page: https://goaccess.io/man
.. _GitHub: https://github.com/allinurl/goaccess
.. _MIT License: https://github.com/allinurl/goaccess/blob/master/COPYING
.. _installation documentation: https://goaccess.io/download#installation
.. _cron jobs: https://manual.uberspace.de/daemons-cron.html

----

Tested with Uberspace 7.3.10 and GoAccess 1.3

.. authors:: 
