.. highlight:: console

.. author:: Nikolas <https://nikolasdas.de>

.. tag:: lang-php
.. tag:: web
.. tag:: database

.. sidebar:: About

  .. image:: _static/images/adminer.svg
      :align: center

#######
Adminer
#######

.. tag_list::

Adminer_ (formerly phpMinAdmin) is a full-featured database management tool written in PHP. Conversely to phpMyAdmin, it consist of a single file ready to deploy to the target server. Adminer is available for :manual:`MySQL <database-mysql>`, MariaDB, :lab:`PostgreSQL <guide_postgresql>`, SQLite, MS SQL, Oracle, Firebird, SimpleDB, Elasticsearch and :lab:`MongoDB <guide_mongodb>`.

----

.. note::

  Uberspace provides instances of Adminer_ and phpMyAdmin_ for everbody to use. Therefore this guide is mainly for people who would like to customize Adminer to their needs.

  * Adminer: https://mysql.uberspace.de/adminer/
  * phpMyAdmin: https://mysql.uberspace.de/phpmyadmin/


License
=======

Adminer_ is released under `Apache License 2.0`_ or `GPL 2`_.

Installation (with Plugin Support)
==================================

Check the current version of Adminer at `GitHub <https://github.com/vrana/adminer/releases>`_ and go the the folder where you want Adminer to be installed.

.. code-block:: console

  [isabell@stardust ~]$ VERSION=4.7.8
  [isabell@stardust ~]$ cd ~/html
  [isabell@stardust html]$ wget -O adminer.php https://github.com/vrana/adminer/releases/download/v$VERSION/adminer-$VERSION.php
  [isabell@stardust html]$ mkdir -p plugins
  [isabell@stardust html]$ wget -O plugins/plugin.php https://raw.githubusercontent.com/vrana/adminer/master/plugins/plugin.php
  [isabell@stardust html]$

Create an ``index.php`` file in the same directory:

.. code-block:: php

  <?php

  function adminer_object() {
    foreach (glob("plugins/*.php") as $filename) {
      include_once "./$filename";
    }

    $plugins = array(
      // ...
    );

    return new AdminerPlugin($plugins);
  }

  include "./adminer.php";

This will include all plugins located in the ``plugins`` folder. To use a plugin you also need to initialize it inside the ``$plugins`` array.

You can find a list of available Plugins `here <https://www.adminer.org/plugins/>`_.

Example Plugin: Themes
----------------------

.. code-block:: console

  [isabell@stardust html]$ THEME_VERSION=1.7
  [isabell@stardust html]$ wget -O theme.zip https://github.com/pematon/adminer-theme/archive/v$THEME_VERSION.zip
  [isabell@stardust html]$ unzip -o theme.zip
  [isabell@stardust html]$ cp -r adminer-theme-$THEME_VERSION/lib/* .
  [isabell@stardust html]$ rm -rf theme.zip adminer-theme-$THEME_VERSION
  [isabell@stardust html]$

Update the ``index.php`` to include the new Plugin:

.. code-block:: php
  :emphasize-lines: 9

  <?php

  function adminer_object() {
    foreach (glob("plugins/*.php") as $filename) {
      include_once "./$filename";
    }

    $plugins = array(
      new AdminerTheme("default-orange")
    );

    return new AdminerPlugin($plugins);
  }

  include "./adminer.php";

Updates
=======

Just repeat the installation steps with the new ``VERSION``.


.. _Adminer: https://www.adminer.org/
.. _phpMyAdmin: https://www.phpmyadmin.net/
.. _Apache License 2.0: https://www.apache.org/licenses/LICENSE-2.0.html
.. _GPL 2: https://www.gnu.org/licenses/gpl-2.0.txt

----

Tested with Adminer 4.7.8, Uberspace 7.8.0.0

.. author_list::
