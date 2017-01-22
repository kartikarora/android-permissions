"""
    MIT License

    Copyright (c) 2017 Kartik Arora

    Permission is hereby granted, free of charge, to any person obtaining a copy
    of this software and associated documentation files (the "Software"), to deal
    in the Software without restriction, including without limitation the rights
    to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
    copies of the Software, and to permit persons to whom the Software is
    furnished to do so, subject to the following conditions:

    The above copyright notice and this permission notice shall be included in all
    copies or substantial portions of the Software.

    THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
    IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
    FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
    AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
    LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
    OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
    SOFTWARE.
"""
import os
import re

from dicttoxml import dicttoxml
from flask import Flask, render_template, json, jsonify, make_response, Response
from jinja2 import evalcontextfilter, Markup, escape

app = Flask(__name__)

with open(os.path.dirname(os.path.abspath(__file__)) + '/static/json/permission_names.json') as perms_names_fp:
    data = perms_names_fp.read().encode('ascii', 'ignore')
    perms_names = json.loads(data)

with open(os.path.dirname(os.path.abspath(__file__)) + '/static/json/permission_info.json') as perms_info_fp:
    data = perms_info_fp.read().encode('ascii', 'ignore')
    perms_info = json.loads(data)

perms_names_xml = dicttoxml(obj=perms_names, custom_root='permissions')


@app.route('/')
def home():
    return render_template('layout.html', container='home', perms_names=perms_names, perms_info=perms_info)


@app.route('/list')
def list():
    return render_template('layout.html', container='list', permissions=perms_names)


@app.route('/list/json', methods=['GET', 'POST'])
@app.route('/api/list/json', methods=['GET', 'POST'])
def list_json():
    return make_response(jsonify(perms_names), 200)


@app.route('/list/xml', methods=['GET', 'POST'])
@app.route('/api/list/xml', methods=['GET', 'POST'])
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
@app.route('/api/detail/<string:permission>/json', methods=['GET', 'POST'])
def detail_json(permission):
    name = permission.upper()
    permission = perms_info[name]
    permission['name'] = name
    permission['url'] = 'https://developer.android.com/reference/android/Manifest.permission.html#' + name
    return make_response(jsonify(permission), 200)


@app.route('/detail/<string:permission>/xml', methods=['GET', 'POST'])
@app.route('/api/detail/<string:permission>/xml', methods=['GET', 'POST'])
def detail_xml(permission):
    name = permission.upper()
    permission = perms_info[name]
    permission['name'] = name
    permission['url'] = 'https://developer.android.com/reference/android/Manifest.permission.html#' + name
    response = make_response(dicttoxml(obj=permission, custom_root=name), 200)
    response.headers['Content-type'] = 'application/xml'
    return response


@app.route('/api')
def api():
    return render_template('layout.html', container='api')


@app.template_filter()
@evalcontextfilter
def nl2br(eval_ctx, value):
    _paragraph_re = re.compile(r'(?:\r\n|\r|\n){2,}')
    result = u'\n\n'.join(u'<h5>%s</h5>' % p.replace('\n', '<br>\n') \
                          for p in _paragraph_re.split(escape(value)))
    if eval_ctx.autoescape:
        result = Markup(result)
    return result


port = os.getenv('PORT', '5000')
if __name__ == "__main__":
    app.run(debug=True, host='0.0.0.0', port=int(port), threaded=True)
