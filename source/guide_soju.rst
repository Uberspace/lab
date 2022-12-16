.. highlight:: console

.. author:: apoxa <https://github.com/apoxa>

.. tag:: lang-go
.. tag:: irc
.. tag:: bouncer

.. spelling::
    Soju
    soju
    upstreams

##########
Soju
##########

.. tag_list::

soju_ is a user-friendly IRC bouncer which supports multiple users, multiple clients for a single user with backlog synchronization and multiple upstreams via a single IRC connection to the bouncer.

----

.. note:: For this guide you should be familiar with the basic concepts of

  * :manual:`Firewall Ports <basics-ports>`
  * :manual:`supervisord <daemons-supervisord>`

License
=======

All relevant legal information can be found here:

  * https://git.sr.ht/~emersion/soju/tree/master/item/LICENSE

Prerequisites
=============

.. include:: includes/open-port.rst

You should note down this port. You will need it later in the configuration file.

Installation
============

Clone the source into your home directory and enter the directory:

.. code-block:: console

 [isabell@stardust ~]$ git clone https://git.sr.ht/~emersion/soju

Compile and install soju to your home directory:

.. code-block:: console

 [isabell@stardust ~]$ cd ~/soju
 [isabell@stardust soju]$
 [isabell@stardust soju]$ make -W doc/soju.1
 [...]
 [isabell@stardust soju]$ PREFIX="/.local" DESTDIR="$HOME" make install
 [...]
 [isabell@stardust soju]$

Configuration
=============

Configure soju
--------------

Save the following as your soju configuration in ``~/etc/soju/config``.

.. code-block:: ini

 listen ircs://0.0.0.0:40132
 tls /home/isabell/etc/certificates/isabell.uber.space.crt /home/isabell/etc/certificates/isabell.uber.space.key
 hostname isabell.uber.space
 db sqlite3 /home/isabell/var/lib/soju/soju.db

.. warning:: Replace `ìsabell` with your username and the port with the one you opened in the firewall in the first step.

Setup daemon
------------
Create ``~/etc/services.d/soju.ini`` with the following content:

.. code-block:: ini

 [program:soju]
 command=%(ENV_HOME)s/.local/bin/soju -config %(ENV_HOME)s/etc/soju/config
 autostart=yes
 autorestart=yes

.. include:: includes/supervisord.rst

If it's not in state RUNNING, check your configuration.

Create a user
-------------
.. note:: Replace ``isabell`` with your username!

.. code-block:: console

 [isabell@stardust ~]$ ./.local/bin/sojuctl -config $HOME/etc/soju/config create-user <username> -admin
 Password:
 [isabell@stardust ~]$

Replace `<username>` with the username you want to use in the bouncer.
It will prompt you for a password now.

You can add additional users with the same command or later via the BouncerServ_ builtin service.

Connect your client
-------------------

Add a new server in your local IRC client. The username and password are the ones you provided in the `create-user` command before.

* Hostname: `<username>.uber.space`
* Port: your port
* Username: soju nickname
* Password: soju password
* Encryption: yes

You can also append an IRC server to your username. This is called the Single Upstream Mode and will automatically connect you to this network.
If you don't do this, you will use the Multiple Upstream Mode.
Check the manpage_ for more information about this.

Updates
=======

.. note:: Check the gitrefs_ regularly to stay informed about the newest version.

To update an existing installation, first stop the service (``supervisorctl stop soju``). After that remove the ``~/soju`` directory (``rm -rf ~/soju``) and repeat the **Installation** steps. Execute ``supervisorctl restart soju`` to start the new version.

.. _soju: https://soju.im/
.. _gitrefs: https://git.sr.ht/~emersion/soju/refs
.. _manpage: https://soju.im/doc/soju.1.html
.. _bouncerserv: https://soju.im/doc/soju.1.html#IRC_SERVICE

----

Tested with soju 0.4.0, Uberspace 7.12.1

.. author_list::
