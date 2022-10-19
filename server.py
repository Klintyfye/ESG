import os      # For File Manipulations like get paths, rename
from flask import Flask, flash, request, redirect, render_template
from werkzeug.utils import secure_filename
import shutil
import json
from fileinput import filename
import requests




app=Flask(__name__)
app.secret_key = "secret key" # for encrypting the session
#It will allow below 16MB contents only, you can change it
app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024
path = os.getcwd()
# file Upload
UPLOAD_FOLDER = os.path.join(path, 'uploads')
# Make directory if "uploads" folder not exists
if not os.path.isdir(UPLOAD_FOLDER):
    os.mkdir(UPLOAD_FOLDER)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
# ALLOWED_EXTENSIONS = set(['txt', 'pdf', 'png', 'jpg', 'jpeg', 'gif', 'json', 'config', 'drconf', 'js', 'ttf', 'svg', 'html', 'css'])
# def allowed_file(filename):
#     return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS
def virustotal(path):

    path = "C:/Users/saifa/OneDrive/Dokument/DV1512/projekt_code/flask/uploadeZip.zip"
    
    url = "https://www.virustotal.com/_ah/upload/AMmfu6ZG99JZRGLT08fhgX2Ba2H77pveadINOHBs9H6B2JxujB_TUfTBJgGksVO4VYOLvVlS3FqSInZ3o33DcGm43OgeE4C0TOEZl13xWy_DEbRgv39EBhExtGF8I22SrIHEQvAgQbOcO9FhpElzzME4zo34NOTSi3LcTFKQSaAcaa7KG4j_yjpsnJ6omCOFV2WbD_qbF9zUSbyhUnMV2O7XxG6a_4TaMoxppU21AThyLdA-SqCoxyg1ZroMMbhunwZWxrtJwZlDEFxvnWtqATzKjTnrAL-3sIGDlK9cTQNposQqXSIlaeK5yTbe4ckzrca2grZBzzm_IoLUKJIqseGF6RHkp3HwxMlMe70wIjRFJTklOnujcJQUo4uMivY55RO9lnEV2tnF8EipOZF68YOt7cBK4FgZZ7vxb8CoJPi1WoAcfppblHefjvQ-igvCiKghSukX-EVUxR7ji5W-CzbpRuvqSFqOttBbFxLyPRWa9vHcznycQy5exNTaYlVHj9wdjVpicGBVgjCFN5w3mgOgKv9zteFgfvbd7hYWw-TXm06TIVbUSlWD4Y4hQGEcWBUUyiKC87AB5JbI77H6bx3LLxpw8iSIrRXdTlpBCVzuALUoysh_9CAg_HoxwXq0Ndo2TlAUZzsD_0VEQdehG2nqUt5kDkxTyale_nYtYHtpyfDTamO8Ir8ICPLXXpRzBGGk3C5tteNmIEjMTFzKM7YSqGfaH42T3qgwHTi_f49aH6xwVfZSw35bLPVAoAjwM2ACvSmdYt8I3xDGG0cpD7kpiVHpJ8dwwRAImmye2sBOva9w2O9kY_C-HajXpwR3Or2adSQrARfz91HQq6nf148FN8Vrn0_RyQcZHVmsgUfYW3pwKpTC7igD0VzRBHtWnBYZb21_JpW7rOw6DgaPiBVf2zRA0mrqWziq14Dvvn0DJMmlLv8J95FK9gV4JeGGKFkxWvAvqFYh4e9ePvlgy_R54Qjjyp-52r-ke78wL431xdNnanBM5bmj6mgLNsjCkNHMJsDD6s4QLTSSztbN2WpjCETgWeSwH5wRDSpxlvSDflImz4IQyAgDKALuVT6qMqYtxnND4FDa3iefmflQcm8SUnI50ubdUS7r2XH_ruoM3yMc1Da_8nXjShF8er6tcmU-RQK8AaYIgRs67T-aOtrCFXOChW-4EeiwBlzcnRUSmlp-PiKlPOGFDdqdp8MP8Q2mEIWV9e7b000QTfxzuYiTUg36_7zpz-uGph0B9crXbNfi4P3DSQ8enzHOo-rz6eGmr_N8jUQ_/ALBNUaYAAAAAY1APMkl2HLCM6QUnepW_iGKEroBU8iQA/"

    files = {"file": open(path, "rb")}
    headers = {
        "accept": "application/json",
        "x-apikey": "51bff97d51ac2996b0b64155402f55cc8960cdfbfcd3f5361eff4fd9f2dc65b2"
    }

    response = requests.post(url, files=files, headers=headers)

    check = True
    stringedRes = ""
    stringresp = response.text

    for i in range(len(stringresp)):
        if stringresp[i] == "i" and stringresp[i+1] == "d":
            i = i+5
            while check:
                if stringresp[i+1] == '"':
                    check = False
                    break
                stringedRes = stringedRes + stringresp[i+1]
                i = i+1
                



    url2 = "https://www.virustotal.com/api/v3/analyses/"+stringedRes
    headers1 = {
        "accept": "application/json",
        "x-apikey": "51bff97d51ac2996b0b64155402f55cc8960cdfbfcd3f5361eff4fd9f2dc65b2"
    }

    response1 = requests.get(url2, headers=headers)

    #print(response1.text)


    json_data = json.loads(response1.text)
    print(json_data)

    filename = "json_data.json"

    with open(filename, "w") as file_object:
        json.dump(json_data, file_object)



def retireJS():
    print("Scanning, please wait...")

    os.system("retire --outputpath temp.json --outputformat json --path uploads")

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

        if 'files[]' not in request.files:
            flash('No file part')
            return redirect(request.url)

        files = request.files.getlist('files[]')
        for file in files:
            if file:      # and allowed_file(file.filename)
                filename = secure_filename(file.filename)
                file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
        shutil.make_archive("uploadeZip", "zip", app.config['UPLOAD_FOLDER'])
        virustotal()
        # retireJS()

        flash('Folder successfully uploaded')
        return redirect('/')


if __name__ == "__main__":
    app.run(host='127.0.0.1',port=5000,debug=True,threaded=True)




