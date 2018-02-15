#####
Ghost
#####

Install ``ghost-cli``
=====================

Use ``npm`` to install ``ghost-cli``

.. code-block:: bash

 [isabell@philae ~]$ npm i -g ghost-cli

Install Ghost
=============

Create a ``ghost`` directory in your home, ``cd`` to it and then run the installer. Enter your URL and your MySQL username, password, and database name. You can find these in your ``~/.my.cnf``. Do not start Ghost yet.

.. code-block:: bash

 [isabell@philae ~]$ mkdir ~/ghost && cd ~/ghost
 [isabell@philae ~]$ ghost install --no-stack --no-setup-linux-user --no-setup-systemd --no-setup-nginx --no-setup-mysql
 ✔ Checking system Node.js version
 ✔ Checking current folder permissions
 ℹ Checking operating system compatibility [skipped]
 ✔ Checking for a MySQL installation
 ✔ Checking for latest Ghost version
 ✔ Setting up install directory
 ✔ Downloading and installing Ghost v1.21.2
 ✔ Finishing install process
 ? Enter your blog URL: https://isabell.uber.space
 ? Enter your MySQL hostname: localhost
 ? Enter your MySQL username: isabell
 ? Enter your MySQL password: [hidden]
 ? Enter your Ghost database name: isabell_ghost
 ✔ Configuring Ghost
 ✔ Setting up instance
 ℹ Setting up "ghost" mysql user [skipped]
 ℹ Setting up Nginx [skipped]
 Task ssl depends on the 'nginx' stage, which was skipped.
 ℹ Setting up SSL [skipped]
 ℹ Setting up Systemd [skipped]
 ✔ Running database migrations
 ? Do you want to start Ghost? No

Change Ghost port
=================

Find a free port and write it to the ``$GHOSTPORT`` variable:

.. code-block:: bash

 [isabell@philae ~]$ GHOSTPORT=$(( $RANDOM % 4535 + 61000)); netstat -tulpen | grep $GHOSTPORT && echo "try again" || echo $GHOSTPORT
 62841

If successful, this will output your Ghost port. If not, try again.

Set the new port in the config file:

.. code-block:: bash

 [isabell@philae ~]$ sed -i "s/2369,/${GHOSTPORT},/" ~/ghost/config.production.json

Set up ``supervisord``
======================

Create ``~/etc/services.d/ghost.ini``:

.. code-block:: bash

 [isabell@philae ~]$ cat > ${HOME}/etc/services.d/ghost.ini <<__EOF__
 [program:ghost]
 directory=${HOME}/ghost
 command=env NODE_ENV=production /bin/node current/index.js
 __EOF__

.. note:: The above is one multi-line command.

Let ``supervisord`` re-read its configuration and start the Ghost service:

.. code-block:: bash

 [isabell@philae ~]$ supervisorctl reread
 ghost: available
 [isabell@philae ~]$ supervisorctl update
 ghost: added process group

Now check the log file to be sure that Ghost is running:

.. code-block:: bash

 [isabell@philae ~]$ supervisorctl tail ghost
 [2018-02-09 11:37:44] WARN Theme's file locales/en.json not found.
 [2018-02-09 11:37:45] INFO Ghost is running in production...
 [2018-02-09 11:37:45] INFO Your blog is now available on https://isabell.uber.space/
 [2018-02-09 11:37:45] INFO Ctrl+C to shut down
 [2018-02-09 11:37:45] INFO Ghost boot 1.556s

Create an ``.htaccess`` file to connect Ghost to the Apache web server:

.. code-block:: bash

 [isabell@philae ~]$ cat > /var/www/virtual/${USER}/html/.htaccess <<__EOF__
 DirectoryIndex disabled
 
 RewriteEngine On
 RewriteRule ^(.*) http://localhost:${GHOSTPORT}/\$1 [P]
 __EOF__

Create a user account
=====================

Point your browser to ``https://<user>.uber.space/ghost`` and create a user account in Ghost.

Updating
========

Check Ghost's `releases <https://github.com/TryGhost/Ghost/releases>`_ for a new version and copy the link to the ``.zip`` archive. Replace the version number in the following snippet with the newest version:

.. code-block:: bash

 [isabell@philae ~]$ cd ~/ghost/versions/
 [isabell@philae versions]$ wget https://github.com/TryGhost/Ghost/releases/download/1.21.2/Ghost-1.21.2.zip
 [isabell@philae versions]$ unzip Ghost-1.21.2.zip -d 1.21.2

Install the required ``node`` modules:

.. code-block:: bash

 [isabell@philae ~]$ cd ~/ghost/versions/1.21.2/content
 [isabell@philae content]$ npm install --production

Replace the ``current`` symlink and link to the newest version. Again, replace the version number with the newest version.

.. code-block:: bash

 [isabell@philae ~]$ rm ~/ghost/current
 [isabell@philae ~]$ ln -s $HOME/ghost/versions/1.21.2 $HOME/ghost/current
 [isabell@philae ~]$ supervisorctl restart ghost

