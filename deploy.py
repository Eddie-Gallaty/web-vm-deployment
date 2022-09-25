from cgi import test
from inspect import ClosureVars
from flask import Flask, render_template
from vm import VM

app = Flask(__name__)
#new vm object
vm = VM()

#  get folders and clusters list
folders = vm.get_folders()
clusters = vm.get_clusters()
datastores = vm.get_datastores()
networks = vm.get_networks()

@app.route('/index')
def index():
    
    return render_template("index.html", mytitle='Hello World!', folders=folders, clusters=clusters, datastores=datastores, networks=networks)
