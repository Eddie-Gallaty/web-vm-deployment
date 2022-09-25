from cgi import test
from inspect import ClosureVars
from flask import Flask, render_template
from vminfo import Vminfo

app = Flask(__name__)
#new vminfo object
vminfo = Vminfo()

#  get folders and clusters list
folders = vminfo.get_folders()
clusters = vminfo.get_clusters()
datastores = vminfo.get_datastores()
networks = vminfo.get_networks()

@app.route('/index')
def index():
    
    return render_template("index.html", mytitle='Hello World!', folders=folders, clusters=clusters, datastores=datastores, networks=networks)
