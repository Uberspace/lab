.. highlight:: console

.. author:: Dave Wilding <https://github.com/dwilding>

.. tag:: privacy
.. tag:: web

.. sidebar:: Logo

  .. image:: _static/images/frogtab.svg
      :align: center

#######
Frogtab
#######

.. tag_list::

Frogtab_ is a web-based task manager that prioritizes privacy and minimalism. Your data is stored in your browser and isn't sent to your Uberspace.

After installing Frogtab, you'll be able to create a personal link. This will enable you to send tasks to Frogtab from any device, using your Uberspace as temporary storage for (encrypted) tasks.

----

Installation
============

::

[isabell@stardust ~]$ wget https://frogtab.com/install_frogtab.sh
[isabell@stardust ~]$ chmod +x install_frogtab.sh
[isabell@stardust ~]$ ./install_frogtab.sh ~/html
[isabell@stardust ~]$

The installation is complete. To use Frogtab, open ``https://isabell.uber.space`` in your browser.

To create a personal link, see `Registering for a personal link`_ on the help page of Frogtab.

Best practices
==============

Anyone who knows the URL of your Uberspace will be able to create their own personal link. You probably don't want to provide this service to the general public (that's what frogtab.com is for), so after you've created your personal link you should configure Frogtab to reject further registrations.

To configure Frogtab to reject registrations, set ``allow_registration = false`` in ``~/frogtab.toml``.

Updates
=======

.. note:: Check the update feed_ regularly to stay informed about the newest version.

To update Frogtab, run the following command:

::

[isabell@stardust ~]$ ./install_frogtab.sh ~/html
[isabell@stardust ~]$

The installer will ask for confirmation before overwriting the files that you originally installed.

Backup data
===========

Your data is stored in your browser. You can export a backup at any time. In some browsers, you can also enable automatic backups. See `Backing up your data`_ on the help page of Frogtab.

Frogtab stores information about personal links in ``~/frogtab.db``. If several people have created personal links, you should back up ``frogtab.db`` regularly in case you reinstall Frogtab from scratch. If you're the only person who has created a personal link, it's less important to back up ``frogtab.db``.

.. _Frogtab: https://frogtab.com
.. _feed: https://frogtab.com/changes.xml
.. _Registering for a personal link: https://isabell.uber.space/help#registering-for-a-personal-link
.. _Backing up your data: https://isabell.uber.space/help#backing-up-your-data

----

Tested with Frogtab pull/28, Uberspace 7.16.7

.. author_list::
