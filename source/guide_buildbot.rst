.. highlight:: console

.. author:: Thomas Hoffmann <uberlab@emptyweb.de>

.. sidebar:: Logo

  .. image:: _static/images/buildbot.svg
      :align: center

########
Buildbot
########

Buildbot is an open-source framework for automating software build, test, and release processes. At its core, Buildbot is a job scheduling system: it queues jobs, executes the jobs when the required resources are available, and reports the results. It can be easily installed and serve as a continuous integration platform to be used together with a variety of version control solutions, including gitea.

In this tutorial, we will first follow along with the official installation manual and set up a ``hello world``-system that we will then extend to be used with gitea.

----

.. note:: For this guide you should be familiar with the basic concepts of

  * Python_
  * git_
  * ssh port forwarding
  * Folder/File Permissions

.. note:: Recommended reads to follow along and go beyond this guide:

  * `Official Buildbot Manual <https://docs.buildbot.net/latest/manual/index.html>`_
  * `Official Buildbot Tutorial <https://docs.buildbot.net/latest/tutorial/index.html>`_
  * `Buildbot in 5 Minutes User Tutorial <https://docs.buildbot.net/latest/tutorial/fiveminutes.html>`_ (warning: based on an older version of buildbot! Code examples should be taken with a grain of salt. It explains the mechanics quite nicely, though)

License
=======

Buildbot is released under the GNU General Public License v2.0

  * https://www.gnu.org/licenses/old-licenses/gpl-2.0

Prerequisites
=============

For ease of use, you should set your default Python_ version to 3.6 and upgrade the ``pip3.6`` installation as well:

::

 [isabell@stardust ~]$ ln -s /usr/bin/python3.6 $HOME/bin/python
 [isabell@stardust ~]$ python --version
 Python 3.6.5
 [isabell@stardust ~]$ pip3.6 install --upgrade pip --user
 [isabell@stardust ~]$ pip --version
 pip 18.1 from /home/isabell/.local/lib/python3.6/site-packages/pip (python 3.6)

If pip doesn't report the new version right away, try logging out and back in again (or ``source .bashrc``).

Installation
============

You can install the buildbot bundle using pip:

::

 [isabell@stardust ~]$ pip install buildbot[bundle] --user

If you want to get e-mail notifications from buildbot later on, you will also need to install ``pyopenssl`` and ``service-identity``:

::

 [isabell@stardust ~]$ pip install pyopenssl service-identity --user


Configuration of the master
===========================

Step 1
------
Prepare the buildbot folders. We are going to use one folder for all of our masters and another for all the workers:

::

 [isabell@stardust ~]$ mkdir bb-master bb-workers

Step 2
------

Create the first master:

::

 [isabell@stardust ~]$ cd bb-master
 [isabell@stardust bb-master]$ buildbot create-master master

This will create the directory ``bb-master/master``, set up a sqlite database and deposit a configuration sample.

Step 3
------

Move the sample configuration:

::

 [isabell@stardust bb-master]$ mv master/master.cfg.sample master/master.cfg


Step 4
------

For buildbot to work, we need to find two open ports on your uberspace host. One for the master's webinterface and one for the workers to communicate with the master:

::

 [isabell@stardust bb-master] FREEPORT=$(( $RANDOM % 4535 + 61000 )); ss -ln src :$FREEPORT | grep $FREEPORT && echo "try again" || echo $FREEPORT
 12345
 [isabell@stardust bb-master] FREEPORT=$(( $RANDOM % 4535 + 61000 )); ss -ln src :$FREEPORT | grep $FREEPORT && echo "try again" || echo $FREEPORT
 54321

We'll use ``12345`` for the webinterface and ``54321`` for the worker connections. You will get other ports as results (something between 61000 and 65535).


Step 5
------

Edit the file ``/home/isabell/bb-master/master/master.cfg``.

Change the following lines:

.. code:: python

 c['protocols'] = {'pb': {'port': 9989}}

to

.. code:: python

 c['protocols'] = {'pb': {'port': 54321}}

 and

 .. code:: python

 c['www'] = dict(port=8010,
                plugins=dict(waterfall_view={}, console_view={}, grid_view={}))

to

.. code:: python

 c['www'] = dict(port=12345,
                 plugins=dict(waterfall_view={}, console_view={}, grid_view={}))

You should read through the rest already, but leave things to their default values for now.

Step 6
------

That's it! Our master should be able to start now:

::

 [isabell@stardust bb-master] buildbot start master
 Following twistd.log until startup finished..
 The buildmaster appears to have (re)started correctly.

If you don't get the same output, check the log at ``master/twistd.log`` for errors.

Configuration of the worker
===========================

Now that the master is done, let's create the first worker!

Step 1
------

Change directories and create the worker:

::

 [isabell@stardust bb-master] cd ~/bb-workers
 [isabell@stardust bb-workers] buildbot-worker create-worker example-worker localhost example-worker pass

This will create the directory ``example-worker`` and deposit the worker configuration file (``example-worker/buildbot.tac``) as well as some additional files with meta information about this worker. The creation tool will give you some output and instructions on what to edit afterwards - you should definitely take a look at the mentioned files and enter your information.


Configuration of the SSH connection
===================================

Step 1
------

In order to view the Buildbot master's webinterface, we need to forward the respective port through our SSH connection.

You can either do this via the ``ssh`` command like so:

::

 [isabell@desktop ~] ssh -L 12345:localhost:12345 isabell@stardust.uberspace.de

Or you can adjust your local ``.ssh/config`` file by adding the ``LocalForward`` option to the Uberspace host. The host entry would look something like this:

::

 Host stardust
 	HostName stardust.uberspace.de
 	User isabell
 	LocalForward 12345 localhost:12345

You can then connect via

::

 [isabell@desktop ~] ssh stardust


Step 2
------

Now that the connection is established with port forwarding, you can call up ``http://localhost:12345/`` to access the Buildbot webinterface!

Execute the first build
=======================

force runtests build with hello world project via webinterface

Integration with gitea
======================

install buildbot_gitea
set up webhook


Examples
========

refer to official documentation - include links to relevant pages as much as possible

Simple pipeline for use with git repository
-------------------------------------------

adapt configuration (use hello world project again?) and set up change_sources, workers, builders, webhook


Using the MailNotifier reporter
-------------------------------

set up mailnotifier reporter


Using the doStepIf condition
----------------------------

helper functions, how to, example with simple backup


.. _Mailman: http://www.list.org/
.. _Python: https://manual.uberspace.de/en/lang-python.html
.. _supervisord: https://manual.uberspace.de/en/daemons-supervisord.html
.. _mailbox: https://manual.uberspace.de/en/mail-mailboxes.html#setup-a-new-mailbox
.. _documentation: https://www.gnu.org/software/mailman/mailman-install.txt


.. authors::