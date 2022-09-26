import requests
import urllib3
from pprint import pprint
from vmware.vapi.vsphere.client import create_vsphere_client

# request to create a session
session = requests.session()
# ****research what this is actually doing
session.verify = False

# ** JUST FOR TESTING NEED TO FIGURE OUT PASSING AS ARGS!!!*** connect to vCenter Server using username and password
vsphere_client = create_vsphere_client(server='', username='', password='', session=session)

#  **RESEARCH THIS!*** var for  disable warning for insecure request warnings ** This is not recommended in a production environment.**
#urllibvar = urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

class Vminfo():
    def __init__(self):
        pass
    
    def get_folders(self):
        vsphere_client
        # Disable cert verification for demo purpose. 
        # This is not recommended in a production environment.
        #session.verify = False
        # Disable the secure connection warning for demo purpose.
        # This is not recommended in a production environment.
        urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)
        # List all VMs inside the vCenter Server
        list_of_folders = vsphere_client.vcenter.Folder.list()
        #pprint(list_of_vms) #test
        folders = []
        for folder in list_of_folders:
            folders.append(folder.name)
        return folders
    
    def get_clusters(self):
        vsphere_client
        urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)
        list_of_clusters = vsphere_client.vcenter.Cluster.list()
        clusters = []
        for cluster in list_of_clusters:
            clusters.append(cluster.name)
        return clusters
    
    def get_datastores(self):
        vsphere_client
        urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)
        list_of_datastores = vsphere_client.vcenter.Datastore.list()
        datastores = []
        for datastore in list_of_datastores:
            datastores.append(datastore.name)
        return datastores

    def get_networks(self):
        vsphere_client
        urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)
        list_of_networks = vsphere_client.vcenter.Network.list()
        networks = []
        for network in list_of_networks:
            networks.append(network.name)
        return networks








