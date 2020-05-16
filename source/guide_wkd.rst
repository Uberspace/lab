.. highlight:: console

.. author:: Starkstromkonsument <it@starkstromkonsument.de>

.. tag:: audience-admins
.. tag:: mail
.. tag:: self-hosting

#######################
Web Key Directory (WKD)
#######################

.. tag_list::

[WKD] stands for "`Web Key Directory`_" and is a standard for making a users GnuPG / OpenPGP public key available via their e-mail provider or server with the domain that corresponds to their e-mail address. There's several clients (such as Enigmail in Thunderbird or OpenKeyChain on Android) that will use this standard to automatically fetch a user's public key, when writing an e-mail to them.

Web Key Directories provide an easy way to discover public keys through HTTPS. They provide an important piece to the infrastructure to improve the user experience for exchanging secure emails and files. In contrast to the public keyservers a Web Key Directory does not publish mail addresses and it is an authoritative pubkey source for its domain.

----

.. note:: For this guide you should be familiar with the basic concepts of

  * e-mail encryption with GnuPG / OpenPGP 
  * :manual:`domains <web-domains>`

Prerequisites
=============

You need the public keys for the e-mail identities you want to provide via WKD (e.g. isabell@stardust.uberspace.de). This guide does not explain how to generate GnuPG / OpenPGP keys.

The domain for the advanced method has to be set up at your DNS-Hoster and within your uberspace:

::

 [isabell@stardust ~]$ uberspace web domain list
 openpgpkey.stardust.uberspace.de
 [isabell@stardust ~]$


Create Directory Structure
==========================

Advanced method
---------------

The "advanced" method seems to be queried in front of the "direct" method by clients. If the subdomain openpgpkey resolves to a valid IP but the host at this IP does not provide the WKD (e.g. because of a wildcard in the DNS-Records), the WKD-lookup may fail.

Create the directories and the empty files:

::

 [isabell@stardust ~]$ cd /var/www/virtual/$USER/
 [isabell@stardust isabell]$ mkdir -p openpgpkey.stardust.uberspace.de/.well-known/openpgpkey/stardust.uberspace.de/hu/
 [isabell@stardust isabell]$ touch openpgpkey.stardust.uberspace.de/.well-known/openpgpkey/stardust.uberspace.de/policy
 [isabell@stardust isabell]$ touch openpgpkey.stardust.uberspace.de/.well-known/openpgpkey/stardust.uberspace.de/.htaccess
 [isabell@stardust ~]$

Add the following lines to the empty ``.htaccess`` file to set the correct headers:

.. code-block:: apache

 ## WEB KEY DIRECTORY ##
 <IfModule mod_mime.c>
    ForceType application/octet-stream
    Header always set Access-Control-Allow-Origin "*"
 </IfModule>

.. warning:: Make sure that there is no automatic directory listing! It is not necessary and it reveals the number of emailadresses (and their hashes) in the WKD (this can be a privacy issue)!


Direct method
-------------

Create the directories and symlinks

::

 [isabell@stardust ~]$ cd ~/
 [isabell@stardust ~]$ mkdir -p html/.well-known
 [isabell@stardust ~]$ ln -s /var/www/virtual/$USER/openpgpkey.stardust.uberspace.de/.well-known/openpgpkey/stardust.uberspace.de/ /var/www/virtual/$USER/html/.well-known/openpgpkey
 [isabell@stardust ~]$
 
Create another symlink to facilitate uploading keys via scp:

::

 [isabell@stardust ~]$ ln -s /var/www/virtual/$USER/openpgpkey.stardust.uberspace.de/.well-known/openpgpkey/stardust.uberspace.de/hu/ ./
 [isabell@stardust ~]$

Upload GPG keys
===============

Obtaining the WKD-Hashes
------------------------

The keys are stored in files named by the WKD-Hashes of the Mailuser. Take the prefix of your e-mail address (i.e. in isabell@stardust.uberspace.de, this would be `isabell`), hash it with SHA-1 and then encode the output with z-base-32.

You can get the hashes for all identities of your GPG key with this command:

::

 [someuser@somehost ~]$ gpg --with-wkd-hash --list-public-keys "isabell@stardust.uberspace.de"
 [...]
       0123456789ABCDEF0123456789ABCDEF01234567
 uid           [ unknown] Isabell <isabell@stardust.uberspace.de>
            mmuhurigesr7z8hzf6sh5cmfsnmiiyyr@stardust.uberspace.de
 [...]
 [someuser@somehost ~]$

Alternatively you can use https://cryptii.com/pipes/z-base-32 for that (add a hash-block with SHA-1 before the z.base-32-block).

Summary:
 * E-Mail: isabell@startdust.uberspace.de
 * Prefix: isabell
 * WKD-Hash: mmuhurigesr7z8hzf6sh5cmfsnmiiyyr


Exporting a GPG key
-------------------

::

 [someuser@somehost ~]$ gpg --no-armor --export isabell@stardust.uberspace.de > mmuhurigesr7z8hzf6sh5cmfsnmiiyyr
 [someuser@somehost ~]$
 
.. note:: The public key is the the same for all identities of a key. You can simply duplicate the exported key, using the corresponding WKD-Hash as filename.

Upload
------

::

 [someuser@somehost ~]$ scp mmuhurigesr7z8hzf6sh5cmfsnmiiyyr isabell@stardust.uberspace.de:hu/
 [someuser@somehost ~]$

Testing
=======

First of all, these two URLs should be available using your browser:

 * Advanced method: https://openpgpkey.stardust.uberspace.de/.well-known/openpgpkey/stardust.uberspace.de/hu/mmuhurigesr7z8hzf6sh5cmfsnmiiyyr
 * Direct method: https://stardust.uberspace.de/.well-known/openpgpkey/hu/mmuhurigesr7z8hzf6sh5cmfsnmiiyyr

or ``curl``:

.. code-block:: console
 :emphasize-lines: 4,6

 [someuser@somehost ~]$ curl -I https://openpgpkey.stardust.uberspace.de/.well-known/openpgpkey/stardust.uberspace.de/hu/mmuhurigesr7z8hzf6sh5cmfsnmiiyyr
 HTTP/2 200 
 date: Sat, 02 May 2020 19:16:17 GMT
 content-type: application/octet-stream
 content-length: 5298
 access-control-allow-origin: *
 last-modified: Mon, 13 Apr 2020 18:15:20 GMT
 etag: "14b2-5a33010e34bb7"
 accept-ranges: bytes
 server: nginx
 referrer-policy: strict-origin-when-cross-origin
 strict-transport-security: max-age=172800
 x-content-type-options: nosniff
 x-xss-protection: 1; mode=block
 x-frame-options: SAMEORIGIN
 [someuser@somehost ~]$ 

You can test the WKD-download by running:

::

 [someuser@somehost ~]$ env GNUPGHOME=$(mktemp -d) gpg --locate-keys --auto-key-locate clear,wkd,nodefault isabell@stardust.uberspace.de
 gpg: keybox '/tmp/tmp.c8iW067tlp/pubring.kbx' created
 gpg: /tmp/tmp.c8iW067tlp/trustdb.gpg: trustdb created
 gpg: key 89ABCDEF01234567: public key "Isabell <isabell@stardust.uberspace.de>" imported
 gpg: Total number processed: 1
 gpg:               imported: 1
 [...]
       0123456789ABCDEF0123456789ABCDEF01234567
 uid           [ unknown] Isabell <isabell@stardust.uberspace.de>
 [...]
 [someuser@somehost ~]$

Alternatively you can use this Web-Tool: https://metacode.biz/openpgp/web-key-directory

Credits
=======

 * https://wiki.gnupg.org/WKDHosting
 * https://spacekookie.de/blog/usable-gpg-with-wkd/
 * https://www.kuketz-blog.de/gnupg-web-key-directory-wkd-einrichten/ (German)

.. _Web Key Directory: https://wiki.gnupg.org/WKD

----

Tested with Uberspace 7.6.0.0

.. author_list::
