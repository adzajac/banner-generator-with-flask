from flask import Flask
from flask import render_template, redirect, url_for, request
from jinja2 import Template
import os

app = Flask(__name__)

OUTPUT_DIR = "output/"

from jinja2 import Environment, PackageLoader, select_autoescape
env = Environment(
    loader=PackageLoader('app', 'templates'),
    autoescape=select_autoescape(['html', 'xml', 'txt'])
)


@app.route('/')
def index():
    if request.args:
        data = {
            'width':request.args.get('width', 300, type=str),
            'height':request.args.get('height', 250, type=str),
            'bkg_color':request.args.get('bkg_color', '#ffffff', type=str),
            'border':request.args.get('border', 'off', type=str),
            'clicktag':request.args.get('clicktag', 'on', type=str),
            'tweenmax':request.args.get('tweenmax', 'off', type=str),
            'ad_serving':request.args.get('ad_serving', 'None', type=str)
        }
        dir_name = data["width"]+ "x" + data["height"]
        if not os.path.exists(OUTPUT_DIR + dir_name):
            os.makedirs(OUTPUT_DIR + dir_name)
        env.get_template('ad_base.html').stream(data=data).dump(OUTPUT_DIR + dir_name + "/" + "index.html")
        env.get_template('ad_main.js').stream(data=data).dump(OUTPUT_DIR + dir_name + "/" + "main.js")
        env.get_template('ad_style.css').stream(data=data).dump(OUTPUT_DIR + dir_name + "/" + "style.css")
    return render_template('index.html')

