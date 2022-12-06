import os      # For File Manipulations like get paths, rename
from flask import Flask, flash, request, redirect, render_template, url_for
from werkzeug.utils import secure_filename
from fileinput import filename
from zipfile import ZipFile
# <<<<<<< HEAD
import CWS_API
import scan
# >>>>>>> cbcc4ee8b36e1e54d42017d9a1fc70f29ba66876
import crx_downloader
import time
import glob


import base64
from io import BytesIO
import matplotlib.pyplot as Figure
import mongo_API
from datetime import datetime
import hashlib







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
        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            file.save(os.path.join(app.config['UPLOAD_CRX_FOLDER'], filename))
        else:
            flash('Only crx files')
            return redirect('/')
        flash('File successfully uploaded')
        return render_template('loading.html')



@app.route('/results', methods=['POST', 'GET'])
def results():
    path = max(glob.iglob(app.config['UPLOAD_CRX_FOLDER']+'/*'),key=os.path.getctime)
    with open(path,"rb") as f:
        bytes = f.read() # read entire file as bytes
        readable_hash = hashlib.sha256(bytes).hexdigest();
    exist = mongo_API.getByHash(readable_hash)
    if( exist == None):

        extension_id= path.split('/')[-1]
        # path2 = max(glob.iglob(app.config['UPLOAD_FOLDER'] + '/'+extension_id),key=os.path.getctime)
        if not extension_id.split('.')[-1] == 'crx':
            extension_info = CWS_API.get_item(extension_id)
            for i in range(len(extension_info)):
                if len(extension_info) > 1:
                    extension_info.pop()
            print(extension_info)
            meta = {"cwsId":extension_id, "name": extension_info[0][1]}
            scan.scan(path, meta)
            result, test = pie(path)
            history_img = history(extension_id)
            return render_template("results.html", extension_info = extension_info ,result = result,test = test, test2 = history_img )
        else:
            meta = {"cwsId":"None", "name": extension_id}
            result = scan.scan(path, meta)
            return render_template("results.html", result=result)
    else:
        extension_id= path.split('/')[-1]
        extension_info = CWS_API.get_item(extension_id)
        result, test = pie(path)
        history_img = history(extension_id)
        print('########################')
        return render_template("results.html", result = exist, extension_info = extension_info,test = test, test2 = history_img)

@app.route('/search', methods=['POST', 'GET'])
def search():
    """ Takes a search term and returns a list of search results to the Web UI"""
    if request.method == 'POST':
        extension_name = request.form.get('search')
        if not extension_name:
            flash('No input')
            return redirect('/')
        extension_ifo_list = CWS_API.get_item(extension_name)
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
    print(CWS_API.autocomplete(output))
    suggest_list = CWS_API.autocomplete(output);
    return suggest_list

@app.route('/analyze', methods=['POST', 'GET'])
def analyze():
    """ Takes in the request Extension from the list that tha search() funktion returns and downloads it under crxuploads folder
    anzips the file and save it under uploads folder
    scans the file and the unzipd folder in virustotal and retireJS
    returen: loading.html
     """
    if request.method == 'POST':
        extension_name = request.form.get('extension_name')
        crx_downloader.download_crx(extension_name)
        return render_template('loading.html')


def pie(filename):
    # filename = input("Enter the input file name: ")
    with open(filename,"rb") as f:
        bytes = f.read() # read entire file as bytes
        readable_hash = hashlib.sha256(bytes).hexdigest();
    print(readable_hash)
    result = mongo_API.getByHash(readable_hash)
    labels = []
    sizes = []
    explode = []
    vtResult = dict(result["virusTotal"])
    vtTotal = result["virusTotalSum"]

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
    # print(data)
    # test = 'data:image/png;base64,'+data+"'"
    # return test
    return result, f"data:image/png;base64,{data}"

def history(id):

    result = list(mongo_API.getById(id))

    dates = []
    risks = []
    for object in result:
        #adds just the date as time isn't that important and cuts the first two numbers of the year
        dates.append(str(object['meta']["date"]).split()[0][2:])
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

    return f"data:image/png;base64,{data}"

if __name__ == "__main__":
    app.run(host='127.0.0.1',port=5000,debug=True,threaded=True)
