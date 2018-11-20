.. author:: Pascal Iske <info@pascal-iske.de>
.. highlight:: console

.. sidebar:: Logo

  .. image:: _static/images/composer-satis.png
      :align: center

##############
Composer Satis
##############

To manage private composer packages you can either use a private packagist account or host it for free by yourself with composer satis.
The latter is as easy as cloning the official composer satis repository and editing the config file.
Satis will then build a static html site with your packages.
This guide shows you how to quickly setup satis on your Uberspace account.

----

.. note:: For this guide you should be familiar with the basic concepts of

  * cronjobs_
  * composer_

Installation
============

Clone the satis repository
--------------------------

Use ``composer`` to create a new satis project locally:

::

  [isabell@stardust ~] composer create-project composer/satis --stability=dev --keep-vcs

Configuration
=============

Configure satis
---------------

Create a json config file (e.g. ``/home/$USER/satis/satis.json``) with your private composer packages inside:

::

  {
    "name": "My Satis Repository",
    "homepage": "http://isabell.uber.space",
    "require-all": true,
    "repositories": [
      { "type": "vcs", "url": "https://github.com/mycompany/privaterepo" },
      { "type": "vcs", "url": "https://github.com/mycompany/privaterepo2" }
    ]
  }

Create a script for building
----------------------------

Create a shell script (e.g. ``/home/$USER/bin/satisupdate``) that keeps the call for the build step:

::

  #!/bin/bash

  # change into satis folder
  cd /home/$USER/satis/

  # update satis
  php bin/satis build satis.json "/home/$USER/html/" --no-interaction --quiet

Build static site
=================

Now you can build the static packages site with the following command:

::

  [isabell@stardust ~] satisupdate

This will build the static site inside your Uberspace document root (``/home/$USER/html``).

Optional tips
=============

Automate the building with a cron job
-------------------------------------

To automate the building of the static site you can add a cron job, e.g.:

::

  */5 * * * * /home/$USER/bin/satisupdate

You can learn more about cronjobs in the `uberspace manual cron <https://manual.uberspace.de/en/daemons-cron.html>`_.

Add your custom domain
----------------------

If you want to use a custom domain you can add it to your uberspace by following the steps of the `uberspace manual domains <https://manual.uberspace.de/en/web-domains.html>`_.

After that you can add your domain to the third line of the satis config file containing the word homepage.

Updates
=======

To update the satis tool you just have to pull the latest changes and run composer install:

::

  [isabell@stardust ~] cd /home/$USER/satis/
  [isabell@stardust satis] git pull
  [isabell@stardust satis] composer install

----

Tested with Satis 1.0.0, Uberspace 7.1.14.0

.. _composer: https://getcomposer.org
.. _cronjobs: https://manual.uberspace.de/en/daemons-cron.html
