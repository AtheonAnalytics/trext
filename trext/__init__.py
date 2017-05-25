# -*- coding: utf-8 -*-
"""
This is the entry point for the library

Usage for trext:

Create an extract

>>> import trext
>>> tde = trext.Extract()
>>> connection_string = "appropriate db connection string"
>>> tde.create("db.schema.table", conn_string=connection_string, dbtype='exasol')
Created!
>>> tde.location
/temp/extract.tde


Publish to Tableau Server (overwrites existing extract)

>>> tableau_auth_details = ("username", "password")
>>> publish_details = ("site_content_url", "project_name")
>>> tde.publish("tableau server address", auth=tableau_auth_details, params=publish_details)
Published!

Refreshing an extract is now replaced with creating and publishing an extract.
You can use this is conjunction with TabAuto (not yet open source) or with Tableau's 
server-client-python library to get the datasource names that need refreshing.

"""

__title__ = 'trext'
__version__ = '0.2.1'
__author__ = 'Vathsala Achar'
__license__ = 'MIT'

from api import Extract
