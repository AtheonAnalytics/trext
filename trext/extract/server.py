"""

connection for tableau

"""
from tableausdk.Server import ServerAPI, ServerConnection

from trext.extract.utils import get_extract_name


class Tableau(object):
    """
    Tableau server connection class
    """

    def __init__(self):
        self.server_init = ServerAPI()
        self.server_init.initialize()
        self.server = ServerConnection()

    def connect(self, host, username, password, site_content_url='Default'):
        """
        Connect to the Tableau server
        
        :param host: address of the Tableau server 
        :param username: Tableau Server username
        :param password: Tableau Server password
        :param site_content_url: Site to publish to
        """
        self.server.connect(host, username, password, site_content_url)

    def publish(self, tde_path, project_name='Default', datasource_name=None, overwrite=True):
        """
        Publishes an extract to the Tableau Server
        
        :param tde_path: path of tde to publish
        :param project_name: name of project on the Tableau site to publish to 
        :param datasource_name: the name of the .tde to publish as
        :param overwrite: boolean to flag if the .tde needs an overwrite when publishing
        """
        if not datasource_name:
            datasource_name = get_extract_name(tde_path)
        self.server.publishExtract(tde_path, project_name, datasource_name, overwrite)

    def close(self):
        """
        Close connection to Tableau Server
        """
        self.server.disconnect()
        self.server_init.cleanup()
