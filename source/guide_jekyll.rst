.. highlight:: console

.. author:: Pascal Nowak <pascal@nowak.app>

.. sidebar:: Logo


  .. image:: _static/images/jekyll.png
      :align: center


#########
Jekyll
#########

Jekyll_ is an easy to use static site generator that builds fast, blog-aware, responsive websites.

The website is created with markdown and Jekyll generates the html files and deploys it to the webserver.
It is possible to connect Jekyll to git, so that the website can be created on a local machine and then pushed to git where it gets deployed automatically via git hooks.

Jekyll is written in Ruby and licensed under the MIT license.

----

.. note:: For this guide you should be familiar with the basic concepts of

  * :manual:`Ruby <lang-ruby>`
  * git_
  * :manual:`Domains <web-domains>`

License
=======

All relevant legal information can be found here

  * https://github.com/jekyll/jekyll/blob/master/LICENSE

Prerequisites
=============
We're using :manual:`Ruby <lang-ruby>` in the version 2.5.3:

::

 [isabell@stardust ~]$ ruby -v
 ruby 2.5.3p105 (2018-10-18 revision 65156) [x86_64-linux]
 [isabell@stardust ~]$

Your domain needs to be setup:

.. include:: includes/web-domain-list.rst

You need to install a gem called Jekyll:
::

 [isabell@stardust ~]$ gem install bundler jekyll
 Fetching bundler-2.0.1.gem
 [...]
 Successfully installed jekyll-3.8.5
 26 gems installed
 [isabell@stardust ~]$

Installation
============
Jekyll is a ruby gem that creates dummy files and directories for us that contain your website. We can modify these files to make your website look like we want it to.

Just let Jekyll create a new folder containing your website by typing:
::

 [isabell@stardust ~]$ jekyll new website
 Running bundle install in /home/isabell/website...
 [...]
 New jekyll site installed in /home/isabell/website.
 [isabell@stardust ~]$

After Jekyll finished, navigate into your website folder and install all needed gems for your website:
::

 [isabell@stardust ~]$ cd ~/website
 [isabell@stardust website]$ bundle install --path vendor/bundle
 The dependency tzinfo-data (>= 0) will be unused by any of the platforms Bundler is installing for. Bundler is installing for ruby but the dependency is only for x86-mingw32, x86-mswin32, x64-mingw32, java. To add those platforms to the bundle, run `bundle lock --add-platform x86-mingw32 x86-mswin32 x64-mingw32 java`.

 Fetching gem metadata from https://rubygems.org/...........
 [...]
 Bundle complete! 4 Gemfile dependencies, 29 gems now installed.
 Bundled gems are installed into `./vendor/bundle`
 [...]

 [isabell@stardust website]$

Since it is not allowed to install gems at the system default path, you have to add an option for installing gems:

  * ``--path``: Specifies another path for installing gems (here ``vendor/bundle``).

Now you can build and deploy your website to your document root:
::

 [isabell@stardust website]$ bundle exec jekyll build --destination ~/html

 Configuration file: /home/isabell/website/_config.yml
             Source: /home/isabell/website
        Destination: /home/isabell/html
  Incremental build: disabled. Enable with --incremental
       Generating...
        Jekyll Feed: Generating feed for posts
                     done in 0.919 seconds.
  Auto-regeneration: disabled. Use --watch to enable.
 [isabell@stardust website]$

We need to tell Jekyll in what folder to build the website. Since we want it to appear in our document root, we have to add a configuration for the build process:

  * ``--destination``: Tells Jekyll where to build the website (here ``~/html``).

Finishing installation
======================

Now open a browser and navigate to your URL where you can see your beautiful responsive website.

Best practices
======================
If you dont want to create and modify your website on your uberspace, you can install Ruby, Jekyll and git on your local machine and then push it to your uberspace where it gets deployed automatically. This is an easy way to work with an editor of your choice and you can test your website befor publishing it.

To install Ruby, Windows users should use RubyInstaller_, Linux and Mac users could use RVM_.

On your uberspace, create a folder, enter it and initialize a bare git repository.
::

 [isabell@stardust ~]$ mkdir ~/website
 [isabell@stardust website]$ cd ~/website
 [isabell@stardust website]$ git init --bare
 Initialized empty Git repository in /home/isabell/website/
 [isabell@stardust website]$

Since we just need an empty repository to upload our website to, we need to add an option for initializing a repository:

  * ``--bare``: Creates an empty repository for sharing.

Clone that repository on your local machine, enter the parent folder and create a new website by typing:
::

 [user@localhost ~]$ jekyll new website
 [user@localhost ~]$

.. note:: By entering the parent folder and using the same name for your website as the cloned repository you can create the website directly insite the repository folder. If you give your website a different name, you have to copy your website into your repository.

After Jekyll created the website you can enter it and run the local webserver for testing:
::

 [user@localhost ~]$ cd website
 [user@localhost website]$ bundle exec jekyll serve
 [...]
 Server address: http://127.0.0.1:4000/
 Server running... press ctrl-c to stop.

 [user@localhost website]$

Now open a browser and navigate to http://127.0.0.1:4000 to see your website on your local machine.

The next thing we we want to do is creating a post-update rule in git to deploy our website automatically when pushing from our local machine to our remote repository.

Therefor we have to enter our remote repository and create a post-update hook file ``~/website/hooks/post-update`` with the following content:

.. code-block:: bash

  GIT_REPO=$HOME/website
  TMP_GIT_CLONE=$(mktemp -d)
  GEMFILE=$TMP_GIT_CLONE/Gemfile
  PUBLIC_WWW=/var/www/virtual/$USER/html

  git clone $GIT_REPO $TMP_GIT_CLONE
  BUNDLE_GEMFILE=$GEMFILE bundle install --path vendor/bundle
  BUNDLE_GEMFILE=$GEMFILE bundle exec jekyll build --source $TMP_GIT_CLONE --destination $PUBLIC_WWW
  rm -Rf $TMP_GIT_CLONE

.. note:: If needed, ``PUBLIC_WWW`` can be adapted to serve on a different domain.

We need to tell Jekyll where to find the source files of the website and where to deploy. So we have to add a configuration for the build process:

  * ``--source``: Tells Jekyll where to find the source of the website (here ``$TMP_GIT_CLONE``).
  * ``--destination``: Tells Jekyll where to build the website (here ``$PUBLIC_WWW``).

All we have to do now is to commit and push from our local to our remote repository. The remote git will now clone the website on your uberspace, build it with Jekyll and deploy the website in your document root. After deploying, the cloned repository will be deleted, because it is not needed anymore.

Tuning
======

For further information about creating pages, posts or using themes, go to https://jekyllrb.com/docs/


Updates
=======

Since Jekyll is a ruby gem, you can update Jekyll and every gem needed by your website by entering your website folder and typing:
::

 [isabell@stardust ~]$ cd website
 [isabell@stardust website]$ bundle update
 [...]
 Bundle updated!
 [isabell@stardust website]$

.. _Jekyll: https://jekyllrb.com/
.. _RubyInstaller: https://rubyinstaller.org/downloads/
.. _RVM: https://rvm.io/rvm/install
.. _git: https://git-scm.com/

----

Tested with Ruby 2.5.3, Jekyll 3.8.5, Uberspace 7.2.2

.. authors::
