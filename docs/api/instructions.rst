Usage Instructions
==================

The current version of TRExt works with:

- Python 2.7
- pyodbc == 4.0.16
- Tableau SDK <= 10.1.4 (see :ref:`notes`)
- EXASol Python SDK >=5.0.13 and <= 5.0.17


Installation of dependencies
----------------------------

You will need to install Tableau SDK and pyodbc as a minimum to use this library. The EXASol
library will be needed if you want to connect to EXASol to create an extract.

pyodbc
``````

PyODBC should be installed when you install TRExt from pip see :ref:`install`. But if you have any
issues setting up pyodbc to connect to a database you might find the `PyODBC wiki
<https://github.com/mkleehammer/pyodbc/wiki>`_ useful.


Tableau SDK Installation
````````````````````````

The documentation for Tableau SDK is available at the `Tableau Documentation
<http://onlinehelp.tableau.com/current/api/sdk/en-us/help.htm>`_.

The library I have used to develop and test with is available in the `vendor folder
<https://github.com/AtheonAnalytics/trext/tree/master/vendor>`_ and this is only for Linux
Distribution. If you prefer to use versions for other Operating systems you can find them `here
<http://onlinehelp.tableau.com/current/api/sdk/en-us/SDK/tableau_sdk_installing.htm#downloading>`_.

The installation of the Linux version is as follows:

Download the correct `tar.gz` file for Python (32 or 64 bit depending on your OS) and then,

.. code-block:: bash

    $ tar -xzvf Tableau-SDK-Python-Linux-xxBit-10-x-x.tar.gz
    $ cd /Tableau*/
    $ python setup.py install


EXASol SDK Installation
```````````````````````
Skip to the next section if you do not use EXASol.

The EXASol Python SDK can be downloaded from their `Download section
<https://www.exasol.com/portal/display/DOWNLOAD/5.0>`_. We use version 5.0.17 for this version of
TRExt but I have also tested on some older versions.

Download from Packages and SDK the version you want, preferably in the `tar.gz` format and
install as follows,

.. code-block:: bash

    $ tar -xzvf EXASolution_SDK-5.0.xx.tar.gz
    $ cd /EXASolution_SDK-5.0.xx/Python/
    $ python setup.py install


Additional Setup
----------------

To connect to MSSQL you need to set up the MSSQL driver and driver manager.

Installation of the ODBC driver for Linux is available from `Microsoft
<https://docs.microsoft.com/en-us/sql/connect/odbc/linux/installing-the-microsoft-odbc-driver-for-sql-server-on-linux>`_.

Instructions on setting up the driver manager to connect to MSSQL is available from `pyodbc
<https://github.com/mkleehammer/pyodbc/wiki/Connecting-to-SQL-Server-from-RHEL-or-Centos>`_.

Once you have your connection information in `odbc.ini` you should be able to test the connection
with the `DSN` parameter using pyodbc. You should get a pyodbc.Connection object if the
connection was successful.

.. code-block:: bash

    $ python -c 'import pyodbc; print(pyodbc.connect("DSN=MySQLServerDatabase;UID=username;PWD=password"))'
    <pyodbc.Connection object at 0x7f8597333200>


.. _usage:

Usage of the api
----------------

Create a TRExt Extract
``````````````````````

The TRExt Extract is the interface to the `create` and `publish` methods. Initialise the Extract,

.. code-block:: python

    >>> import trext
    >>> tde = trext.Extract()

Create an extract for MSSQL
```````````````````````````
Assuming that you can connect to the MSSQL server, you can now create a .tde extract using the
following,

.. code-block:: python

    >>> conn_string = "DSN=MySQLServerDatabase;UID=username;PWD=password"
    >>> tde.create("db.schema.table", conn_string=conn_string)
    Created!

Create an extract for EXASol
````````````````````````````
Note here that in the create api we use an extra argument called `dbtype` set to `'exasol'`. This
is how TRExt extends to other databases. Currently only MSSQL and EXAsol have been tested.

.. code-block:: python

    >>> conn_string = "DSN=EXAServer"
    >>> tde.create("db.schema.table", conn_string=conn_string, dbtype='exasol')
    Created!

Location of the extract
```````````````````````

Once you have created the extract and you want to know the location of your extract simply do,

.. code-block:: python

    >>> tde.location
    /temp/location/of/extract.tde

Publish to Tableau Server
`````````````````````````
The default behaviour of publish is to overwrite the existing extract. This will be extended in
the future versions.

.. code-block:: python

    >>> tableau_auth_details = ("username", "password")
    >>> publish_details = ("site_content_url", "project_name")
    >>> tde.publish("tableau server address", auth=tableau_auth_details, params=publish_details)
    Published!

Close the Extract
`````````````````
Once you are done creating and/or publishing an extract, perform the `close` operation,

.. code-block:: python

    >>> tde.close()

This api ensures that the tde created locally gets destroyed.

Publish existing .tde to Tableau Server
```````````````````````````````````````
You can also use this api to publish a local .tde file to the Tableau Server, simply set the
location of the TRExt extract to the path of the .tde you want to publish

.. code-block:: python

    >>> tde.location = "local/path/to/extract.tde"
    >>> tde.publish("tableau server address", auth=tableau_auth_details, params=publish_details)
    Published!

.. _notes:

Notes
-----
(*) I have not tested to see if Tableau SDK still supports versions 8 and 9 but this code was
based on Tableau SDK for Tableau 8; another area that needs testing and improvement for TRExt.