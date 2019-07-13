.. highlight:: console

.. author:: Timo Josten <https://dropshare.app>

.. tag:: ssh
.. tag:: file-storage
.. tag:: business

.. sidebar:: About

  .. image:: _static/images/dropshare.png
      :align: center

##########
Dropshare
##########

.. tag_list::

_Dropshare is a customizable, flexible file sharing tool for macOS and iOS and offers, among various popular cloud hosting services, to use a custom SCP/SSH endpoint as file storage. It works well with Uberspace.

Prerequisites
=============

Dropshare supports password or SSH key authentication. Please make sure to set up either in the _Dashboard before continuing.

Password
--------

When using a password, open the Dropshare connection preferences and select *New Connection*, *Customized Cloud* and *SCP over SSH*. The following preferences are required:

+-----------------+-------------------------------------------------------+
| **Hostname**    | Your Uberspace hostname, e.g. *stardust.uberspace.de* |
+-----------------+-------------------------------------------------------+
| **Username**    | Your Uberspace username, e.g. *isabell*               |
+-----------------+-------------------------------------------------------+
| **Password**    | The password you set in the _Dashboard                |
+-----------------+-------------------------------------------------------+
| **Upload Path** | Your DocumentRoot (found                              |
|                 | in the _Datasheet, can also be a sub folder but must  |
|                 | be created on the server first), e.g.                 |
|                 | /home/isabell/html/                                   |
+-----------------+-------------------------------------------------------+
| **URL to Path** | Your HTTPS URL (found in the _Datasheet, if you use   |
|                 | sub folders, append them to the URL), usually         |
|                 | https://isabell.uber.space.                           |
+-----------------+-------------------------------------------------------+

SSH Key
-------

When using a SSH key, open the Dropshare connection preferences and select *New Connection*, *Customized Cloud* and *SCP over SSH*. The following preferences are required:

+-----------------+-------------------------------------------------------+
| **Hostname**    | Your Uberspace hostname, e.g. *stardust.uberspace.de* |
+-----------------+-------------------------------------------------------+
| **Username**    | Your Uberspace username, e.g. *isabell*               |
+-----------------+-------------------------------------------------------+
| **Password**    | The password of your SSH Private Key, optional        |
+-----------------+-------------------------------------------------------+
| **SSH Key Pair**| Select your SSH Private and Public Key                |
+-----------------+-------------------------------------------------------+
| **Upload Path** | Your DocumentRoot (found                              |
|                 | in the _Datasheet, can also be a sub folder but must  |
|                 | be created on the server first), e.g.                 |
|                 | /home/isabell/html/                                   |
+-----------------+-------------------------------------------------------+
| **URL to Path** | Your HTTPS URL (found in the _Datasheet, if you use   |
|                 | sub folders, append them to the URL), usually         |
|                 | https://isabell.uber.space.                           |
+-----------------+-------------------------------------------------------+

Test Connection
---------------

Click the *Test Connection* button to validate your credentials are correct and Dropshare can successfully establish a connection to your Uberspace server. Happy file sharing!


.. _Dropshare: https://dropshare.app
.. _Dashboard: https://dashboard.uberspace.de/dashboard/authentication
.. _Datasheet: https://dashboard.uberspace.de/dashboard/datasheet

----

Tested with Dropshare 5, Uberspace 7.1.1

.. author_list::