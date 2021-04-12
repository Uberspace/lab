.. highlight:: console

.. author:: Sascha Groetzner <https://groetzner.net>

.. tag:: web

.. sidebar:: Logo

  .. image:: _static/images/apache.png
      :align: center

########################
Multidomain DocumentRoot
########################

.. tag_list::

Using Apache Rewrite to split multiple domains/subdomains within one DocumentRoot.

----

.. note:: For this guide you should be familiar with the basic concepts of

  * :manual:`domains <web-domains>`

Prerequisites
=============

.. warning:: We strongly suggest to use different accounts for different projects due to security reasons. If one of the DocumentRoots gets compromised (e.g. because of a `CVE <http://www.cvedetails.com/product/4096/Wordpress-Wordpress.html?vendor_id=2337>`_), all other files within all other DocumentRoots can be compromised as well.

We're using the following Domains for our setup:
 * isabell.uber.space
 * example1.com
 * example2.com
 * dev.example2.com
Additional we will us a symlink for www.example1.com to example1.com
 * www.example1.com -> example1.com

Your domains needs to be setup:

::

 [isabell@stardust ~]$ uberspace web domain list
 isabell.uber.space
 [isabell@stardust ~]$ uberspace web domain add example1.com
 [isabell@stardust ~]$ uberspace web domain add www.example1.com
 [isabell@stardust ~]$ uberspace web domain add example2.com
 [isabell@stardust ~]$ uberspace web domain add dev.example2.com
 [isabell@stardust ~]$ uberspace web domain list
 isabell.uber.space
 example1.com
 example2.com
 dev.example2.com
 www.example1.com

Configure Environment
=====================
Create directories
------------------
Create directories for each domain outside of the DocumentRoot:

::

 [isabell@stardust ~]$ cd /var/www/virtual/isabell/
 [isabell@stardust isabell]$ mkdir example1_com
 [isabell@stardust isabell]$ mkdir example2_com
 [isabell@stardust isabell]$ mkdir dev_example2_com
 [isabell@stardust isabell]$ ls
 dev_example2_com
 example1_com
 example2_com

Create symlinks
------------------
Create symlinks within html-folder to our domains-directories

::

 [isabell@stardust ~]$ ln -s /var/www/virtual/isabell/example1_com /var/www/virtual/isabell/html/example1_com
 [isabell@stardust ~]$ ln -s /var/www/virtual/isabell/example2_com /var/www/virtual/isabell/html/example2_com
 [isabell@stardust ~]$ ln -s /var/www/virtual/isabell/dev_example2_com /var/www/virtual/isabell/html/dev_example2_com
 [isabell@stardust ~]$ ls -l /var/www/virtual/isabell/html/
 ... dev_example2_com -> /var/www/virtual/isabell/dev_example2_com
 ... example1_com -> /var/www/virtual/isabell/example1_com
 ... example2_com -> /var/www/virtual/isabell/example2_com

Configure the web server
------------------------
We will use Apache Rewrite with .htaccess to split the domains to your created folders.
Create ``/var/www/virtual/isabell/html/.htaccess`` with the following content:

.. code-block:: ini

 RewriteEngine on

 # example1.com
 RewriteCond %{HTTP_HOST} ^example1.com [OR]
 RewriteCond %{HTTP_HOST} ^www.example1.com
 RewriteCond %{REQUEST_URI} !^/example1_com
 RewriteRule ^(.*)$ /example1_com/$1 [L]

 # example2.com
 RewriteCond %{HTTP_HOST} ^example2.com
 RewriteCond %{REQUEST_URI} !^/example2_com
 RewriteRule ^(.*)$ /example2_com/$1 [L]

 # dev.example2.com
 RewriteCond %{HTTP_HOST} ^dev.example2.com
 RewriteCond %{REQUEST_URI} !^/dev_example2_com
 RewriteRule ^(.*)$ /dev_example2_com/$1 [L]


Best practices
==============
To not get in conflict with existing directorys/files in your ``html directory`` you can move all domain-symlinks to a ``hidden``-subfolder

.. warning:: This is only Security through obscurity. If you know the ``foldername`` you have access to all other domains

Generate an ``openssl -hex`` key now and and make a new directory within ``html``.

::

 [isabell@stardust ~]$ openssl rand -hex 16
 c6d23206601cabbdc20112fe2cd2f258
 [isabell@stardust ~]$ mkdir /var/www/virtual/isabell/html/c6d23206601cabbdc20112fe2cd2f258

Now we modify/replace our upper example to the following symlinks

::

 [isabell@stardust ~]$ ln -s /var/www/virtual/isabell/example1_com /var/www/virtual/isabell/html/c6d23206601cabbdc20112fe2cd2f258/example1_com
 [isabell@stardust ~]$ ln -s /var/www/virtual/isabell/example2_com /var/www/virtual/isabell/html/c6d23206601cabbdc20112fe2cd2f258/example2_com
 [isabell@stardust ~]$ ln -s /var/www/virtual/isabell/dev_example2_com /var/www/virtual/isabell/html/c6d23206601cabbdc20112fe2cd2f258/dev_example2_com

We have also to modify/replace our upper ``/var/www/virtual/isabell/html/.htaccess``

.. code-block:: ini

 RewriteEngine on

 # example1.com
 RewriteCond %{HTTP_HOST} ^example1.com [OR]
 RewriteCond %{HTTP_HOST} ^www.example1.com
 RewriteCond %{REQUEST_URI} !^/c6d23206601cabbdc20112fe2cd2f258/example1_com
 RewriteRule ^(.*)$ /c6d23206601cabbdc20112fe2cd2f258/example1_com/$1 [L]

 # example2.com
 RewriteCond %{HTTP_HOST} ^example2.com
 RewriteCond %{REQUEST_URI} !^/c6d23206601cabbdc20112fe2cd2f258/example2_com
 RewriteRule ^(.*)$ /c6d23206601cabbdc20112fe2cd2f258/example2_com/$1 [L]

 # dev.example2.com
 RewriteCond %{HTTP_HOST} ^dev.example2.com
 RewriteCond %{REQUEST_URI} !^/c6d23206601cabbdc20112fe2cd2f258/dev_example2_com
 RewriteRule ^(.*)$ /c6d23206601cabbdc20112fe2cd2f258/dev_example2_com/$1 [L]

----

Tested with Uberspace 7.10.0

.. author_list::

