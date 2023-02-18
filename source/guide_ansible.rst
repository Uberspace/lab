.. author:: Friesenkiwi <friesenkiwi@denk-nach-mcfly.de>

.. tag:: Ansible

.. highlight:: console

.. sidebar:: Logo

  .. image:: _static/images/ansible.svg
      :align: center

#######
Ansible
#######

.. tag_list::

Ansible is a provisioning, configuration and orchestration tool maintained by Red Hat, written in Python that works over SSH. It doesn't need any installation on the controlled machine, so it works right out of the box with any uberspace. It used by the Uberspace team itself extensively for the administration of the servers hosting the uberspaces. However, many publicly available role e.g. from the Galaxy assume a "usual" server administration with sudo priviledges and distribution package  installation.

Some ansible roles have been developed specifically to be compatible with a uberspace and interface with the unique features it provides.

* by user snapstromegon: https://github.com/Snapstromegon/ansible-roles-uberspace
  * uberspace_web_backend
  * uberspace_web_domain
  * uberspace_mail_domain
  * uberspace_mail_user
  * uberspace_mail_catchall
  * uberspace_mail_forward
  * uberspace_mail_spamfilter
  * uberspace_tools_version
* by user friesenkiwi: https://github.com/friesenkiwi/ansible-collection-uberspace - a collection, that contains roles for
  * account management - registering, deleting, authorization, accounting, gathering facts, configuring, tools, ports, web backends, web headers, domains (even including INWX DNS)
  * babybuddy <guide_babybuddy>
  * coturn <guide_coturn>
  * pleroma <guide_pleroma>
  * prosody <guide_prosody>
  * more to come
