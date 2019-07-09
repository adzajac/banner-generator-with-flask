import os
from flask import Flask, render_template, redirect, url_for, request
from jinja2 import Environment, PackageLoader, select_autoescape

OUTPUT_DIR = "output/"


app = Flask(__name__)

env = Environment(
    loader=PackageLoader('app', 'templates'),
    autoescape=select_autoescape(['html', 'xml', 'txt'])
)

@app.route('/')
def index():
    if request.args:
        ad_params = {
            'width':request.args.get('width', 300, type=int),
            'height':request.args.get('height', 250, type=int),
            'bkg_color':request.args.get('bkg_color', '#ffffff', type=str),
            'border_color':request.args.get('border_color', '#525252', type=str),
            'border':request.args.get('border', 'off', type=str),
            'clicktag':request.args.get('clicktag', 'off', type=str),
            'tweenmax':request.args.get('tweenmax', 'off', type=str),
            'sample_animation':request.args.get('sample_animation', 'off', type=str),
            'ad_serving':request.args.get('ad_serving', 'None', type=str)
        }
        
        dir_name = OUTPUT_DIR + str(ad_params["width"])+ "x" + str(ad_params["height"])
        
        if not os.path.exists(dir_name):
            os.makedirs(dir_name)
            
        env.get_template('ad_base.html').stream(ad_params=ad_params).dump(dir_name + "/index.html")
        env.get_template('ad_main.js').stream(ad_params=ad_params).dump(dir_name + "/main.js")
        env.get_template('ad_style.css').stream(ad_params=ad_params).dump(dir_name + "/style.css")
        return render_template('success.html')
    return render_template('index.html')


