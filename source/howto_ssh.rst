.. _ssh:

###############
Connect via SSH
###############

Here at Uberspace, many administrative tasks are preferably done on the **shell**, a text-based command line interface.
At first glance this might seem complex or even confusing for people that are more used to web interfaces.
But for many developers, web designers and generally advanced users, the shell is the preferred way of interacting with a server
because it offers nearly unimaginable possibilities that even *we* haven't been thinking about.

If you're completely new to using a shell - don't fear! It's easy to get started,
we're here to help, and we're pretty sure you will get used to it quickly, never looking back.

.. note::

  To connect to the shell of your Uberspace account, Secure Shell (**SSH**) is the way to go.
  As a widely-used protocol it is supported by clients on basically all operating systems, even on smartphones.


Starting your local shell
=========================

To connect to your account, you will first need to start a shell on your local device. How this is done
and how it will look like depends on your Operating System but is pretty much the same for Linux, MacOS or Windows.

Whether you are using Windows, Linux/Unix or MacOS there are many names to look for your shell app. On your device search for an app called ``Terminal``,
``Command Line`` or ``Shell`` to start it. Sometimes you can just use the keyboard shortcut ``strg+alt+t`` or ``super+t``
to open your local shell.

.. tip::
  If this does not work for you and are not able to find and open the shell on your local device, you should search the internet for your Operating System together
  with the terms ``terminal``, ``shell`` or ``command line``. This should assist you with specific guides how to set it up.

After starting your shell app you should see a window with something like this:

  .. image:: _static/images/howto-ssh-terminal.png
     :width: 450
     :align: center
     :alt: terminal window

The exact appearance again depend very much on your operating system and the app you use for providing the shell. It can also come in all colors from black background
with green letters to simple black on white. It is just important that you are able to type simple text commands here.

We can try this now with a very basic command that should work for most operating systems. The following is a code-block which you will see
a lot in our manuals and guides:

.. code-block:: console

  localuser@localhost ~ $ whoami
  localuser

This means as much as ``type the word "whoami" and then press Enter``, the second line will show the output of your command,
in this case it answers on *"Who am I?"* and returns the current username.

.. warning::
  You will most probably need to copy-paste something from and to your shell. In the most shell apps this is **not** done with ``strg+c`` and ``strg+v``
  but ``strg+shift+c`` and ``strg+shift+v``.

Connecting via SSH
==================

Now that you have started the local shell we need to use SSH to connect to the shell on *another* computer. In our case that means you will connect with a
machine in our data centers where your personal account is registered.

So fasten your seat belts! we will very soon make contact with your Uberspace! But first we will need to check for *ssh* on your device and get your *login data*.


Prepare the SSH command
~~~~~~~~~~~~~~~~~~~~~~~

Before using SSH, we need to check if the command is available, do so by typing
``ssh -V`` to your shell:

.. code-block:: console

  localuser@localhost ~ $ ssh -V
  OpenSSH_7.4p1, OpenSSL 1.0.2k-fips  26 Jan 2017

If the output in the second line is anything like this it is totally fine and we can be sure that you are able to use SSH on your device without further obstacles.

.. note::
  The ``-V`` here is a so called "switch" or "argument" that can modify the command ``ssh``, in this case it will just return the current version of SSH.

.. tip::
  When using Windows 8.1 or any other not up-to-date versions of Windows, you will most probably get an error message when trying to execute the ``ssh`` command.
  You will either need to update to a more recent version of Windows or use our `howto for Putty <howto_ssh-putty.html>`_ instead of this one here.


Prepare your login data
~~~~~~~~~~~~~~~~~~~~~~~

You'll need three pieces of information to connect with your account by SSH:

#. A **username** - this is the username you've chosen yourself when registering an account with us.
#. A **hostname** - this is the hosting system we've created your account on.
   You can find this hostname under the `Datasheet <https://uberspace.de/dashboard/datasheet>`_ section.
   It's always in the form ``<something>.uberspace.de``.
#. A **password** or **private key** - for this *HOWTO* we will start with a simple password but explain
   using a more secure and convenient key after the basics.


For this introduction we're assuming your username is ``isabell`` and you're on ``stardust.uberspace.de``.


Start the first login attempt
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

We will now use the SSH command and your login data to connect to your Uberspace, you will of course need to replace the username and hostname with your personal data:

.. code-block:: console

  localuser@localhost ~ $ ssh isabell@stardust.uberspace.de
  The authenticity of host 'stardust.uberspace.de (ip.ip.ip.ip)' can't be established.
  ED25519 key fingerprint is SHA256:DtwUpr0MzHCZBej70iWO9CyzxXRDPK3jr14PJPMQIP4.
  Are you sure you want to continue connecting (yes/no)?

Most probably you will stuck at an interactive question like here in the last line and need to confirm that you are connecting with the correct machine.

This is a security measure because you are going to give your personal password somewhere else and you should be sure that it is actually
our server and not another party which intercepted the connection. To make sure of it, check if the "host fingerprint" shown on your command output
is also shown on your `Datasheet <https://dashboard.uberspace.de/dashboard/datasheet>`_.

.. tip::

  If the fingerprints do not match please check again if you connected to the correct host.

.. warning::

  If you are sure that the hostname used within your ssh command fits to the one that you got from your datasheet, but the fingerprints do not match,
  please `contact us <mailto:hallo@uberspace.de>`_.


Continue and provide password
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

If the fingerprint is correct, just type ``yes`` and press enter to go on. (The next time you connect to the same host you will not need to verify the identity again.)

.. code-block:: console

  [..]
  Are you sure you want to continue connecting (yes/no)? yes
  Warning: Permanently added 'stardust.uberspace.de,ip.ip.ip.ip' (ED25519) to the list of known hosts.

Next you're getting asked for your password. Nothing is shown while entering it; that's absolutely correct and works as intended - just **enter it blindly** and press Enter!

.. code-block:: console

  [..]
  isabell@stardust.uberspace.de's password:

And then finally! The ``[isabell@stardust ~]$`` prompt shows that you're now successfully connected!

.. code-block:: console

  [..]
  Welcome to Uberspace 7!

  Current version: 7.12.0
  [..]
  [isabell@stardust ~]$

Every command you're about to enter will get executed on your Uberspace.


First steps on your uberspace shell
===================================

.. note::
  Because you are now on our system, it will be much easier to support you with clean information and instructions, we no longer depend (that much) on your local prerequisites.

While you're already logged in now, take the chance try yourself out. For example use the command ``pwd`` to show the current working directory you are in:

.. code-block:: console

  [isabell@stardust ~]$ pwd
  /home/isabell

Or use ``ls`` to show it's subfolders:

.. code-block:: console

  [isabell@stardust ~]$ ls
  bin  etc  html  logs  Maildir  tmp  users

Change directories with ``cd``, show a file content with ``cat`` etc.:

.. code-block:: console

  [isabell@stardust ~]$ cd html
  [isabell@stardust html]$ ls
  nocontent.html
  [isabell@stardust html]$ cd ..
  [isabell@stardust ~]$ cd etc
  [isabell@stardust etc]$ ls
  certificates  php.d  services.d  userfacts
  [isabell@stardust etc]$ cd userfacts
  [isabell@stardust userfacts]$ ls
  quota.yaml  versions.yml  versions.yml.orig
  [isabell@stardust userfacts]$ cat quota.yaml
  soft: 10

These are just a few basic commands to show you how it looks like, you will get to know a lot more when you use our guides and howtos.

To leave the shell on your Uberspace you just need to enter ``exit``:

.. code-block:: console

  [isabell@stardust ~]$ exit
  Connection to stardust.uberspace.de closed.
  localuser@localhost ~ $

You're now back on your local workstation.

.. tip::

  To improve your connection security and usability check out our `howto for ssh keys <howto_ssh-keys.html>`_.
