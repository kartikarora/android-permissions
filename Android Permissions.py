import os

from flask import Flask, render_template, json

app = Flask(__name__)

with open(name=os.path.dirname(__file__) + '/static/json/permission_names.json') as perms_names_fp:
    data = perms_names_fp.read().encode('ascii', 'ignore')
    perms_names = json.loads(data)

with open(name=os.path.dirname(__file__) + '/static/json/permission_info.json') as perms_info_fp:
    data = perms_info_fp.read().encode('ascii', 'ignore')
    perms_info = json.loads(data)


@app.route('/')
def home():
    return render_template('layout.html', container='home', perms_names=perms_names, perms_info=perms_info)


@app.route('/list')
def list():
    return render_template('layout.html', container='list', perms_names=perms_names)


@app.route('/detail/<string:permission>')
def detail(permission):
    name = permission
    permission = perms_info[name]
    permission['name'] = name
    return render_template('layout.html', container='detail', permission=permission)


if __name__ == '__main__':
    app.run(debug=True)
