from cgi import test
from flask import Flask, render_template
from vm import VM

app = Flask(__name__)
vm = VM()
getvms = []
getvms = vm.get_vmName()
print(getvms)
@app.route('/index')
def index():
    vm = VM()
    getvms = vm.get_vmName()
    print(getvms)
    return render_template("index.html", mytitle='Hello World!', getvms=getvms, vms="VMs")
