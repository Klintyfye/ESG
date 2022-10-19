from fileinput import filename
import string
import requests
import json
import pathlib
import os


path = "/Users/mossabkadhom/Desktop/projekt/claroread.crx"
#os.path.dirname(os.path.abspath(__file__))

url = "https://www.virustotal.com/api/v3/files"

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

#if file is queued

url3 = "https://www.virustotal.com/api/v3/files/"+stringedRes+"/analyse"

headers2 = {
    "accept": "application/json",
    "x-apikey": "51bff97d51ac2996b0b64155402f55cc8960cdfbfcd3f5361eff4fd9f2dc65b2"
}

response2 = requests.post(url3, headers=headers)

print(response2.text)