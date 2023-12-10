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

Your website domain or subdomain needs to be setup up:

.. include:: includes/web-domain-list.rst

We're using :manual:`Node.js <lang-nodejs>` version 20, but others should work too:

::

  [isabell@stardust ~]$ uberspace tools version use node 20
  Selected Node.js version 20
  The new configuration is adapted immediately. Minor updates will be applied automatically.
  [isabell@stardust ~]$

Setup your URL:

.. include:: includes/web-domain-list.rst

Installation
============

Start with cloning the Cryptpad source code from Github_ and be sure to replace the branch ``5.5.0`` with the current release number from the feed_:

.. code-block:: console

  [isabell@stardust ~]$ git clone --branch 5.5.0 --depth 1 https://github.com/cryptpad/cryptpad.git ~/cryptpad
  Cloning into '~/cryptpad'...
  remote: Enumerating objects: 15111, done.
  remote: Counting objects: 100% (15111/15111), done.
  remote: Compressing objects: 100% (11685/11685), done.
  remote: Total 15111 (delta 3527), reused 14548 (delta 3359), pack-reused 0
  Receiving objects: 100% (15111/15111), 84.83 MiB | 16.52 MiB/s, done.
  Resolving deltas: 100% (3527/3527), done.
  Note: checking out 'b0b4029556d89d8b6b0c30e9dfab528edb65813b'.

  You are in 'detached HEAD' state. You can look around, make experimental
  changes and commit them, and you can discard any commits you make in this
  state without impacting any branches by performing another checkout.

  If you want to create a new branch to retain commits you create, you may
  do so (now or later) by using -b with the checkout command again. Example:

  git checkout -b <new-branch-name>

  Checking out files: 100% (19152/19152), done.
  [isabell@stardust ~]$


Now we need to install the dependencies:

.. code-block:: console

  [isabell@stardust ~]$ cd ~/cryptpad
  [isabell@stardust cryptpad]$ npm install
  added 469 packages, and audited 470 packages in 57s
  (...)
  found 0 vulnerabilities
  [isabell@stardust cryptpad]$ npm run install:components
  (...)
  [isabell@stardust cryptpad]$


Configuration
=============

Copy example configuration
--------------------------

.. code-block:: console

  [isabell@stardust ~]$ cd ~/cryptpad/
  [isabell@stardust cryptpad]$ cp config/config.example.js config/config.js
  [isabell@stardust cryptpad]$


Update configuration
--------------------

Open ``config/config.js`` in an editor and edit following lines:

1. Replace your instance URL for ``httpUnsafeOrigin:`` like so:

.. code-block:: js

  httpUnsafeOrigin: 'https://isabell.uber.space/',

This is the URL that will be used from the outside to access the Cryptpad installation.

2. Find the line ``//httpAddress: '::',`` and uncomment it by removing the two slashes. The value ``::`` remains as it is.
This will make sure that the server listens on all network interfaces.

3. Find the line ``//httpSafePort: 3000,``, uncomment it and replace the port with 80:

.. code-block:: js

  httpSafePort: 80,

Unfortunatley, it seems impossible to run Cryptpad with an unsafe and a safe domain as suggested. This would make it possible to mitigate cross site scripting attacks. That is why only the `httpUnsafeOrigin` is set while the `httpSafeOrigin`is not set. So it is surprsing that the `httpSafePort` needs to be set. This is a hack to make Cryptpad generate the correct URL in the HTML.

.. note::
  If you forget to make change 2, the command ``uberspace web backend list`` will later complain as follows:

  .. code-block:: console

   [isabell@stardust ~]$ uberspace web backend list
   / http:3000 => NOT OK, wrong interface (127.0.0.1): PID 15682, /usr/bin/node server

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


Configure web server
--------------------

.. note::

    Cryptpad is running on port 3000. You need to use ``/`` or a sub-domain since subfolders are not allowed in cryptpad.

.. include:: includes/web-backend.rst

Customization
=============

For any further configuration or customization you should have a look at the `Cryptpad Wiki`_.

Also you should configure a password salt as explained in the `Cryptpad Admin Guide`. You probably want to set up an admin account in ``config/config.js``.

Updates
=======

.. note:: Check the update feed_ regularly to stay informed about the newest version.


If there is a new version available, you can get the code using git. Replace the version number ``5.5.0`` with the latest version number you got from the release feed_:

.. code-block:: console

  [isabell@stardust ~]$ cd ~/cryptpad
  [isabell@stardust cryptpad]$ git pull origin 5.5.0
  From https://github.com/cryptpad/cryptpad
   * tag                 5.5.0     -> FETCH_HEAD
  Already up to date.

  [isabell@stardust cryptpad]$

Now update the dependencies:

.. code-block:: console

  [isabell@stardust cryptpad]$ npm update
  removed 1 package and audited 313 packages in 14.535s
  found 0 vulnerabilities

  [isabell@stardust cryptpad]$ npm run install:components
  (...)
  [isabell@stardust cryptpad]$

Then you need to restart the service, so the new code is used by the webserver:

.. code-block:: console

  [isabell@stardust cryptpad]$ supervisorctl restart cryptpad
  [isabell@stardust cryptpad]$

.. _`Cryptpad`: https://cryptpad.fr/
.. _`ChainPad`: https://github.com/cryptpad/chainpad
.. _Github: https://github.com/cryptpad/cryptpad
.. _feed: https://github.com/cryptpad/cryptpad/releases
.. _`Cryptpad Admin Guide`: https://docs.cryptpad.org/en/admin_guide/customization.html


----

Tested with Cryptpad 5.5.0 and Uberspace 7.15.6

.. author_list::
