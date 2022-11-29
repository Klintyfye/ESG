import os      # For File Manipulations like get paths, rename
from flask import Flask, flash, request, redirect, render_template, url_for
from werkzeug.utils import secure_filename
from fileinput import filename
from zipfile import ZipFile
import retireJS 
import virustotal 
import api 
import crx_downloader
import time

app=Flask(__name__)
app.secret_key = "juvsnpqb##?+`okojpj##¤¤%&#pakia" # for encrypting the sessions
#It will allow below 250MB contents only, you can change it
app.config['MAX_CONTENT_LENGTH'] = 250 * 1024 * 1024
path = os.getcwd()
# file Upload
UPLOAD_CRX_FOLDER = os.path.join(path, 'crxuploads')
# Make directory if "uploads" folder not exists
if not os.path.isdir(UPLOAD_CRX_FOLDER):
    os.mkdir(UPLOAD_CRX_FOLDER)
app.config['UPLOAD_CRX_FOLDER'] = UPLOAD_CRX_FOLDER
#unzipd crxfile folder
UPLOAD_FOLDER = os.path.join(path, 'uploads')
# Make directory if "uploads" folder not exists
if not os.path.isdir(UPLOAD_FOLDER):
    os.mkdir(UPLOAD_FOLDER)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
ALLOWED_EXTENSIONS = set(['crx'])
def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS
    


@app.route('/')
def upload_form():
    """Rendering the upload.html file"""
    return render_template('upload.html')

@app.route('/loading')
def loading():
    return render_template('loading.html')

@app.route('/upload', methods=['POST', 'GET'])
def upload_file():
    """Takes in the uploaded file and save it under crxuploads folder 
    anzips the file and save it under uploads folder 
    scans the file and the unzipd folder in virustotal and retireJS
    returen: INTE KLAR ÄN 
    """
    if request.method == 'POST':
        file = request.files['crxfile']
        if not file:
            flash('No file uploaded!')
            return redirect('/')
        start_time = time.time()
        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            file.save(os.path.join(app.config['UPLOAD_CRX_FOLDER'], filename))
            path = os.path.join(app.config['UPLOAD_CRX_FOLDER'], filename)
            with ZipFile(path) as crx_unzip:
            # Extracting all the members of the zip 
            # into a specific location.
                crx_unzip.extractall(
                    path = os.path.join(app.config['UPLOAD_FOLDER'], filename))
            path2 = os.path.join(app.config['UPLOAD_FOLDER'], filename)
            virustotal.virustotal(path)
            retireJS.retireJS(path2)
        else:
            flash('Only crx files')
            return redirect('/')
        endtime = (time.time() - start_time)
        flash('File successfully uploaded')
        return redirect('/loading')


@app.route('/search', methods=['POST', 'GET'])
def search():
    """ Takes a search term and returns a list of search results to the Web UI"""
    if request.method == 'POST':
        extension_name = request.form.get('search')
        if not extension_name:
            flash('No input')
            return redirect('/')
        extension_ifo_list = api.get_item(extension_name)
        if extension_ifo_list == []:
            flash('No extensions found')
            return redirect('/')
        for i in range(len(extension_ifo_list)):
            extension_ifo_list[i][5] = round(extension_ifo_list[i][5],1)

        return render_template('upload.html', content = extension_ifo_list )
    

@app.route('/analyze', methods=['POST', 'GET'])
def analyze():
    """ Takes in the request Extension from the list that tha search() funktion returns and downloads it under crxuploads folder 
    anzips the file and save it under uploads folder 
    scans the file and the unzipd folder in virustotal and retireJS
    returen: INTE KLAR ÄN 
     """
    if request.method == 'POST':
        start_time = time.time()
        extension_name = request.form.get('extension_name')
        name = extension_name.split('/')[-2]
        if not os.path.isfile(os.path.join(app.config['UPLOAD_CRX_FOLDER'], name+'.crx')):
            crx_downloader.download_crx(extension_name)
            path = os.path.join(app.config['UPLOAD_CRX_FOLDER'], name+'.crx')
            with ZipFile(path) as crx_unzip:
            # Extracting all the members of the zip 
            # into a specific location.
                crx_unzip.extractall(
                    path = os.path.join(app.config['UPLOAD_FOLDER'], name+'.crx'))
            path2 = os.path.join(app.config['UPLOAD_FOLDER'], name+'.crx')
            virustotal.virustotal(path)
            retireJS.retireJS(path2)
        else:
            path = os.path.join(app.config['UPLOAD_CRX_FOLDER'], name+'.crx')
            path2 = os.path.join(app.config['UPLOAD_FOLDER'], name+'.crx')
            virustotal.virustotal(path)
            retireJS.retireJS(path2)
        endtime = (time.time() - start_time)
        print(endtime)
        flash('File successfully uploaded')
        return render_template('loading.html')

if __name__ == "__main__":
    app.run(host='127.0.0.1',port=5000,debug=True,threaded=True)    