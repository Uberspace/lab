.. highlight:: console

.. author:: Thomas Hoffmann <uberlab@emptyweb.de>

.. sidebar:: Logo

  .. image:: _static/images/buildbot.svg
      :align: center

########
Buildbot
########

Buildbot is an open-source framework for automating software build, test, and release processes. At its core, Buildbot is a job scheduling system: it queues jobs, executes the jobs when the required resources are available, and reports the results. It can be easily installed and serve as a continuous integration platform to be used together with a variety of version control solutions, including gitea.

In this tutorial, we will first follow along with the official installation manual and set up a ``hello world``-system and will extend the standard installation of Buildbot_ with a gitea_-Plugin.

----

.. note:: For this guide you should be familiar with the basic concepts of

  * Python_
  * git_
  * supervisord_
  * ssh port forwarding
  * Folder/File Permissions

.. note:: Recommended reading to follow along and go beyond this guide:

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

If pip doesn't report the new version right away, try logging out and back in again.

Installation
============

You can install the BuildBot_ bundle using pip:

::

 [isabell@stardust ~]$ pip install buildbot[bundle] --user

If you want e-mail notifications from BuildBot_ to work later on, you will also need to install ``pyopenssl`` and ``service-identity``:

::

 [isabell@stardust ~]$ pip install pyopenssl service-identity --user


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

Edit the file ``/home/isabell/bb-master/master/master.cfg``, which is basically a Python_ file. For now, we only need to change the ports. In ``c['www']``, change the port of the webinterface to ``12345`` (as selected before) and in ``c['protocols']``, change the port to ``54321``. That is going to be the port that the workers will communicate through. You should read through the rest of the options already, but leave things to their default values for now.

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
 [isabell@stardust bb-workers] buildbot-worker create-worker example-worker localhost:54321 example-worker pass

This will create the directory ``example-worker`` and deposit the worker configuration file (``example-worker/buildbot.tac``) as well as some additional files with meta information about this worker. The creation tool will give you some output and instructions on what to edit afterwards - you should definitely take a look at the mentioned files and enter your information.


Configuration of the SSH connection
===================================

Step 1
------

In order to view the Buildbot master's webinterface, we need to forward the respective port through our SSH connection.

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


Step 2
------

Now that the connection is established with port forwarding, you can call up ``http://localhost:12345/`` in your browser to access the Buildbot_ webinterface! We have now basically completed the `'First Run' tutorial of the official manual <https://docs.buildbot.net/latest/tutorial/firstrun.html>`_ and you should be able to force an execution of the ``runtests`` builder.

Integration with gitea
======================

One useful thing to do with BuildBot_ is to use it as a continuous integration runner. Since gitea_ also works on Uberspace but doesn't support 'direct' CI/CD integration like github and gitlab, we can use gitea_'s web hooks to trigger our BuildBot_ installation to do something.

Step 1
------

For this, we will need to install the ``buildbot_gitea`` plugin for BuildBot, developed by Marvin Pohl of lab132. First, clone their git repository and then run the installation:

::

 [isabell@stardust ~] git clone https://github.com/lab132/buildbot-gitea.git
 [isabell@stardust ~] cd buildbot-gitea
 [isabell@stardust buildbot-gitea] pip install . --user

Step 2
------

Now that we installed the ``buildbot_gitea`` plugin, we can use ``gitea`` as a dialect for accepting incoming webhook messages via ``http://localhost:12345/change_hook/gitea``. For this, return to editing the ``master.cfg`` from earlier. There, add the following to enable incoming webhook messages from gitea:

::

 c['www']['change_hook_dialects'] = {
	'gitea': {
		'secret': 'SomeSecretPassPhraseToAuthenticateGitea',
	}}

That's it! Restart your BuildBot_ master via ``buildbot restart master`` and continue by adding the webhook to the desired gitea repository!

Step 3
------

Adding the webhook to a repository works pretty much as expected. Go to the desired repository, click on ``Settings > Webhooks > Add Webhook > Gitea`` and enter ``http://localhost:12345/change_hook/gitea`` as the URL and whatever you entered as a secret as secret. This of course assumes that you installed gitea on the same Uberspace host as BuildBot_.

And that's it! Now, push-events in your gitea repository will trigger the runtests-builder from the example setup.

Finishing Installation
======================

Setting up supervisord
----------------------

.. warning:: Don't forget to stop your buildbot master and worker before completing this step! Otherwise, your supervised processes will not start.



BuildBot_ can be run in the foreground as well - which is great news for us because we can use supervisord_ to watch and control the process. To set that up, we need to create two files - one for the master, one for the worker.

Create the file ``~/etc/services.d/buildbot-master.ini`` with the following content (adjust the paths to match your account, of course):

::

 [program:buildbot-master]
 command=/home/isabell/.local/bin/buildbot start --nodaemon /home/isabell/bb-master/master

Secondly, create the file ``~/etc/services.d/buildbot-worker.ini`` with the following content (again, adjust the paths, please):

::

 [program:buildbot-worker]
 command=/home/isabell/.local/bin/buildbot-worker start --nodaemon /home/isabell/bb-worker/example-worker

After creating these files, call ``supervisorctl reread`` and ``supervisorctl update`` to finalize the supervisord_ setup.

Congratulations! You now have an operational BuildBot_ installation on your Uberspace! Continue with the recommended reading from the beginning to learn more about the architecture of BuildBot_ and how to set up your own repositories and builders.


.. _BuildBot: https://buildbot.net/
.. _Python: https://manual.uberspace.de/en/lang-python.html
.. _gitea: https://lab.uberspace.de/en/guide_gitea.html
.. _git: https://git-scm.com/
.. _supervisord: https://manual.uberspace.de/en/daemons-supervisord.html

.. authors::