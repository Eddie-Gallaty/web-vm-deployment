from cgi import test
from inspect import ClosureVars
from flask import Flask, render_template, request
from vminfo import Vminfo

app = Flask(__name__)
#new vminfo object
vminfo = Vminfo()

@app.route('/', methods=['GET', 'POST'])
@app.route('/index', methods=['GET', 'POST'])
def index():
    vcenter_name = request.form.get("vcentername")
    username = request.form.get("username")
    password = request.form.get("password")

    # on "submit" button click
    if request.method == 'POST':
        folders = vminfo.get_folders(vcenter_name, username, password)
        clusters = vminfo.get_clusters(vcenter_name, username, password)
        datastores = vminfo.get_datastores(vcenter_name,username, password)
        networks = vminfo.get_networks(vcenter_name, username, password)
        return render_template("/index.html", mytitle='Hello World!', folders=folders, clusters=clusters, datastores=datastores, networks=networks)
    else:
        return render_template("/index.html", mytitle='Hello World!')
