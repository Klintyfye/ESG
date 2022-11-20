import os      # For File Manipulations like get paths, rename
from flask import Flask, flash, request, redirect, render_template
from werkzeug.utils import secure_filename
import json
from fileinput import filename
import requests
import time
from zipfile import ZipFile


app=Flask(__name__)
app.secret_key = "secret key" # for encrypting the session
#It will allow below 16MB contents only, you can change it
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
def virustotal( path):
    path = path
    url_for_large_file()
    url_for_upload(path)
    url_for_analysis_report(path)
    url_for_analysis_report_from_hash(path)
    if_file_queued(path)
#path = "C:/Users/saifa/OneDrive/Dokument/DV1512/projekt_code/flask/uploadeZip.zip"
# path = "/mnt/c/Users/saifa/OneDrive/Dokument/DV1512/projekt_code/flask/uploadeZip.zip"


def url_for_large_file():

    url_for_large_files = "https://www.virustotal.com/api/v3/files/upload_url"
    refined_url = ""
    cnt = 15
    first_header = {
        "accept": "application/json",
        "x-apikey": "51bff97d51ac2996b0b64155402f55cc8960cdfbfcd3f5361eff4fd9f2dc65b2"
    }
    
    first_second_response = requests.get(url_for_large_files, headers=first_header)
    while (first_second_response.text[cnt] != '"'):
        refined_url += first_second_response.text[cnt]
        cnt += 1
    time.sleep(3)
    return refined_url
    

def url_for_upload(path):
    url_for_upload = url_for_large_file()
    files = {"file": open(path, "rb")}
    second_header = {
        "accept": "application/json",
        "x-apikey": "4926e23cc9acaa6110047cd35fa667a46e8acf4c889d5d7881e8859008df4e3c"
    }

    second_response = requests.post(url_for_upload, files=files, headers=second_header)

    check = True
    stringedRes = ""
    stringresp = second_response.text

    for i in range(len(stringresp)):
        if stringresp[i] == "i" and stringresp[i+1] == "d":
            i = i+5
            while check:
                if stringresp[i+1] == '"':
                    check = False
                    break
                stringedRes = stringedRes + stringresp[i+1]
                i = i+1
    #print(url_for_upload)
    time.sleep(5)
    #print(stringedRes)
    return stringedRes
    

def url_for_analysis_report(path):
    rest_of_string = url_for_upload(path)
    url_for_analysis_report = "https://www.virustotal.com/api/v3/analyses/"+rest_of_string
    fourth_header = {
        "accept": "application/json",
        "x-apikey": "d16649ccb180832552aa0a0d6a91b57103da5fd1a6d979cda653401f301185e6"
    }
    third_response = requests.get(url_for_analysis_report, headers=fourth_header)
    json_data = json.loads(third_response.text)
    return json_data
    
def if_file_queued(path):
    switch = True
    while switch:
        info = url_for_analysis_report(path)
        if info["data"]["attributes"]["status"] == "completed":
            switch = False
            break
        print("Process is in queue, please wait...")
        time.sleep(5) 
            
        


    filename = "virustotal_output.json"
    sha256_value = info["meta"]["file_info"]["sha256"]
    #print(sha256_value)
    with open(filename, "w") as file_object:
        json.dump(info, file_object)
        

    
        
    #time.sleep(3)
    return sha256_value
    
    

def url_for_analysis_report_from_hash(path):
    sha256 = if_file_queued(path)
    url_for_analysis_hash = "https://www.virustotal.com/api/v3/files/"+sha256
    fourth_header = {
        "accept": "application/json",
        "x-apikey": "51bff97d51ac2996b0b64155402f55cc8960cdfbfcd3f5361eff4fd9f2dc65b2"
    }

    fourth_response= requests.get(url_for_analysis_hash, headers=fourth_header)
    json_data1 = json.loads(fourth_response.text)
    #print(json_data1)
    filename = "virustotal_output.json"
    with open(filename, "w") as file_object:
       json.dump(json_data1, file_object)

    
def retireJS(path2):
    path = path2
    print("Scanning, please wait...")

    os.system("retire --outputpath temp.json --outputformat json --path " + path)
    print("Scan successful!")

    print("\nCleaning, please wait...")

    f = open("humanOutput.txt", "w")
    with open("temp.json") as json_file:
        file = json.load(json_file)
        
        # Print the file of dictionary
        for object in file["data"]:
            f.write("////////////////////////////\n")
            f.write("Vulnerable file:"+ object["file"]+"\n")
            for results in object["results"]:
                f.write("\tComponent:"+ results["component"]+"\n")
                for vulnerabilities in results["vulnerabilities"]:
                    f.write("\t\tSummary:"+ vulnerabilities["identifiers"]["summary"]+"\n")
                    f.write("\t\t\tCVE:"+ vulnerabilities["identifiers"]["CVE"][0]+"\n")
                    f.write("\t\t\tSeverity:"+ vulnerabilities["severity"]+"\n")

    f.close()
    print("Clean successful!")

@app.route('/')
def upload_form():
    return render_template('upload.html')


@app.route('/', methods=['POST'])
def upload_file():
    if request.method == 'POST':
        file = request.files['files[]']
        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            file.save(os.path.join(app.config['UPLOAD_CRX_FOLDER'], filename))
        path = os.path.join(app.config['UPLOAD_CRX_FOLDER'], filename)
        print(path)
        with ZipFile(path) as crx_unzip:
        # Extracting all the members of the zip 
        # into a specific location.
            crx_unzip.extractall(
                path = os.path.join(app.config['UPLOAD_FOLDER'], filename))
        path2 = os.path.join(app.config['UPLOAD_FOLDER'], filename)
      
        virustotal(path)
        retireJS(path2)
        flash('Folder successfully uploaded')
        return redirect('/')

# @app.route('/analyze', methods=['POST', 'GET'])
# def analys():
#      if request.method == 'POST':
#         extension_name = request.form.get('extension_name')
#         print(extension_name)
#         crx_downloader.download_crx(extension_name)
#         name = extension_name
#         # print(name[5])
#         path = os.path.join(app.config['UPLOAD_CRX_FOLDER'], name[5]+'.crx')
#         with ZipFile(path) as crx_unzip:
#         # Extracting all the members of the zip 
#         # into a specific location.
#             crx_unzip.extractall(
#                 path = os.path.join(app.config['UPLOAD_FOLDER'], name[5]+'.crx'))
#         path2 = os.path.join(app.config['UPLOAD_FOLDER'], name[5]+'.crx')
#         # print(path2)
#         virustotal.virustotal(path)
#         retireJS.retireJS(path2)
#         flash('File successfully uploaded')

# crx_downloader.download_crx(extension_ifo_list[0][0])
        # name = extension_ifo_list[0].split('/')
        # # print(name[5])
        # path = os.path.join(app.config['UPLOAD_CRX_FOLDER'], name[5]+'.crx')
        # with ZipFile(path) as crx_unzip:
        # # Extracting all the members of the zip 
        # # into a specific location.
        #     crx_unzip.extractall(
        #         path = os.path.join(app.config['UPLOAD_FOLDER'], name[5]+'.crx'))
        # path2 = os.path.join(app.config['UPLOAD_FOLDER'], name[5]+'.crx')
        # # print(path2)
        # virustotal.virustotal(path)
        # retireJS.retireJS(path2)
        # flash('File successfully uploaded')

if __name__ == "__main__":
    app.run(host='127.0.0.1',port=5000,debug=True,threaded=True)