from cgi import test
import dis
from inspect import ClosureVars
from flask import Flask, render_template, request, jsonify
from vminfoT import Vminfo
from pyVim.connect import SmartConnect, Disconnect


app = Flask(__name__)
#new vminfo object
vminfo = Vminfo()

@app.route('/', methods=['GET', 'POST'])
@app.route('/index', methods=['GET', 'POST'])

def index():
    vcenter_name = request.form.get("vcentername")
    username = request.form.get("username")
    password = request.form.get("password")
    network_select = request.form.get("Networks")
    create_folder = request.form.get("new_folder")
    deploy_vm = request.form.get("template")
    test = request.args.get("dsc")

    

    if request.method == 'POST':
        if 'submit' in request.form :
            templates = vminfo.get_templates(vcenter_name, username, password)
            folders = vminfo.get_folders(vcenter_name, username, password)
            clusters = vminfo.get_clusters(vcenter_name, username, password)
            datastore_cluster = vminfo.get_datastore_clusters(vcenter_name, username, password)
            datastores = vminfo.get_datastores(vcenter_name,username, password)
            networks = vminfo.get_networks(vcenter_name, username, password)
            print("hi")
            return render_template("/index.html", mytitle='Hello World!', templates=templates, folders=folders, clusters=clusters, datastore_cluster=datastore_cluster, datastores=datastores, networks=networks)
        elif 'add' in request.form:
            #this is testing passing input from textbox to variables
            print(network_select)
        elif 'create_folder' in request.form:
            #create new folder
            vminfo.create_vm_folder(vcenter_name, username, password, create_folder)
        elif 'deploy_vm' in request.form:
            print(deploy_vm)
#        elif 'deploy_vm' in request.form:
            #deploy new vm from template
            #vminfo.clone_vm(vcenter_name, username, password, template, vmname, folder,cluster, power, datastore_name, dsc)
            #if 'submit' in request.form:
        else:
            template = request.form['template']
            folder = request.form['folder']
            cluster = request.form['cluster']
            dsc = request.form['dsc']
            ds = request.form['ds']
            #Just for testing 
            vm = ""
            network = request.form['network']
            print("hello world!")
            print(template, folder, cluster, dsc, ds, network)
            # This is just for testing more to come
            vcenter_name = ""
            username = ""
            password = ""
            vminfo.clone_vm(vcenter_name, username, password, template, vm, folder, cluster, True, ds, dsc)
            #vminfo.create_vm_folder(vcenter_name, username, password, create_folder)
            # place holder for now
            #return jsonify(template=template)
            return render_template("/index.html", mytitle='Hello World!')

            

    return render_template("/index.html", mytitle='Hello World!')
    

