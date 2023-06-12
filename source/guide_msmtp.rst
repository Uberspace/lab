.. author:: CptSanifair  <https://github.com/CptSanifair>

.. tag:: mail
.. tag:: dkim
.. tag:: sendmail
.. tag:: lang-cpp


##########
msmtp
##########

.. tag_list::

msmtp_ is a very simple SMTP Client, usable as sendmail_ and ssmtp_ alternative. msmtp is faily sendmail compatible.

----

License
=======

msmtp is free software; you can redistribute it and/or modify it under the terms of the GNU General Public License as published by the Free Software Foundation; either version 3 of the License, or (at your option) any later version.

More information can be found here:
  * https://marlam.de/msmtp/
  * https://www.gnu.org/licenses/gpl-3.0.en.html

----

Installation
============

Create and join a new directory, download version 1.8.12 (how is able to compile on U7 with GnuTLS 3.3.29) and unpack files:

.. code-block:: console

  [isabell@stardust ~]$ mkdir ~/msmtp; cd ~/msmtp
  [isabell@stardust msmtp]$ wget https://marlam.de/msmtp/releases/msmtp-1.8.12.tar.xz
  [isabell@stardust msmtp]$ tar -xvf msmtp-1.8.12.tar.xz --strip-components=1
  [isabell@stardust msmtp]$


Compile msmtp, install it and cleanup your home directory:

.. code-block:: console

  [isabell@stardust msmtp]$ ./configure --prefix=$HOME --without-msmtpd
  [...]
  Install prefix ......... : /home/isabell
  NLS support ............ : yes
  TLS support ............ : yes (Library: GnuTLS)
  IDN support ............ : no
  GNU SASL support ....... : no (most likely unnecessary)
  Libsecret support (GNOME): no
  MacOS X Keychain support : no
  Build msmtpd ............: no
  [isabell@stardust msmtp]$ make; make install
  [...]
  [isabell@stardust msmtp]$ cd ~; rm msmtp -rf
  [isabell@stardust ~]$

Configuration
=============

.. note:: Your E-Mail-Account configuration needs to be stored in ~/.msmtprc


If your provider Supports RFC 6186 (Use of SRV Records for Locating Email Submission/Access Services) you can easyly create a configuration.
(Uberspace actually does not provide Support for RFC 6186)

.. code-block:: console

  [isabell@stardust ~]$ msmtp --configure=isabell@isabell.uber.space
  [...]
  [isabell@stardust ~]$


If your provider does not Supports the RFC you can get a sample configuration from https://marlam.de/msmtp/msmtprc.txt

.. code-block:: console

  [isabell@stardust ~]$ wget https://marlam.de/msmtp/msmtprc.txt -O .msmtprc
  [isabell@stardust ~]$ chmod 0600 ~/.msmtprc
  [isabell@stardust ~]$

Open the configuration with the editor of your choice.

Example Configuration
---------------------

.. note:: dont connect to 'localhost' otherwise the certificate validation will fail.

.. code-block:: console

  # Example for a user configuration file ~/.msmtprc
  
  # This example focusses on TLS and authentication. Features not used here
  # include logging, timeouts, SOCKS proxies, TLS parameters, Delivery Status
  # Notification (DSN) settings, and more.
  
  # Set default values: use the mail submission port 587, and always use TLS.
  # On this port, TLS is activated via STARTTLS.
  defaults
  port 587
  tls on
  tls_starttls on
  
  # Define a mail account at a mail service
  account uberspace
  
  # Host name of the SMTP server
  host stardust.uberspace.de
  
  # Envelope-from address
  from isabell@isabell.uber.space
  
  # Authentication
  # The following user / password methods are supported:
  # PLAIN, SCRAM-SHA-1, SCRAM-SHA-256, CRAM-MD5, DIGEST-MD5, LOGIN, NTLM
  # see https://marlam.de/msmtp/msmtp.html#Authentication for more informations
  auth on
  user isabell@isabell.uber.space
  
  # Password method 1: Add the password to the system keyring, and let msmtp get
  # it automatically. To set the keyring password using libsecret:
  # $ secret-tool store --label=msmtp \
  #   host smtp.freemail.example \
  #   service smtp \
  #   user joe.smith
  
  # Password method 2: Store the password in an encrypted file, and tell msmtp
  # which command to use to decrypt it. This is usually used with GnuPG, as in
  # this example. Usually gpg-agent will ask once for the decryption password.
  #passwordeval gpg2 --no-tty -q -d ~/.msmtp-password.gpg
  
  # You can also store the password directly in this file or have msmtp ask you
  # for it each time you send a mail, but one of the above methods is preferred.
  password <IsabellsTopSecretPassword>
  
  # Set a default account
  account default : uberspace


Test your configuarion
-------------------

.. code-block:: console

  [isabell@stardust ~]$ echo "Lorem ipsum dolor sit amet, consectetur adipisici elit" | msmtp post@isabell.uber.space
  [isabell@stardust ~]$


.. _sendmail: https://www.sendmail.com/
.. _msmtp: https://marlam.de/msmtp/
.. _ssmtp: https://packages.qa.debian.org/s/ssmtp.html


----

Tested with msmtp 1.8.12, Uberspace 7.15

.. author_list:: 


