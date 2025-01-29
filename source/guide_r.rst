.. author:: mspt <marcus@mspittler.eu>

.. tag:: lang-r
.. tag:: audience-developers
.. tag:: statistics

.. highlight:: console

.. sidebar:: Logo

  .. image:: _static/images/r.svg
      :align: center

#####
R
#####

.. tag_list::

R_ is a programming language for statistical computing and data visualization.
It has been adopted in the fields of data mining, bioinformatics and data analysis.

----

.. note:: Most Uberspace instances have an older version of R pre-installed
  (3.6.0, released on 2019-04-26). This guide explains how to install R version 4.X.X, currently 4.4.2.

Prerequisites
=============

We are following the install **R** from source instructions_. The installation may be time-consuming.

Installation
============

Download source
---------------

Check the CRAN_ release page for the latest version.

.. code-block:: console

  # Set latest version
  [isabell@stardust ~]$ export R_VERSION=4.4.2
  # Download source
  [isabell@stardust ~]$ curl https://cran.r-project.org/src/base/R-4/R-${R_VERSION}.tar.gz | tar -xJv

Installation
------------

.. code-block:: console

  [isabell@stardust ~]$ cd R-4.4.2/
  [isabell@stardust ~]$ ./configure --prefix=$HOME/.local
  [isabell@stardust ~]$ make
  [isabell@stardust ~]$ make install

Verifying (optional)
--------------------

.. code-block:: console

  [isabell@stardust ~]$ which R
  ~/.local/bin/R
  [isabell@stardust ~]$ R --version | head -1
  R version 4.4.2 (2024-10-31) -- "Pile of Leaves"

.. ##### Link section #####

.. _R: https://www.r-project.org/
.. _CRAN: https://cran.r-project.org/
.. _instructions: https://cran.r-project.org/doc/manuals/r-patched/R-admin.html#Installation-1

----

Tested with R 4.4.2, Uberspace 7.15.15 (2024-05-08)

.. author_list::
