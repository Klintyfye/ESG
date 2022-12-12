from fileinput import filename
from hashlib import sha256
import requests
import json
import time



def url_for_large_file():

    url_for_large_files = "https://www.virustotal.com/api/v3/files/upload_url"
    refined_url = ""
    cnt = 15
    first_header = {
        "accept": "application/json",
        "x-apikey": "4926e23cc9acaa6110047cd35fa667a46e8acf4c889d5d7881e8859008df4e3c"
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
        "x-apikey": "d4d50fe1962ad63bd711835def05540f49413c3c522a05983256df870da0a950"
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
        "x-apikey": "aeb0ce92bba877752c47a65ac431ecc9988c782ca3679a84abc792b1f326610b"
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
    filename = "vtResult.json"
    sha256_value = info["meta"]["file_info"]["sha256"]
    #print(sha256_value)
    with open(filename, "w") as file_object:
        json.dump(info, file_object)
    time.sleep(3)
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
    filename = "vtResult.json"
    with open(filename, "w") as file_object:
       json.dump(json_data1, file_object)


def virustotal(path):
    url_for_analysis_report_from_hash(path)
    if_file_queued(path)
