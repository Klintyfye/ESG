import os      # For File Manipulations like get paths, rename
from flask import Flask, flash, request, redirect, render_template, url_for
from werkzeug.utils import secure_filename
from fileinput import filename
# <<<<<<< HEAD
import CWS_API
import scan
# >>>>>>> cbcc4ee8b36e1e54d42017d9a1fc70f29ba66876
import crx_downloader
import glob
import base64
from io import BytesIO
import matplotlib.pyplot as Figure
import mongo_API
import hashlib

#????????????????????????
app=Flask(__name__, template_folder='Templates/')

#Secret key for encrypting sessions
app.secret_key = "juvsnpqb##?+`okojpj##¤¤%&#pakia"

#It will allow below 250MB contents only, you can change it
app.config['MAX_CONTENT_LENGTH'] = 250 * 1024 * 1024

#Get current working directory
path = os.getcwd()
"""current workign directory"""

#Sets path of crx upload folder
UPLOAD_CRX_FOLDER = os.path.join(path, 'crxuploads')
"""crx upload folder directory"""
#Make directory if "uploads" folder not exists
if not os.path.isdir(UPLOAD_CRX_FOLDER):
    os.mkdir(UPLOAD_CRX_FOLDER)
app.config['UPLOAD_CRX_FOLDER'] = UPLOAD_CRX_FOLDER

#Unzipped crxfile folder
UPLOAD_FOLDER = os.path.join(path, 'uploads')
"""unzipped upload folder directory"""
#Make directory if "uploads" folder not exists
if not os.path.isdir(UPLOAD_FOLDER):
    os.mkdir(UPLOAD_FOLDER)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

#Sets allowed file extension
ALLOWED_EXTENSIONS = set(['crx'])
def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

#Renders upload html as root page
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

    #Checks request method. If not post, don't do anything
    if request.method == 'POST':
        #Read file by filename from html
        file = request.files['crxfile']
        #Cancel if no file was uploaded
        if not file:
            flash('No file uploaded!')
            return redirect('/')

        #If allowed file was upploaded get the name and save the file.
        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            file.save(os.path.join(app.config['UPLOAD_CRX_FOLDER'], filename))
        #If file is not of allowed type, flash error and cancel
        else:
            flash('Only crx files')
            return redirect('/')

        #If everything was successful move on to loading.html
        flash('File successfully uploaded')
        return render_template('loading.html')


@app.route('/results', methods=['POST', 'GET'])
def results():
    #Chose most recently uploaded crx as path
    path = max(glob.iglob(app.config['UPLOAD_CRX_FOLDER']+'/*'),key=os.path.getctime)
    """path to crx"""
    #Get hash of crx
    with open(path,"rb") as f:
        bytes = f.read() # read entire file as bytes
        readable_hash = hashlib.sha256(bytes).hexdigest()

    #Check if extension already exists in database
    exist = mongo_API.getByHash(readable_hash)

    #if extension is NOT in database
    if exist == None:
        #Get extension id
        extension_id= path.split('/')[-1]

        #Extension id NOT ending in "crx" signifies CWS
        if extension_id.split('.')[-1] != 'crx':
            extension_info = CWS_API.get_item(extension_id)

            #Gathers metadata of extension
            meta = {"cwsId":extension_id, "name": extension_info[0][1]}

            #Scans crx
            scan.scan(path, meta)

            #Creates charts of file and history
            result, test = pie(path)
            history_img = history(extension_id)

            #Renders result
            return render_template("results.html", extension_info = extension_info[0] ,result = result,test = test, test2 = history_img )

        #Extension id ending in "crx" signifies local upload
        else:
            #Gathers metadata of extension
            meta = {"cwsId":"None", "name": extension_id}

            #Scans crx
            result = scan.scan(path, meta)

            #Creates pie chart
            result, test = pie(path)

            #Renders result
            return render_template("results.html", result = result)

    #if extension is already in database
    else:

        #Get extension id
        extension_id= path.split('/')[-1]
        extension_info = CWS_API.get_item(extension_id)

        #Creates charts of file and history
        result, test = pie(path)
        history_img = history(extension_id)

        print('########################')

        return render_template("results.html", result = exist, extension_info = extension_info,test = test, test2 = history_img)

@app.route('/search', methods=['POST', 'GET'])
def search():
    """ Takes a search term and returns a list of search results to the Web UI"""

    #Checks request method. If not post, don't do anything
    if request.method == 'POST':
        extension_name = request.form.get('search')

        #Cancel if no extension name
        if not extension_name:
            flash('No input')
            return redirect('/')

        extension_info_list = CWS_API.get_item(extension_name)

        #If item extension does not exist cancel
        if extension_info_list == []:
            flash('No extensions found')
            return redirect('/')

        #Saves list of extensions
        for i in range(len(extension_info_list)):
            extension_info_list[i][5] = round(extension_info_list[i][5],1)

        return render_template('upload.html', content = extension_info_list )

@app.route("/auto_complete", methods = ["POST"])
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
    vt_result = dict(result["virusTotal"])
    vt_total = result["virusTotalSum"]

    #Iterates through vt results and adds correct values labels, sizes, and explode
    for key in vt_result:
        #If no engines flagged don't include in pie chart
        if vt_result[key] > 0:
            val = vt_result[key]
            #Sets useful label: type \n (percent, nr)
            labels.append(f"{key}\n({round(val/vt_total*100,1)}%, {val})")
            sizes.append(vt_result[key])
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
    return result, f"data:image/png;base64,{data}"

def history(id):
    result = list(mongo_API.getById(id))

    dates = []
    risks = []
    for object in result:
        #adds just the date as time isn't that important and cuts the first two numbers of the year
        dates.append(str(object["meta"]["date"]).split()[0][2:])
        risks.append(int(object["retireSeverity"]))

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

    #sort dates
    dates.sort()

    fig, ax = Figure.subplots()
    #define chart

    #
    none = []
    low = []
    medium = []
    high = []
    critical = []
    for x in risks:
        none.append(x["none"])
        low.append(x["low"])
        medium.append(x["medium"])
        high.append(x["high"])
        critical.append(x["critical"])

    ax.plot(dates, none, label="none")
    ax.plot(dates, low, label="low")
    ax.plot(dates, medium, label="medium")
    ax.plot(dates, high, label="high")
    ax.plot(dates, critical, label="critical")

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
