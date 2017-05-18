TRExt
=====

Tableau Refresh Extract (Externally)
------------------------------------

TRExt is a means to refresh a Tableau Extract (.tde files) externally so the Tableau Server can 
serve visual content without having to compete for resources while refreshing extracts internally.

The main dependencies are:

- `Tableau SDK <https://onlinehelp.tableau.com/current/api/sdk/en-us/SDK/tableau_sdk_installing.htm>`_
- pyodbc

The repo also supports

- any other pyodbc wrapper such as `EXASol Python SDK <https://www.exasol.com/portal/display/DOWNLOAD/5.0>`_
 
------------------

Disclaimer
``````````

**TRExt is still a Work-in-Progress** 

I wrote most of this codebase when Tableau SDK was released for Tableau 8 and never got around to
moving it from a POC/local copy to open source, so this a rough-and-ready type of library.
 
This is fair warning to anyone who uses this repo: there will be bugs, bad documentation and no 
tests for a short while till I fix it up. So *please use with care* and if you find issues submit
a bug report or a PR.

If you want to contribute and add tests, better documentation, new connectors, cleaner 
interface etc, **please do** and submit a PR. 
 
Oh and don't forget to add yourself to AUTHORS_
 
 .. _AUTHORS: https://github.com/AtheonAnalytics/trext/blob/master/AUTHORS.rst