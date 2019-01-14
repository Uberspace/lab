.. highlight:: console

.. author:: Christian Kantelberg <uberlab@mailbox.org>

.. sidebar:: Logo

  .. image:: _static/images/hugo-logo.png
      :align: center

##########
Hugo
##########

Hugo is a fast and modern static site generator written in Go, and designed to make website creation fun again.

----

.. note:: For this guide you should be familiar with the basic concepts of

  * Git_
  * Domains_
  * supervisord_

License
=======

Hugo v0.15 and later are released under the Apache 2.0 license. 
Earlier versions of Hugo were released under the Simple Public License.

All relevant legal information can be found here 

  * https://opensource.org/licenses/Simple-2.0

Prerequisites
=============

Your URL needs to be setup:

::

 [isabell@stardust ~]$ uberspace web domain list
 isabell.uber.space
 [isabell@stardust ~]$

Installation
============

Step 1
------

Preparing to set up on the Uberspace various directories for further action.

::
 
 [isabell@stardust ~]$ mkdir apps
 [isabell@stardust ~]$ mkdir apps/hugo_render
 [isabell@stardust ~]$ mkdir hugo_website
 [isabell@stardust ~]$ 
 
Step 2
------

To run Hugo from any directory, add the path to Hugo in PATH. To do this, open bashrc with an editor of your choice (e.g. vim, nano) and add the following line at the end:

::

 [isabell@stardust ~]$ nano ~/.bashrc
 [isabell@stardust ~]$ export PATH=$HOME/apps/hugo_render/hugo:$PATH
 [isabell@stardust ~]$

Then restart bashrc with source ``~/.bashrc`` to apply the change.

Step 3
------

Now change the directory ``~/apps/hugo_render`` and set up Hugo.

::

 [isabell@stardust ~]$ cd apps/hugo_render
 [isabell@stardust hugo_render]$ wget https://github.com/spf13/hugo/releases/download/hugo_42.23.1_Linux-64bit.tar.gz
 [isabell@stardust hugo_render]$ tar -xvzf hugo_42.23.1_Linux-64bit.tar.gz
 [isabell@stardust hugo_render]$ rm hugo_42.23.1_Linux-64bit.tar.gz
 [isabell@stardust hugo_render]$ cd ~
 [isabell@stardust ~]$ 
 
After setting up, test if Hugo works. The output is the version number of Hugo.

::

 [isabell@stardust ~]$ hugo version
 Hugo Static Site Generator v42.23.1-8FC339DC2529FF77E494A1C12CD1FF9FBCB880A4 linux/amd64 BuildDate: 2018-12-24T08:26:10Z
 [isabell@stardust ~]$ 
 
 
Step 4
------
 
After Hugo is now installed on the Uberspace, now put on the Hugo side. To do this, switch to the corresponding directory and create the Hugo page there.

::
 
 [isabell@stardust ~]$ cd ~/hugo_website
 [isabell@stardust hugo_website]$ hugo new site hugo_web
 [isabell@stardust ~]$ 
 
Step 5
------

Since Hugo is basically delivered without a theme, this must now be installed. To do so, look for a corresponding theme at https://themes.gohugo.io/ and install it in the folder of the same name in the newly created hugo_web page. This example uses the theme FutureImperfect_. Then copy the sample files into the hugo_web page.

::
 
 [isabell@stardust ~]$ cd hugo_website/hugo_web/themes
 [isabell@stardust themes]$ git clone https://github.com/jpescador/hugo-future-imperfect.git
 Cloning into 'hugo-future-imperfect'...
 [isabell@stardust ~]$ cp -R hugo-future-imperfect/exampleSite/* ../.
 [isabell@stardust ~]$ 

Configuration
=============

Configure port
--------------

Get a free port number:

.. include:: includes/generate-port.rst

Setup .htaccess
---------------

.. include:: includes/proxy-rewrite.rst

Setup daemon
------------

Finally, you should set up a service that keeps Hugo_ alive while you are gone. Therefor create the file ``~/etc/services.d/hugo.ini`` with the following content:

.. warning:: Replace ``<yourport>`` with the new portnumber you got and ``<yoururl>`` with the url of your uberspace!

.. code-block:: ini

 [program:hugo]
 environment =
  LISTEN_ADDR="127.0.0.1:<yourport>",
  BASE_URL="<yoururl>"
 
 directory=%(ENV_HOME)s/hugo_website/hugo_web
 command=%(ENV_HOME)s/apps/hugo_render/hugo server -p<yourport> --baseUrl=<yoururl> --bind=0.0.0.0 --appendPort=false --watch=true 2>&1
 autostart=yes
 autorestart=yes

In our example this would be:

.. code-block:: ini

 [program:hugo]
 environment =
  LISTEN_ADDR="127.0.0.1:9000",
  BASE_URL="https://isabell.uber.space"
 
 directory=%(ENV_HOME)s/hugo_website/hugo_web
 command=%(ENV_HOME)s/apps/hugo_render/hugo server -p9000 --baseUrl=https://isabell.uber.space --bind=0.0.0.0 --appendPort=false --watch=true 2>&1
 autostart=yes
 autorestart=yes

Tell supervisord_ to refresh its configuration and start the service:

.. code-block:: console

 [isabell@stardust ~]$ supervisorctl reread
 hugo: available
 [isabell@stardust ~]$ supervisorctl update
 hugo: added process group
 [isabell@stardust ~]$ supervisorctl status
 hugo                            RUNNING   pid 26024, uptime 0:00:18
 [isabell@stardust ~]$

If it's not in state RUNNING, check your configuration.

Finishing installation
======================

Now point your Browser to your installation URL ``https://isabell.uber.space``. 

Tuning
======

To finish configuring your Hugo website, creating pages and posts, go to https://gohugo.io/documentation .

Updates
=======

.. note:: Check the update feed_ regularly to stay informed about the newest version.


If there is a new version available, update your hugo file in ``apps/hugo_render`` (look at Step 3)



.. _Git: https://git-scm.com/book/en/v2/Getting-Started-Installing-Git/
.. _Hugo: https://gohugo.io/getting-started/installing/
.. _Domains: https://manual.uberspace.de/en/web-domains.html
.. _feed: https://github.com/gohugoio/hugo/releases.atom
.. _FutureImperfect: https://github.com/jpescador/hugo-future-imperfect
.. _supervisord: https://manual.uberspace.de/en/daemons-supervisord.html

----

Tested with Hugo 0.53, Uberspace 7.2.1.0

.. authors::
