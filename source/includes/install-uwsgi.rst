Install the required uwsgi package with pip.

::

 [isabell@stardust ~]$ pip3.6 install uwsgi --user
 [isabell@stardust ~]$

After that, continue with setting it up as a service.

Create  ``~/etc/services.d/uwsgi.ini`` with the following content:

.. code-block:: ini

  [program:uwsgi]
  command=%(ENV_HOME)s/.local/bin/uwsgi --master --emperor %(ENV_HOME)s/uwsgi/apps-enabled
  autostart=true
  autorestart=true
  stderr_logfile = ~/uwsgi/err.log
  stdout_logfile = ~/uwsgi/out.log
  stopsignal=INT

Create needed folders and files for uwsgi:

::

 [isabell@stardust ~]$ mkdir -p ~/uwsgi/apps-enabled
 [isabell@stardust ~]$ touch ~/uwsgi/err.log 
 [isabell@stardust ~]$ touch ~/uwsgi/out.log
 [isabell@stardust ~]$

Tell ``supervisord`` to refresh its configuration and start the service:

::

 [isabell@stardust ~]$ supervisorctl reread
 uwsgi: available
 [isabell@stardust ~]$ supervisorctl update
 uwsgi: added process group
 [isabell@stardust ~]$ supervisorctl status
 uwsgi                            RUNNING   pid 26020, uptime 0:03:14
 [isabell@stardust ~]$


If it's not in state RUNNING, check your configuration.
