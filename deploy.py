from cgi import test
import dis
from inspect import ClosureVars
from flask import Flask, render_template, request
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

    if request.method == 'POST':
        if 'submit' in request.form :
            folders = vminfo.get_folders(vcenter_name, username, password)
            clusters = vminfo.get_clusters(vcenter_name, username, password)
            datastores = vminfo.get_datastores(vcenter_name,username, password)
            networks = vminfo.get_networks(vcenter_name, username, password)
            return render_template("/index.html", mytitle='Hello World!', folders=folders, clusters=clusters, datastores=datastores, networks=networks)
        elif 'add' in request.form:
            #this is testing passing input from textbox to variables
            print(network_select)
        elif 'create_folder' in request.form:
            #create new folder
            vminfo.create_vm_folder(vcenter_name, username, password, create_folder)

    return render_template("/index.html", mytitle='Hello World!')