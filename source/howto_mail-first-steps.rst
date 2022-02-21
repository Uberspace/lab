.. _firstday-mail:

###########################
Eine E-Mail-Adresse einrichten
###########################

Ziel:
=====

Du hast:
- eine eigene Domain my-mail-domain.com
- einen Account isabell auf dem Server stardust

Du willst:
- ein Postfach post@my-mail-domain.com
- einen Alias inbox@my-mail-domain.com
- Mails über das Webinterface abrufen

Verbinden über SSH
------------------

`macOS <https://support.apple.com/en-gb/guide/terminal/welcome/mac>`_
`Windows <https://docs.microsoft.com/en-us/windows-server/administration/openssh/openssh_install_firstuse>`_

:ref:`ssh-using-linux`

.. image:: _static/images/firstday_ssh.png
  :alt: Alternative text

Domain eintragen
----------------

:ref:`mail-domains`

``uberspace mail domain add my-mail-domain.com``


.. image:: _static/images/firstday_mail_domain_add.png
  :alt: Alternative text


DNS-Records eintragen
---------------------

.. image:: _static/images/firstday_dns.png
  :alt: Alternative text


Postfach anlegen
----------------

 :ref:`new-mailbox`
.. image:: _static/images/firstday_mailbox.png
  :alt: Alternative text


Mails abrufen
-------------

:ref:`mail-access`
