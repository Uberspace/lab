.. author:: bliepp <https://github.com/bliepp>

.. tag:: lang-go
.. tag:: audience-developers
.. tag:: file-storage
.. tag:: database
.. tag:: authentication

.. highlight:: console

.. sidebar:: Logo

  .. image:: _static/images/pocketbase.svg
      :scale: 300%
      :align: center

.. spelling:wordlist:
  pocketbase
  Pocketbase

##########
Pocketbase
##########

.. tag_list::

Pocketbase_ is a self-hosted Backend as a Service with a functionality similar to Google Firebase or Supabase.
It provides APIs for a managed SQLite database, user authentication, file storage and more.
As most applications written in Go it's easy to install.

----

.. note:: For this guide you should be familiar with the basic concepts of

  * :manual:`Web Backends <web-backends>`
  * :manual:`supervisord <daemons-supervisord>`
  * :manual:`domains <web-domains>`


License
=======

Pocketbase is licensed under the MIT license

     https://github.com/pocketbase/pocketbase/blob/master/LICENSE.md



Installation
============

Download the latest release and extract it to your binary folder:

.. code-block:: console

    [isabell@stardust ~]$ wget -O pocketbase.zip https://github.com/pocketbase/pocketbase/releases/download/v0.22.8/pocketbase_0.22.8_linux_amd64.zip
    [...]
    Saving to: ‘pocketbase.zip’

    100%[====================================================================================================================================================>] 14,321,393  23.1MB/s   in 0.6s

    2024-04-11 11:22:32 (23.1 MB/s) - ‘pocketbase.zip’ saved [14321393/14321393]
    [isabell@stardust ~]$ unzip pocketbase.zip pocketbase -d ~/bin/
    Archive:  pocketbase.zip
      inflating: /home/isabell/bin/pocketbase
    [isabell@stardust ~]$

It should be added to your path automatically. Now test if it works:

.. code-block:: console

    [isabell@stardust ~]$ pocketbase -v
    pocketbase version 0.22.8
    [isabell@stardust ~]$


Setup Supervisord
=================

First create a folder where all data is stored:

.. code-block:: console

    [isabell@stardus ~]$ mkdir ~/pocketbase
    [isabell@stardus ~]$


.. warning::
    To modify this specific running instance of Pocketbase (e.g. updating, user management),
    all ``pocketbase`` commands must be executed in the folder you just created!


Now, create a configuration file ``~/etc/services.d/pocketbase.ini``:

.. code-block:: ini

    [program:pocketbase]
    directory=%(ENV_HOME)s/pocketbase
    command=pocketbase serve --http :8090
    autostart=yes
    autorestart=yes
    startsecs=60

.. include:: includes/supervisord.rst

.. note::
    Pocketbase is running on port 8090.

.. include:: includes/web-backend.rst


Creating an admin user
======================

First, find out your domain name:

.. include:: includes/web-domain-list.rst

To create an admin user open ``https://isabel.uber.space/_/`` (mind the underscore in the URL) and follow through the
instructions of the installer. Alternatively you can use the admin CLI via ``pocketbase admin`` to create, delete and
update admin users.


Updates
=======

.. note:: Check the update documentation_ or releases_ page regularly to stay informed about the newest version.

To update the current executable you have two choices:

* Repeat the steps in the *Installation* section above.
* Run the built-in updater using ``pocketbase update`` inside ``~/pocketbase``

After updating, tell :manual:`supervisord <daemons-supervisord>` to restart the service:

.. code-block:: console

    [isabell@stardust ~]$ supervisorctl restart pocketbase
    SERVICE: stopped
    SERVICE: started
    [isabell@stardust ~]$ supervisorctl status
    SERVICE                            RUNNING   pid 26020, uptime 0:03:14
    [isabell@stardust ~]$


Breaking changes
----------------

Pocketbase is still in early development. Hence, a new realease might introduce breaking changes.
While updating you might need to run a migration using ``pocketbase migrate``. Please refer to the documentation_.


..
  ##### Link section #####

.. _Pocketbase: https://pocketbase.io/
.. _documentation: https://pocketbase.io/docs/
.. _releases: https://github.com/pocketbase/pocketbase/releases
.. _dashboard: https://uberspace.de/dashboard/authentication

----

Tested with Pocketbase 0.22.8, Uberspace 7.15.14

.. author_list::
