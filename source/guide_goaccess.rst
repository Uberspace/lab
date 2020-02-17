.. highlight:: console

.. author:: FM <git.fm@mmw9.de>

.. tag:: lang-c
.. tag:: audience-admins
.. tag:: analytics

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

Download and extract the tarball containing the source code into a temporary
directory:

::

 [isabell@stardust ~]$ cd ~/tmp
 [isabell@stardust ~/tmp]$ curl https://tar.goaccess.io/goaccess-1.3.tar.gz | tar -xvz
    % Total    % Received % Xferd  Average Speed   Time    Time     Time  Current
                                  Dload  Upload   Total   Spent    Left  Speed
   0     0    0     0    0     0      0      0 --:--:-- --:--:-- --:--:--     0
 goaccess-1.3/
 goaccess-1.3/ChangeLog
 goaccess-1.3/resources/
 (...)
 goaccess-1.3/m4/lib-link.m4
 goaccess-1.3/m4/nls.m4
 goaccess-1.3/m4/po.m4
 [isabell@stardust ~/tmp]$

Step 2 - Source Code Configuration, Compiling and Installation
--------------------------------------------------------------

Configure and compile the source code with the commands ``configure``, ``make`` and finally install it with ``make install``.

.. note:: Please use single steps instead of combining all three in one process to see and identify possible errors.

Before we start, we have to consider some aspects, especially a shared hosting environment like Uberspace:

 * ``--prefix=$HOME``: Put the resulting binary in ~/bin.
 * ``--enable-utf8``: Compile with wide character support.
 * ``--enable-geoip=legacy``: Compile with GeoLocation support, legacy will utilize the original GeoIP databases.

Other options can be found in the GoAccess `installation documentation`_.

::

 [isabell@stardust ~]$ cd ~/tmp/goaccess-1.3/
 [isabell@stardust ~/tmp/goaccess-1.3]$ ./configure --enable-utf8 --enable-geoip=legacy --prefix=$HOME
 [isabell@stardust ~/tmp/goaccess-1.3]$ make
 [isabell@stardust ~/tmp/goaccess-1.3]$ make install
 [isabell@stardust ~/tmp/goaccess-1.3]$

Configuration
=============

After the installation of GoAccess, it is necessary to enable the web server logs and to configure GoAccess with the right log format.

Step 1 - Enable the Web Server Log
----------------------------------

Please follow the instructions in :manual:`the uberspace manual <web-logs>` to enable the web server logs.

.. note:: Please consider, after the web server log enabling, it needs some time to have some entries in your new log files. Depends on the web traffic.

Step 2 - GoAccess Configuration
-------------------------------

Edit the configuration file ``~/etc/goaccess/goaccess.conf`` and reach out for the following parameters to uncomment these.

.. code-block:: bash
 :emphasize-lines: 2,5,8,11

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

 [isabell@stardust ~]$ goaccess --agent-list --config-file ~/etc/goaccess/goaccess.conf --log-file ~/logs/webserver/access_log

Scroll with your cursor keys up and down. With "q" you can quit GoAccess.

Step 2 - HTML Output
--------------------

This is the graphical variant as static HTML web page. I consider a new folder inside the html location, that you have access from outside on your statistics.

::

 [isabell@stardust ~]$ mkdir ~/html/statistics
 [isabell@stardust ~]$

The command to create a static file with GoAccess is:

::

 [isabell@stardust ~]$ goaccess --agent-list --config-file ~/etc/goaccess/goaccess.conf --log-file ~/logs/webserver/access_log --output ~/html/statistics/report.html

.. warning:: The content of ``~/html`` is publicly accessible. To protect it from unintended visitors, set up HTTP basic authentication using an ``.htaccess`` file.

To view the statistics, point your browser to your uberspace URL, e.g. ``https://isabell.uber.space/statistics/report.html``.

Step 3 - Script File
--------------------

To create a GoAccess file with a cron job every hour as example, a script is helpful. The location and name for the script file is: ``~/bin/goaccess_generate_statistics.sh``

.. code-block:: bash

 #!/bin/bash

 goaccess --agent-list --config-file ~/etc/goaccess/goaccess.conf --log-file ~/logs/webserver/access_log --output ~/html/statistics/report.html

Make your script file executable with:

::

 [isabell@stardust ~]$ chmod +x ~/bin/goaccess_generate_statistics.sh
 [isabell@stardust ~]$

Step 4 - Cron Job
-----------------

`Cron jobs`_ are described in detail in the Uberspace manual. In this case i consider the following task:

::

 [isabell@stardust ~]$ crontab -e
 [isabell@stardust ~]$

and content:

.. code-block:: bash

 0 * * * * $HOME/bin/goaccess_generate_statistics.sh >/dev/null 2>&1

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

.. author_list::
