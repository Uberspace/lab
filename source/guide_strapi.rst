.. author:: Richard Henkenjohann <richardhenkenjohann@googlemail.com>

.. tag:: lang-nodejs
.. tag:: web
.. tag:: backend
.. tag:: api

.. highlight:: console

.. sidebar:: Logo

  .. image:: _static/images/strapi.svg
      :align: center

#####
Strapi
#####

.. tag_list::

Strapi_ is a open source headless CMS to build APIs. It’s 100% Javascript, fully customizable and developer-first.

----

.. note:: For this guide you should be familiar with the basic concepts of

  * :manual:`Node.js <lang-nodejs>` and its package manager :manual_anchor:`npm <lang-nodejs.html#npm>`
  * :manual:`MySQL <database-mysql>`
  * :manual:`supervisord <daemons-supervisord>`
  * :manual:`domains <web-domains>`

Prerequisites
=============

We're using :manual:`Node.js <lang-nodejs>` in the stable version 10:

::

 [isabell@stardust ~]$ uberspace tools version use node 10
 Using 'Node.js' version: '10'
 Selected node version 10
 The new configuration is adapted immediately. Patch updates will be applied automatically.
 [eliza@dolittle ~]$

.. include:: includes/my-print-defaults.rst

Your blog URL needs to be setup:

.. include:: includes/web-domain-list.rst

Installation
============

Start with a local project
--------------------------

When Strapi is in production mode (which should be targeted on Uberspace), the Content Type Creator is disabled. This requires us to build the project locally to be able to make changes on the API and deploy it for production on Uberspace.

We will start with creating a new Strapi project. Use yarn to install the Strapi project (locally).

.. code-block:: console

 [local@My-Computer ~]$ yarn create strapi-app my-project --quickstart


.. note::

    When you use --quickstart to create a Strapi project locally, a SQLite database is used. We will later configure a MySQL database that is used in production mode on Uberspace.


Init a Git repository
---------------------

We will initialize a Git repository and commit our initial project files.


.. code-block:: console

 cd my-project
 git init
 git add .
 git commit -m "Initial Commit"

Push your changes to a remote repository, like GitHub. We will later clone this repository.

.. code-block:: console

 git branch -M main
 git remote add origin git@github.com:me/my-project.git
 git push -u origin main

Preparing the MySQL connection
------------------------------

Install the mysql client so that Stripe can use a MySQL connection.


.. code-block:: console

 [local@My-Computer ~]$ yarn intall sails-mysql


Create a new ``database.js`` for the production environment. This will be used whenever ``NODE_ENV=production`` (which is the case for Uberspace in our setup).


.. code-block:: console

 [local@My-Computer ~]$ mkdir -p config/env/production
 [local@My-Computer ~]$ touch config/env/production/database.js


Put the following content into the ``database.js``:

.. code-block:: js

  module.exports = ({env}) => ({
    defaultConnection: 'default',
    connections: {
      default: {
        connector: 'bookshelf',
        settings: {
          client: "mysql",
          host: env('DATABASE_HOST', 'localhost'),
          port: env('DATABASE_PORT', 3306),
          database: env('DATABASE_NAME', 'default'),
          username: env('DATABASE_USERNAME', 'root'),
          password: env('DATABASE_PASSWORD', ''),
        },
        options: {
          useNullAsDefault: true,
        },
      },
    },
  });

Commit and push your changes again:

.. code-block:: console

 [local@My-Computer ~]$ git add .
 [local@My-Computer ~]$ git commit -m "Update database config"
 [local@My-Computer ~]$ git push origin main


Deploy local project on Uberspace
---------------------------------

You can chooose to checkout the Git repostiory on Uberspace or to copy the files manually or via rsync.

Using Git (recommended)
***********************

This is actually the first time, we will connect to our Uberspace. So connect to your Uberspace:

.. code-block:: console

 [local@My-Computer ~]$ ssh isabell@stardust.uberspace.de

In order to clone the Git repository, your Uberspace needs to have a SSH key.

Check for an existing SSH key:


.. code-block:: console

 [isabell@stardust ~]$ cat ~/.ssh/id_rsa.pub


If it shows an SSH key, copy it. If it shows an error, create a new SSH key:


.. code-block:: console

 [isabell@stardust ~]$ ssh-keygen -t rsa -b 4096


Finish the process of SSH key generation (just hit enter multiple times), then copy your SSH key (using the beforementioned command).

Place this SSH key as deploy key in the GitHub or GitLab repository.

Once the deploy key is added to the remote repository, you should be able to clone the repository:


.. code-block:: console

 [isabell@stardust ~]$ git@github.com:me/my-project.git strapi

This will clone the project inside the ``strapi`` directory in the home folder.

Using rsync (alternative)
*************************

We can also use ``rsync`` to copy the project files to Uberspace because it is convenient (the Uberspace does not require read access on the Git repository).

Run the following command from your local machine:

.. code-block:: console

 [local@My-Computer ~]$ rsync -a --exclude="/.*" --exclude="node_modules" my-project/ isabell@stardust.uberspace.de:strapi

Configure Strapi
----------------

The Strapi project files are now present on the Uberspace, so we can start configuring the project.

Install all dependencies with the following command:

.. code-block:: console

 [isabell@stardust strapi]$ yarn install

Create a new ``.env`` file inside the Strapi project folder:

.. code-block:: console

 [isabell@stardust strapi]$ touch .env

Put the following content inside the ``.env`` file (use the database credentials you retrieved from the step in the very beginning):

.. code-block:: env

 DATABASE_NAME=isabell
 DATABASE_USERNAME=isabell
 DATABASE_PASSWORD=MySuperSecretPassword


Configure web server
--------------------

.. note::

    Use port 1337.

.. include:: includes/web-backend.rst


Setup daemon
------------


Create ``~/etc/services.d/strapi.ini`` with the following content:

.. code-block:: ini

 [program:strapi]
 directory=%(ENV_HOME)s/strapi
 command=env NODE_ENV=production yarn run start
 startsecs=60

.. include:: includes/supervisord.rst

If it's not in state RUNNING, check your configuration.

Finished!
---------

Strapi should now be accessible via ``https://isabell.uber.space/admin``. Strapi is in production mode, meaning that the Content Type creator is disabled. To make changes on the API, you have to re-deploy the project.

Continuous Delivery
-------------------

Automatic deployment (e.g. Push-to-Deploy) can be achieved with GitHub actions, GitLab CI or similiar services. An exemplary GitHub workflow can look like this:

.. code-block:: yaml

  name: Deploy

  on:
    push:
      branches: [ main ]

  jobs:
    deploy:
      runs-on: ubuntu-latest
      steps:
        - name: Checkout and build
          uses: appleboy/ssh-action@master
          env:
            SSH_USER: ${{ secrets.SSH_USER }}
            GITHUB_SHA: ${{ GITHUB.SHA }}
            NODE_ENV: 'production'
          with:
            host: "${{ secrets.SSH_HOST }}"
            username: "${{ secrets.SSH_USER }}"
            key: "${{ secrets.SSH_PRIVATE_KEY }}"
            envs: SSH_USER,GITHUB_SHA,NODE_ENV
            script: |
              cd /home/$SSH_USER/strapi
              git fetch --all
              git checkout --force "${GITHUB_SHA}"
              yarn install
              supervisorctl restart strapi


.. _Strapi: https://strapi.io

----

Tested with Strapi 3 on Uberspace 7

.. author_list::
