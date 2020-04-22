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

We're using :manual:`Node.js <lang-nodejs>` in the stable version 12:

::

 [isabell@stardust ~]$ uberspace tools version use node 12
 Selected Node.js version 12
 [isabell@stardust ~]$

We also need `Bower`:

::

 [isabell@stardust ~]$ npm install -g bower
 npm WARN deprecated bower@1.8.8: We don't recommend using Bower for new projects. Please consider Yarn and Webpack or Parcel. You can read how to migrate legacy project here: https://bower.io/blog/2017/how-to-migrate-away-from-bower/

Please ignore Bower's warning. As of this writing, CryptPad still uses Bower (not Yarn, not Parcel), and so will you.

Installation
============

Start with cloning the Cryptpad source code from Github_ and be sure to replace the branch ``3.16.0`` with the current release number from the feed_:

.. code-block:: console

  [isabell@stardust ~]$ git clone --branch 3.16.0 https://github.com/xwiki-labs/cryptpad.git ~/cryptpad
  Cloning into '~/cryptpad'...
  remote: Enumerating objects: 136, done.
  remote: Counting objects: 100% (136/136), done.
  remote: Compressing objects: 100% (86/86), done.
  remote: Total 75814 (delta 79), reused 93 (delta 50), pack-reused 75678
  Receiving objects: 100% (75814/75814), 171.23 MiB | 21.62 MiB/s, done.
  Resolving deltas: 100% (48757/48757), done.
  Note: checking out 'b0b4029556d89d8b6b0c30e9dfab528edb65813b'.


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
  added 212 packages from 231 contributors and audited 375 packages in 9.467s
  (...)
  found 0 vulnerabilities
  [isabell@stardust cryptpad]$ bower install
  (...)
  bower install       open-sans-fontface#1.4.2
  bower install       jquery#2.2.4
  bower install       bootstrap#4.4.1
  (...)

Configuration
=============

Copy example configuration
--------------------------

.. code-block:: console

  [isabell@stardust cryptpad]$ cp config/config.example.js config/config.js

Edit ``config/config.js`` and edit following lines:

1. Uncomment the line beginning with ``//httpSafeOrigin:`` by removing the two slashes, and replace your instance URL like so:

.. code-block:: js

  httpSafeOrigin: "https://isabell.uber.space/",


2. Find the line ``//httpAddress: '::',`` and uncomment it by removing the two slashes. The value `::` remains as it is.

3. Find the line ``adminEmail: 'i.did.not.read.my.config@cryptpad.fr',`` and replace your e-mail address.

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
  [isabell@stardust cryptpad]$ git pull origin 3.16.0
  From https://github.com/xwiki-labs/cryptpad
   * tag                 3.16.0     -> FETCH_HEAD
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

Tested with Cryptpad 3.16.0 and Uberspace 7.6.0.0

.. author_list::
