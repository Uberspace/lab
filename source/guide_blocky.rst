.. highlight:: console

.. author:: Thomas Johnson <https://johnson.tj/>

.. tag:: lang-go
.. tag:: dns

.. sidebar:: Logo

  .. image:: _static/images/blocky.svg
      :align: center

######
Blocky
######

.. tag_list::

Blocky_  is a DNS proxy and ad-blocker for the local network written in Go.

.. note:: In this guide we use it to setup a our own DoH (DNS over HTTPS) server. It can also be configured as a standard DNS and DoT (DNS over TLS) server. But you won't be able to run it on standard ports 53 and 853. We only cover DoH in this guide.

----

.. note:: For this guide you should be familiar with the basic concepts of

  * :manual:`domains <web-domains>`
  * :manual:`supervisord <daemons-supervisord>`
  * :manual:`web backends <web-backends>`

Installation
============

We create the working directory, download the latest version and extract the file.

.. code-block:: console

 [isabell@stardust ~]$ mkdir blocky
 [isabell@stardust ~]$ cd blocky
 [isabell@stardust blocky]$ wget https://github.com/0xERR0R/blocky/releases/download/v0.25/blocky_v0.25_Linux_x86_64.tar.gz
 [isabell@stardust blocky]$ tar -xzf blocky_v0.25_Linux_x86_64.tar.gz
 [isabell@stardust blocky]$ rm blocky_v0.25_Linux_x86_64.tar.gz
 [isabell@stardust blocky]$

Configuration
=============

To setup blocky you have to create a ``config.yml`` file with your favorite text editor.

.. code-block:: yaml

 upstreams:
   groups:
     default:
       - https://dns.quad9.net/dns-query
 blocking:
   denylists:
     ads:
       - https://raw.githubusercontent.com/StevenBlack/hosts/master/hosts
   clientGroupsBlock:
     default:
       - ads
 ports:
   dns:
   http: 4000

Service
=======

Now you should set up a service that keeps blocky alive while you are gone. Create the file ``~/etc/services.d/blocky.ini`` with the following content:

.. code-block:: ini

 [program:blocky]
 directory=%(ENV_HOME)s/blocky
 command=%(ENV_HOME)s/blocky/blocky --config config.yml
 autostart=yes
 autorestart=yes
 startsecs=30

.. include:: includes/supervisord.rst

Web Backend
===========

.. note::

    Blocky should now be running on port 4000.

.. include:: includes/web-backend.rst

::

 [isabell@stardust ~]$ uberspace web backend set / --http --port 4000
 [isabell@stardust ~]$

Updates
=======

.. note:: Check the update feed_ regularly to stay informed about the newest version.

Change the version and repeat the installation step.


.. _Blocky: https://0xerr0r.github.io/blocky/latest/
.. _feed: https://github.com/0xERR0R/blocky/releases.atom


----

Tested with Blocky 0.25, Uberspace 7.16.3

.. author_list::
