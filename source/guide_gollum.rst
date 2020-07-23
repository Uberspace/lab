.. author:: Moritz Stückler <https://twitter.com/MoStueck>

.. tag:: lang-ruby
.. tag:: wiki
.. tag:: web

.. highlight:: console

######
Gollum
######

.. tag_list::

Gollum_ is a simple wiki software written in :manual:`Ruby <lang-ruby>`. It is the software component that drives many popular wiki integrations (e.g. GitHub and GitLab wikis). It is a very simple, small and fast wiki alternative to larger systems like :lab:`Dokuwiki <guide_dokuwiki>`. Gollum is Git-backed, so all changes made through the web interface are also committed to the underlying Git repository.

----

.. note:: For this guide you should be familiar with the basic concepts of

  * :manual:`Ruby <lang-ruby>` and its package manager gem
  * :manual:`web backends <web-backends>`
  * :manual:`supervisord <daemons-supervisord>`


Prerequisites
=============


Since Ruby and its package manager Gem are already installed by default on Uberspace, one might think, that a simple ``gem install gollum`` would do the trick. Unfortunately that's not the case, because currently (June 2020) Uberspace uses a rather old version of CMake (2.8.12.2). So we need to install a recent version (> 3.5.1) of CMake first, before we can run Gollum.


Install recent CMake version
----------------------------

To install a recent CMake version, the fastest way is to run the official installer script in your home folder (alternatively you could also use brew to install the current CMake version). Make sure to copy the link to the latest version from the `official website <https://cmake.org/download/>`_ (look for "Latest Release" and ``Linux x86_64``).

::

  [isabell@stardust ~]$ wget https://github.com/Kitware/CMake/releases/download/v3.17.3/cmake-3.17.3-Linux-x86_64.sh
  [isabell@stardust ~]$ bash cmake-3.17.3-Linux-x86_64.sh
  [isabell@stardust ~]$

When you run this command, you will be presented with the CMake terms of service, which you need to agree to (Press space bar to scroll down to the end of the file and then agree with ``y``). It will now ask for the target folder. Just stick with the default setting (``/home/isabell/cmake-3.17.3-Linux-x86_64``) for now by again entering ``y``.

Now that CMake is installed, we need to make sure, that Gollum will use the new CMake version for its own install process. Therefore we need to add the new CMake binary to the PATH variable temporarily.

::

  [isabell@stardust ~]$ export PATH=$HOME/cmake-3.17.3-Linux-x86_64/bin/:$PATH
  [isabell@stardust ~]$

Now make sure that your new CMake version works correctly by checking the version number using this command:

::

  [isabell@stardust ~]$ cmake --version
  cmake version 3.17.3
  [isabell@stardust ~]$


All good! Now we're ready to install Gollum.

Create directory for Gollum content
-----------------------------------

All the data within Gollum is kept in one directory, which is also where the underlying Git repository is located. You should create a new, empty directory in your home folder if you want to start a new wiki (or clone an existing Git repository instead).

::

  [isabell@stardust ~]$ git init wiki
  [isabell@stardust ~]$


Install Gollum
==============

Gollum can now be installed via the ruby package manager by running:

::

  [isabell@stardust ~]$ gem install gollum
  [isabell@stardust ~]$

You can now remove CMake (both the installer and the folder) again, if you want to. You should also edit your ``.bash_profile`` to remove the CMake folder from the ``PATH`` variable.

::

  [isabell@stardust ~]$ rm -rf cmake-3.17.3-Linux-x86_64.sh cmake-3.17.3-Linux-x86_64
  [isabell@stardust ~]$


Now you should be able to start Gollum via:

::

  [isabell@stardust ~]$ gollum $HOME/wiki
  [isabell@stardust ~]$

However Gollum is not yet reachable from the internet. So, close the Gollum application again (by pressing ``CTRL + C``).

Setting up a web backend
------------------------

.. note:: By default Gollum runs on port 4567, so we need to create a web backend for this port. 
.. include:: includes/web-backend.rst

.. note:: If you want to run Gollum under a different URL, just adjust the "/" parameter in the command above to match your preferred path.

Now you can start Gollum again and you should be able to open it in your browser using your Uberspace URL (e.g. ``https://isabell.uber.space/``).

Gollum as a service
======================

If you want to run Gollum on your Uberspace permanently it's probably a good idea to :manual:`run it as a service<daemons-supervisord>`, meaning it will run in the background and autostart when the system reboots. Create a new file ``~/etc/services.d/gollum.ini`` and paste this:

.. code-block:: ini

  [program:gollum]
  command=gollum %(ENV_HOME)s/wiki
  autostart=yes
  autorestart=yes

.. include:: includes/supervisord.rst


.. _Gollum: https://github.com/gollum/gollum


----

Tested with CMake 3.17.3, Gollum 5.0.1, Uberspace 7.7.1.2

.. author_list::
