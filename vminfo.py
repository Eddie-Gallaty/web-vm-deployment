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
    
    def wait_for_task(self, task):
        """ wait for a vCenter task to finish """
        task_done = False
        while not task_done:
            if task.info.state == 'success':
                return task.info.result

            if task.info.state == 'error':
                print("there was an error")
                print(task.info.error)
                task_done = True

    def __init__(self):
       # ***RESEARCH THIS MORE*** Disable the secure connection warning for demo purpose. This is not recommended in a production environment!!!!.
       #urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)
       pass

    def get_obj(self, si, vimtype, name):
        """
        Get the vsphere object associated with a given text name
        """
        obj = None
        container = si.content.rootFolder
        viewType = vimtype
        container_view = si.content.viewManager.CreateContainerView(container, viewType, True)
        #container = content.viewManager.CreateContainerView(content.rootFolder, vimtype, True)
        print(container)
        for c in container_view.view:
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
        #create view
        #container_view = si.content.viewManager.CreateContainerView(content.rootFolder, viewType, recursive)
        container_view = si.content.viewManager.CreateContainerView(container, viewType, recursive)
        print(container)
        for child in container_view.view:
            obj.append(child)
        return obj#[child for child in container_view.view]

            #content = si.RetrieveContent()
    
    def get_templates(self, server, un, pw):
        si = SmartConnect(host=server, user=un, pwd=pw, port=443, disableSslCertValidation=True)
        list_of_templates = self.get_objs(si, [vim.VirtualMachine], True)
        templates = []
        for vm in list_of_templates:
            if vm.config.template:
                templates.append(vm.config.name)
        return templates

    def get_folders(self, server, un, pw):
        si = SmartConnect(host=server, user=un, pwd=pw, port=443, disableSslCertValidation= True)
        list_of_folders = self.get_objs(si, [vim.Folder], True)
        folders = []
        for folder in list_of_folders:
            folders.append(folder.name)
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
            clusters.append(cluster.name)
        return clusters
    
    def get_datastores(self, server, un, pw):
        si = SmartConnect(host=server, user=un, pwd=pw, port=443, disableSslCertValidation=True)
        list_of_datastores = self.get_objs(si, [vim.Datastore], True)
        datastores = []
        for datastore in list_of_datastores:
            datastores.append(datastore.name)
        return datastores
    
    def get_datastore_clusters(self, server, un, pw):
        si = SmartConnect(host=server, user=un, pwd=pw, port=443, disableSslCertValidation=True)
        list_of_datastoreClusters = self.get_objs(si, [vim.StoragePod], True)
        datastore_clusters = []
        for dsc in list_of_datastoreClusters:
            datastore_clusters.append(dsc.name)
        return datastore_clusters



    def get_networks(self, server, un, pw):
        si = SmartConnect(host=server, user=un, pwd=pw, port=443, disableSslCertValidation=True)
        list_of_networks = self.get_objs(si, [vim.Network], True)
        networks = []
        for network in list_of_networks:
            networks.append(network.name)
        return networks
    
    def create_vm_folder(self, host, un, pw, folder_name):
        #vsphere_client = create_vsphere_client(server=server, username=un, password=pw, session=session)
        si = SmartConnect(host=host, user=un, pwd=pw, port=443, disableSslCertValidation = True)
        dc = si.content.rootFolder.childEntity[0]
        #for child in dc:
        #   print(child)
        #print(dcobj)
        #dc = pchelper.get_obj(si.content, [vim.Datacenter], dcobj.name)
        #if dc is None:
        #    raise Exception("failed to find Datacenter name")
        dc.vmFolder.CreateFolder(folder_name)
        Disconnect(si)
        #new_folder = vim.Datacenter(dc, si._stub).vmFolder.CreateFolder()
        #print(datacenter)
        #folder_mo = datacenter.vmFolder.Create()
        #print("Created Folder: " +folder_name)
        #print(datacenter)

    #basically ripped off Dann Bohn :) https://github.com/vmware/pyvmomi-community-samples/blob/master/samples/clone_vm.py
    def clone_vm(self, host, un, pw, template_name, vmname, vmfolder, cluster_name, power_on, datastore_name, datastore_cluster):
        si = SmartConnect(host=host, user=un, pwd=pw, port=443, disableSslCertValidation = True)
        dc = si.content.rootFolder.childEntity[0]
        vmconf = vim.vm.ConfigSpec()
        destfolder = self.get_obj(si, [vim.Folder], vmfolder)
        datastore = self.get_obj(si, [vim.Datastore], datastore_name)
        cluster = self.get_obj(si, [vim.ClusterComputeResource], cluster_name)
        template = self.get_obj(si, [vim.VirtualMachine], template_name)
        #protip: clusters have a default resource pool
        resource_pool = cluster.resourcePool
        template = self.get_obj(si, [vim.VirtualMachine], template_name)
        if datastore_cluster:
            #for storage cluster selection "pod is the cluster"
            pod_selection = vim.storageDrs.PodSelectionSpec()
            pod = self.get_obj(si, [vim.StoragePod], datastore_cluster)
            pod_selection.storagePod = pod
            #for passing vm to "pod"
            storagespec = vim.storageDrs.StoragePlacementSpec()
            storagespec.podSelectionSpec = pod_selection
            storagespec.type = 'create'
            storagespec.folder = destfolder
            storagespec.resourcePool = resource_pool
            storagespec.configSpec = vmconf
            try:
                rec = si.storageResourceManager.RecommendDatastores(
                storageSpec=storagespec)
                rec_action = rec.recommendations[0].action[0]
                real_datastore_name = rec_action.destination.name
            except Exception:
                real_datastore_name = template.datastore[0].info.name

            datastore = self.get_obj(si, [vim.Datastore], real_datastore_name)
        #set relocaton spec
        relospec = vim.vm.RelocateSpec()
        relospec.datastore = datastore
        relospec.pool = resource_pool
        clonespec = vim.vm.CloneSpec()
        clonespec.location = relospec
        clonespec.powerOn = power_on

        print("cloning VM...")
        task = template.Clone(folder=destfolder, name=vmname, spec=clonespec)
        self.wait_for_task(task)
        print("VM cloned.")
