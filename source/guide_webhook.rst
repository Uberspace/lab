.. highlight:: console

.. author:: Bastian Greshake Tzovaras <bgreshake@googlemail.com>

.. tag:: lang-go
.. tag:: web
.. tag:: automation
.. tag:: continuous-integration

.. sidebar:: Logo

  .. image:: _static/images/webhook.png
      :align: center

#######
webhook
#######

.. tag_list::

`webhook`_  is a small, configurable tool that allows creating HTTP endpoints (hooks) on in your uberspace. When triggered, these webhooks can then be used to execute different commands. You can also pass data from the HTTP request (headers, payload or query variables) to your commands. Furthermore, you can also set up specific rules that need to be met before a hook will trigger. Overall, this can enable your uberspace to integrate with a wide set of external services, for example for triggering deploys as part of a continuous integration/deployment pipeline. Webhook is written in :manual:`Go <lang-golang>`.

----

.. note:: For this guide you should be familiar with the basic concepts of

  * :manual:`Go <lang-golang>`
  * :manual:`web backends <web-backends>`
  * :manual:`supervisord <daemons-supervisord>`
  * :manual:`domains <web-domains>` (optional, if you want to setup a domain/subdomain)

License
=======

All relevant legal information can be found here

  * https://github.com/adnanh/webhook/blob/master/LICENSE

Prerequisites
=============

Your URL needs to be setup:

.. include:: includes/web-domain-list.rst


Installation
============

Download
--------
The easiest way to setup webhook is to build it from the project's Git repository. Clone from GitHub and change into the folder:

::

 [isabell@stardust ~]$ git clone https://github.com/adnanh/webhook.git
 [isabell@stardust ~]$ cd webhook


Install dependencies and build
------------------------------

Now install the required Go dependencies and build webhook using the following commands

::

 [isabell@stardust webhook]$ go mod tidy
 [isabell@stardust webhook]$ go build

Following this you will have a compiled version of webhook ready to go in :code:`~/webhook/webhook`

Writing a first webhook
=======================

Webhook can be configured using both YAML and JSON files. It also offers a wide range of options that you can find in the `webhook documentation <https://github.com/adnanh/webhook/tree/master/docs>`_. To get started, we create a simple demo webhook using a YAML file.

Using a text editor of your choice create the file :code:`~/webhook/hooks.yaml` and enter the following to get started:

.. code-block::

  - id: test-hook
    execute-command: /home/isabell/hook-triggered.sh
    command-working-directory: /home/isabell
    response-message: the test-hook was triggered!


The :code:`id` will be the endpoint at which the webhook will be listening, while :code:`execute-command` specifies which command will be run when the hook is triggered, for testing this can just be a simple print-statement, e.g. you could have your :code:`hook-triggered.sh` be as simple as the below to get started.

Using a text editor of your choice, create the file :code:`~/hook-triggered.sh` and enter the following to get started:

.. code-block::

  #!/bin/env bash
  echo "This command was triggered by the webhook"

After saving it, make it executable using :code:`chmod 755 ~/hook-triggered.sh`

Configuration
=============

With webhook installed and a first hook written, we now need to setup a service for `webhook` to run automatically.

Creating a service
------------------

We can create a file ``~/etc/services.d/webhook.ini`` with the following content (adapt the values to your own directories if you have adapted them!):

.. code-block:: ini

    [program:webhook]
    directory=%(ENV_HOME)s/webhook
    command=/home/isabell/webhook/webhook -hooks hooks.yaml -logfile %(ENV_HOME)s/logs/webhook.log -hotreload
    startsecs=15

The :code:`-hotreload` parameter will automatically reload your hook-definitions whenever you edit them. This config will also write a logfile with the outputs in :code:`~/logs/webhook.log`.

.. include:: includes/supervisord.rst

Optional: Adding a (sub)domain
------------------------------

If you want to use a custom domain or a sub-domain, set it up now, e.g. using

::

 [isabell@stardust ~]$ uberspace web domain add webhook.isabell.uber.space


Configuring the Web Backend
---------------------------

.. include:: includes/web-backend.rst

By default, webhook listens on port 9000, if you have setup a sub-domain, the command to start the backend could look like this:

::

 [isabell@stardust ~]$ uberspace web backend set webhook.isabell.uber.space --http --port 9000


Testing your first webhook
==========================

By now, webhook is running and waiting to be triggered. In this example, your test-hook would be listening at :code:`https://webhook.isabell.uber.space/hooks/test-hook`. You can try using curl from your host machine (or your uber space):

::

 [your@host ~]$ curl https://webhook.isabell.uber.space/hooks/test-hook


On your uberspace you should then see the following in your :code:`~/logs/webhook.log`:

::

  [isabell@stardust ~]$ cat ~/logs/webhook.log
  [webhook] 2024/09/06 18:26:31 [1e48aa] incoming HTTP GET request from [ip]:xxxx
  [webhook] 2024/09/06 18:26:31 [1e48aa] test-hook got matched
  [webhook] 2024/09/06 18:36:50 [9fbc68] test-hook hook triggered successfully
  [webhook] 2024/09/06 18:36:50 [9fbc68] 200 | 18 B | 312.198µs | webhook.isabell.uber.space | GET /hooks/test-hook
  [webhook] 2024/09/06 18:36:50 [9fbc68] executing /home/isabell/hook-triggered.sh (/home/isabell/hook-triggered.sh) with arguments ["/home/isabell/hook-triggered.sh"] and environment [] using /home/isabell as cwd
  [webhook] 2024/09/06 18:37:09 [9fbc68] command output: This command was triggered by the hook
  [webhook] 2024/09/06 18:37:09 [9fbc68] finished handling test-hook

Congratulations, you now ran your first webhook on your uberspace!

Securing your webhook
=====================

The example above allows anyone with knowledge of your webhook URL to trigger the specified action on your uberspace. To avoid this and make your webhook more secure, you should require the additional sending of secret information.

For example, you can require a secret token to be sent over as part of the trigger for the webhook, like this:

.. code-block::

  - id: test-hook
    execute-command: /home/isabell/hook-triggered.sh
    command-working-directory: /home/isabell
    response-message: the test-hook was triggered!
    trigger-rule:
      and:
        - match:
          type: value
          value: <secretkey>
          parameter:
            source: payload
            name: secret_hook_token


.. warning:: Replace ``<secretkey>`` with a random sequence of characters! You can create one for your own hook by running :code:`pwgen 32 1`.

With this configuration, you will have to send over a JSON payload to your :code:`test-hook` that contains :code:`secret_hook_token` as value and the right :code:`<secretkey>` as value. Using curl you can run it like this:

::

  [your@host ~]$ curl -X POST https://webhook.isabell.uber.space/hooks/deploy-api \
    -H "Content-Type: application/json" \
    -d '{"secret_hook_token": "<secretkey>"}'

If you provide the correct secret, the hook will normally, as seen in the logs:

::

  [isabell@stardust ~]$ cat ~/logs/webhook.log
  [webhook] 2024/09/06 18:36:50 [9fbc68] incoming HTTP POST request from [IP]:xxxx
  [webhook] 2024/09/06 18:36:50 [9fbc68] test-hook got matched
  [webhook] 2024/09/06 18:36:50 [9fbc68] test-hook hook triggered successfully

Otherwise, you will see an error message in the logs:

::

  [isabell@stardust ~]$ cat ~/logs/webhook.log
  [webhook] 2024/09/06 18:36:14 [7f70d8] incoming HTTP POST request from [IP]:xxxx
  [webhook] 2024/09/06 18:36:14 [7f70d8] test-hook got matched
  [webhook] 2024/09/06 18:36:14 [7f70d8] test-hook got matched, but didn't get triggered because the trigger rules were not satisfied


You can check out the `webhook "hook-rules" documentation <https://github.com/adnanh/webhook/blob/master/docs/Hook-Rules.md>`_ for more details on how to secure your webhooks.

.. _`webhook`: https://github.com/adnanh/webhook/

----

Tested with go1.23.0 linux/amd64, Uberspace 7.15

.. author_list::
