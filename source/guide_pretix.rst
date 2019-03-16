.. highlight:: console

.. author:: ezra <ezra@posteo.de>

.. sidebar:: About

  .. image:: _static/images/pretix.svg
      :align: center

##########
pretix
##########

pretix_ is an open source ticketing solution. It is written in Django_ and can be highly customized for the process of ticket sales.

----

.. note:: For this guide you should be familiar with the basic concepts of

  * :manual:`Python <lang-python>` and its package manager pip
  * :manual:`supervisord <daemons-supervisord>`

License
=======

All relevant legal information can be found here 

  * https://pretix.eu/about/en/terms

Prerequisites
=============

.. include:: includes/my-print-defaults.rst

Your URL needs to be setup:

::

 [isabell@stardust ~]$ uberspace web domain list
 isabell.uber.space
 [isabell@stardust ~]$

Installation
============

Step 1
------
Get the pretix source code from Github and clone it to ``~/pretix``, be sure to replace the pseudo branch number ``release/6.6.x`` here with the latest release branch from the Github repository at https://github.com/pretix/pretix/branches/active:

::

 [isabell@stardust ~]$ git clone https://github.com/pretix/pretix.git --depth=1 --branch release/6.6.x
 [...]
 Receiving objects: 100% (1852/1852), 7.06 MiB | 910.00 KiB/s, done.
 Resolving deltas: 100% (337/337), done.
 Checking connectivity... done.
 [isabell@stardust ~]$

Also, you need to create an extra data folder:

::

 [isabell@stardust ~]$ mkdir ~/pretix_data
 [isabell@stardust ~]$ 
 
Step 2
------
Install the requirements for pretix_:

::

 [isabell@stardust ~]$ pip3.6 install -r ~/pretix/src/requirements.txt --user
 [...]
 Running setup.py install for mt-940 ... done
 Running setup.py install for vobject ... done
 Running setup.py install for vat-moss ... done
 [...]
 [isabell@stardust ~]$ 
 
Step 3
------
To work correctly with the Uberspace Proxy, you need to add this option to the end of the file ``~/pretix/src/pretix/settings.py``:

.. code-block:: ini

   USE_X_FORWARDED_HOST = True 

Step 4
------
Now you need to set up the configuration, create the file ``~/.pretix.cfg`` and insert the following content:

.. warning:: Be sure, to replace all values with correct data of your own Uberspace account!

.. code-block:: ini
  :emphasize-lines: 2,3,5,9,10,11,15,16,17,18

    [pretix]
    instance_name=Isabells pretix
    url=https://isabell.uber.space
    currency=EUR
    datadir=/home/isabell/pretix_data

    [database]
    backend=mysql
    name=isabell_pretix
    user=isabell
    password=MySuperSecretPassword
    host=localhost

    [mail]
    from=isabell@uber.space
    host=stardust.uberspace.de
    user=isabell@uber.space
    password=MySuperSecretPassword
    port=587
    tls=on

Step 5
------
Run this code to create the database ``<username>_pretix`` in MySQL:

.. code-block:: console

 [isabell@stardust ~]$ mysql -e "CREATE DATABASE ${USER}_pretix DEFAULT CHARACTER SET utf8 DEFAULT COLLATE utf8_general_ci;"
 [isabell@stardust ~]$

You will also need to install a mysqlclient package:

::

 [isabell@stardust ~]$ pip3.6 install mysqlclient --user
 [...]
 Successfully installed mysqlclient-1.3.13
 [isabell@stardust ~]$

Step 6
------
Initialize the pretix_ database tables and generate the static files:

::

 [isabell@stardust ~]$ python3.6 ~/pretix/src/manage.py rebuild
 [isabell@stardust ~]$ python3.6 ~/pretix/src/manage.py makemigrations
 [isabell@stardust ~]$ python3.6 ~/pretix/src/manage.py migrate
 [isabell@stardust ~]$

Step 7
------
Install Gunicorn_ as backend server:

::

 [isabell@stardust ~]$ pip3.6 install gunicorn --user
 [isabell@stardust ~]$

Step 8
------
Get a free port number:

.. include:: includes/generate-port.rst

Step 9
------

.. include:: includes/proxy-rewrite.rst

Step 10
-------

Finally, you should set up a service that keeps pretix_ alive while you are gone. Therefor create the file ``~/etc/services.d/pretix.ini`` with the following content:

.. warning:: Replace ``<yourport>`` with the new portnumber you got!

.. code-block:: ini

 [program:pretix]
 command=gunicorn --reload --chdir %(ENV_HOME)s/pretix/src --bind 127.0.0.1:<yourport> --workers 4 pretix.wsgi --name pretix --max-requests 1200 --max-requests-jitter 50
 autostart=true
 autorestart=true
 stopsignal=INT

In our example this would be:

.. code-block:: ini

 [program:pretix]
 command=gunicorn --reload --chdir %(ENV_HOME)s/pretix/src --bind 127.0.0.1:9000 --workers 4 pretix.wsgi --name pretix --max-requests 1200 --max-requests-jitter 50
 autostart=true
 autorestart=true
 stopsignal=INT

Tell :manual:`supervisord <daemons-supervisord>` to refresh its configuration and start the service:

.. code-block:: console

 [isabell@stardust ~]$ supervisorctl reread
 pretix: available
 [isabell@stardust ~]$ supervisorctl update
 preitx: added process group
 [isabell@stardust ~]$ supervisorctl status
 pretix                            RUNNING   pid 26020, uptime 0:00:13
 [isabell@stardust ~]$

If it's not in state RUNNING, check your configuration.


Step 11
-------
Now point your Browser to your installation URL ``https://isabell.uber.space``. You will find the administration panel at ``https://isabell.uber.space/control``. 

Use ``admin@localhost`` as username and ``admin`` as password for your first login. You should change this password immediately after login!


Updates
=======

.. note:: Check the update feed_ regularly to stay informed about the newest version.


If there is a new version available, update your branch according to the version number (``v6.6.6`` would be ``release/6.6.x``)

::

 [isabell@stardust ~]$ cd ~/pretix
 [isabell@stardust pretix]$ git pull origin release/6.6.x
 [isabell@stardust pretix]$


.. _pretix: https://pretix.eu/
.. _Django:  https://www.djangoproject.com/
.. _Gunicorn: https://gunicorn.org/
.. _Github: https://github.com/pretix/pretix
.. _feed: https://github.com/pretix/pretix/releases.atom
.. _bullshit: https://bullenscheisse.de/2018/pretix-auf-einem-uberspace/

----

Tested with pretix 2.1.0 and Uberspace 7.1.15.0

.. authors::

This guide was written with the help of a former text on "bullshit_", thanks to Nathan.
