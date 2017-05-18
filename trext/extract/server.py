"""

connection for tableau

"""
import re
from tableausdk.Server import ServerAPI, ServerConnection


class Tableau(object):
    def __init__(self):
        self.server_init = ServerAPI()
        self.server_init.initialize()
        self.server = ServerConnection()

    @staticmethod
    def _get_extract_name(extract_path):
        extract_name_regex = re.compile("(\w*).tde$")
        extract_name = extract_name_regex.findall(extract_path)[0]
        return extract_name

    def connect(self, host, username, password, site_content_url='Default'):
        self.server.connect(host, username, password, site_content_url)

    def publish(self, tde_path, project_name='Default', datasource_name=None, overwrite=True):
        if not datasource_name:
            datasource_name = self._get_extract_name(tde_path)
        self.server.publishExtract(tde_path, project_name, datasource_name, overwrite)
        return "Published!"

    def close(self):
        self.server.disconnect()
        self.server_init.cleanup()
