.. highlight:: console

.. author:: Thomas Hoffmann <uberlab@emptyweb.de>

.. tag:: lang-python

.. sidebar:: Logo

  .. image:: _static/images/buildbot.svg
      :align: center

########
Buildbot
########

.. tag_list::

Buildbot is an open-source framework for automating software build, test, and release processes. At its core, Buildbot is a job scheduling system: it queues jobs, executes the jobs when the required resources are available, and reports the results. It can be easily installed and serve as a continuous integration platform to be used together with a variety of version control solutions, including gitea.

In this tutorial, we will first follow along with the official installation manual and set up a ``hello world``-system and will extend the standard installation of Buildbot_ with a :lab:`gitea <guide_gitea>`-Plugin.

----

.. note:: For this guide you should be familiar with the basic concepts of

  * :manual:`Python <lang-python>`
  * git_
  * :manual:`supervisord <daemons-supervisord>`
  * ssh port forwarding
  * Folder/File Permissions

.. note:: Recommended reading to follow along and go beyond this guide:

  * `Official Buildbot Manual <https://docs.buildbot.net/latest/manual/index.html>`_
  * `Official Buildbot Tutorial <https://docs.buildbot.net/latest/tutorial/index.html>`_
  * `Buildbot in 5 Minutes User Tutorial <https://docs.buildbot.net/latest/tutorial/fiveminutes.html>`_ (warning: based on an older version of buildbot! Code examples should be taken with a grain of salt. It explains the mechanics quite nicely, though)

License
=======

Buildbot is released under the `GNU General Public License v2.0 <https://www.gnu.org/licenses/old-licenses/gpl-2.0>`_.


Installation
============

You can install the BuildBot_ bundle using ``pip3.6``:

::

 [isabell@stardust ~]$ pip3.6 install buildbot[bundle] --user

If you want e-mail notifications from BuildBot_ to work later on, you will also need to install ``pyopenssl`` and ``service-identity``:

::

 [isabell@stardust ~]$ pip3.6 install pyopenssl service-identity --user


Configuration of the master
===========================

Step 1
------
Prepare the BuildBot_ folders. We are going to use one folder for all of our masters and another for all the workers:

::

 [isabell@stardust ~]$ mkdir ~/bb-master ~/bb-workers

Step 2
------

Create the first master:

::

 [isabell@stardust ~]$ cd ~/bb-master
 [isabell@stardust bb-master]$ buildbot create-master master

This will create the directory ``bb-master/master``, set up a sqlite database and deposit a sample configuration.

Step 3
------

Move the sample configuration:

::

 [isabell@stardust bb-master]$ mv master/master.cfg.sample master/master.cfg


Step 4
------

For BuildBot_ to work, we need to find two open ports on your uberspace host. One for the master's webinterface and one for the workers to communicate with the master:

::

 [isabell@stardust bb-master] FREEPORT=$(( $RANDOM % 4535 + 61000 )); ss -ln src :$FREEPORT | grep $FREEPORT && echo "try again" || echo $FREEPORT
 12345
 [isabell@stardust bb-master] FREEPORT=$(( $RANDOM % 4535 + 61000 )); ss -ln src :$FREEPORT | grep $FREEPORT && echo "try again" || echo $FREEPORT
 54321

We'll use ``12345`` for the webinterface and ``54321`` for the worker connections. You will get other ports as results (something between 61000 and 65535).


Step 5
------

Edit the file ``/home/isabell/bb-master/master/master.cfg``, which is basically a :manual:`Python <lang-python>` file. For now, we only need to change the ports. In ``c['www']``, change the port of the webinterface to ``12345`` (as selected before) and in ``c['protocols']``, change the port to ``54321``. That is going to be the port that the workers will communicate through. You should read through the rest of the options already, but leave things to their default values for now.

.. note:: This step will leave the ``hello world`` demo that Buildbot_ automatically enters into the configuration file intact. In combination with a worker, the example builder will clone the ``buildbot/hello-world`` github repository and run the ``test_hello.py`` script from that repository. More information on how to configure builders is available in the `official Buildbot manual <https://docs.buildbot.net/latest/manual/index.html>`_.

Step 6
------

That's it! Our master should be able to start now:

.. note:: We are starting buildbot with the ``--nodaemon`` option, forcing it to start in the foreground. In order to continue with the guide, you'll need to terminate it using Ctrl+C after it starts successfully.

::

 [isabell@stardust bb-master] buildbot start --nodaemon master
 Following twistd.log until startup finished..
 The buildmaster appears to have (re)started correctly.

If you don't get the same output, check the log at ``master/twistd.log`` for errors.

Step 7
------

In this step, we will set up :manual:`supervisord <daemons-supervisord>` to take control of our Buildbot_ master.

Create the file ``~/etc/services.d/buildbot-master.ini`` with the following content:

::

 [program:buildbot-master]
 command=buildbot start --nodaemon %(ENV_HOME)s/bb-master/master

After saving, update :manual:`supervisord <daemons-supervisord>` and check on the master's status:

::

 [isabell@stardust bb-master] supervisorctl reread && supervisorctl update
 [isabell@stardust bb-master] supervisorctl status
 buildbot-master                  RUNNING   pid 3032, uptime 0 days, 0:06:35

If it does not show ``RUNNING`` as a status, check the ``twistd.log`` for errors again.


Configuration of the worker
===========================

Now that the master is done, let's create the first worker!

Step 1
------

Change directories and create the worker:

::

 [isabell@stardust bb-master] cd ~/bb-workers
 [isabell@stardust bb-workers] buildbot-worker create-worker example-worker localhost:54321 example-worker pass

This will create the directory ``example-worker`` and deposit the worker configuration file (``example-worker/buildbot.tac``) as well as some additional files with meta information about this worker. The creation tool will give you some output and instructions on what to edit afterwards - you should definitely take a look at the mentioned files and enter your information.

Step 2
------

The worker also requires its own process for which we will use :manual:`supervisord <daemons-supervisord>` again.

Create the file ``~/etc/services.d/buildbot-worker.ini`` with the following content:

::

 [program:buildbot-worker]
 command=buildbot-worker start --nodaemon %(ENV_HOME)s/bb-workers/example-worker

After saving, update :manual:`supervisord <daemons-supervisord>` and check on the worker's status:

::

 [isabell@stardust bb-master] supervisorctl reread && supervisorctl update
 [isabell@stardust bb-master] supervisorctl status
 buildbot-master                  RUNNING   pid 3032, uptime 0 days, 0:06:35
 buildbot-worker                  RUNNING   pid 3092, uptime 0 days, 0:03:14

If it does not show ``RUNNING`` as a status, check the ``twistd.log`` for errors again.


Securing the BuildBot Installation
==================================

Now that we have a working BuildBot_ master and worker, it's time to take a look at securing the webinterface. BuildBot_ was developed under the assumption that access to the webinterface would only be allowed from a private network and not the world wide web - so, by default, there is no permission or authentication management configured. Even if you don't plan on exposing the webinterface to the world, you should probably take a look at the `www authentication section in the official manual <https://docs.buildbot.net/latest/manual/configuration/www.html#web-authentication>`_ and use one of the available modules as otherwise all users on the same Uberspace host as you would be able to access your Buildbot_ freely.


Using SSH Tunnel to keep BuildBot private
-----------------------------------------

A better way to keep the webinterface secure is to never expose it to the public in the first place and use an SSH tunnel instead. This limits access to users who can connect to your Uberspace account via SSH.

You can either do this via the ``ssh`` command like so:

::

 [isabell@desktop ~] ssh -L 12345:localhost:12345 isabell@stardust.uberspace.de

Or you can adjust your local ``~/.ssh/config`` file by adding the ``LocalForward`` option to the Uberspace host. The host entry would look something like this:

::

 Host stardust
 	HostName stardust.uberspace.de
 	User isabell
 	LocalForward 12345 localhost:12345

You can then connect via

::

 [isabell@desktop ~] ssh stardust

Now that the connection is established with port forwarding, you can call up ``http://localhost:12345/`` in your browser to access the Buildbot_ webinterface! We have now basically completed the `'First Run' tutorial of the official manual <https://docs.buildbot.net/latest/tutorial/firstrun.html>`_ and you should be able to force an execution of the ``runtests`` builder.

Restricting SSH access to port forwarding only
----------------------------------------------

If you don't want to give everyone who needs access to the BuildBot_ webinterface full shell access to your Uberspace account, there is support for that as well! You can simply prepend their public key in the ``~/.ssh/authorized_keys`` file with the following:

::

 command="echo 'This account can only be used for port forwarding to buildbot'",no-agent-forwarding,no-X11-forwarding,permitopen="localhost:12345" ssh-rsa ...

This will allow the respective users to connect to the tunnel like this (the ``-N`` prevents execution of remote commands):

::

 [isabell@desktop ~] ssh -N -L 12345:localhost:12345 isabell@stardust.uberspace.de

After which they will also be able to open ``http://localhost:12345/``, but won't have an open shell to which they could issue other commands or forward to any other port than ``12345``. You can also verify that it's working by connecting without the ``-N`` parameter - that should show you the error message configured in ``command`` beforehand.



Integration with gitea
======================

One useful thing to do with BuildBot_ is to use it as a continuous integration runner. Since :lab:`gitea <guide_gitea>` also works on Uberspace but doesn't support 'direct' CI/CD integration like github and gitlab, we can use :lab:`gitea <guide_gitea>`'s web hooks to trigger our BuildBot_ installation to do something.

Step 1
------

For this, we will need to install the ``buildbot_gitea`` plugin for BuildBot, developed by Marvin Pohl of lab132. We will install directly from their git repository using pip:

::

 [isabell@stardust ~] pip3.6 install git+https://github.com/lab132/buildbot-gitea.git --user

Step 2
------

Now that we installed the ``buildbot_gitea`` plugin, we can use ``gitea`` as a dialect for accepting incoming webhook messages via ``http://localhost:12345/change_hook/gitea``. For this, return to editing the ``master.cfg`` from earlier. There, add the following to enable incoming webhook messages from gitea:

::

 c['www']['change_hook_dialects'] = {
	'gitea': {
		'secret': 'SomeSecretPassPhraseToAuthenticateGitea',
	}}

That's it! Restart your BuildBot_ master via ``supervisorctl restart buildbot-master`` and continue by adding the webhook to the desired gitea repository!

Step 3
------

Adding the webhook to a repository works pretty much as expected. Go to the desired repository, click on ``Settings > Webhooks > Add Webhook > Gitea`` and enter ``http://localhost:12345/change_hook/gitea`` as the URL and whatever you entered as a secret as secret. This of course assumes that you installed gitea on the same Uberspace host as BuildBot_.

.. note:: If gitea and Buildbot are installed on different hosts, you will either need to set up an SSH tunnel between them or expose the Buildbot webinterface to the public. You may refer to the section on securing the Buildbot installation as a starting point. `autossh <http://www.harding.motd.ca/autossh/>`_ might also be interesting to you.

And that's it! Now, push-events in your gitea repository will trigger the runtests-builder from the example setup.

Finishing Installation
======================

Congratulations! You now have an operational BuildBot_ installation on your Uberspace! Continue with the recommended reading from the beginning to learn more about the architecture of BuildBot_ and how to set up your own repositories and builders.


.. _BuildBot: https://buildbot.net/
.. _git: https://git-scm.com/

.. author_list::
