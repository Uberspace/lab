############
use SSH keys
############

Connecting to your account using a SSH *password* is quite ok, but using **keys** is the preferred way of authentication. To do so you will need to create a pair
of keys on your local system and copy the public part to your Uberspace. That way you can login there without re-entering your password each time and
you have a much more convenient and secure way of managing your account(s).

.. tip::
  It's best practice to generate a separate key pair for every device you're using; you can allow as many SSH keys to access your account as you like,
  and using different keys makes it easy to e.g. remove a single key if one of your devices gets lost.


Generate the key on your local system
-------------------------------------

We will again use *OpenSSH* to generate the pair of keys, open your `local shell <https://lab.uberspace.de/XXX>`_ and enter the following command:

.. code-block:: console

  localuser@localhost ~ $ ssh-keygen -t ed25519 -a 100
  Generating public/private ed25519 key pair.
  [..]

At first you will be asked for a filename, here you can just press ``Enter`` to confirm the default name and path:

.. code-block:: console

  [..]
  Enter file in which to save the key (/home/localuser/.ssh/id_ed25519):

You will then have to enter a passphrase **blindly**, this is correct and intended (you have to enter it twice to make sure it's entered without any typos):

.. code-block:: console

  [..]
  Enter passphrase (empty for no passphrase):
  Enter same passphrase again:

You should then receive a confirmation output like this:

.. code-block:: console

  [..]
  Your identification has been saved in /home/localuser/.ssh/id_ed25519.
  Your public key has been saved in /home/localuser/.ssh/id_ed25519.pub.
  The key fingerprint is:
  SHA256:fpfpfpfpfpfpfpfpfpfpfpfpfpfpfpfpfpfpfpfpfpf localuser@localhost
  The key's randomart image is:
  [..]

You should now have 2 files (within the path that you confirmed before) and it is important to know the difference:

* ``id_ed25519`` is your **private** key file that should never leave your device.
* ``id_ed25519.pub`` is the **public** part of your new keypair. The content of that file should be shared with a server to establish the verification.


Add the public ssh key to your Uberspace
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

To add the public key to your Uberspace, first get the content of the ``id_ed25519.pub`` file. You can open the file with a simple text editor
or you may again use the shell to show its content (the command may differ on your local system):

..  code-block:: console

  localuser@localhost ~ $ cat ~/.ssh/id_ed25519.pub
  ssh-ed25519 AAAAC3NzaC1lZDI1NTE5AAAAICXeB9uga0aDoGLCMNkCJN4EoFlsI3MZi+8Xa6K5hMGF localuser@localhost

Then login to your Uberspace `Dashboard <https://dashboard.uberspace.de>`_ and copy the content (aka your public key) to the ``Add a SSH public key`` field on the
`Logins page <https://dashboard.uberspace.de/dashboard/authentication>`_.


Login using the SSH key
-----------------------

You may use the same simple SSH command to use your key for login to your Uberspace:

.. code-block:: console

  localuser@localhost ~ $ ssh isabell@stardust.uberspace.de

For the first time doing so you will need to *unlock your private key* with the password you have chosen before when *generating your private key*.
(Do not get confused, this is **not** the password you entered in the Uberspace Dashboard for your first key-less SSH login.)


Add your key to the ssh-agent
-----------------------------

From now on you'd have to enter the passphrase of your private key whenever you're about to connect to a server, **but**:
Most Linux distributions have already set up ``ssh-agent`` for you.

This is a program running in the background, started upon login, holding your unencrypted key *in memory* (not on disk) as long as your local session lasts.
This means that until you reboot your local system, you only need to unlock your private key *once* irrespective of how many destinations you're using it for.

Simply add your private key to the agent's keyring:

.. code-block:: console

  localuser@localhost ~ $ ssh-add ~/.ssh/id_ed25519
  Enter passphrase for ~/.ssh/id_ed25519:
  Identity added: ~/.ssh/id_ed25519 (localuser@localhost)

And that's it! If ``ssh-agent`` unexpectedly is *not* preconfigured on your local system, please refer to your operating system's documentation
on how to do it (different operating systems use slightly different ways to achieve this).
