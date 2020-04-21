.. author:: humbug <uberspace@humbug.pw>

.. tag:: lang-nodejs
.. tag:: web
.. tag:: file-storage
.. tag:: collaborative-editing

.. highlight:: console

.. sidebar:: Logo

  .. image:: _static/images/cryptpad.png
      :align: center

########
Cryptpad
########

.. tag_list::

`Cryptpad`_ is a Zero Knowledge realtime collaborative editor. It is based on :manual:`Node.js <lang-nodejs>` and comes with encryption. It relies on the `ChainPad`_.

----

.. note:: For this guide you need some tools:

  * :manual:`web backends <web-backends>`
  * :manual:`Node.js <lang-nodejs>` and its package manager :manual_anchor:`npm <lang-nodejs.html#npm>`
  * :manual:`supervisord <daemons-supervisord>`
  * :manual:`domains <web-domains>`

Prerequisites
=============

Set up the backends:

::

  [isabell@stardust ~]$ uberspace web backend set / --http --port 3000
  Set backend for / to port 3000; please make sure something is listening!
  You can always check the status of your backend using "uberspace web backend list".
  [isabell@stardust ~]$

You need to use ``/`` or ``domain.example/`` in the domain part since subfolders are not allowed in cryptpad.

Now let's get started with Cryptpad.

We're using :manual:`Node.js <lang-nodejs>` in the stable version 10:

::

 [isabell@stardust ~]$ uberspace tools version use node 10
 Selected Node.js version 10
 [isabell@stardust ~]$

We also need `Bower`:

::

 [isabell@stardust ~]$ npm install -g bower
 [isabell@stardust ~]$

Installation
============

Start with cloning the Cryptpad source code from Github_ and be sure to replace the branch ``2.21.0`` with the current release number from the feed_:

.. code-block:: console

  [isabell@stardust ~]$ git clone --branch 2.21.0 https://github.com/xwiki-labs/cryptpad.git ~/cryptpad
  Cloning into '~/cryptpad'...
  remote: Enumerating objects: 172, done.
  remote: Counting objects: 100% (172/172), done.
  remote: Compressing objects: 100% (105/105), done.
  remote: Total 43165 (delta 99), reused 109 (delta 67), pack-reused 42993
  Receiving objects: 100% (43165/43165), 85.51 MiB | 4.81 MiB/s, done.
  Resolving deltas: 100% (30989/30989), done.
  Note: checking out '135182ea0a3500d27afe0146c94e112e1726ae7e'.

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

  [isabell@stardust ~]$ cd ~/cryptpad
  [isabell@stardust cryptpad]$ npm install
  (...)
  added 168 packages from 186 contributors and audited 311 packages in 14.352s
  found 0 vulnerabilities
  [isabell@stardust cryptpad]$ bower install
  (...)
  bower install       open-sans-fontface#1.4.2
  bower install       jquery#2.1.4
  bower install       bootstrap#4.3.1
  (...)

Configuration
=============

Copy example configuration
--------------------------

.. code-block:: console

  [isabell@stardust cryptpad]$ cp config/config.example.js config/config.js

Edit ``config/config.js`` and change the value of the variable ``_domain`` to your domain, like so:

.. code-block:: js

  /*
      globals module
  */
  var _domain = 'https://isabell.uber.space/';

Setup daemon
------------

Create ``~/etc/services.d/cryptpad.ini`` with the following content:

.. code-block:: ini

 [program:cryptpad]
 directory=%(ENV_HOME)s/cryptpad
 command=node server
 startsecs=60
 autorestart=yes

Now let's start the service:

.. include:: includes/supervisord.rst


Customization
=============

For any further configuration or customization you should have a look at the `Cryptpad Wiki`_.

Updates
=======

.. note:: Check the update feed_ regularly to stay informed about the newest version.


If there is a new version available, you can get the code using git. Replace the version number ``2.19.0`` with the latest version number you got from the release feed_:

.. code-block:: console

  [isabell@stardust ~]$ cd ~/cryptpad
  [isabell@stardust cryptpad]$ git pull origin 2.19.0
  From https://github.com/xwiki-labs/cryptpad
   * tag                 2.19.0     -> FETCH_HEAD
  Already up to date.

  [isabell@stardust cryptpad]$

Now updated dependencies:

.. code-block:: console

  [isabell@stardust cryptpad]$ npm i
  removed 1 package and audited 313 packages in 14.535s
  found 0 vulnerabilities

  [isabell@stardust cryptpad]$ bower update
  {... bower output ...}
  [isabell@stardust cryptpad]$

Then you need to restart the service, so the new code is used by the webserver:

.. code-block:: console

  [isabell@stardust cryptpad]$ supervisorctl restart cryptpad
  [isabell@stardust cryptpad]$

.. _`Cryptpad`: https://cryptpad.fr/
.. _`ChainPad`: https://github.com/xwiki-contrib/chainpad/
.. _`Bower`: https://bower.io/
.. _Github: https://github.com/xwiki-labs/cryptpad
.. _feed: https://github.com/xwiki-labs/cryptpad/releases
.. _`Cryptpad Wiki`: https://github.com/xwiki-labs/cryptpad/wiki/

----

Tested with Cryptpad 2.19.0 and Uberspace 7.2.4.0

.. author_list::
