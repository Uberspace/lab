.. author:: Eike Broda <uberlab@ebroda.de>

.. tag:: monitoring
.. tag:: web
.. tag:: analytics
.. tag:: self-hosting
.. tag:: privacy
.. tag:: lang-go

.. highlight:: console

###########
Fathom Lite
###########

.. abstract::
  `Fathom Lite`_ is a :manual:`Go <lang-go>`-based website analytics service that respects the privacy of the users and does not collect any personally identifiable information. It is released under the MIT license.

----

.. note:: For this guide you should be familiar with the basic concepts of

  * :manual:`Go <lang-go>`
  * :manual:`supervisord <daemons-supervisord>`

Prerequisites
=============
Your website domain or subdomain needs to be setup up:

.. include:: includes/web-domain-list.rst


Installation
============

Create a folder fathom in the home directory of your account and move there.
Get the current binary from Github Releases_. Use the fathom_x.x.x_linux_amd64.tar.gz and unpack the release.

::

  [isabell@stardust ~]$ mkdir fathom
  [isabell@stardust ~]$ cd fathom
  [isabell@stardust ~]$ wget https://github.com/usefathom/fathom/releases/download/v1.2.1/fathom_1.2.1_linux_amd64.tar.gz
  ...
  [isabell@stardust ~]$ tar xfv fathom_1.2.1_linux_amd64.tar.gz
  LICENSE
  README.md
  fathom
  [isabella@stardust ~]$

You can now check if fathom is working properly by checking it's version.

::

  [isabella@stardust ~]$ ./fathom --version
  Fathom version 1.2.1, commit 8f7c[...], built at 2018-11-30T09:21:37Z
  [isabella@stardust ~]$


Configuration
=============

Create the configuration file
-----------------------------
For the configuration Fathom Lite uses an .env file. Create a file ``~/fathom/.env`` and set the basic information like shown below. Replace the value of `FATHOM_SECRET` with some random value.

.. code-block:: ini

  FATHOM_SERVER_ADDR=:5432
  FATHOM_GZIP=true
  FATHOM_DATABASE_DRIVER="sqlite3"
  FATHOM_DATABASE_NAME="fathom.db"
  FATHOM_SECRET="random-secret-string"

We use the port 5432 and the integrated support for sqlite. Fathom also supports the usage of MySQL. You find details for that in the `configuration documentation`_.

Setup daemon
------------
Create ``~/etc/services.d/fathom.ini`` with the following content:

.. code-block:: ini

  [program:fathom]
  directory=%(ENV_HOME)s/fathom
  command=%(ENV_HOME)s/fathom/fathom server
  autostart=true
  autorestart=true
  stopsignal=INT

.. include:: includes/supervisord.rst

If it's not in state RUNNING, check your configuration.

Configure web server
--------------------

.. note::

    Fathom Lite is running on port 5432, as defined in ``~/fathom/.env``. Fathom does not work in sub-directories, but works smoothly on sub-domains.

.. include:: includes/web-backend.rst


Usage
=====
Please also refer to Fathoms Lite's `quick start guide`_.

On the first launch Fathom Lite asks you to add a website you want to track. After giving the name the tracking code is offered that needs to be integrated into your website to be tracked.

.. note::
  By default and as long as there are no users the Fathom Lite instance is public, so everybody can see the statistics.

You can track multiple pages with this instance. Therefore you need to create at least (temporary) one user which can access the dashboard. You can create users using the ``fathom`` command.

::

  [isabella@stardust ~]$ ~/fathom/fathom user add --email=your@email.com --password=secret

Now the dashboard is no longer public and instead a login prompt is shown by Fathom Lite. After login you can add additional sites to track in the upper right corner.

To make the dashboard public visible again, you have to delete all users. Fathom Lite does not provide a list of all users, but you can check them in your database.

::

 [isabella@stardust ~]$ sqlite3 ~/fathom/fathom.db
 SQLite version 3.28.0 2019-04-16 19:49:53
 Enter ".help" for usage hints.
 sqlite> SELECT email from users;
 your@email.com
 sqlite> .exit
 [isabella@stardust ~]$ ~/fathom/fathom user delete --email=your@email.com
 [isabella@stardust ~]$


Privacy
=======
Fathom Lite respects the DoNotTrack settings of the browser. It's not tracking IP addresses, but it's setting a small cookie for some technical reasons (explanation_).

Please check if you need to update your Privacy Policy regarding Fathom Lite.

Updates
=======

.. note:: Check the update feed_ regularly to stay informed about the newest version.

Go to ~/fathom and rename the current fathom executable to fathom_old.
Then download the new version like described on the installation part.

And restart the service.

::

[isabell@stardust ~]$ supervisorctl restart fatom
[isabell@stardust ~]$


.. _Fathom Lite: https://usefathom.com/
.. _Repositoriy:  https://github.com/usefathom/fathom
.. _quick start guide: https://github.com/usefathom/fathom/blob/master/docs/Installation%20instructions.md
.. _configuration documentation: https://github.com/usefathom/fathom/blob/master/docs/Configuration.md
.. _feed: https://github.com/usefathom/fathom/releases
.. _Releases: https://github.com/usefathom/fathom/releases
.. _explanation: https://github.com/usefathom/fathom/issues/40#issuecomment-392461879

----

Tested with Fathom 1.2.1, Uberspace 7.5.0.1

.. author_list::
