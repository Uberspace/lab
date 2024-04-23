.. highlight:: console

.. author:: EV21 <uberlab@ev21.de>

.. tag:: lang-python

.. sidebar:: Logo

  .. image:: _static/images/jupyter.svg
      :align: center

################
Jupyter Notebook
################

.. tag_list::

`Jupyter Notebook`_ is a web-based interactive computational environment for creating Jupyter notebook documents. A Jupyter Notebook document is a JSON document, following a versioned schema, and containing an ordered list of input/output cells which can contain code, text (using Markdown), mathematics, plots and rich media, usually ending with the ".ipynb" extension.

----

.. note:: For this guide you should be familiar with the basic concepts of

  * :manual_anchor:`pip <lang-python.html#pip>`
  * :manual:`supervisord <daemons-supervisord>`
  * :manual:`web-backends <web-backends>`

License
=======

`Jupyter Notebook`_ is released under the `BSD 3-Clause "New" or "Revised" License`_. All relevant information can be found in the LICENSE_ file in the repository of the project.

Prerequisites
=============

Make sure :manual_anchor:`pip <lang-python.html#pip>` is up-to-date:

.. code-block:: console

 [isabell@stardust ~]$ pip3 install --user --upgrade pip
 Collecting pip
  Using cached https://files.pythonhosted.org/packages/43/84/23ed6a1796480a6f1a2d38f2802901d078266bda38388954d01d3f2e821d/pip-20.1.1-py2.py3-none-any.whl
 Installing collected packages: pip
 Successfully installed pip-20.1.1
 [isabell@stardust ~]$

.. note:: If you are using :manual_anchor:`pip <lang-python.html#pip>` with the default configured Python 2.7.5 you may get a syntax error while installing jupyter. This guide uses pip3 so you do not need to change it.

Installation
============

.. code-block:: console

 [isabell@stardust ~]$ pip3 install --user jupyter
 Downloading ...<- All the download operations will be displayed.
 Installing collected packages: tornado, six, python-dateutil, ipython-genutils, decorator, traitlets, jupyter-core, pyzmq, jupyter-client, backcall, ptyprocess, pexpect, parso, jedi, wcwidth, prompt-toolkit, pickleshare, pygments, ipython, ipykernel, qtpy, qtconsole, MarkupSafe, jinja2, zipp, importlib-metadata, attrs, pyrsistent, jsonschema, nbformat, Send2Trash, terminado, webencodings, pyparsing, packaging, bleach, mistune, entrypoints, testpath, defusedxml, pandocfilters, nbconvert, prometheus-client, notebook, widgetsnbextension, ipywidgets, jupyter-console, jupyter
  Running setup.py install for tornado ... done
  Running setup.py install for pyrsistent ... done
  Running setup.py install for pandocfilters ... done
 Successfully installed MarkupSafe-1.1.1 Send2Trash-1.5.0 attrs-19.3.0 backcall-0.2.0 bleach-3.1.5 decorator-4.4.2 defusedxml-0.6.0 entrypoints-0.3 importlib-metadata-1.7.0 ipykernel-5.3.1 ipython-7.16.1 ipython-genutils-0.2.0 ipywidgets-7.5.1 jedi-0.17.1 jinja2-2.11.2 jsonschema-3.2.0 jupyter-1.0.0 jupyter-client-6.1.5 jupyter-console-6.1.0 jupyter-core-4.6.3 mistune-0.8.4 nbconvert-5.6.1 nbformat-5.0.7 notebook-6.0.3 packaging-20.4 pandocfilters-1.4.2 parso-0.7.0 pexpect-4.8.0 pickleshare-0.7.5 prometheus-client-0.8.0 prompt-toolkit-3.0.5 ptyprocess-0.6.0 pygments-2.6.1 pyparsing-2.4.7 pyrsistent-0.16.0 python-dateutil-2.8.1 pyzmq-19.0.1 qtconsole-4.7.5 qtpy-1.9.0 six-1.15.0 terminado-0.8.3 testpath-0.4.4 tornado-6.0.4 traitlets-4.3.3 wcwidth-0.2.5 webencodings-0.5.1 widgetsnbextension-3.5.1 zipp-3.1.0
 [isabell@stardust ~]$

.. note:: With the following command you can start the jupyter server to test the basic installation without having a config file.
  ``jupyter notebook --no-browser --ip 0.0.0.0 --port 8888``
  Without having set a password the server would generate a token instead which you use as a parameter in the url.
  The token would then be displayed in the console output. You can also see if the selected port (in this case 8888) is available. Use another port for your configuration if this is the case. Terminate it with pressing ``Ctrl + c`` two times.

Configuration
=============

Let's generate a config file.

.. code-block:: console

 [isabell@stardust ~]$ jupyter notebook --generate-config
 Writing default config to: /home/isabell/.jupyter/jupyter_notebook_config.py
 [isabell@stardust ~]$

Modify the ``~/.jupyter/jupyter_notebook_config.py`` and add the following parameters.

.. code-block:: ini

 c.NotebookApp.allow_password_change = False
 c.NotebookApp.ip = '0.0.0.0'
 c.NotebookApp.open_browser = False
 c.ContentsManager.root_dir = '/home/isabell/'

.. note:: The parameter ``c.ContentsManager.root_dir`` sets the root of the Jupyter file manger. So you could browse your whole user directory with this setting.
  You may want to create a subfolder and then set the ``root_dir`` to ``/home/isabell/subfolder/``

Set a password for a secure web access.

.. code-block:: console
 :emphasize-lines: 2,3

 [isabell@stardust ~]$ jupyter notebook password
 Enter password:
 Verify password:
 [NotebookPasswordApp] Wrote hashed password to /home/isabell/.jupyter/jupyter_notebook_config.json
 [isabell@stardust ~]$

Setup daemon
------------

Create ``~/etc/services.d/jupyter.ini`` with the following content:

.. code-block:: ini

 [program:jupyter]
 command=jupyter notebook
 autostart=true
 autorestart=true

.. include:: includes/supervisord.rst

Setup web backend
-----------------

If you have your own :manual:`domain <web-domains>` you can set a domain specific web backend configuration.
This guide overrides the default setting, so the default html folder is not accessible.
Other options are described in the :manual:`web-backend manual <web-backends>`.

.. note:: *Jupyter* is running on port 8888 by default.
.. include:: includes/web-backend.rst

Let's check if it is working.

.. code-block:: console

 [isabell@stardust ~]$ uberspace web backend list
 / http:8888 => OK, listening: PID 29269, /usr/bin/python3 /home/isabell/.local/bin/jupyter-notebook
 [isabell@stardust ~]$

Now you can access the Jupyter webinterface via https://isabell.uber.space

Updates
=======

.. code-block:: console

 [isabell@stardust ~]$ pip3 install --user --upgrade jupyter
 [isabell@stardust ~]$

.. note:: Check the update feed_ of the releases_ on GitHub regularly to stay informed about the newest version.


.. _Jupyter Notebook: https://jupyter.org/
.. _LICENSE: https://github.com/jupyter/notebook/blob/master/LICENSE
.. _BSD 3-Clause "New" or "Revised" License: https://spdx.org/licenses/BSD-3-Clause.html
.. _feed: https://github.com/jupyter/notebook/releases.atom
.. _releases: https://github.com/jupyter/notebook/releases

----

Tested with Jupyter 6.0.3, Uberspace 7.7.1.2

.. author_list::
