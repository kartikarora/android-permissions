import os

import untangle
from dicttoxml import dicttoxml
from flask import Flask, render_template, json, jsonify, make_response, Response

app = Flask(__name__)

with open(name=os.path.dirname(__file__) + '/static/json/permission_names.json') as perms_names_fp:
    data = perms_names_fp.read().encode('ascii', 'ignore')
    perms_names = json.loads(data)

with open(name=os.path.dirname(__file__) + '/static/json/permission_info.json') as perms_info_fp:
    data = perms_info_fp.read().encode('ascii', 'ignore')
    perms_info = json.loads(data)

perms_names_xml = dicttoxml(obj=perms_names, custom_root='permissions')


@app.route('/')
def home():
    return render_template('layout.html', container='home', perms_names=perms_names, perms_info=perms_info)


@app.route('/list')
def list():
    print perms_names
    return render_template('layout.html', container='list', permissions=perms_names)


@app.route('/list/json', methods=['GET', 'POST'])
def list_json():
    return make_response(jsonify(perms_names), 200)


@app.route('/list/xml', methods=['GET', 'POST'])
def list_xml():
    response = make_response(perms_names_xml, 200)
    response.headers['Content-type'] = 'application/xml'
    return response


@app.route('/detail/<string:permission>')
def detail(permission):
    name = permission.upper()
    permission = perms_info[name]
    permission['name'] = name
    return render_template('layout.html', container='detail', permission=permission)


@app.route('/detail/<string:permission>/json', methods=['GET', 'POST'])
def detail_json(permission):
    name = permission.upper()
    permission = perms_info[name]
    permission['name'] = name
    permission['url'] = 'https://developer.android.com/reference/android/Manifest.permission.html#' + name
    return make_response(jsonify(permission), 200)


@app.route('/detail/<string:permission>/xml', methods=['GET', 'POST'])
def detail_xml(permission):
    name = permission.upper()
    permission = perms_info[name]
    permission['name'] = name
    permission['url'] = 'https://developer.android.com/reference/android/Manifest.permission.html#' + name
    response = make_response(dicttoxml(obj=permission, custom_root=name), 200)
    response.headers['Content-type'] = 'application/xml'
    return response


port = os.getenv('PORT', '5000')
if __name__ == "__main__":
    app.run(debug=True, host='0.0.0.0', port=int(port), threaded=True)
