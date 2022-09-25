import requests
import urllib3
from pprint import pprint
from vmware.vapi.vsphere.client import create_vsphere_client
import com.vmware.vcenter.inventory_client

# request to create a session
session = requests.session()

# ****research what this is actually doing
session.verify = False

# ** JUST FOR TESTING NEED TO FIGURE OUT PASSING AS ARGS!!!*** connect to vCenter Server using username and password
vsphere_client = create_vsphere_client(server='', username='', password='', session=session)

#  **RESEARCH THIS!*** var for  disable warning for insecure request warnings ** This is not recommended in a production environment.**
urllibvar = urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

class VM():
    def __init__(self):
        pass
    
    def get_vmName(self):
        vsphere_client
        # Disable cert verification for demo purpose. 
        # This is not recommended in a production environment.
        #session.verify = False
        # Disable the secure connection warning for demo purpose.
        # This is not recommended in a production environment.
        urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)
        # List all VMs inside the vCenter Server
        list_of_vms = vsphere_client.vcenter.VM.list()
        #pprint(list_of_vms) #test
        vmname = []
        for vm in list_of_vms:
            vmname.append(vm.name)
        return vmname







