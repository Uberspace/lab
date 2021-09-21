.. highlight:: console

.. author:: step21 <step21@devtal.de>

.. tag:: lang-prolog

.. sidebar:: Logo

  .. image:: _static/images/jupyter.svg
      :align: center

################
SWISH/SWI-Prolog
################

.. tag_list::

`SWISH`_ is a web-based interactive computational environment for SWI-Prolog, a logic programming language. It offers both programs that then can be queried, as well as a notebook environment where programs, queries and descriptions can be mixed.
----

.. note:: For this guide you should be familiar with the basic concepts of

  * :manual:`web-backends <web-backends>`

License
=======

`SWI-Prolog`_ is released under the `Simplified BSD License`_. All relevant information can be found in the LICENSE_ file in the repository of the project.
`SWISH` is released under the `Simplified BSD License`_ as well.

Prerequisites
=============

As the cmake on uberspace is relatively old, a newer cmake has to be installed. In addition, the ninja build system also has to be installed.

.. code-block:: console

 wget https://github.com/Kitware/CMake/releases/download/v3.17.3/cmake-3.17.3-Linux-x86_64.sh
 bash cmake-3.17.3-Linux-x86_64.sh --skip-license --prefix=$HOME
 rm cmake-3.17.3-Linux-x86_64.sh
 hash -r
 cmake --version

 [isabell@stardust ~]$

.. code-block:: console

 wget https://github.com/ninja-build/ninja/releases/download/v1.10.2/ninja-linux.zip
 unzip ninja-linux.zip
 rm ninja-linux.zip
 mv ninja ~/bin
 mv ninja bin/
 
libarchive has to be installed manually as it is not present on uberspace.
 
 .. code-block:: console
  
  wget https://www.libarchive.org/downloads/libarchive-3.5.2.tar.gz
  ./configure --prefix=$HOME
  make && make install

- Note: This was tested with node v12 and the yarn package manager already installed. I am not sure anymore if they were installed by default, if not, install them.

Installation
============



.. code-block:: console

 
 git clone https://github.com/SWI-Prolog/swipl-devel.git
 cd swipl-dev
 git submodule update --init
 mkdir build
 cd build
 cmake -DCMAKE_INSTALL_PREFIX=$HOME -DCMAKE_BUILD_TYPE=Release -G Ninja ..
 
Then, the path to libarchive has to be specified manually. Make sure that libarchive points to the right path in swipl-devel/build/CMakeCache.txt
Look for the right line in vim with `/` `archive` + enter. Then ensure it matches (based on the current example) the following lines:
 
.. code-block:: editor

 //libarchive include directory
 LibArchive_INCLUDE_DIR:PATH=/home/<user>/lib/include
 
 //libarchive library
 LibArchive_LIBRARY:FILEPATH=/home/<user>/lib/lib/libarchive.so

.. code-block:: console

 ninja
 ninja install

 [isabell@stardust ~]$ 
 git clone https://github.com/SWI-Prolog/swish.git
 cd swish
 git submodule update --init
 make packs
 (assuming node is up to date and working with yarn)
 yarn
 make src

Configuration
=============

Setting some configuration values for authenticated access and creating a user.

.. code-block:: console

 cd swish
 mkdir -p config-enabled
 (cd config-enabled && ln -s ../config-available/auth_http_always.pl)

 
Then inside the SWI-Prolog prompt, add a new user by following the prompts. (Only really relevant are username and password)

 
.. code-block:: swipl
 
 swipl run.pl
 -? swish_add_user.
 

Setup daemon
------------

.. code-block:: console

 swipl daemon.pl --http --port=3050
 
 (or replace with whatever port is free or you prefer)

Setting up the web backend
-----------------

.. code-block:: console

 [isabell@stardust ~]$ uberspace web backend list
 uberspace web domain add swish.yourdomain.eu # add subdomain for swish
 uberspace web backend set swish.yourdomain.eu --http --port 3050
 uberspace web backend list
 [isabell@stardust ~]$

Now you can access the SWISH webinterface via http://swish.yourdomain.eu

Updates
=======


.. _SWISH: https://github.com/SWI-Prolog/swish
.. SWI-Prolog https://github.com/SWI-Prolog/swipl-devel
.. _LICENSE: https://github.com/SWI-Prolog/swish/blob/master/LICENSE
.. _BSD 2-Clause "Simplified" License: https://spdx.org/licenses/BSD-2-Clause.html


----

Tested with Swish and SWI Prolog 8.x, Uberspace 7.x

.. author_list::
