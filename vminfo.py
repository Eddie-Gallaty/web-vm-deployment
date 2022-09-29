import requests
import urllib3
from pprint import pprint
from vmware.vapi.vsphere.client import create_vsphere_client
from pyVim.connect import SmartConnect, Disconnect
from com.vmware.vcenter_client import (Folder)

# request to create a session
session = requests.session()
# ****research what this is actually doing***** Disable cert verification for demo purpose. This is not recommended in a production environment!!!
session.verify = False

class Vminfo():
    def __init__(self):
       # ***RESEARCH THIS MORE*** Disable the secure connection warning for demo purpose. This is not recommended in a production environment!!!!.
       urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)
    
    def get_folders(self, server, un, pw):
        vsphere_client = create_vsphere_client(server=server, username=un, password=pw, session=session)
        # List all VM folders inside the datacenter
        list_of_folders = vsphere_client.vcenter.Folder.list(Folder.FilterSpec(type=Folder.Type.VIRTUAL_MACHINE))
        #pprint(list_of_vms) #test
        folders = []
        for folder in list_of_folders:
            folders.append(folder.name)
        return folders

    def get_clusters(self, server, un, pw):
        vsphere_client = create_vsphere_client(server=server, username=un, password=pw, session=session)
        #list all clusters in the vCenter Server
        list_of_clusters = vsphere_client.vcenter.Cluster.list()
        clusters = []
        for cluster in list_of_clusters:
            clusters.append(cluster.name)
        return clusters
    
    def get_datastores(self, server, un, pw):
        vsphere_client = create_vsphere_client(server=server, username=un, password=pw, session=session)
        #list all datastores in the vCenter Server
        list_of_datastores = vsphere_client.vcenter.Datastore.list()
        datastores = []
        for datastore in list_of_datastores:
            datastores.append(datastore.name)
        return datastores

    def get_networks(self, server, un, pw):
        vsphere_client = create_vsphere_client(server=server, username=un, password=pw, session=session)
        #list all networks in the vCenter Server
        list_of_networks = vsphere_client.vcenter.Network.list()
        networks = []
        for network in list_of_networks:
            networks.append(network.name)
        return networks

    def create_vm_folder(self, host, un, pw):
        si = SmartConnect(host=host, user=un, pwd=pw, port=443, disableSslCertValidation = True)
        dc = si.content.rootFolder.childEntity[0]
        dc.vmFolder.CreateFolder("TestEGDev2")
        Disconnect(si)