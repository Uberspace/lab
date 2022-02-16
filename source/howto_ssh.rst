.. _ssh:

###
SSH
###

Introduction
============

.. toctree::
   :maxdepth: 2

.. tip:: If you're already used to SSH, you can safely head over to the :ref:`ssh-advanced-topics` section.

Here at Uberspace, many administrative tasks are preferably done on the shell, a text-based command line interface.
At first glance this might seem complex or even confusing for people that are more used to web interfaces,
but for many developers, web designers and generally advanced users, the shell is the preferred way of interacting with a server
because it offers nearly unimaginable possibilities that even *we* haven't been thinking about.

If you're completely new to using a shell - don't fear! It's easy to get started,
we're here to help, and we're pretty sure you will get used to it quickly, never looking back.

To connect to the shell of your account, Secure Shell (SSH) is the way to go.
As a widely-used protocol it is supported by clients on basically all operating systems, even on smartphones.

.. include:: includes/sftp-warning.rst

.. _ssh-login-data:

Login data
----------

You'll need three pieces of information to connect with your account by SSH:

#. A **username** - this is the username you've chosen yourself when registering an account with us.
#. A **hostname** - this is the hosting system we've created your account on.
   You can find this hostname under the `Datasheet <https://uberspace.de/dashboard/datasheet>`_ section.
   It's always in the form ``<something>.uberspace.de``.
#. A **password** or **private key** - as a newbie, simply set a password under the `Logins <https://uberspace.de/dashboard/authentication>`_ section.
   You can always switch to using SSH keys later, see :ref:`ssh-working-with-keys`.

For this introduction we're assuming your username is ``isabell`` and you're on ``stardust.uberspace.de``.

We're now guiding you through your first successful connection to your account. Fasten seat belts!

.. tip:: If your client supports ``SHA256`` fingerprints, we strongly recommend to make sure that the fingerprint shown in the `Datasheet <https://uberspace.de/dashboard/datasheet>`_ matches the one shown by your client. If you only see an ``MD5`` fingerprint, your client doesn't support ``SHA256`` and there is no secure way to verify the server's identity.

.. _ssh-using-linux:

Using Linux, macOS, any other Unix, or modern Windows 10
--------------------------------------------------------

On Linux, macOS and practically every other Unix operating system, as well as Windows 10 since the September 2017 "Fall Creators Update" version, `OpenSSH <https://www.openssh.com/>`_
comes preinstalled so you can use it out of the box. This is how your first connection will look like;
your local workstation is represented by a ``[localuser@localhost ~]$`` prompt:

.. code-block:: console

  [localuser@localhost ~]$ ssh isabell@stardust.uberspace.de
  The authenticity of host 'stardust.uberspace.de (ip.ip.ip.ip)' can't be established.
  ED25519 key fingerprint is SHA256:DtwUpr0MzHCZBej70iWO9CyzxXRDPK3jr14PJPMQIP4.
  Are you sure you want to continue connecting (yes/no)? yes
  Warning: Permanently added 'stardust.uberspace.de,ip.ip.ip.ip' (ED25519) to the list of known hosts.
  isabell@stardust.uberspace.de's password: 
  [isabell@stardust ~]$

What you're first seeing is the fingerprint of the host key of the server you're about to connect.
Please check your `Datasheet <https://uberspace.de/dashboard/datasheet>`_ which shows the fingerprint you *should* be seeing here.
If you're presented with a different fingerprint, please check if you have mistyped the hostname, which is the most common error.
If the hostname is correct but you're still getting the wrong fingerprint, please `contact us <mailto:hallo@uberspace.de>`_.

This part is important because you're about to send your password to the host, so you should make sure it's the *correct* host
and you're not accidentially giving your password to some unknown party which would compromise it.

If the fingerprint is correct, enter `yes` and press Enter to continue. OpenSSH will remember the fingerprint for you so you won't get asked again to check it.
It will complain *loudly* if the host key (and thus its fingerprint) suddenly changes, which should never happen through the lifetime of a host.
If you ever experience such a situation, please don't continue and `contact us <mailto:hallo@uberspace.de>`_ instead.

Next you're getting asked for your password. Nothing is shown while entering it; that's absolutely correct and works as intended - just **enter it blindly** and press Enter!

The ``[isabell@stardust ~]$`` prompt shows that you're now successfully connected. Every command you're about to enter will get executed on your Uberspace.

Entering ``exit`` (or pressing Ctrl+D) leaves the shell, closing your connection:

.. code-block:: console

  [isabell@stardust ~]$ exit
  Connection to stardust.uberspace.de closed.
  [localuser@localhost ~]$

You're now back on your local workstation.


Using older versions of Windows
-------------------------------

Older versions of Windows do not include a SSH client by default, but there are plenty of options,
`PuTTY <http://www.chiark.greenend.org.uk/~sgtatham/putty/download.html>`_ probably being the choice of most Windows users.

If you want or need to use PuTTY, please refer to our :doc:`PuTTY guide <putty>`.

.. _ssh-advanced-topics:

Advanced topics
===============


.. _ssh-working-with-keys:

Working with keys
-----------------

Logging in with keys is the preferred way of authentication over password-based logins.
For every client that should be able to connect you're generating a key pair (consisting of a public key which you deposit on your Uberspace,
and a password-protected private key which should never leave the device it's generated on, except for backup purposes).
It's best practice to generate a separate key pair for every device you're using; you can allow as many SSH keys to access your account as you like,
and using different keys makes it easy to e.g. remove a single key if one of your devices gets lost.

Using OpenSSH
~~~~~~~~~~~~~

Generate a key pair on your local system - you can safely accept the default filename if you don't have a key pair yet.
You have to enter a passphrase **blindly**, this is correct and intended. You have to enter it twice to make sure it's entered without any typos.

.. code-block:: console

  [localuser@localhost ~]$ ssh-keygen -t ed25519 -a 100
  Generating public/private ed25519 key pair.
  Enter file in which to save the key (/home/localuser/.ssh/id_ed25519):
  Enter passphrase (empty for no passphrase):
  Enter same passphrase again:
  Your identification has been saved in /home/localuser/.ssh/id_ed25519.
  Your public key has been saved in /home/localuser/.ssh/id_ed25519.pub.
  The key fingerprint is:
  SHA256:fpfpfpfpfpfpfpfpfpfpfpfpfpfpfpfpfpfpfpfpfpf localuser@localhost
  The key's randomart image is:
  +--[ED25519 256]--+
  | . . . . . . . . |
  | . . . . . . . . |
  | . . . . . . . . |
  | . . . . . . . . |
  | . . . . . . . . |
  | . . . . . . . . |
  | . . . . . . . . |
  | . . . . . . . . |
  | . . . . . . . . |
  +----[SHA256]-----+

.. warning: While you can *technically* omit a passphrase and thus save your private key unencrypted,
  we strongly advise against this. Otherwise anybody who gets access to this file (think about having your laptop stolen!)
  will automatically own your Uberspace as well. Please use a *good* passphrase instead, which primarily means a *long* one
  which you don't use at any other place.

Now you have to put the contents of the ``id_ed25519.pub`` file (not those of the ``id_ed25519`` which contains your *private* key) into the ``~/.ssh/authorized_keys`` file on your Uberspace.
You can use either the ``ssh-copy-id`` command or use the `authentication menu <https://uberspace.de/dashboard/authentication>`_ on your Dashboard which should be pretty self-explaining.
Here's how it looks using ``ssh-copy-id`` - when you're asked for a password, it's *not* the passphrase of your key (you only need this passphrase when connecting with the key)
but the conventional SSH password of your Uberspace.

.. code-block:: console

  [localuser@localhost ~]$ ssh-copy-id -i ~/.ssh/id_ed25519.pub isabell@stardust.uberspace.de
  /usr/bin/ssh-copy-id: INFO: Source of key(s) to be installed: "id_ed25519.pub"
  /usr/bin/ssh-copy-id: INFO: attempting to log in with the new key(s), to filter out any that are already installed
  /usr/bin/ssh-copy-id: INFO: 1 key(s) remain to be installed -- if you are prompted now it is to install the new keys
  Password:
  
  Number of key(s) added: 1
  
  Now try logging into the machine, with:   "ssh 'isabell@stardust.uberspace.de'"
  and check to make sure that only the key(s) you wanted were added.

From now on you'd have to enter the passphrase of your private key whenever you're about to connect to an account where this key is used, but:
Most Linux distributions have already set up ``ssh-agent`` for you. This is a program running in the background, started upon login,
holding your unencrypted key *in memory* (not on disk) as long as your local session lasts. This means that until you reboot your local system,
you only need to unlock your private key *once* irrespective of how many destinations you're using it for. Simply add your private key to the agent's keyring:

.. code-block:: console

  [localuser@localhost ~]$ ssh-add ~/.ssh/id_ed25519
  Enter passphrase for ~/.ssh/id_ed25519:
  Identity added: ~/.ssh/id_ed25519 (localuser@localhost)

And that's it! If ``ssh-agent`` unexpectedly is *not* preconfigured on your local system, please refer to your operating system's documentation
on how to do it (different operating systems use slightly different ways to achieve this).

Using PuTTY/PuTTYgen/Pageant
~~~~~~~~~~~~~~~~~~~~~~~~~~~~

PuTTY itself is only a SSH terminal client, but the author also provides the PuTTYgen tool to generate key pairs.

Generating a key pair
.....................

Start PuTTYgen. The basic key generation dialog opens.

Please make sure that "ED25519" is the selected key type.

Click on the "Generate" button to start the process of key generation. You have to move your mouse over the blank area to generate some randomness.
When done, a box titled "Public key for pasting into OpenSSH authorized_keys file" is shown with a bunch of characters.
Please select the whole content of this box and copy it to the clipboard (Ctrl+C).

Please enter a passphrase both into the "Key passphrase:" and "Confirm passphrase:" text boxes.

.. warning: While you can *technically* omit a passphrase and thus save your private key unencrypted,
  we strongly advise against this. Otherwise anybody who gets access to this file (think about having your laptop stolen!)
  will automatically own your Uberspace as well. Please use a *good* passphrase instead, which primarily means a *long* one
  which you don't use at any other place.

Now save both your public and your private key file with the respective buttons.
You're free to chose any filename you want, but for convention we suggest to use
a ``.pub`` extension for your public key file and a ``.ppk`` extension for your private key file.

Put the public key in place
...........................

Now open the `authentication menu <https://uberspace.de/dashboard/authentication>`_ of your dashboard and paste the contents of your clipboard.
The dashboard will put this public key into the ``~/.ssh/authorized_keys`` file of your Uberspace.

Your work with PuTTYgen is done here and you can safely close it. Let's head over to PuTTY!

Connecting with your private key
................................

If you already have a session for profile created, load it (just load, don't connect yet).

Head over to "Connection | SSH | Auth" in the tree menu on the left. Click on the "Browse..." button next to the "Private key file for authentication:"
text box and select your private key file (that one with the ``.ppk`` extension).

Get back to "Session" in the tree menu on the left and save your freshly changed session.

From now on PuttY won't ask you for your *password* (that password that you set on your Uberspace host) but for your *passphrase* (the passphrase
that you entered when generating the key pair with PuTTYgen). While that's more secure than before, it doesn't provide more comfort. Enter Pageant!

Have Pageant remember your passphrase
.....................................

To prevent having to enter your private key's passphrase over and over again, you can use the Pageant tool of the same author like PuTTY.
It keeps your unencrypted key in memory (not on disk) so you only have to unlock it once per local session.

Start Pageant. A small icon in your tray will appear, showing an icon of a computer with a hat.

Double-click on the icon and a window with a list of keys will appear (for now, this list is empty).

Click on "Add Key" and select your private key file (that one with the ``.ppk`` extension). You have to enter your passphrase to unlock the key.

And that's it! From now on, whenever PuTTY tries to login with your private key, Pageant happily serves that key so you don't have to enter any password or passphrase.


Using connection multiplexing
-----------------------------

When using SSH, *connecting* is the most resource-consuming part of the session because that's where the more complicated parts of the crypto stuff happen.
If you find yourself in the situation that you need to open *many* SSH connections to the same destination (both in parallel or serialized),
you should definitely use connection multiplexing (OpenSSH) respectively connection sharing (PuTTY).
Common use cases are tools like Integrated Development Environments (IDE) which talk to remote Git repositories by SSH
as well as configuration management tools like Ansible which heavily rely on SSH to execute many commands.

Using connection multiplexing/sharing, only the very first connection needs to do the complicated part of the crypto stuff.
Any further connection will simply hop on the already existing, already authenticated session,
opening another channel which acts like a session on its own but is reusing the same connection.

Using OpenSSH
~~~~~~~~~~~~~

Simply put this into your local `~/.ssh/config` file (in this example we're focusing on ``Host *.uberspace.de``, but feel free to apply this to ``Host *`` instead):

.. code-block:: none

  Host *.uberspace.de
    ControlMaster auto
    ControlPersist yes
    ControlPath ~/.ssh/socket-%r@%h:%p

When opening a connection as ``isabell`` to ``stardust.uberspace.de``, OpenSSH will first check if there is a local socket named ``~/.ssh/socket-isabell@stardust.uberspace.de:22`` and hop on it.
If there isn't such a local socket, it will connect as usual, *providing* such a socket for any further connection.

