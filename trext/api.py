from trext.extract import server
from trext.extract.build import ExtractBuilder
import os


class Extract(object):
    """
    A Tableau Extract.
    
    Provides the endpoint to create and/or publish .tde extracts. 
    Usage:
    
        Create an extract
        >>> import trext
        >>> tde = trext.Extract()
        >>> connection_string = "appropriate db connection string"
        >>> tde.create("db.schema.table", conn_string=connection_string)
        Created!
        >>> tde.location
        /temp/extract.tde
        
        Publish to Tableau Server (overwrites existing extract)
        
        >>> tableau_auth_details = ("username", "password")
        >>> publish_details = ("site_content_url", "project_name")
        >>> tde.publish("tableau server address", auth=tableau_auth_details, params=publish_details)
        Published!
        
        Clean up after create and/or publish
        >>> tde.close()
    """

    def __init__(self, is_temp=True):
        """
        :param is_temp: True if this is a temporary extract that needs to be deleted after 
        publishing or False if this an extract that needs publishing and not deleting
        """
        self._location = None
        self._is_temp = is_temp

    def create(self, view_or_table_name, conn_string, dbtype=None):
        """
        Method to create an extract based on a view or a table on a database
        
        :param view_or_table_name: view or table to create an extract from
        :param conn_string: connection string to the database
        :param dbtype: type of database to connect to
        :return: `Created!` or `Failed!` message on creation
        """
        # create instance of ExtractBuilder
        builder = ExtractBuilder()
        # connect to the db
        builder.connect_to_db(view_or_table_name, conn_string, dbtype)
        # build extract for view_or_table and assign path to tde to _location
        self._location = builder.create_extract()
        # close connections to database
        builder.close()
        return "Created!" if self._location else "Failed!"

    @property
    def location(self):
        """
        :return: location of the .tde file if it was created or set up 
        """
        return self._location

    @location.setter
    def location(self, tde_path):
        """
        Sets the location of the extract
        
        :param tde_path: temporary path set in `ExtractBuilder._build_temp_tdepath` 
        """
        self._location = tde_path

    def publish(self, host_address, auth, params):
        """
        Publish to Tableau Server (overwrites existing extract) 
        
        :param host_address: Address of the Tableau server to publish to
        :param auth: a tuple of username and password for authentication
        :param params: currently a typle of two parameters: site to publish to and project name
        :return: Message on completing publishing
        """
        # create tableau server instance
        ts = server.Tableau()
        # extract the details needed to pass to the server
        username, password = auth
        site_content_url, project_name = params
        # connect to the server to a particular site
        ts.connect(host_address, username, password, site_content_url)
        # publish tde to project
        ts.publish(self.location, project_name)
        # close connection to server
        ts.close()
        return "Published!"

    def close(self):
        """
        Clean up on exit. Delete the extract only if temporary flag is True
        
        :return: if it is not a temporary extract 
        """
        if not self._is_temp:
            return
        os.remove(self.location)
