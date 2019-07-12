.. author:: Michael Kühnel <https://michael-kuehnel.de>

.. tag:: lang-nodejs
.. tag:: web
.. tag:: iot

.. highlight:: console

.. sidebar:: Logo

  .. image:: _static/images/mosca.png
      :align: center

#####
Mosca
#####

.. tag_list::

Mosca_ Mosca is a MQTT broker. It implements the MQTT protocol, so that you can run your own MQTT server on Node.js.

----

.. note:: For this guide you should be familiar with the basic concepts of

  * :manual:`Node.js <lang-nodejs>` and its package manager :manual_anchor:`npm <lang-nodejs.html#npm>`
  * :manual:`Firewall Ports <basics-ports>`
  * :manual:`web backends <web-backends>`
  * :manual:`Domains <web-domains>`
  * :manual:`supervisord <daemons-supervisord>`

Prerequisites
=============

Node and npm
------------

.. warning::
  We have to use :manual:`Node.js <lang-nodejs>` in version 6.x. since Mosca can’t be installed with newer versions until `this issue <https://github.com/mcollina/mosca/issues/782/>`_ is fixed.

  So we have to install the Node Version Manager (`nvm <https://github.com/nvm-sh/nvm>`_) to simply switch between Node.js versions.

Install nvm:

.. code-block:: bash

 [isabell@stardust ~]$ curl -o- https://raw.githubusercontent.com/nvm-sh/nvm/v0.34.0/install.sh | bash
 [isabell@stardust ~]$ source .bashrc
 [isabell@stardust ~]$

Check if nvm is properly installed:

.. code-block:: bash

 [isabell@stardust ~]$ nvm --version
 0.34.0
 [isabell@stardust ~]$

This should return ``0.34.0`` or above.

Install Node 6:

.. code-block:: bash

 [isabell@stardust ~]$ nvm install 6
 [isabell@stardust ~]$ node --version
 v6.17.1
 [isabell@stardust ~]$

This should return version ``v6.17.1`` or a greater Node 6.x.x version.

We will need to update the Node Package Manager npm:

.. code-block:: bash

  [isabell@stardust ~]$ npm install npm@latest -g
  [isabell@stardust ~]$ npm --version
  6.10.1
  [isabell@stardust ~]$

This should return a version from ``6.10.1`` upwards.

.. _retrieved:

Opening ports
-------------

.. include:: includes/open-port.rst

.. important::
  You have to repeat this step **four** times to make use of all possible connection types:

  1. MQTT, encrypted
  2. MQTT over WebSockets, encrypted
  3. MQTT, unencrypted
  4. MQTT over WebSockets, unencrypted

Domain
------

Your URL needs to be setup:

.. include:: includes/web-domain-list.rst

.. tip:: See :manual:`Domains <web-domains>` to setup an own domain pointing to your uberspace.

Installation
============

Global installation
-------------------

Mosca (and the logging library Bunyan) needs to be installed globally via:

.. code-block:: bash

  [isabell@stardust ~]$ npm install --global mosca bunyan
  [isabell@stardust ~]$

.. note:: You don’t have to take care about warnings during the installation process.

Configuration
=============

Additional files
----------------

Create the needed files and directories needed for our setup:

.. code-block:: bash

  [isabell@stardust ~]$ mkdir -p ~/mqtt-server/public
  [isabell@stardust ~]$ cd ~/mqtt-server
  [isabell@stardust ~]$ touch public/{index.html,style.css}
  [isabell@stardust ~]$

.. _index.html:

Fill ``~/mqtt-server/public/index.html`` with the following content:

.. important::
  Replace the [port] numbers with the 4 different ones you retrieved_ before.

  Enter ``uberspace port list`` to list them.

.. code-block:: html

  <!DOCTYPE html>
  <html lang="en">
    <head>
      <title>MQTT Broker!</title>
      <meta charset="utf-8" />
      <meta http-equiv="X-UA-Compatible" content="IE=edge" />
      <meta name="viewport" content="width=device-width, initial-scale=1" />
      <link rel="stylesheet" href="/style.css" />
    </head>
    <body>
      <header>
        <h1>MQTT Broker</h1>
      </header>
      <main>
        <p class="bold">Oh hi,</p>
        <p>it’s me. A simple MQTT Broker.</p>
        <p>I’m listening on the following ports:</p>
        <ul>
          <li>[port] : MQTT, encrypted</li>
          <li>[port] : MQTT over WebSockets, encrypted</li>
          <li>[port] : MQTT, unencrypted</li>
          <li>[port] : MQTT over WebSockets, unencrypted</li>
        </ul>
      </main>
    </body>
  </html>


Fill ``~/mqtt-server/public/style.css`` with the following content:

.. code-block:: css

  * { box-sizing: border-box; }

  body {
    font-family: system, -apple-system, "Roboto", "Segoe UI", "Helvetica Neue", sans-serif;
    margin: 2em;
  }

  h1 {
    font-style: italic;
    color: #915bf6;
  }

  .bold { font-weight: bold; }

  ul {
    list-style-type: none;
    padding-left: 10px;
  }

  li:before {
    display: inline-block;
    content: '–';
    margin-right: 10px;
  }

Authentication
--------------

Mosca supports user authentication through the use of a specific json file.

In order to create ``credentials.json`` and a default user run the following command:

.. warning::
  Replace ``<user>`` and ``<pass>`` with your desired credentials.
  The default user is authorized to publish and subscribe to each and every channel!

.. code-block:: bash

  [isabell@stardust ~]$ cd ~/mqtt-server
  [isabell@stardust ~]$ mosca adduser <user> <pass> --credentials ./credentials.json
  [isabell@stardust ~]$

.. tip::
  See Moscas documentation about `Authorization <https://github.com/mcollina/mosca/wiki/Mosca-as-a-standalone-service.#authorization>`_ to learn how to add users with specifying authorized topics und how to remove users.

  Store your credentials securely because they are stored hashed and salted in ``credentials.json``.

Configure web server
--------------------

.. important::

  Replace ``<port>`` with the the port you defined for *»MQTT over WebSockets, unencrypted* in your index.html_.

.. include:: includes/web-backend.rst

Finishing installation
======================

Starting the server
-------------------

.. important::

  Replace the ``<PORT>`` numbers with the correct ones you have defined for the different protocols in your index.html_.

  Replace ``<username>`` with your Uberspace username.

.. code-block:: bash

  [isabell@stardust ~]$ cd ~
  [isabell@stardust ~]$ mosca --credentials ~/mqtt-server/credentials.json \
     --non-secure \
     --port <MQTT_PORT> \
     --secure-port <SECURE_MQTT_PORT> \
     --http-port <HTTP_PORT> \
     --https-port <HTTPS_PORT> \
     --http-static ~/mqtt-server/public \
     --broker-id myMosca \
     --cert ~/etc/certificates/<username>.uber.space.crt \
     --key ~/etc/certificates/<username>.uber.space.key \
     --verbose
  [isabell@stardust ~]$

.. note:: See `Moscas documentation <https://github.com/mcollina/mosca/wiki/Mosca-as-a-standalone-service.#configuration>`_ for all available options.

Check installation
------------------

If you did configured the ports the right way the MQTT server should show the HTML page when you open the server via https in the browser:

.. note:: Replace ``<username>`` with your Uberspace username.

`https://<username>.uber.space <https://isabell.uber.space>`_

You should additionally check if you can connect via the other protocols with the defined credentials by using a MQTT GUI Client like `MQTT Explorer <http://mqtt-explorer.com/>`_.

.. _alias:

Setup an alias
--------------

I guess you would like to setup an alias to prevent typos when entering that pretty long command to start the server.

Just enter the following in ``~/.bashrc``:

.. important::

  Replace the ``<PORT>`` numbers with the correct ones you have defined for the different protocols in your index.html_.

  Replace ``<username>`` with your Uberspace username.

.. code-block:: bash

  alias startserver="mosca --credentials ~/mqtt-server/credentials.json --non-secure --port <MQTT_PORT> --secure-port <SECURE_MQTT_PORT> --http-port <HTTP_PORT> --https-port <HTTPS_PORT> --http-static ~/mqtt-server/public --broker-id myMosca --cert ~/etc/certificates/<username>.uber.space.crt --key ~/etc/certificates/<username>.uber.space.key --verbose"

.. tip:: Reload bash via ``source ~/.bashrc`` to immediately make use of that alias.

Setup daemon
------------

Create ``~/etc/services.d/mosca.ini`` with the following content:

.. warning:: The ``command`` will only work if you have set up the alias_ ``startserver`` like described above.

.. code-block:: ini

  [program:mosca]
  command=/bin/bash -c -i "source ~/.bashrc && startserver"
  autostart=yes
  autorestart=yes

.. include:: includes/supervisord.rst

.. _Mosca: https://github.com/mcollina/mosca

----

Tested with Mosca 2.8.3 and Uberspace 7.3.3.0

.. author_list::
