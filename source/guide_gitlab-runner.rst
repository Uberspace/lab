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
GitLab Runner
#############

.. tag_list::

GitLab Runner is the open source project that is used to run your jobs and send the results back to `GitLab`_. It is used in conjunction with `GitLab`_ CI, the open-source continuous integration service included with `GitLab`_ that coordinates the jobs.

----

.. note:: For this guide you should be familiar with the basic concepts of

  * :manual:`supervisord <daemons-supervisord>`

Prerequisites
=============

GitLab project
--------------

You need to have a project in GitLab that you want to deploy using GitLab Runner.

For further information please refer to the official `GitLab Runner docs`_

Obtain registration token
--------------------------

To create a specific Runner without having admin rights to the GitLab instance, visit the project or group you want to make the Runner work for in GitLab:

 Go to Settings > **CI/CD** to obtain the token

Installation
============

Download latest version
-----------------------

Use ``wget`` to download the latest version of GitLab Runner:

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

  This basic setup uses the **shell executor**. See: `GitLab Runner Executors`_

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
  command=%(ENV_HOME)s/bin/gitlab-runner.sh

.. include:: includes/supervisord.rst

If it’s not in state RUNNING, check your configuration.


Updates
=======
To update the GitLab Runner the service needs to be stopped. Then you should backup your old executable. Afterwards its common to the installation:
You download the current release and make it executable. Afterwards see if it prints the current version and then (re)start your service.

::

  [isabell@stardust ~]$ supervisorctl stop gitlab-runner
  gitlab-runner: stopped
  [isabell@stardust ~]$ mv /home/$USER/bin/gitlab-runner /home/$USER/bin/gitlab-runner-old
  [isabell@stardust ~]$ wget -O /home/$USER/bin/gitlab-runner https://gitlab-runner-downloads.s3.amazonaws.com/latest/binaries/gitlab-runner-linux-amd64
  [isabell@stardust ~]$ chmod +x /home/$USER/bin/gitlab-runner
  [isabell@stardust ~]$ /home/$USER/bin/gitlab-runner -v
  Version:      13.6.0
  Git revision: ...
  (...)
  [isabell@stardust ~]$ supervisorctl start gitlab-runner
  gitlab-runner: started


Now check in your GitLab instance if the runner runs normally by triggering a job or pipeline.
If you encounter problems, you can return to your old runner by stopping the service, renaming the old executable back to gitlab-runner and (re)start the service.


.. _GitLab: https://gitlab.com
.. _GitLab Runner docs: https://docs.gitlab.com/runner/
.. _GitLab Runner executors: https://docs.gitlab.com/runner/executors/README.html

----

Tested with GitLab Runner 13.6.0, Uberspace 7.8.0.0

.. author_list::
