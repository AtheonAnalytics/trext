from trext.extract.server import Tableau
import os


class Extract(object):
    def __init__(self, is_temp=True):
        self._location = None
        self._is_temp = is_temp

    def create(self, view_or_table_name, conn_string, dbtype=None):
        """        
        Create an extract
        >>> import trext
        >>> tde = trext.Extract()
        >>> connection_string = "appropriate db connection string"
        >>> tde.create("db.schema.table", conn_string=connection_string)
        Created!
        
        :param view_or_table_name: 
        :param conn_string: 
        :param dbtype: 
        :return: 
        """
        # todo
        self._location = 'path_to_tde'

    @property
    def location(self):
        """
        >>> tde.location
        /temp/extract.tde
        
        :return: 
        """
        return self._location

    @location.setter
    def location(self, tde_path):
        self._location = tde_path

    def publish(self, host_name, auth, params):
        """
        Publish to Tableau Server (overwrites existing extract)

        >>> tableau_auth_details = ("username", "password")
        >>> publish_details = ("site_content_url", "project_name")
        >>> tde.publish("tableau server address", auth=tableau_auth_details, params=publish_details)
        Published!
        """
        ts = Tableau()
        username, password = auth
        site_content_url, project_name = params
        ts.connect(host_name, username, password, site_content_url)
        ts.publish(self.location, project_name)
        ts.close()

    def cleanup(self):
        """
        delete only if temporary
        :return: 
        """
        if not self._is_temp:
            return
        os.remove(self.location)
