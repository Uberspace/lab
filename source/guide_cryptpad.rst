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

Your webseite domain or subdomain needs to be setup up:

.. include:: includes/web-domain-list.rst


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

Start with cloning the Cryptpad source code from Github_ and be sure to replace the branch ``3.16.0`` with the current release number from the feed_:

.. code-block:: console

  [isabell@stardust ~]$ git clone --branch 3.16.0 --depth 1 https://github.com/xwiki-labs/cryptpad.git ~/cryptpad
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
  added 212 packages from 231 contributors and audited 375 packages in 4.828s
  (...)
  found 0 vulnerabilities
  [isabell@stardust cryptpad]$ bower install
  (...)
  [isabell@stardust cryptpad]$ 

Configuration
=============

Copy example configuration
--------------------------

.. code-block:: console

  [isabell@stardust cryptpad]$ cp config/config.example.js config/config.js

Edit ``config/config.js``, enable and change the value of the variable ``httpSafeOrigin:`` to your domain, like below. Additionally change the ``httpAddress`` that the web backends can listen to them.

.. code-block:: js

  httpSafeOrigin: "https://isabell.uber.space",
  (...)
  httpAddress: '0.0.0.0',

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

Updates
=======

.. note:: Check the update feed_ regularly to stay informed about the newest version.


If there is a new version available, you can get the code using git. Replace the version number ``3.16.0`` with the latest version number you got from the release feed_:

.. code-block:: console

  [isabell@stardust ~]$ cd ~/cryptpad
  [isabell@stardust cryptpad]$ git pull origin 3.16.0
  From https://github.com/xwiki-labs/cryptpad
   * tag                 3.16.0     -> FETCH_HEAD
  Already up to date.

  [isabell@stardust cryptpad]$

Now update the dependencies:

.. code-block:: console

  [isabell@stardust cryptpad]$ npm install
  removed 1 package and audited 313 packages in 14.535s
  found 0 vulnerabilities

  [isabell@stardust cryptpad]$ bower update
  (...)
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

Tested with Cryptpad 3.16.0 and Uberspace 7.6.0

.. author_list::
