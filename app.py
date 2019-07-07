from flask import Flask
from flask import render_template, redirect, url_for, request
from jinja2 import Template

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
            'height':request.args.get('height', 250, type=str)
        }
        env.get_template('ad_base.html').stream(data=data).dump(OUTPUT_DIR+data["width"] + "x" + data["height"] + ".html")
    return render_template('index.html')

