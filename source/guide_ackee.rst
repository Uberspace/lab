.. author:: tobimori <tobias@moeritz.cc>

.. tag:: monitoring
.. tag:: web
.. tag:: analytics
.. tag:: self-hosting
.. tag:: privacy
.. tag:: lang-nodejs

.. highlight:: console

#####
Ackee
#####

.. tag_list::

Ackee_ is a self-hosted, :manual:`Node.js <lang-nodejs>` based analytics tool "for those who care about privacy."

----

.. note:: For this guide you should be familiar with the basic concepts of

  * :manual:`Node.js <lang-nodejs>`
  * :manual:`web backends <web-backends>`
  * :manual:`supervisord <daemons-supervisord>`
  * :manual:`domains <web-domains>`

License
=======

Ackee_ is released under the `MIT License`_.

Prerequisites
=============

Ackee needs a working :lab:`MongoDB <guide_mongodb>` installation. 
Follow and install MongoDB as written in the Uberlab guide :lab:`here <guide_mongodb>`.

Then setup your domain:

.. include:: includes/web-domain-list.rst

Also install ``yarn`` globally to later use as package manager for :manual:`Node.js <lang-nodejs>`.

.. code-block:: console

  [isabell@stardust ~]$ npm install yarn -g
  /home/isabell/bin/yarn -> /home/isabell/lib/node_modules/yarn/bin/yarn.js
  /home/isabell/bin/yarnpkg -> /home/isabell/lib/node_modules/yarn/bin/yarn.js
  + yarn@1.22.4
  installed 1 package in 1.002s
  [isabell@stardust ~]$ 

Installation
============

Clone the `GitHub repository of Ackee`_:

.. code-block:: console

  [isabell@stardust ~]$ git clone https://github.com/electerious/Ackee ~/ackee
  Cloning into '/home/isabell/ackee'...
  remote: Enumerating objects: 1528, done.
  remote: Counting objects: 100% (1528/1528), done.
  remote: Compressing objects: 100% (884/884), done.
  remote: Total 7991 (delta 1016), reused 1083 (delta 641), pack-reused 6463
  Receiving objects: 100% (7991/7991), 1.97 MiB | 3.95 MiB/s, done.
  Resolving deltas: 100% (5471/5471), done.
  [isabell@stardust ~]$ 

.. _Ackee: https://ackee.electerious.com/
.. _GitHub repository of Ackee: https://github.com/electerious/Ackee
.. _MIT License: https://github.com/electerious/Ackee/blob/master/LICENSE

----

Tested with Ackee v1.7.1 on Uberspace v7.7.1.2

.. author_list::
