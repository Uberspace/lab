.. author:: Michael Stötzer <hallo@bytekeks.de>

.. tag:: lang-go
.. tag:: audience-developers
.. tag:: continuous-integration
.. tag:: automation

.. highlight:: console

.. sidebar:: Logo

  .. image:: _static/images/gitlab-logo.png
      :align: center

#############
Gitlab Runner
#############

.. tag_list::

GitLab Runner is the open source project that is used to run your jobs and send the results back to `GitLab`_. It is used in conjunction with `GitLab`_ CI, the open-source continuous integration service included with `GitLab`_ that coordinates the jobs.

----

.. note:: For this guide you should be familiar with the basic concepts of

  * :manual:`supervisord <daemons-supervisord>`

Prerequisites
=============

gitlab project
--------------

You need to have a project in gitlab that you want to deploy using Gitlab Runner.

For further information please refer to the official `Gitlab Runner docs`_

Obtain registration token
--------------------------

To create a specific Runner without having admin rights to the GitLab instance, visit the project you want to make the Runner work for in GitLab:

 Go to Settings > **CI/CD** to obtain the token

Installation
============

Download latest version
-----------------------

Use ``wget`` to download the latest version of Gitlab Runner:

::

  [isabell@stardust ~]$ wget -O /home/$USER/bin/gitlab-runner https://gitlab-runner-downloads.s3.amazonaws.com/latest/binaries/gitlab-runner-linux-amd64

Make it executable:

::

  [isabell@stardust ~]$ chmod +x /home/$USER/bin/gitlab-runner

**Optional** check runner version:

::

  [isabell@stardust ~]$ /home/$USER/bin/gitlab-runner -v

Create working directory
------------------------

Create a working directory for the runner:

::

  [isabell@stardust ~]$ mkdir /home/$USER/gitlab-runner

Register the runner
-------------------

.. note:: You need your registration token you copied above.

  This basic setup uses the **shell executor**. See: `Gitlab Runner Executors`_

::

  [isabell@stardust ~]$ /home/$USER/bin/gitlab-runner register

Configure the supervisord service
=================================

Create a shell script (e.g. ``/home/$USER/bin/gitlab-runner.sh``) that keeps the call for the runner:

::

  #!/bin/bash
  /home/$USER/bin/gitlab-runner run --working-directory=/home/$USER/gitlab-runner/

Make it executable:

::

  [isabell@stardust ~]$ chmod +x /home/$USER/bin/gitlab-runner.sh

Create supervisord ini (e.g. ``/home/$USER/etc/services.d/gitlab-runner.ini``:

::

  [program:gitlab-runner]
  command=/home/$USER/bin/gitlab-runner.sh

.. include:: includes/supervisord.rst

If it’s not in state RUNNING, check your configuration.

.. _Gitlab: https://gitlab.com
.. _Gitlab Runner docs: https://docs.gitlab.com/runner/
.. _Gitlab Runner executors: https://docs.gitlab.com/runner/executors/README.html

----

Tested with Gitlab Runner 11.1.0, Uberspace 7.1.7.0

.. author_list::
