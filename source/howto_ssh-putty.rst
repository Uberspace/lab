.. _putty:

#####
PuTTY
#####

Older versions of Windows do not include a SSH client by default, but there are plenty of options,
`PuTTY <http://www.chiark.greenend.org.uk/~sgtatham/putty/download.html>`_ probably being the choice of most Windows users.

Other popular choices include `Git BASH <https://git-for-windows.github.io/>`_ which provides a basic shell including
the widely-used Git version control system and OpenSSH as an SSH client.
If you're looking for a large distribution of GNU and Open Source utils that feels more-or-less like a Linux distribution,
head over to `Cygwin <https://www.cygwin.com/>`_.
If you opt for one of the last two, you should better follow :ref:`ssh-using-linux` after installation because you will then
effectively use the OpenSSH command-line utils.

.. warning:: Some SFTP clients do also offer a way to enter commands to be executed through SSH on the server,
  for example FileZilla with its ``Server | Enter custom command...`` feature.
  While there are legitimate use cases for such a feature, this is strictly for one-shot commands and does *not* provide you with the
  interactive terminal you need.

For this guide we're using PuTTY, but feel free to use any other SSH client of your personal taste.

Downloading PuTTY
~~~~~~~~~~~~~~~~~

First, download the *MSI (Windows installer)* package from the `PuTTY download page <https://www.chiark.greenend.org.uk/~sgtatham/putty/latest.html>`_
which includes all PuTTY tools we're going to use (PuTTY itself, the PuTTYgen key pair generator and the Pageant SSH agent).
The 32-bit version works on all Windows installations; if you have a 64-bit Windows installation you can download the 64-bit version instead.

Installing the PuTTY tool suite should be pretty common; you don't need to do anything special here - just accept the defaults.


Creating a session profile
~~~~~~~~~~~~~~~~~~~~~~~~~~

Start PuTTY. The configuration dialog automatically opens.

Head over to "Connection | Data" in the tree menu on the left. Enter your username (``isabell`` in our example)
into the "Auto-login username" text box.

Head over to "Session" in the tree menu on the left. Enter your hostname (``stardust.uberspace.de`` in our example)
into the "Host Name (or IP address)" text box.

For your convenience, save these settings under a session name of your choice.
For that, enter a description (e.g. "isabell on stardust" or something like "My personal Uberspace") into the "Saved Sessions" text box.
Click the "Save" button. From now on, you can simply double-click on your saved profile and PuTTY will automatically connect to your Uberspace.

First connection
~~~~~~~~~~~~~~~~

On your first connection PuTTY will present you the ``MD5`` fingerprint of the host key of the server you're about to connect. Unfortunately, checking the ``SHA256`` fingerprint is not possible with PuTTY, because it only supports insecure ``MD5`` fingerprints.

Next you're getting asked for your password. Nothing is shown while entering it; that's absolutely correct and works as intended - just **enter it blindly** and press Enter!
This is what you should be seeing inside the PuTTY terminal window:

.. code-block:: console

  Using username "isabell".
  Using keyboard-interactive authentication.
  Password:
  [isabell@stardust ~]$

The ``[isabell@stardust ~]$`` prompt shows that you're now successfully connected. Every command you're about to enter will get executed on your Uberspace.

Entering ``exit`` (or pressing Ctrl+D) leaves the shell, closing your connection.

Using PuTTY
~~~~~~~~~~~

Header over to "Connections | SSH" in the tree menu on the left. Enable the checkbox at "Share SSH connections if possible".

If you're working with session profiles, you can also load a session of your choice (don't double-click it, but click its name once, then click "Load"),
activate the connection sharing setting, then save the session again.

When opening your first connection to a host, PuTTY will ask you for your password as usual (or login with your key).
If you're now choosing "Duplicate session" from the window menu you'll get another session *immediately*, showing
"Reusing a shared connection to this server" right before your prompt to indicate you're on a reused connection.

