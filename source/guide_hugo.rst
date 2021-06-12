.. highlight:: console

.. author:: Christian Kantelberg <uberlab@mailbox.org>
.. author:: luto <http://luto.at>
.. author:: Julian Oster <https://jlnostr.de>

.. tag:: lang-go
.. tag:: blog
.. tag:: cms

.. sidebar:: Logo

  .. image:: _static/images/hugo-logo.png
      :align: center

####
Hugo
####

.. tag_list::

.. abstract::
  Hugo is a fast and modern static site generator written in Go, and designed to make website creation fun again.

----

.. note:: For this guide you should be familiar with the basic concepts of

  * Git_
  * :manual:`Domains <web-domains>`

License
=======

From version 0.15 on Hugo is released under the `Apache 2.0 license`_.

Prerequisites
=============

Your URL needs to be setup:

::

 [isabell@stardust ~]$ uberspace web domain list
 isabell.uber.space
 [isabell@stardust ~]$

Installation
============

Create website root
-------------------

Create a new directory containing the sources for your website.

::

 [isabell@stardust ~]$ mkdir hugo_websites
 [isabell@stardust ~]$

Download
--------

Check the Hugo_ website or `Github Repository`_ for the latest release and copy the download link to the Linux-64bit.tar.gz file. Then use ``wget`` to download it. Replace the URL with the one you just got from GitHub.

::

 [isabell@stardust ~]$ wget https://github.com/gohugoio/hugo/releases/download/v0.57.2/hugo_0.57.2_Linux-64bit.tar.gz
 […]
 Saving to: ‘hugo_0.57.2_Linux-64bit.tar.gz’

 100%[======================================>] 7,750,708   6.64MB/s   in 1.1s

 2019-01-14 16:56:27 (6.64 MB/s) - ‘hugo_0.57.2_Linux-64bit.tar.gz’ saved [7750708/7750708]
 [isabell@stardust ~]$

Get the hugo binary from the archive, delete the archive and enable hugo to be executed easily. Replace the version in the archive file name with the one you just downloaded.

::

 [isabell@stardust ~]$ tar -xvf hugo_0.57.2_Linux-64bit.tar.gz hugo
 hugo
 [isabell@stardust ~]$ rm hugo_0.57.2_Linux-64bit.tar.gz
 [isabell@stardust ~]$ mv hugo ~/bin
 [isabell@stardust ~]$

After setting up, test if Hugo works. The output is the version number of Hugo.

::

 [isabell@stardust ~]$ hugo version
 Hugo Static Site Generator v0.57.2-A849CB2D linux/amd64 BuildDate: 2019-08-17T17:54:13Z
 [isabell@stardust ~]$


Create first website
--------------------

Hugo is now installed on your Uberspace. This means you're ready to create your first Hugo site! To do this, switch to the corresponding directory and create the Hugo page there.

::

 [isabell@stardust ~]$ cd ~/hugo_websites
 [isabell@stardust hugo_websites]$ hugo new site hugo_web
 Congratulations! Your new Hugo site is created in /home/isabell/hugo_websites/hugo_web.

 Just a few more steps and you're ready to go:

 1. Download a theme into the same-named folder.
    Choose a theme from https://themes.gohugo.io/, or
    create your own with the "hugo new theme <THEMENAME>" command.
 2. Perhaps you want to add some content. You can add single files
    with "hugo new <SECTIONNAME>/<FILENAME>.<FORMAT>".
 3. Start the built-in live server via "hugo server".

 Visit https://gohugo.io/ for quickstart guide and full documentation.
 [isabell@stardust hugo_websites]$

Add theme
---------

Since Hugo is delivered without a theme, this must now be installed. To do so, look for a theme you like at https://themes.gohugo.io/ and install it into the ``themes`` directory of your site. This example uses the theme FutureImperfect_, but you are free to use any other theme. Then copy the sample files into the project root, to quickly bootstrap you new site.

::

 [isabell@stardust ~]$ cd ~/hugo_websites/hugo_web/themes
 [isabell@stardust themes]$ git clone https://github.com/jpescador/hugo-future-imperfect.git
 Cloning into 'hugo-future-imperfect'...
 remote: Enumerating objects: 1, done.
 remote: Counting objects: 100% (1/1), done.
 remote: Total 1386 (delta 0), reused 0 (delta 0), pack-reused 1385
 Receiving objects: 100% (1386/1386), 4.38 MiB | 6.65 MiB/s, done.
 Resolving deltas: 100% (789/789), done.
 [isabell@stardust themes]$ cp -R hugo-future-imperfect/exampleSite/* ../.
 [isabell@stardust themes]$

Deploying your site
===================

Hugo is a static site generator. It will build a bunch of HTML and CSS files, which can be served by any web server. In our case, there is a httpd set up to serve files in ``~/html``, so we tell hugo to drop the files there. This step needs to be repeated each time you change something about your site. Using the ``--destination`` parameter, you can also deploy the files to a different directory or domain for testing.
Before that, the `HUGO_CACHEDIR` environment variable is set to the local `tmp` directory. Otherwise the build will fail, because Hugo is trying to access the global `/tmp` folder, which is not allowed.

.. warning::

  The following command will delete all existing files in your document root.
  Make sure it is empty before running it.

::

  [isabell@stardust ~]$ cd ~/hugo_websites/hugo_web
  [isabell@stardust hugo_web]$ HUGO_CACHEDIR=$HOME/tmp hugo --cleanDestinationDir --destination /var/www/virtual/$USER/html

Finishing installation
======================

Point your Browser to your installation URL ``https://isabell.uber.space`` and
admire your shiny new website!

Tuning
======

To finish configuring your Hugo website, creating pages and posts, go to https://gohugo.io/documentation.

Updates
=======

.. note:: Check the update feed_ regularly to stay informed about the newest version.

If there is a new version available, update the ``hugo`` binary in ``~/bin`` (repeat "Download"). It might be a good idea to rebuild your site, too, but that's not strictly necessary.


.. _Git: https://git-scm.com/book/en/v2/Getting-Started-Installing-Git/
.. _Hugo: https://gohugo.io/getting-started/installing/
.. _feed: https://github.com/gohugoio/hugo/releases.atom
.. _FutureImperfect: https://github.com/jpescador/hugo-future-imperfect
.. _Apache 2.0 License: https://github.com/gohugoio/hugo/blob/master/LICENSE
.. _Github Repository: https://github.com/gohugoio/hugo/releases

----

Tested with Hugo 0.57.2, Uberspace 7.3.5.1

.. author_list::
