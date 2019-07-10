import os
from flask import Flask, render_template, redirect, url_for, request, send_file
from jinja2 import Environment, PackageLoader, select_autoescape
import zipfile


OUTPUT_DIR = "output/"


app = Flask(__name__)

env = Environment(
    loader=PackageLoader('app', 'templates'),
    autoescape=select_autoescape(['html', 'xml', 'txt'])
)


def zipdir(path, ziph):
    # ziph is zipfile handle
    for root, dirs, files in os.walk(path):
        print(dirs)
        for file in files:
            arch_file_path = os.path.relpath(os.path.join(root,file), path)
            ziph.write(os.path.join(root, file), arch_file_path)


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/generate', methods=['GET','POST'])
def generate():
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
        
        ad_name = str(ad_params["width"])+ "x" + str(ad_params["height"])
        ad_path = OUTPUT_DIR + ad_name
        
        if not os.path.exists(ad_path):
            os.makedirs(ad_path)
            
        env.get_template('ad_base.html').stream(ad_params=ad_params).dump(ad_path + "/index.html")
        env.get_template('ad_main.js').stream(ad_params=ad_params).dump(ad_path + "/main.js")
        env.get_template('ad_style.css').stream(ad_params=ad_params).dump(ad_path + "/style.css")
        
        zipped_ad = zipfile.ZipFile(ad_path+'.zip', 'w', zipfile.ZIP_DEFLATED)
        zipdir(ad_path+'/', zipped_ad)
        zipped_ad.close()
        
        return redirect(url_for('success',filename=ad_name+'.zip'))
    
    else:
        return redirect(url_for('index'))
    
    
@app.route('/success/<filename>')
def success(filename):
    return render_template('success.html',filename=filename)


@app.route('/download/<filename>')
def download(filename):
    try:
        return send_file(OUTPUT_DIR+filename, attachment_filename=filename, as_attachment=True)
    except Exception as e:
        return str(e)