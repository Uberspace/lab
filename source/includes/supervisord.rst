To make sure the service is restarted after failure and after server reboots,
configure a ``~/etc/services.d/SERVICE.ini`` for :manual:`supervisord <daemons-supervisord>`:

.. code-block:: ini

  [program:SERVICE]
  command=%(ENV_HOME)s/bin/SERVICE
  autorestart=yes
  autostart=yes
  environment=
    PATH="%(ENV_HOME)s/SPECIALBINS:$PATH",
    SERVICE_DIR=%(ENV_HOME)s/SERVICE,
    LOGDIR=%(ENV_HOME)s/logs/

Tell :manual:`supervisord <daemons-supervisord>` to refresh its configuration and start the service:

.. code-block:: console

 [isabell@stardust ~]$ supervisorctl reread
 SERVICE: available
 [isabell@stardust ~]$ supervisorctl update
 SERVICE: added process group
 [isabell@stardust ~]$ supervisorctl status
 SERVICE                            RUNNING   pid 26020, uptime 0:03:14
 [isabell@stardust ~]$

