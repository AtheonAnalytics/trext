.. image:: https://travis-ci.org/AtheonAnalytics/trext.svg?branch=master
    :target: https://travis-ci.org/AtheonAnalytics/trext

.. image:: https://badge.fury.io/py/TRExt.svg
    :target: https://badge.fury.io/py/TRExt

.. image:: https://coveralls.io/repos/github/AtheonAnalytics/trext/badge.svg?branch=master
    :target: https://coveralls.io/github/AtheonAnalytics/trext?branch=master

TRExt
=====

TRExt is short for Tableau Refresh Extract (Externally).

TRExt is a means to refresh a Tableau Extract (.tde files) externally so the Tableau Server can 
serve visual content without having to compete for resources while refreshing extracts internally.


Dependencies
````````````

The main dependencies are:

- `Tableau SDK <https://onlinehelp.tableau.com/current/api/sdk/en-us/SDK/tableau_sdk_installing.htm>`_
- pyodbc

The repo also supports

- pyodbc wrapper such as `EXASol Python SDK <https://www.exasol.com/portal/display/DOWNLOAD/5.0>`_


.. _install:

Installation
````````````

You need `pip` to install TRExt.

You can install the latest version of the package straight from PyPI using:

.. code-block:: bash

    $ pip install trext


You can also directly install from GitHub directly using:

.. code-block:: bash

    $ pip install git+git@github.com:AtheonAnalytics/trext.git

or

.. code-block:: bash

    $ pip install git+https://github.com/AtheonAnalytics/trext.git


Usage
`````

Create an extract

.. code-block:: python

    >>> import trext
    >>> tde = trext.Extract()
    >>> connection_string = "appropriate db connection string"
    >>> tde.create("db.schema.table", conn_string=connection_string, dbtype='exasol')
    Created!
    >>> tde.location
    /temp/extract.tde


Publish to Tableau Server (overwrites existing extract)

.. code-block:: python

    >>> tableau_auth_details = ("username", "password")
    >>> publish_details = ("site_content_url", "project_name")
    >>> tde.publish("tableau server address", auth=tableau_auth_details, params=publish_details)
    Published!

Refreshing an extract is now replaced with creating and publishing an extract.
You can use this is conjunction with TabAuto (not yet open source) or with Tableau's
`server-client-python <https://github.com/tableau/server-client-python>`_ library to get the datasource names that need refreshing.

------------------

Disclaimer
``````````

**TRExt is still a Work-in-Progress** 

I wrote most of this codebase when Tableau SDK was released for Tableau 8 and never got around to
moving it from a POC/local copy to open source, so this a rough-and-ready type of library.
 
This is fair warning to anyone who uses this library: there will be bugs, bad documentation and no
tests for a short while till I fix it up. So *please use with care* and if you find issues submit
a bug report or a PR.

If you want to contribute and add tests, better documentation, new connectors, cleaner 
interface etc, *please do* and submit a PR.
 
Oh and don't forget to add yourself to AUTHORS_
 
 .. _AUTHORS: https://github.com/AtheonAnalytics/trext/blob/master/AUTHORS.rst

**Note**: I have tested TRExt only on a Linux distro, so if you find any issues on other
Operating Systems please do create a bug report and I can try to fix it, but if you do know how
to fix it please also submit a PR.