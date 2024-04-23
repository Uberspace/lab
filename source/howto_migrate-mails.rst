.. highlight:: console

######################
Migrate mail addresses
######################

If you have your own domain with email addresses currently hosted at another site
you can move to Uberspace as your new mailprovider. This *HOWTO* explains how to set
up your mail domain and email addresses and how to move your mail archive to your Uberspace.


Prerequisites
-------------

- You have your own domain like ``example.com`` with the ability to change DNS records
- You currently have set up this domain to an external mailserver like ``gmail.com``
- You have mail addresses like ``info@example.com`` with existing mails and want to move all of them to your Uberspace
- You have `created <https://dashboard.uberspace.de/register>`_ a fresh Uberspace account and you have `ssh access <https://manual.uberspace.de/basics-ssh/>`_ there


Set up your mailaddresses
-------------------------

First you will need to `create mailboxes <https://manual.uberspace.de/mail-mailboxes/>`_ for the mailaddresses you want to import:

.. code-block::

    [isabell@stardust ~]$ uberspace mail user add info
    Enter a password for the mailbox:
    Please confirm your password:
    New mailbox created for user: 'info', it will be live in a few minutes...

    [isabell@stardust ~]$

.. note::

    You will need to do this for each mailaddress you want to import. If you like you can set up the same passwords here
    as you already are using at your old mail provider.

If you just use an email address as `forward or alias <https://manual.uberspace.de/mail-forwarding/>`_ without a mailbox, you can set it up like this:

.. code-block::

    [isabell@stardust ~]$ uberspace mail user forward set forwardme mail@example2.com
    Mail to forwardme will be forwarded to mail@example2.com.

    [isabell@stardust ~]$

This will create a forward for ``forwardme@example.com -> mail@example2.com``


Import mails
------------

We propose to use the preinstalled tool ``imapsync`` to import your existing mail archive to your new mailboxes. The following will
explain how to import a single mailbox with the name ``info``. You will need to repeat this for each mailbox.

.. note::

    All Uberspaces come with a default mail domain ``USERNAME.uber.space``. While your original email addresses are still
    pointing to your old mail provider, we can use this here to make the import-export possible with the ``imap`` protocol.

.. tip::

    Because there are some settings you will need to provide for the import tool, you should copy the following lines
    somewhere else to adjust the values.

First you will need to start the command and provide a proper logging path:

.. code-block:: ini

    imapsync \
    --logdir ~/logs/imapsync \

Then you will need to provide the login data for your old mailbox, the server address ``host1`` and
username ``user1`` shown here depend on your old mail provider. They should be the same like they advice
you to use for any mail client:

.. code-block:: ini

    --host1 imap.example.com \
    --user1 info@example.com \
    --ssl1 \

If your old mailserver is located at Gmail, you must activate IMAP-Access in the settings over there
and "less secure app access", too and then use the following *instead* (this will provide the correct
settings for Google Mails):

.. code-block:: ini

    --gmail1 \
    --user1 info@example.com \

Then you need to define the target mailbox on your Uberspace. Keep in mind to replace ``info``
with the correct mailbox.

.. code-block:: ini

    --host2 localhost \
    --user2 info@$USER.uber.space \
    --ssl2 \

Copy all configured lines at once to the command line like:

.. code-block::

    [isabell@stardust ~]$ imapsync \
    --logdir ~/logs/imapsync \
    --host1 imap.example.com \
    --user1 info@example.com \
    --ssl1 \
    --host2 localhost \
    --user2 info@$USER.uber.space \
    --ssl2 \

After executing the command, you will be asked for the old and new mail address passwords to enter,
then ``imapsync`` should take some time and import the mail and folder structure from your old mail account.

.. tip::
    The command tool ``imapsync`` is very powerful with a lot of configuration options. While the settings explained here
    should suit for the most cases, you might want or need to change some of them. Have a look at the `repo <https://github.com/imapsync/imapsync>`_.


Set up mail domain
------------------

After importing the mails you can continue to switch the domain to the new location. First add the domain to your Uberspace
so it will be recognised by the host:

.. code-block::

    [isabell@stardust ~]$ uberspace mail domain add example.com
    The mailserver's configuration has been adapted.
    Now you can use the following record for your DNS:
        MX  -> stardust.uberspace.de.
        TXT -> v=spf1 include:spf.uberspace.de ~all

    The trailing dot may be skipped, if the interface does not accept it.

    [isabell@stardust ~]$

This will provide you the neccessary ``DNS`` records you have to set up at your **domain registrar**. You will need to replace
the ``MX`` record of your old mailserver to fully connect your domain to your Uberspace.

After changing the ``DNS`` records, it might take a short time until our server could check for the correct settings,
run the Uberspace command to get the current status:

.. code-block::

    [isabell@stardust ~]$ uberspace mail domain list
    example.com DNS INVALID (checked 2022-02-08 20:36)
    isabell.uber.space

    [isabell@stardust ~]$

When the ``DNS INVALID`` warning is not shown any longer, the settings are correct and mails might already be delivered to your new Uberspace.

.. warning::
    Mails sent to your domain within your domain's `time-to-live (TTL) <https://en.wikipedia.org/wiki/Time_to_live#DNS_records>`_ after updating
    the DNS records could still be sent to your old mail provider. You should check your old mailbox on received mails for this time frame.


Troubleshooting
---------------


Accessing your new mailbox
~~~~~~~~~~~~~~~~~~~~~~~~~~

If you use a mail client like Thunderbird you will have to update your settings there to connect correctly to the Uberspace mail server. For that
have a look at our `manual mail access <https://manual.uberspace.de/mail-access>`_ page.

You may also simply use our `Webmailer <https://webmail.uberspace.de>`_ to check if your mail address migration was successfull at first.


DNS invalid
~~~~~~~~~~~

If the mail domain status stays ``DNS INVALID`` for a longer time after you have updated the ``MX`` records, first check if this was done correctly:

.. code-block::

    [isabell@stardust ~]$ dig example.com MX +short
    0 stardust.uberspace.de.

    [isabell@stardust ~]$

The output should look like this with your domain and hostname instead.


Multiple spamfolders
~~~~~~~~~~~~~~~~~~~~

Due to deviating labels it is possible that some special folders like `junk` seem to show up multiple times. In this case you should just move them
to the newer folder which should be highlighted by your client.


Missing calendars and contacts
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

This *HOWTO* covers only the migration of mail domains, mailboxes and their archives. If you also want to migrate your *calendars* and *addressbooks* have a look
at our guides for installing groupware services like `Nextcloud <https://lab.uberspace.de/guide_nextcloud>`_, `Baïkal <https://lab.uberspace.de/guide_baikal>`_,
`Radicale <https://lab.uberspace.de/guide_radicale>`_ etc.
