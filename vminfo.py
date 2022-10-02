import requests
import urllib3
from pprint import pprint
from vmware.vapi.vsphere.client import create_vsphere_client
from com.vmware.vcenter_client import (Folder)
from pyVmomi import vim, vmodl
from pyVim.connect import SmartConnect, Disconnect
# request to create a session
session = requests.session()
# ****research what this is actually doing***** Disable cert verification for demo purpose. This is not recommended in a production environment!!!
session.verify = False

class Vminfo():
    
    def __init__(self):
       # ***RESEARCH THIS MORE*** Disable the secure connection warning for demo purpose. This is not recommended in a production environment!!!!.
       # urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)
       pass
    def get_obj(content, vimtype, name):
        """
        Get the vsphere object associated with a given text name
        """
        obj = None
        container = content.viewManager.CreateContainerView(content.rootFolder, vimtype, True)
        print(container)
        for c in container.view:
            if c.name == name:
                obj = c
                print("from getobj ", c.name)
                break
        return obj
            
    def get_objs(self, si, vimtype, recursive):
        """
        Get the vsphere object associated with a given text name
        """
        obj = []
        container = si.content.rootFolder #starting point to look into
        viewType = vimtype #object types to look for
        container_view = si.content.viewManager.CreateContainerView(container, viewType, recursive) #create view
        print(container)
        for child in container_view.view:
            obj.append(child.name)
        return obj

    def get_folders(self, server, un, pw):
        si = SmartConnect(host=server, user=un, pwd=pw, port=443, disableSslCertValidation= True)
        list_of_folders = self.get_objs(si, [vim.Folder], True)
        folders = []
        for folder in list_of_folders:
            folders.append(folder)
        return folders
        #### Below is an example for doing this same operation in the vsphere automation sdk ####
        #vsphere_client = create_vsphere_client(server=server, username=un, password=pw, session=session)
        # List all VM folders inside the datacenter
       #list_of_folders = vsphere_client.vcenter.Folder.list(Folder.FilterSpec(type=Folder.Type.VIRTUAL_MACHINE))
        #ignore this
        #pprint(list_of_vms) 
    
    def get_clusters(self, server, un, pw):
        si = SmartConnect(host=server, user=un, pwd=pw, port=443, disableSslCertValidation=True)
        list_of_clusters = self.get_objs(si, [vim.ClusterComputeResource], True)
        clusters = []
        for cluster in list_of_clusters:
            clusters.append(cluster)
        return clusters

    
    def get_datastores(self, server, un, pw):
        si = SmartConnect(host=server, user=un, pwd=pw, port=443, disableSslCertValidation=True)
        list_of_datastores = self.get_objs(si, [vim.Datastore], True)
        datastores = []
        for datastore in list_of_datastores:
            datastores.append(datastore)
        return datastores
    
    def get_datastore_clusters(self, server, un, pw):
        si = SmartConnect(host=server, user=un, pwd=pw, port=443, disableSslCertValidation=True)
        list_of_datastoreClusters = self.get_objs(si, [vim.StoragePod], True)
        datastore_clusters = []
        for dsc in list_of_datastoreClusters:
            datastore_clusters.append(dsc)
        return datastore_clusters



    def get_networks(self, server, un, pw):
        si = SmartConnect(host=server, user=un, pwd=pw, port=443, disableSslCertValidation=True)
        list_of_networks = self.get_objs(si, [vim.Network], True)
        networks = []
        for network in list_of_networks:
            networks.append(network)
        return networks
    
    def create_vm_folder(self, host, un, pw, folder_name):
        si = SmartConnect(host=host, user=un, pwd=pw, port=443, disableSslCertValidation = True)
        dc = si.content.rootFolder.childEntity[0]
        dc.vmFolder.CreateFolder(folder_name)
        Disconnect(si)
