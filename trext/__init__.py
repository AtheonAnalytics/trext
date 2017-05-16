"""
This is the entry point for the library

Usage for trext:

Create an extract

>>> import trext
>>> tde = trext.Extract()
>>> connection_string = "appropriate db connection string"
>>> tde.create("db.schema.table", conn_string=connection_string)
Created!
>>> tde.location
/temp/extract.tde


Publish to Tableau Server (overwrites existing extract)

>>> tableau_auth_details = ("usename", "password")
>>> publish_details = ("site_content_url", "project_name")
>>> tde.publish("tableau server address", auth=tableau_auth_details, params=publish_details)
Published!
"""

from extract import Extract
