After creating the configuration, tell :manual:`supervisord <daemons-supervisord>` to refresh its configuration and start the service:

.. code-block:: console

 [isabell@stardust ~]$ supervisorctl reread
 SERVICE: available
 [isabell@stardust ~]$ supervisorctl update
 SERVICE: added process group
 [isabell@stardust ~]$ supervisorctl status
 SERVICE                            RUNNING   pid 26020, uptime 0:03:14
 [isabell@stardust ~]$

