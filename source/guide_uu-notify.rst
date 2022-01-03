.. highlight:: console

.. author:: franok <https://franok.de>

.. categorize your guide! refer to the current list of tags: https://lab.uberspace.de/tags
.. tag:: lang-nodejs
.. tag:: updates

.. sidebar:: Logo

  .. image:: _static/images/uu-notify-icon.png
      :align: center

##########
uuNotify
##########

.. tag_list::

uuNotify_ is a script that can be used to regularly check for updates of software, which you have installed on your Uberspace.

It requires a `gotify server <https://gotify.net/>`_, which will send notifications to your client (e.g. a smartphone), if updates are available. The script will not install the updates automatically.


----

.. note:: For this guide you should be familiar with the basic concepts of

  * :manual:`Node.js <lang-nodejs>` and its package manager :manual_anchor:`npm <lang-nodejs.html#npm>`
  * The concepts mentioned in the :lab:`Gotify Guide <guide_gotify>`

  Furthermore, you need a GitHub account to create a `personal access token <https://docs.github.com/en/github/authenticating-to-github/keeping-your-account-and-data-secure/creating-a-personal-access-token>`_. The token is only used for fetching the latest release information from GitHub. No scopes required.

.. note:: Wherever mentioned, replace ``v0.0.0`` with the latest_ version tag.

License
=======

All relevant legal information is mentioned in uuNotify's LICENSE_.

Prerequisites
=============

Node.js version
---------------

We're using :manual:`Node.js <lang-nodejs>` version 14.

.. code-block:: console

  [isabell@stardust ~]$ uberspace tools version use node 14
  Selected Node.js version 14
  The new configuration is adapted immediately. Minor updates will be applied automatically.
  [isabell@stardust ~]$


Gotify Server
-------------

You have installed and configured your Gotify server, :lab:`as described in the respective guide <guide_gotify>`.

Limitations
===========

Since uuNotify uses the GitHub API, only software available on GitHub is checked for updates. It is planned to support other release feeds in a future version of uuNotify (see `uuNotify GitHub issues <https://github.com/franok/uu-notify/issues/2>`_).

Installation
============

Clone the `GitHub repository <https://github.com/franok/uu-notify>`_, checkout the latest_ version and run the setup script.

.. code-block:: console

  [isabell@stardust ~]$ UUN_VERSION=v0.0.0
  [isabell@stardust ~]$ git clone https://github.com/franok/uu-notify
  [isabell@stardust ~]$ cd uu-notify/
  [isabell@stardust uu-notify]$ git checkout $UUN_VERSION
  [isabell@stardust uu-notify]$ git branch
  * (HEAD detached at <latest version>)
    main
  [isabell@stardust uu-notify]$ ./setup.sh
  --- uuNotify setup ---
  Existing files in config/ will not be overwritten.

  Running 'npm clean-install' ...
  [...]
  Done.

  Copy configuration files...
  Creating config.json from config.json.template ...
  Done.
  Creating software-deps.mjs from software-deps.mjs.example ...
  Done.

  --- COMPLETED uuNotify setup ---
  [isabell@stardust uu-notify]$

Configuration
=============

.. _id-gotify-application:

Gotify application
------------------

Create a Gotify application.
Log in to your Gotify server's WebUI, click the ``Apps``-tab in the menu bar and create an application. An app token is generated automatically. You'll need it in the :ref:`next step <id-configure-uuNotify>`.


.. _id-configure-uuNotify:

Configure uuNotify
------------------

In the uuNotify directory, navigate into the ``config/`` folder:

.. code-block:: console

  [isabell@stardust uu-notify]$ cd config/
  [isabell@stardust config]$

Edit the file ``config.json``.

Add your Gotify server url and the app token from the previous step. Example:

.. code-block:: json

  {
    "gotify": {
        "url": "https://isabell.uber.space/gotify",
        "token": "AbccRsTUvwXX5yQ"
    },
    [...]
  }

.. note:: The gotify server URL must end **without** trailing forward slash ``/``

  | Good example: ``https://isabell.uber.space/gotify``
  | Bad example: ``https://isabell.uber.space/gotify/``


Now add your `personal GitHub access token <https://docs.github.com/en/github/authenticating-to-github/keeping-your-account-and-data-secure/creating-a-personal-access-token>`_. This token does not require any scopes. Example:

.. code-block:: json

  {
    [...]
    "github": {
        "personalAccessToken": "ghp_oJoo9cootieKieyahzei7eifieHiyoh6"
    }
  }


Add your software dependencies
------------------------------

Edit the file ``software-deps.mjs`` and add a new object into the array for every software you wish to receive update notifications for. Example:

.. code-block:: js

  export const software = [
    {
        name: "uu-notify",
        feedUrl: "https://github.com/franok/uu-notify/releases.atom",
        github: {
            org: "franok",
            repo: "uu-notify"
        }
    },
    {
        name: "other-software-name",
        feedUrl: "https://github.com/org/repo/releases.atom",
        github: {
            org: "org-name",
            repo: "repo-name"
        }
    }
  ];

If you wish to add further software later, just update this file. With the next (scheduled) execution, uuNotify will also check for updates for the newly added entries.

.. _id-client-side:

Client side
===========

To receive the uuNotify update notifications, you need to have a Gotify client in place. You can use Gotify's built-in web-ui, or the Android app (available via `F-Droid <https://f-droid.org/de/packages/com.github.gotify/>`_, `GooglePlay <https://play.google.com/store/apps/details?id=com.github.gotify>`_ or `direct APK download <https://github.com/gotify/android/releases/latest>`_). There is `no native iOS App <https://github.com/gotify/server/issues/87>`_, but iPhone users could use the web-ui and get browser notifications.


Finishing installation
======================

Initialize uuNotify by running the script manually:

.. code-block:: console

  [isabell@stardust ~]$ cd uu-notify/
  [isabell@stardust uu-notify]$ node index.mjs
  Script finished.
  [isabell@stardust uu-notify]$

You should receive initial notifications for all your registered software.

After that, register uuNotify in your :manual:`crontab <daemons-cron>`.

.. code-block:: console

  [isabell@stardust ~]$ crontab -e

Copy and paste the following lines into your crontab, by appending them to the end of the existing entries:

.. code-block:: bash

  #MAILTO=""
  0 18 * * SUN /usr/bin/node /home/isabell/uu-notify/index.mjs

This crontab configuration will run uuNotify every Sunday at 18:00.
If there are any software updates, you'll receive a notification.

If you want uuNotify to check for updates more often, you can adjust the time and frequency to your needs. I suggest you to double check your cron schedule expression with `crontab guru <https://crontab.guru/>`_.

Check your crontab configuration:

.. code-block:: console

  [isabell@stardust ~]$ crontab -l
  #MAILTO=""
  0 18 * * SUN /usr/bin/node /home/isabell/uu-notify/index.mjs


Optional
========

Add an icon to your Gotify app
--------------------------------------------

The :ref:`Gotify app you created <id-gotify-application>` will show up in your :ref:`Gotify client<id-client-side>` when notifications are received. You can customize it with an app icon, replacing the default "Go Gopher" mascot icon.

#. Create a client token in the Gotify WebUI (``Client``-tab).
#. Retrieve your app id. Adjust the placeholders in the following curl command and run it from your local computer:

   .. code-block:: console

     [user@localhost ~]$ curl --header "X-Gotify-Key:<gotify-client-token>" https://<gotify-url>/application
     [{"id":42,"token":"********","name":"uuNotify","description":"uuNotify","internal":false,"image":"static/defaultapp.png"}]
     [user@localhost ~]$

#. Using the app id (in this case 42) run the next command:

   .. code-block:: console

      [user@localhost ~]$ curl --header "X-Gotify-Key:<gotify-client-token>"  -k -X POST -F 'file=@/home/<localuser>/path/to/image/uu-notify-icon.png'  https://<gotify-url>/application/42/image
      {"id":42,"token":"********","name":"uuNotify","description":"uuNotify","internal":false,"image":"image/RTHDR0253KDdQyw_FUBOEDom4.png"}
      [user@localhost ~]$

The app should now have a custom icon.

For further details, see the `Gotify API <https://gotify.net/api-docs#/application/uploadAppImage>`_.


Updates
=======

.. note:: Add uuNotify_ itself as software dependency in your ``config/software-deps.mjs`` file to get notified about new versions.

For details check the `GitHub release page`_.

You can update uuNotify to the latest_ version as follows:

.. code-block:: console

  [isabell@stardust ~]$ UUN_VERSION=v0.0.0
  [isabell@stardust ~]$ cd uu-notify/
  [isabell@stardust uu-notify]$ cp -rp config/ backup-config/
  [isabell@stardust uu-notify]$ git fetch
  [...]
  [isabell@stardust uu-notify]$ git checkout $UUN_VERSION
  [isabell@stardust uu-notify]$ git branch
  * (HEAD detached at <latest version>)
    main
  [isabell@stardust uu-notify]$ ./setup.sh
  --- uuNotify setup ---
  Existing files in config/ will not be overwritten.
  Running 'npm clean-install' ...
  [...]
  Done.

  Copy configuration files...
  config.json already exists. Skipping...
  software-deps.mjs already exists. Skipping...

  --- COMPLETED uuNotify setup ---
  [isabell@stardust uu-notify]$

Double check your configuration (``config/config.json`` and ``config/software-deps.mjs``). If everything looks okay, remove the backup folder:

.. code-block:: console

  [isabell@stardust uu-notify]$ rm -rf backup-config/
  [isabell@stardust uu-notify]$


Troubleshooting
===============

If you encounter any issues, e.g. during the installation or update process, you might want to check for the project's GitHub issues that have a `workaround <https://github.com/franok/uu-notify/labels/workaround>`_ label for a quick solution.
If you don't find any useful information there, you can `report a bug <https://github.com/franok/uu-notify/blob/main/contributing.md#bug-reporting>`_.

.. _uuNotify: https://github.com/franok/uu-notify
.. _latest: https://github.com/franok/uu-notify/releases/latest
.. _`GitHub release page`: https://github.com/franok/uu-notify/releases
.. _LICENSE: https://github.com/franok/uu-notify/blob/main/LICENSE.txt

----

Tested with uuNotify 1.1.2, Uberspace 7.11.3.0

.. author_list::
