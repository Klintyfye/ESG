import os      # For File Manipulations like get paths, rename
from flask import Flask, flash, request, redirect, render_template, url_for
from werkzeug.utils import secure_filename
from fileinput import filename
import time
# <<<<<<< HEAD
import CWS_API
import scan
# >>>>>>> cbcc4ee8b36e1e54d42017d9a1fc70f29ba66876
import crx_downloader
import glob
import base64
from io import BytesIO
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as Figure
import mongo_API
import hashlib
import json

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
extension_file_path= []
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
            path = os.path.join(app.config['UPLOAD_CRX_FOLDER'], filename)
            #Get hash of crx
            with open(path,"rb") as f:
                bytes = f.read() # read entire file as bytes
            readable_hash = hashlib.sha256(bytes).hexdigest()
            #Check if extension already exists in database
            hash_exist = mongo_API.get_by_hash(readable_hash)
            #if extension is NOT in database
            if hash_exist == None:
                return render_template('loading.html')
            else:
            #if extension is in database
                return render_template('loading.html', in_db = 'yes')
        #If file is not of allowed type, flash error and cancel
        else:
            flash('Only crx files')
            return redirect('/')



@app.route('/results', methods=['POST', 'GET'])
def results():
    if request.method == 'POST':
        response = request.form.get('response') 
        hash =  request.form.get('hash')
    if extension_file_path != []:
        crx_downloader.download_crx(extension_file_path[0])
        path = os.path.join(app.config['UPLOAD_CRX_FOLDER'], extension_file_path[0].split('/')[-1])
        extension_file_path.pop()
        with open(path,"rb") as f:
            bytes = f.read() # read entire file as bytes
            readable_hash = hashlib.sha256(bytes).hexdigest()
            hash_exist = mongo_API.get_by_hash(readable_hash)
            #if extension is NOT in database
            if hash_exist != None:
                return render_template('loading.html', in_db = 'yes')
    #Chose most recently uploaded crx as path
    path = max(glob.iglob(app.config['UPLOAD_CRX_FOLDER']+'/*'),key=os.path.getctime)
    with open(path,"rb") as f:
            bytes = f.read() # read entire file as bytes
            readable_hash = hashlib.sha256(bytes).hexdigest()
    #Get extension id
    extension_id= path.split('/')[-1]
    #Check the response
    if (response == 'Yes' or response == None) and (hash == None):
    #Extension id NOT ending in "crx" signifies CWS
        if extension_id.split('.')[-1] != 'crx':
            extension_info = CWS_API.get_item(extension_id)
            if len(extension_info) > 1:
                for i in range(len(extension_info)):
                    if extension_id == (extension_info[i][0].split('/')[-1]):
                        extension_info = [extension_info[i]]
                        break
                    else:
                        pass
            #Gathers metadata of extension
            meta = {"cwsId":extension_id, "name": extension_info[0][1]}
            #Scans crx
            result = scan.scan(path, meta)
            #Creates charts of file and history
            result_db, test, labels, colors = pie(readable_hash)
            history_img = history(extension_id)
            previous_hash=[]
            previous_extensions=mongo_API.get_by_id(extension_id)
            for extension in previous_extensions:
                previous_hash.append(extension["hash"])
            # Parse result
            file_path_list, vul_name_list, info_list, severity_list, summary_list, CVE_list = adv_view_data(str(result_db))
            #Renders result
            return render_template("results.html", previous_hash=previous_hash, extension_info = extension_info , result=zip(file_path_list, vul_name_list, info_list, severity_list, summary_list, CVE_list), test = test, test2 = history_img, lables_colors=zip(labels, colors))

        #Extension id ending in "crx" signifies local upload
        else:
            #Gathers metadata of extension
            meta = {"cwsId":"None", "name": extension_id}
            #Scans crx
            result = scan.scan(path, meta)
            #Creates pie chart
            result_db, test , labels, colors = pie(readable_hash)
            # Parse result
            file_path_list, vul_name_list, info_list, severity_list, summary_list, CVE_list = adv_view_data(str(result_db))
            #Renders result
            return render_template("results.html", result=zip(file_path_list, vul_name_list, info_list, severity_list, summary_list, CVE_list), test = test, lables_colors=zip(labels, colors), extension_name = extension_id)
    elif hash:
        result = mongo_API.get_by_hash(hash)
        extension_info = CWS_API.get_item(result['meta']['cwsId'])
        #Creates charts of file and history
        result_db, test, labels, colors = pie(hash)
        history_img = history(result['meta']['cwsId'])
        previous_hash=[]
        previous_extensions=mongo_API.get_by_id(result['meta']['cwsId'])
        for extension in previous_extensions:
            previous_hash.append(extension["hash"])
        # Parse result
        file_path_list, vul_name_list, info_list, severity_list, summary_list, CVE_list = adv_view_data(str(result_db))
        return render_template("results.html",previous_hash=previous_hash, result=zip(file_path_list, vul_name_list, info_list, severity_list, summary_list, CVE_list), extension_info = extension_info ,test = test, test2 = history_img, lables_colors=zip(labels, colors))

    else:
        #Extension id NOT ending in "crx" signifies CWS
        if extension_id.split('.')[-1] != 'crx':
            extension_id= path.split('/')[-1]
            extension_info = CWS_API.get_item(extension_id)
            if len(extension_info) > 1:
                for i in range(len(extension_info)):
                    if extension_id == (extension_info[i][0].split('/')[-1]):
                        extension_info = [extension_info[i]]
                        break
                    else:
                        pass
            #Creates charts of file and history
            result_db, test, labels, colors = pie(readable_hash)
            history_img = history(extension_id)
            previous_hash=[]
            previous_extensions=mongo_API.get_by_id(extension_id)
            for extension in previous_extensions:
                previous_hash.append(extension["hash"])
            # Parse result
            file_path_list, vul_name_list, info_list, severity_list, summary_list, CVE_list = adv_view_data(str(result_db))
            return render_template("results.html",previous_hash=previous_hash, result=zip(file_path_list, vul_name_list, info_list, severity_list, summary_list, CVE_list), extension_info = extension_info ,test = test, test2 = history_img, lables_colors=zip(labels, colors))
        #Extension id ending in "crx" signifies local upload
        else:
            #Creates pie chart
            result_db, test, labels, colors = pie(readable_hash)
            # Parse result
            file_path_list, vul_name_list, info_list, severity_list, summary_list, CVE_list = adv_view_data(str(result_db))
            #Renders result
            return render_template("results.html", result=zip(file_path_list, vul_name_list, info_list, severity_list, summary_list, CVE_list), test = test, lables_colors=zip(labels, colors), extension_name = extension_id)
    
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
    #append the extension file path  to the extension_file_path list
    extension_file_path.append(extension_name)
    return render_template('loading.html')

def pie(hash):
    result = mongo_API.get_by_hash(hash)

    labels = []
    sizes = []
    explode = []
    vt_result = dict(result["virusTotal"])
    vt_total = result["virusTotalSum"]

    #Iterates through vt results and adds correct values labels, sizes, and explode
    for key in vt_result:
        val = vt_result[key]
        #Sets useful label: type \n (percent, nr)
        labels.append(f"{key}: {round(val/vt_total*100,1)}%, ({val} engines )")
        sizes.append(vt_result[key])
        #highlight slices if they are malicious or supicious
        if key in ["malicious", "suspicious"]:
            explode.append(0.1)
        else:
            explode.append(0)

    fig, ax = Figure.subplots()
    #define chart

    colors = ['#66b032', '#fb9902', '#fefe33', '#347c98', '#0247fe', '#8601af', '#fe2712', '#b2d732']

    ##########HÄR SÄTTS LABELS!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!! labels = labels
    #Skulle man kanske kunna lägga till labels som något typ av attribut till
    #den nuvarande returnsatsen som ger bilden? Ser inte hur man kan skicka
    #informationen till html, mid python funktion utan att avbryta med return.
    ax.pie(sizes, explode = explode, startangle=45,
    wedgeprops={'linewidth': 1.0, 'edgecolor': 'white'}, colors = colors)

    ax.axis('equal')
    ax.set_aspect(1.0/ax.get_data_ratio(), adjustable='box')
    # Save it to a temporary buffer.
    buf = BytesIO()
    Figure.savefig(buf, format="png", bbox_inches="tight", transparent=True)

    # Embed the result in the html output.
    data = base64.b64encode(buf.getbuffer()).decode("ascii")
    return result, f"data:image/png;base64,{data}", labels, colors

def history(id):
    result = list(mongo_API.get_by_id(id))

    dates = []
    risks = []
    for object in result:
        #adds just the date as time isn't that important and cuts the first two numbers of the year
        dates.append(str(object["meta"]["date"]).split()[0][2:])
        risks.append(object["retireSeverity"])


    #zip the lists to a touple list
    zipped = zip(risks,dates)
    zipped = list(zipped)

    #Sorts risks dependant on the order of dates
    sort = sorted(zipped, key = lambda x: x[1])

    #reset risks and dates
    risks = []
    dates = []
    #Re-add them in order
    for item in sort:
        risks.append(item[0])
        dates.append(item[1])

    fig, ax = Figure.subplots()
    #define chart

    #Setup value lists for risks
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

    #Plot every function for the risks after dates.
    ax.plot(dates, none, '#a5a5a5')
    ax.plot(dates, low, '#3b85c2')
    ax.plot(dates, medium, '#f18740')
    ax.plot(dates, high, '#ca1f1f')
    ax.plot(dates, critical, '#812094')
    ax.legend(["none","low","medium","high","critical"])
    ax.set_xlabel("Time")
    ax.set_ylabel("Risks")
    ax.set_aspect(1.0/ax.get_data_ratio(), adjustable='box')
    ax.plot('r')
    # Save it to a temporary buffer.
    buf = BytesIO()
    Figure.savefig(buf, format="png", bbox_inches="tight", transparent=True)

    # Embed the result in the html output.
    data = base64.b64encode(buf.getbuffer()).decode("ascii")

    return f"data:image/png;base64,{data}"

def adv_view_data(result):
    result = result.replace("'", '"')

    alist = json.loads(result)

    file_path_list = []
    vul_name_list = []
    info_list = []
    severity_list = []
    summary_list = []
    CVE_list = []

    for i in range(len(alist["retireJs"])):
        for j in range(len(alist["retireJs"][i]["results"][0]["vulnerabilities"])):
            file_path_list.append(alist["retireJs"][i]["file"])
            vul_name_list.append(alist["retireJs"][i]["results"][0]["component"] + " " + alist["retireJs"][i]["results"][0]["version"])
            info_list.append(alist["retireJs"][i]["results"][0]["vulnerabilities"][j]["info"])
            severity_list.append(alist["retireJs"][i]["results"][0]["vulnerabilities"][j]["severity"])
            summary_list.append(alist["retireJs"][i]["results"][0]["vulnerabilities"][j]["identifiers"]["summary"])
            try:
                temp = alist["retireJs"][i]["results"][0]["vulnerabilities"][j]["identifiers"]["CVE"][0]
            except:
                print("no CVE")
            else:
                CVE_list.append(temp)
    return file_path_list, vul_name_list, info_list, severity_list, summary_list, CVE_list

if __name__ == "__main__":
    app.run(host='127.0.0.1',port=5000,debug=True,threaded=True)