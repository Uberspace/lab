.. highlight:: console

.. author:: Karsten Brusch <https://k11h.de>

.. tag:: lang-python
.. tag:: web
.. tag:: blog


.. sidebar:: Logo

  .. image:: _static/images/pelican.png
      :align: center

#########
Pelican
#########

.. tag_list::

Pelican_ is a static site generator implemented in Python_ that combines Jinja templates with content written in Markdown or reStructuredText to produce websites.
The most prominent example is probably `kernel.org <https://www.kernel.org/pelican.html>`_
It is possible to `import <https://docs.getpelican.com/en/latest/importer.html>`_ an existing sites from Wordpress, Tumblr, Blogger and RSS/Atom feeds.
Pelican's source code is available on `GitHub <https://github.com/getpelican/pelican>`_ and it is an implementation of the static site generators concept.

Pelican was released for the first time in 2010 by Alexis Métaireau.

----

License
=======

Pelican is free and open source software licensed under `AGPL 3 <https://www.gnu.org/licenses/agpl-3.0.en.html>`_.

Prerequisites
=============

Pelican currently runs best on Python 3.6+; earlier versions are not supported. 
This version comes preinstalled on your uberspace.

.. note:: If you want to use your own website domain, refer to the uberspace manual for :manual:`domains <web-domains>`

Installation
============

Pelican is installed simply by using pip3

::

 [isabell@stardust isabell]$ pip3 install --upgrade --user "pelican[markdown]"

.. note:: If you prefer to install the latest bleeding-edge version of Pelican rather than a stable release, use the following command:

  ::

    pip3 install --upgrade --user -e "git+https://github.com/getpelican/pelican.git#egg=pelican"


Generate your website
=====================

Initialize
----------

Pelican comes with a handy quickstart wizard that creates the basic structure for you.
Run it inside a subfolder. In this guide, we'll use ``~/pelican``

:: 

  [isabell@stardust isabell]$ mkdir ~/pelican && cd ~/pelican
  [isabell@stardust pelican]$ pelican-quickstart

  Welcome to pelican-quickstart v4.6.0.

  This script will help you create a new Pelican-based website.

  Please answer the following questions so this script can generate the files
  needed by Pelican.

  > Where do you want to create your new web site? [.] <enter>
  > What will be the title of this web site? my-shiny-blogtitle
  > Who will be the author of this web site? isabell
  > What will be the default language of this web site? [de] <enter>
  > Do you want to specify a URL prefix? e.g., https://example.com   (Y/n) <enter>
  > What is your URL prefix? (see above example; no trailing slash) https://isabell.uber.space
  > Do you want to enable article pagination? (Y/n) <enter>
  > How many articles per page do you want? [10] <enter>
  > What is your time zone? [Europe/Paris] Europe/Berlin
  > Do you want to generate a tasks.py/Makefile to automate generation and publishing? (Y/n) <enter>
  > Do you want to upload your website using FTP? (y/N) <enter>
  > Do you want to upload your website using SSH? (y/N) <enter>
  > Do you want to upload your website using Dropbox? (y/N) <enter>
  > Do you want to upload your website using S3? (y/N) <enter>
  > Do you want to upload your website using Rackspace Cloud Files? (y/N) <enter>
  > Do you want to upload your website using GitHub Pages? (y/N) <enter>
  Done. Your new project is available at /home/isabell/pelican

  [isabell@stardust pelican]$ 


.. note:: In case you want to use a custom domain other than isabell.uber.space, you can enter it here or easily change it later in ``~/pelican/pelicanconf.py``

Prepare Publish
---------------

You need to modify ``~/pelican/Makefile`` to make sure the publish process is working correctly on your uberspace.

.. code-block:: diff

  BASEDIR=$(CURDIR)
  INPUTDIR=$(BASEDIR)/content
-  OUTPUTDIR=$(BASEDIR)/output
+  OUTPUTDIR=/var/www/virtual/$(USER)/html


Create Content
--------------

Now create your first blogpost by placing a markdown file in ``~/pelican/content/my-super-post.md``

::

  Title: My super title
  Date: 2010-12-03 10:20
  Modified: 2010-12-05 19:30
  Category: Python
  Tags: pelican, publishing
  Slug: my-super-post
  Authors: Alexis Metaireau, Conan Doyle
  Summary: Short version for index and feeds

  This is the content of my 1st super blog post.

.. note:: More details how to write articles and pages can be found in the `official page <https://docs.getpelican.com/en/latest/content.html>`_

Publish Content
---------------

To generate to final html files and publish them to your uberspace webserver, simply run 

::

  [isabell@stardust isabell]$ cd ~/pelican
  [isabell@stardust pelican]$ make publish

.. warning:: 

  This step will delete all content in ``~/html``, if any.

Then you can simply open `https://isabell.uber.space/ <https://isabell.uber.space/>`_

Configuration
==============

All configuration is done in two files. 
Please refer to the `official docs <https://docs.getpelican.com/en/latest/settings.html>`_ on how to customize them.

1. ``~/pelican/pelicanconf.py`` 
2. ``~/pelican/publishconf.py``


Themes
=======

To install a theme other than the default, please check the `official guide <https://docs.getpelican.com/en/latest/pelican-themes.html>`_.

You can simply choose one from `http://www.pelicanthemes.com/ <http://www.pelicanthemes.com/>`_ and run ``git clone``
In this example I am using the theme maned ``Flex`` 

::

  [isabell@stardust isabell]$ cd ~/pelican
  [isabell@stardust pelican]$ git clone git@github.com:alexandrevicenzi/Flex.git theme

Then add following line to you ``~/pelican/pelicanconf.py``

:: 

  THEME = "theme"


.. _Pelican: https://docs.getpelican.com/
.. _Python: https://www.python.org/

----

Tested with Pelican 4.6.0 and Uberspace 7.3.6

.. author_list::
