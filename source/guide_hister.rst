.. author:: Funk

.. tag:: search
.. tag:: self-hosting
.. tag:: lang-go
.. tag:: web

.. highlight:: console

.. sidebar:: Logo

  .. image:: _static/images/hister.png
      :align: center

######
Hister
######

.. tag_list::

Hister is a general purpose web search engine providing automatic full-text indexing for visited websites.

Use cases

 * Build a private search index of your personal browsing history.
 * Provide a private search index for your personal or teams content (Wiki etc).

----

.. note:: For this guide you should be familiar with the basic concepts of

  * :manual:`supervisord <daemons-supervisord>`
  * :manual:`web backends <web-backends>`
  * :manual:`domains <web-domains>`

License
=======

Hister is released under the `AGPL-3.0 license`_.

All relevant legal information can be found in the `LICENSE`_ file in the repository of the project.

Prerequisites
=============

You might want to expose Hister under a specific sub domain:

.. include:: includes/web-domain-list.rst

.. code-block:: console

  [user@stardust ~]$ uberspace web domain add hister.user.uber.space

Installation
============

Download the latest Hister binary from the releases_ page and place it in your ``~/bin`` directory:

  [user@stardust ~]$ wget -O ~/bin/hister https://github.com/asciimoo/hister/releases/download/v0.15.0/hister_0.15.0_linux_amd64
  [user@stardust ~]$ chmod +x ~/bin/hister

Create default configuration files

.. code-block:: console

  [user@stardust ~]$ hister create-config ~/.config/hister/config.yml


Configuration
=============

Configure an access token
-------------------------

Hister requires an access token for authentication. You can generate a random token using the CLI:

.. code-block:: console

  [user@stardust ~]$ openssl rand -hex 32

Put the generated token in the ``app/access_token`` field of your Hister configuration file (``~/.config/hister/config.yml``):

Configure Hister for Uberspace web backend
------------------------------------------

To run Hister behind Uberspace's native web backend (reverse proxy), you need to:

- Set Hister to listen on interface ``0.0.0.0:4433`` by editing the entry server/address in ``~/.config/hister/config.yml``.
- Configure your public domain that you have created above by setting ``server/base_url`` e.g. ``https://hister.user.uber.space``.

.. note:: For more details, see Histers's Configuration_ documentation.

To validate your configuration, briefly start Hister in the foreground:

.. code-block:: console

 [isabell@stardust ~]$ hister listen

If you see no errors, you can stop Hister with Ctrl+C and continue with the next step.


Setup daemon
------------

Create ``~/etc/services.d/hister.ini`` with the following content:

.. code-block:: ini

  [program:hister]
  command=%(ENV_HOME)s/bin/hister listen
  directory=%(ENV_HOME)s/.config/hister
  stderr_logfile=%(ENV_HOME)s/logs/hister.err.log
  stdout_logfile=%(ENV_HOME)s/logs/hister.out.log
  autostart=true
  autorestart=true
  stopsignal=INT
  startsecs=5


.. include:: includes/supervisord.rst

If it's not in state ``RUNNING``, check your configuration and the logs using ``supervisorctl maintail`` or ``tail -f ~/logs/hister.out.log``.

Configure Uberspace web backend
-------------------------------

Now, connect the Uberspace web backend to your running Hister instance 
(use the port configured in your configuration file, like ``4433`` and your configured domain name instead of /):

.. include:: includes/web-backend.rst

.. note::
   Uberspace's web backend will handle HTTPS and proxy all requests (including WebSockets) to your Hister service.

Usage
=====

Test your setup by visiting your instance in a browser: ``https://hister.user.uber.space``.
You will need your previously generated access token to log in.

Install the browser-extension_ and configure it for your domain.

Disable automatic indexing in the browser extension, unless you want to use Hister on your personal browsing history.

Setup crawl rules to index your content (e.g. Wiki, internal tools etc) and start crawling.

Optional: User handling
=======================

To use your Hister instance with multiple users, you can enable user handling.

Edit the configuration file and set ``app/user_handling`` to ``true``. Then restart the service using supervisorctl:

.. code-block:: console

  [user@stardust ~]$ supervisorctl restart hister

Create an admin user:

.. code-block:: console

 [user@stardust ~]$ hister create-user user --admin

Create additional users accordingly.

Security
========
Make sure to prevent other users from reading Hister data:

.. code-block:: console

  [user@stardust ~]$ chmod -R o-rwx ~/.config/hister

Updates
=======

.. note:: Watch the Hister_ repo on Github to be notified about new releases.



.. _Hister: https://github.com/asciimoo/hister
.. _releases: https://github.com/asciimoo/hister/releases
.. _documentation: https://hister.org/docs
.. _AGPL-3.0 license: https://github.com/asciimoo/hister?tab=AGPL-3.0-1-ov-file
.. _LICENSE: https://github.com/asciimoo/hister/blob/master/LICENSE
.. _Configuration: https://hister.org/docs/configuration
.. _browser-extension: https://hister.org/docs/browser-extension

----

Tested with Hister 0.15.0, Uberspace 7.17.3

.. author_list::

  * funk
