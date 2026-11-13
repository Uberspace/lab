.. highlight:: console

.. author:: Max Mehl <https://mehl.mx>

.. tag:: lang-python
.. tag:: mail
.. tag:: web

.. spelling:word-list::
    CastMail2List
    castmail2list
    IMAP
    SMTP
    SCSS

.. sidebar:: Logo

  .. image:: _static/images/castmail2list.svg
      :align: center

##############
CastMail2List
##############

.. tag_list::

CastMail2List_ is a lightweight, self-hosted mailing list application. It polls standard IMAP mailboxes for incoming messages, distributes them to subscribers, and provides a web interface for list management. It supports broadcast (newsletter) and group (discussion) modes.

----

.. note:: For this guide you should be familiar with the basic concepts of

  * :manual:`Python <lang-python>` and its package manager :manual_anchor:`pip <lang-python.html#pip>`
  * :manual:`supervisord <daemons-supervisord>`
  * :manual:`web backends <web-backends>`
  * :manual:`domains <web-domains>`
  * :manual:`mail <mail-access>`

License
=======

CastMail2List is released under the `Apache License 2.0`_. All relevant legal information can be found in the LICENSE_ file in the repository.

Prerequisites
=============

Your domain needs to be set up:

::

 [isabell@stardust ~]$ uberspace web domain list
 isabell.uber.space
 [isabell@stardust ~]$

You need IMAP and SMTP credentials for the email accounts your mailing lists will use. On Uberspace, you can use your existing mailbox or create dedicated ones, see :manual:`Mailboxes <mail-mailboxes>`.

The default logic for IMAP and SMTP credentials is as follows:
* Each mailing list has its own mailbox, e.g. ``list1@isabell.uber.space``, either with a default or a custom password.
* For sending emails, a dedicated sender account is used for all outgoing emails, e.g. ``list-sender@isabell.uber.space``.

Installation
============

Install CastMail2List
---------------------

Install CastMail2List using pip:

::

 [isabell@stardust ~]$ pip3.12 install --user castmail2list
 Collecting castmail2list
   Downloading castmail2list-0.10.2-py3-none-any.whl
 [...]
 Successfully installed castmail2list-0.10.2 flask-3.1.2 gunicorn-26.0.0 [...]
 [isabell@stardust ~]$

Configuration
=============

Create configuration file
-------------------------

Create the application directory in which the configuration file and database will be stored:

::

 [isabell@stardust ~]$ mkdir -p ~/.config/castmail2list
 [isabell@stardust ~]$

Generate a random secret key you will need in the next step:

::

 [isabell@stardust ~]$ pwgen 32 1
 aiGh8eiqueequoh3aiyahng4ohch3ae
 [isabell@stardust ~]$

Create ``~/.config/castmail2list/config.yaml`` with the following content:

.. warning:: Replace all placeholder values with your actual credentials!

.. code-block:: yaml
  :emphasize-lines: 1,3,4,8,9,10,12,13,14,19

  SECRET_KEY: "your-secret-key-here"
  LANGUAGE: "en"
  DOMAIN: "isabell.uber.space"
  SYSTEM_EMAIL: "noreply@isabell.uber.space"
  HOST_TYPE: "uberspace7"
  CREATE_LISTS_AUTOMATICALLY: True

  IMAP_DEFAULT_HOST: "stardust.uberspace.de"
  IMAP_DEFAULT_USER_DOMAIN: "isabell.uber.space"
  IMAP_DEFAULT_PASS: "your-default-imap-password"

  SMTP_HOST: "stardust.uberspace.de"
  SMTP_USER: "list-sender@isabell.uber.space"
  SMTP_PASS: "the-smtp-password"

  NOTIFY_REJECTED_SENDERS: True
  NOTIFY_REJECTED_KNOWN_ONLY: True
  NOTIFY_REJECTED_TRUSTED_DOMAINS:
    - isabell.uber.space


Initialize the database
-----------------------

Run the database migrations to create the initial schema:

::

 [isabell@stardust ~]$ castmail2list-cli --db init
 Database command 'init' completed
 [isabell@stardust ~]$


Create the first user
---------------------

Create an admin user for the web interface. Use your desired username (``isabell`` in this example) and a strong password:

::

 [isabell@stardust ~]$ castmail2list-cli --create-admin isabell super-secure-password
 Admin user 'isabell' created
 [isabell@stardust ~]$

Configure web backend
---------------------

CastMail2List runs on port 2278 by default. Set up the :manual:`web backend <web-backends>`:

::

 [isabell@stardust ~]$ uberspace web backend set / --http --port 2278
 Set backend for / to port 2278; please make sure something is listening!
 You can always check the status of your backend using "uberspace web backend list".
 [isabell@stardust ~]$

.. note::

    If you want to run CastMail2List on a subdomain or alongside other applications, adjust the web backend path accordingly, e.g. use a dedicated domain and set the backend for ``/``.

Set up the daemon
-----------------

Create ``~/etc/services.d/castmail2list.ini`` with the following content:

.. code-block:: ini

 [program:castmail2list]
 directory=%(ENV_HOME)s/.config/castmail2list
 command=castmail2list
 environment=PYTHONPATH=%(ENV_HOME)s/.config/castmail2list
 autostart=yes
 autorestart=yes
 startsecs=30
 stopasgroup=true

.. include:: includes/supervisord.rst

If it's not in state ``RUNNING`` after 30 seconds, check the logs with ``supervisorctl tail castmail2list stderr``.

Finishing installation
======================

Point your browser to ``https://isabell.uber.space`` and log in. Use the admin credentials you set earlier.

You may now start with adding/creating mailing lists and subscribers.

Updates
=======

.. note:: Check the update feed_ regularly to stay informed about the newest version.

To update CastMail2List, install the new version, run database migrations, and restart the daemon:

::

 [isabell@stardust ~]$ pip3.12 install --user --upgrade castmail2list
 [...]
 Successfully installed castmail2list-0.10.2
 [isabell@stardust ~]$ castmail2list-cli --db upgrade
 [isabell@stardust ~]$ supervisorctl restart castmail2list
 castmail2list: stopped
 castmail2list: started
 [isabell@stardust ~]$

.. warning:: If the new version requires a database schema update (which the changelogs will tell), always run database migrations (``castmail2list-cli --db upgrade``) after updating. Skipping this step may cause errors if the new version includes schema changes.

.. _CastMail2List: https://github.com/mxmehl/castmail2list
.. _feed: https://github.com/mxmehl/castmail2list/releases.atom
.. _Apache License 2.0: https://opensource.org/licenses/Apache-2.0
.. _LICENSE: https://github.com/mxmehl/castmail2list/blob/main/LICENSE

----

Tested with CastMail2List 0.10.2, Uberspace 7.16

.. author_list::
