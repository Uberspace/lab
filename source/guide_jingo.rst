.. author:: ezra <ezra@posteo.de>

.. tag:: lang-nodejs
.. tag:: web
.. tag:: wiki

.. highlight:: console

#####
Jingo
#####

.. tag_list::

Jingo_ is a simple Wiki software that is based on :manual:`Node.js <lang-nodejs>` and Git. The content is stored in markdown files which are managed by a Git repository. In contrast to other Wiki software (like Mediawiki or Dokuwiki), Jingo does not provide too much functions and uses a very decent design. But because the management and versioning of the content is based on Git, it can be used in multiple ways.

At this time, Jingo is no longer actively developed but still supported for security issues.

----

.. note:: For this guide you should be familiar with the basic concepts of

  * :manual:`Node.js <lang-nodejs>` and its package manager :manual_anchor:`npm <lang-nodejs.html#npm>`
  * :manual:`supervisord <daemons-supervisord>`
  * :manual:`domains <web-domains>`

Prerequisites
=============

We're using :manual:`Node.js <lang-nodejs>` in the stable version 8:

::

 [isabell@stardust ~]$ uberspace tools version show node
 Using 'Node.js' version: '8'
 [isabell@stardust ~]$

Your blog URL needs to be setup:

.. include:: includes/web-domain-list.rst

Installation
============

First get the Jingo code from Github_:

.. code-block:: console

  [isabell@stardust ~]$ git clone https://github.com/claudioc/jingo ~/jingo
  Cloning into '/home/isabell/jingo'...
  remote: Counting objects: 2684, done.
  remote: Total 2684 (delta 0), reused 0 (delta 0), pack-reused 2684
  Receiving objects: 100% (2684/2684), 1.88 MiB | 3.19 MiB/s, done.
  Resolving deltas: 100% (1356/1356), done.
  [isabell@stardust ~]$


Then you need to install the dependencies using the node packet manager:

.. code-block:: console

  [isabell@stardust ~]$ cd ~/jingo
  [isabell@stardust jingo]$ npm install
  [...]
  added 626 packages in 17.17s
  [isabell@stardust jingo]$


Configuration
=============

Data storage
------------

Jingo uses a Git repository to manage its data, you just need to create an empty folder and initialize Git within it:

.. code-block:: console

  [isabell@stardust ~]$ mkdir ~/jingo_data
  [isabell@stardust ~]$ cd ~/jingo_data
  [isabell@stardust jingo_data]$ git init
  Initialized empty Git repository in /home/isabell/jingo_data/.git/
  [isabell@stardust jingo_data]$

You then have to configure the Git repository with name and email, if you haven't done it already globally:

.. code-block:: console

  [isabell@stardust ~]$ cd ~/jingo_data
  [isabell@stardust jingo_data]$ git config user.name "$USER"
  [isabell@stardust jingo_data]$ git config user.email "$USER@uber.space"
  [isabell@stardust jingo_data]$

.. note:: You can of course set arbitrary informations here. If you want to share your data using Github for example, you might want to set the appropriate data.

Change the configuration
------------------------

You first need to create a default config file using the ``jingo`` command:

.. code-block:: console

  [isabell@stardust ~]$ ~/jingo/jingo -s > ~/jingo/config.yaml
  [isabell@stardust ~]$

Then you can adjust this file ``~/jingo/config.yaml`` with your settings. First of all, set repository folder. Be sure to replace ``<username>`` with your actual username:

.. code-block:: yaml
  :emphasize-lines: 6

  # Configuration sample file for Jingo (YAML)
  application:
    title: Jingo
    logo: ''
    favicon: ''
    repository: '/home/<username>/jingo_data'
    docSubdir: ''
  [...]

You will also need to set up an account to login. You can choose multiple ways for authentication like *Github*, *Google*, *Ldap*.
For the initial config here, the most simple way is to set up a local account that is stored in the config file. You first need to choose a password and create a hash:

.. code-block:: console

  [isabell@stardust ~]$ ~/jingo/jingo --hash-string MySuperSecretPassword
  7dfd2a21e27be76896430ee382e268b362d812d7
  [isabell@stardust ~]$

Save the returned hash (here ``7dfd2a21e27be76896430ee382e268b362d812d7``) together with your account name within the config file ``~/jingo/config.yaml`` and be sure to set ``enabled`` to ``true``:

.. code-block:: yaml
  :emphasize-lines: 6,8,9,10

  # Configuration sample file for Jingo (YAML)
  [...]
  authentication:
    [...]
    local:
      enabled: true
      accounts:
        - username: 'isabell'
          passwordHash: '7dfd2a21e27be76896430ee382e268b362d812d7'
          email: 'jingo@isabell.uber.space'

.. warning:: Of course you have to change the string ``MySuperSecretPassword`` to your personal password and use the corresponding hash!

Configure web server
--------------------

.. note::

    Jingo is running on port 6067.

.. include:: includes/web-backend.rst

Setup daemon
------------

Create ``~/etc/services.d/jingo.ini`` with the following content:

.. code-block:: ini

  [program:jingo]
  command=%(ENV_HOME)s/jingo/jingo -c %(ENV_HOME)s/jingo/config.yaml

.. include:: includes/supervisord.rst

If it's not in state RUNNING, check your configuration.

Best practices
==============

Personalization
---------------

You can edit the ``~/config.yaml`` to adjust the settings to your needs. You can for example choose different authentication modes or set Git to automatically push to a remote repository.

Security
--------

Be sure to set any random signs for the option ``secret`` within the ``config.yaml`` file.

Updates
=======

.. note:: Check the update feed_ regularly to stay informed about the newest version.


If there is a new version available, you can get the code using Git:

.. code-block:: console

  [isabell@stardust ~]$ cd ~/jingo
  [isabell@stardust jingo]$ git pull origin master
  From git://github.com/claudioc/jingo
  * branch              master -> FETCH_HEAD
  Updating e84c6452..1e35e8fc
  Fast-forward
  [...]
  32 files changed, 2033 insertions(+), 212 deletions(-)
  [...]
  [isabell@stardust jingo]$

Then again install the dependencies:

.. code-block:: console

  [isabell@stardust ~]$ cd ~/jingo
  [isabell@stardust jingo]$ npm install
  [...]
  added 116 packages in 5.607s
  [isabell@stardust jingo]$

In the end you need to restart the service daemon, so the new code is used by the webserver:

.. code-block:: console

  [isabell@stardust ~]$ supervisorctl restart jingo
  jingo: stopped
  jingo: started
  [isabell@stardust ~]$



.. _Jingo: https://github.com/claudioc/jingo
.. _Github: https://github.com/claudioc/jingo
.. _feed: https://github.com/claudioc/jingo/releases.atom

----

Tested with Jingo 1.8.5, Uberspace 7.1.1

.. author_list::
