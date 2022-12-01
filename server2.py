import os      # For File Manipulations like get paths, rename
from flask import Flask, flash, request, redirect, render_template, url_for
from werkzeug.utils import secure_filename
from fileinput import filename
from zipfile import ZipFile
# <<<<<<< HEAD
import retireJS 
import virustotal
import api 
# =======
import retireJS
import virustotal
import api
import CWS_api
# >>>>>>> cbcc4ee8b36e1e54d42017d9a1fc70f29ba66876
import crx_downloader
import time
import glob






import base64
from io import BytesIO
import matplotlib.pyplot as Figure
import mongoAPI
from datetime import datetime








app=Flask(__name__, template_folder='Templates/')
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
            # path2 = os.path.join(app.config['UPLOAD_FOLDER'], filename)
            # virustotal.virustotal(path)
            # retireJS.retireJS(path2)
        else:
            flash('Only crx files')
            return redirect('/')
        endtime = (time.time() - start_time)
        flash('File successfully uploaded')
        return render_template('loading.html')



@app.route('/results', methods=['POST', 'GET'])
def results():
    path = max(glob.iglob(app.config['UPLOAD_CRX_FOLDER']+'/*.crx'),key=os.path.getctime)
    extension_name= path.split('/')[-1]
    path2 = max(glob.iglob(app.config['UPLOAD_FOLDER'] + '/'+extension_name),key=os.path.getctime)
    print(path, '\n', path2, '\n', extension_name )
    virustotal.virustotal(path)
    retireJS.retireJS(path2)
    # print(extension_name.split('.')[0])
    # extension_info = api.get_item(extension_name.split('.')[0])
    # print(extension_info)
    return render_template("results.html")

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

@app.route("/auto_complete", methods=["POST"])
def auto_complete():
    output = request.get_json()
    print(output)
    print(CWS_api.autocomplete(output))
    suggest_list = CWS_api.autocomplete(output);
    return suggest_list

@app.route('/analyze', methods=['POST', 'GET'])
def analyze():
    """ Takes in the request Extension from the list that tha search() funktion returns and downloads it under crxuploads folder
    anzips the file and save it under uploads folder
    scans the file and the unzipd folder in virustotal and retireJS
    returen: INTE KLAR ÄN
     """
    if request.method == 'POST':
        # start_time = time.time()
        extension_name = request.form.get('extension_name')
        name = extension_name.split('/')[-2]
        # if not os.path.isfile(os.path.join(app.config['UPLOAD_CRX_FOLDER'], name+'.crx')):
        crx_downloader.download_crx(extension_name)
        path = os.path.join(app.config['UPLOAD_CRX_FOLDER'], name+'.crx')
        with ZipFile(path) as crx_unzip:
        # Extracting all the members of the zip
        # into a specific location.
            crx_unzip.extractall(
                path = os.path.join(app.config['UPLOAD_FOLDER'], name+'.crx'))
            # path2 = os.path.join(app.config['UPLOAD_FOLDER'], name+'.crx')

            # virustotal.virustotal(path)
            # retireJS.retireJS(path2)
        # else:
            # path = os.path.join(app.config['UPLOAD_CRX_FOLDER'], name+'.crx')
            # path2 = os.path.join(app.config['UPLOAD_FOLDER'], name+'.crx')
            # virustotal.virustotal(path)
            # retireJS.retireJS(path2)
        # endtime = (time.time() - start_time)
        # print(endtime)
        flash('File successfully uploaded')
        return render_template('loading.html')


@app.route("/pie")
def pie():

    result = mongoAPI.getByHash("0d1018ff158a9ac8e6654e4325edf5bc165a095cf2381d87ba018814ec618d13")
    
    labels = []
    sizes = []
    explode = []
    vtResult = dict(result["document"]["virusTotal"])
    vtTotal = result["document"]["virusTotalSum"]

    #Iterates through vt results and adds correct values labels, sizes, and explode
    for key in vtResult:
        #If no engines flagged don't include in pie chart
        if vtResult[key] > 0:
            val = vtResult[key]
            #Sets useful label: type \n (percent, nr)
            labels.append(f"{key}\n({round(val/vtTotal*100,1)}%, {val})")
            sizes.append(vtResult[key])
            #highlight slices if they are malicious or supicious
            if key in ["malicious", "suspicious"]:
                explode.append(0.1)
            else:
                explode.append(0)

    fig, ax = Figure.subplots()
    #define chart
    ax.pie(sizes, labels = labels, explode = explode, startangle=45,
    wedgeprops={'linewidth': 1.0, 'edgecolor': 'white'})


    ax.axis('equal')
    # Save it to a temporary buffer.
    buf = BytesIO()
    Figure.savefig(buf, format="png")

    # Embed the result in the html output.
    data = base64.b64encode(buf.getbuffer()).decode("ascii")

    return f"<img src='data:image/png;base64,{data}'/>"

@app.route("/history")
def history():
    
    result = list(mongoAPI.getById("123")["documents"])
    
    dates = []
    risks = []
    for object in result:
        #adds just the date as time isn't that important and cuts the first two numbers of the year
        dates.append(str(object["date"]).split()[0][2:])
        risks.append(int(object["risk"]))
    
    #Sorts risks dependant on the order of dates
    #zip the lists to a touple list
    ziped = zip(dates,risks)
    #Sort 
    sort = sorted(ziped)
    temp = []
    #add risks to empty list in order of after they've been sorted by dates
    for i in sort:
       temp.append(i[1]) 
    #overwrite risks with sorted version
    risks = temp

    #
    #sort dates
    dates.sort()
    
    fig, ax = Figure.subplots()
    #define chart

    ax.plot(dates, risks)
    ax.set_xlabel("Time")
    ax.set_ylabel("Risk")
    # Save it to a temporary buffer.
    buf = BytesIO()
    Figure.savefig(buf, format="png")

    # Embed the result in the html output.
    data = base64.b64encode(buf.getbuffer()).decode("ascii")

    return f"<img src='data:image/png;base64,{data}'/>"

if __name__ == "__main__":
    app.run(host='127.0.0.1',port=5000,debug=True,threaded=True)
