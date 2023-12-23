.. highlight:: console

.. author:: Kaisa-Marysia <https://www.kasiandras-dreams.de>

.. tag:: rust
.. tag:: blog
.. tag:: cms

####
Zola
####

.. tag_list::

Zola is an in rust written static site generator similar to Hugo and use the Tera template engine.

----

License
=======

Zola is released under the `MIT License <https://github.com/getzola/zola/blob/master/LICENSE>`_.

Sources
=======

  * Documentation_
  * Github_
  * Zola_

Prerequisites
=============

Zola is distributed as a single binary and requires ``GLIBC 2.28``, which isn't available in U7. We need to compile Zola from source with ``GLIBC 2.17``. Also, the default ``Cargo`` configuration will run into **Out Of Memory** during building the binary.

Build from Source
=================

Create working directory
------------------------

First create a working directory in your home and navigate there.

::

  [isabell@stardust ~]$ mkdir ~/git
  [isabell@stardust ~]$ cd ~/git
  [isabell@stardust git]$
  
Clone Repository
----------------

We need to clone the source code from GitHub, so we may build the binary file.

::

  [isabell@stardust git]$ git clone https://github.com/getzola/zola.git
  [isabell@stardust git]$ cd zola
  [isabell@stardust zola]$

Modify the configurations
------------------------

We need to change the `Link-time optimization (LTO) <https://nnethercote.github.io/perf-book/build-configuration.html#link-time-optimization>`_ from true to false, else the building process will fail because of a SIGKILL.
Also, we need to set some cargo configs, which allows allocating more memory for the building process.

Edit the file ``Cargo.toml`` and change the lto value to false:

::

  [...]
  [profile.release]
  lto = false
  [...]

Also create a new file in ``~/.cargo/config`` (if not already exists) with this content:

::

  [target.nightly-x86_64-unknown-linux-gnu]
  rustflags = ["-C", "target-feature=+atomics,+bulk-memory,+mutable-globals", "-C", "link-arg=--max-memory=8589934592"]

Build and install Zola
----------------------

To build Zola we need just to run ``cargo install``. The ``--path`` option set the source directory and ``--root`` as destination for ``bin/zola``. With the ``-j`` option, we set the parallel jobs for the building process.

::

  [isabell@stardust zola]$ cargo install --path . --root ~/ -j 4
  [isabell@stardust zola]$

Create website
==============

After we build and install Zola, we are able to use it.

Create a new project
-------------------

Zola is now build and installed on your Uberspace and you are ready to create your first website.
Navigate to a path you want to store your project and run ``zola init`` to
initial a new project and create a new directory containing the sources for
your website.

::

  [isabell@stardust zola]$ cd
  [isabell@stardust ~]$ zola init website_name
  Welcome to Zola!
  Please answer a few questions to get started quickly.
  Any choices made can be changed by modifying the `config.toml` file later.
  > What is the URL of your site? (https://example.com):
  > https://ulabdev.uberspace.de/blog
  > Do you want to enable Sass compilation? [Y/n]: Y
  > Do you want to enable syntax highlighting? [y/N]: Y
  > Do you want to build a search index of the content? [y/N]: Y

  Done! Your site was created in /var/www/virtual/ulabdev/website_name

  Get started by moving into the directory and using the built-in server: `zola serve`
  Visit https://www.getzola.org for the full documentation.
  [isabell@stardust ~]$
Add theme
---------

The easiest way to install a theme is to clone its repository in the ``themes`` directory:

::

 [isabell@stardust ~]$ cd ~/website_name/themes
 [isabell@stardust themes]$ git clone ``<theme repository URL>``
 [isabell@stardust themes]$
 
A list of themes are on the official `Zola Website <https://www.getzola.org/themes/>`_.

::

  [isabell@stardust themes]$ git clone https://github.com/janbaudisch/zola-hallo.git
  Cloning into 'zola-hallo'...
  remote: Enumerating objects: 158, done.
  remote: Counting objects: 100% (23/23), done.
  remote: Compressing objects: 100% (6/6), done.
  remote: Total 158 (delta 18), reused 17 (delta 17), pack-reused 135
  Receiving objects: 100% (158/158), 1.64 MiB | 21.75 MiB/s, done.
  Resolving deltas: 100% (57/57), done.
  [isabell@stardust themes]$
  
Using a theme
-------------

After you cloned a theme's repository, you need to tell Zola to use the ``theme``, by setting it in the `configuration file <https://www.getzola.org/documentation/getting-started/configuration/>`_.
The theme name has to be the name of the directory you cloned the theme in.
Edit ``~/website_name/config.toml`` and insert above the ``[markdown]`` block the configuration ``theme = "<theme_name>"``.

::

  # The URL the site will be built for
  base_url = "https://ulabdev.uber.space/blog"

  # Whether to automatically compile all Sass files in the sass directory
  compile_sass = true

  # Whether to build a search index to be used later on by a JavaScript library
  build_search_index = true

  # Theme name
  theme = "zola-hallo"

  [markdown]
  # Whether to do syntax highlighting
  # Theme can be customised by setting the `highlight_theme` variable to a theme supported by Zola
  highlight_code = true

  [extra]
  # Put all your custom variables here

Create Content
--------------

Every theme has their own configuration toml file. Take a look at the `GitHub
repository <https://github.com/janbaudisch/zola-hallo>`_ and read the
documentation for further information.

For our first website, we create a markdown file, which will be rendered by
Zola during our deployment.

::

  [isabell@stardust themes]$ cd ..
  [isabell@stardust website_name]$ $EDITOR content/_index.md
  [isabell@stardust website_name]$
  
  +++
  +++
  Hello World. This is a single-page theme named hallo and it's deployed on uberspace.
  Add a portrait, an introduction, several links, and you're set. The introduction goes into content/_index.md. Create a file called portrait.jpg in static/images to replace the standard portrait.

Deploying your site
===================

As a static site generator, Zola build a bunch of HTML files, which can be serve the files in ``~/html`` by the `http stack <https://manual.uberspace.de/background-http-stack>`_.
To create the html files, we use ``zola build`` with the ``-o <PATH>`` option for the output destination and tell Zola to deploy the files into ``~/html/blog``. Each time you do changes, you must repeat this step.

::

  [isabell@stardust website_name]$ zola build -o ~/html/blog
  [isabell@stardust website_name]$
  
Navigate your Browser to your installation URL ``https://isabell.uber.space/blog`` and check your new website.

Updates
=======

To update Zola, you must pull the repository from GitHub and rebuild the binary.

::

  [isabell@stardust ~]$ cd git/zola
  [isabell@stardust zola]$ git pull
  [isabell@stardust zola]$ cargo install --path . --root ~/ -j 4
  [isabell@stardust zola]$
  
.. _Git: https://git-scm.com/book/en/v2/Getting-Started-Installing-Git/
.. _Zola: https://getzola.org
.. _feed: https://github.com/getzola/zola/releases.atom
.. _MIT_License: https://github.com/getzola/zola/releases.atom
.. _Github: https://github.com/getzola/zola/releases
.. _Documentation: https://www.getzola.org/documentation/getting-started/overview/
----

Tested with Zola 1.7.2, Uberspace 7.15.6

.. author_list::
