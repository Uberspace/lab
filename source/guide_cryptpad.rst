.. author:: humbug <uberspace@humbug.pw>
.. highlight:: console

.. sidebar:: Logo

  .. image:: _static/images/cryptpad.png
      :align: center

########
Cryptpad
########

`Cryptpad`_ is a Zero Knowledge realtime collaborative editor. It is based on :manual:`Node.js <lang-nodejs>` and comes with encryption. It relies on the `ChainPad`_.

----

.. note:: For this guide you need some tools:

  * `Web Backends`_ (You have to opt-in the Beta. Write an E-Mail to `hallo@uberspace.de`_
  * :manual:`Node.js <lang-nodejs>` and its package manager :manual_anchor:`npm <lang-nodejs.html#npm>`
  * :manual:`supervisord <daemons-supervisord>`
  * :manual:`domains <web-domains>`

Prerequisites
=============

After we're enrolled into the beta, we need to setup the Web Backends:

::

  [isabell@stardust ~]$ uberspace web backend set isabell.uber.space --http --port 3000
  Set backend for isabell.uber.space/ to port 3000; please make sure something is listening!
  You can always check the status of your backend using "uberspace web backend list".
  [isabell@stardust ~]$

Now let's get started with Cryptpad.

We're using :manual:`Node.js <lang-nodejs>` in the stable version 6:

::

 [isabell@stardust ~]$ uberspace tools version use node 6
 Selected Node.js version 6
 [isabell@stardust ~]$

We also need `Bower`:

::

 [isabell@stardust ~]$ npm install -g bower
 [isabell@stardust ~]$

Installation
============

Start with cloning the Cryptpad source code from Github_ and be sure to replace the branch ``2.18.0`` with the current release number from the feed_:

.. code-block:: console

  [isabell@stardust ~]$ git clone --branch 2.18.0 https://github.com/xwiki-labs/cryptpad.git ~/html
  Cloning into '~/html'...
  remote: Enumerating objects: 172, done.
  remote: Counting objects: 100% (172/172), done.
  remote: Compressing objects: 100% (105/105), done.
  remote: Total 43165 (delta 99), reused 109 (delta 67), pack-reused 42993
  Receiving objects: 100% (43165/43165), 85.51 MiB | 4.81 MiB/s, done.
  Resolving deltas: 100% (30989/30989), done.
  Note: checking out 'dcabff7c08a10930692e13d3f82e2b7e7b764efa'.

  You are in 'detached HEAD' state. You can look around, make experimental
  changes and commit them, and you can discard any commits you make in this
  state without impacting any branches by performing another checkout.

  If you want to create a new branch to retain commits you create, you may
  do so (now or later) by using -b with the checkout command again. Example:

    git checkout -b <new-branch-name>

  Checking out files: 100% (4319/4319), done.
  [isabell@stardust ~]$


Now we need to install some dependencies:

.. code-block:: console

  [isabell@stardust ~]$ cd ~/html
  [isabell@stardust html]$ npm install
  [isabell@stardust html]$ bower install


Configuration
=============

Copy example configuration
--------------------------

.. code-block:: console

  [isabell@stardust html]$ cp config.example.js config.js

Change the value of the variable ``_domain`` to match your newly created ``https://isabell.uber.space``.

Due to the Web Backends we don't need to mess with ``.htaccess`` or any other configuration.

Setup daemon
------------

Create ``~/etc/services.d/cryptpad.ini`` with the following content:

.. warning:: Set ``directory`` to the directory of cryptpad!

.. code-block:: ini

 [program:cryptpad]
 directory=%(ENV_HOME)s/html
 command=node server
 autostart=yes
 autorestart=yes

Now let's start the service:

.. code-block:: console

 [isabell@stardust html]$ supervisorctl reread
 [isabell@stardust html]$ supervisorctl update
 [isabell@stardust html]$ supervisorctl start cryptpad
 [isabell@stardust html]$ supervisorctl status
 cryptpad                         RUNNING   pid 23323, uptime 0:07:29


Customization
=============

For any futher configuration or customization you should have a look at the `Wiki`_.

Updates
=======

.. note:: Check the update feed_ regularly to stay informed about the newest version.


If there is a new version available, you can get the code using git. Replace the pseudo version number ``2.18.0`` with the latest version number you got from the release feed_:

.. code-block:: console

  [isabell@stardust ~]$ cd ~/html
  [isabell@stardust html]$ git pull origin 2.18.0
  From https://github.com/xwiki-labs/cryptpad
   * tag                 2.18.0     -> FETCH_HEAD
  Already up to date.
  [isabell@stardust html]$

Then you need to restart the service, so the new code is used by the webserver:

.. code-block:: console

  [isabell@stardust html]$ supervisorctl restart cryptpad
  [isabell@stardust html]$

.. _`Cryptpad`: https://cryptpad.fr/
.. _`ChainPad`: https://github.com/xwiki-contrib/chainpad/
.. _`Web Backends`: https://blog.uberspace.de/web-backends-websockets/
.. _`hallo@uberspace.de`: hallo@uberspace.de
.. _`Bower`: https://bower.io/
.. _Github: https://github.com/xwiki-labs/cryptpad
.. _feed: https://github.com/xwiki-labs/cryptpad/releases
.. _`Wiki`: https://github.com/xwiki-labs/cryptpad/wiki/

----

Tested with Cryptpad 2.18.0 and Uberspace 7.2.4.0

.. authors::
