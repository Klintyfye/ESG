from fileinput import filename
import string
import requests
import json
import pathlib
import os


path = "/Users/mossabkadhom/Desktop/Projekt/claroread.crx"
#os.path.dirname(os.path.abspath(__file__))

url = "https://www.virustotal.com/_ah/upload/AMmfu6bVJmB1ltPBW5tn5ccsPiAmhcL5hGVnGRwlzyRrMIpn273ByOKi-6G1y5qO-44qZGDvArH2ZBJt_rIL_gcDgyWDOVPj2b71z7Tem0rXIlF8Mj-LQtu_o-XI9gyTN1aoNNIYAe5syNr_7bVkvoUV52jwJgtX836Lakf_x_2egiY-adRZwg3q44wZuFPCs-k2hUa8tsROO8iDUq-xL7mCwEslnWkq0Pm5p8LC0i3YBvijnrmhHHFEdESgS7p0dlPJ-V1WHXPiW5_V6RJzbqO7mkbt0OzB9jB4GYTtnoEJIGr8HjQubthmJdGiAFSHVohnOpxGbqul_pF8OF43tHYZJK3uwPESlmMSQ7Tnmnxg2jsN7FD0Ri45H7XAqjXzSlBtLXicQLwYoRnKX8e9TzcHgL3IVORTRNDaVoVILiJtLbdlfM5SkXLYGj6o2wy5knXkfOWpwMvnDHsLBekhcK1AMp7cdBwRtGUgzpOKpIa-e18k5EWd6F_dJywk4uoe8eTfecVbLF1sq-2zhtiCriklntZM5MUnBoi2URpJPDJSHmM77KHXEPyIZYcA4QoEHSuupmF4HviUh3VYrIeq2qHyoSS5aL1CDPJYPKYtqACvztEz-fTavlZ4ogXmhg3LL7eEd0uSfVvkPVUBzfSJCIsvs9_uWkPJdOo66z5rYwKXRcClkLBFEfW35Yut0Q-pIV3j0slUf0ZAj5Gx84ovMcu_9EmNtAB9M0-ym5C4ROdbAGCIlgUmWySsgMrWk6eHQZFMUVk7WiTJZMzpoIoqp1q39wzv9fE7kfGwAUIZnW4LkbwRJ-LvxMW99cPHjLvRG4wwNkV2QCGyYz4aSRrZmzsStZ_pkXUXX8Rrmo9r2Xiv9ETliGG6o5BM0hcCV-M3fphkOjJpkxCpFUCRkbZcwtWGeOzR4UcidadgM0fxGqeVkSJdb1w2wA0OnsA9kYGkANFKczR6YOmMEHPHEg9H9jgXvULV4YXRXMrNhJI2ice1M5lJ8-pZ3RbqQIweOY-Tb1uWn_o0phOqMah-9q_bz-BI1cAveVICDy5RiNgDy4XoazrRAXBRW9pb5HliuXbC3IwmuYJfN0UNaPlFvaGjDoBJ5bpeOJjFzw4vH8_HiEgVizInoi7sMrAS4J6N69nBRRJdZ9_GmKAfKbVvLv2Lcn8hyHo5mMUGKzg30S3UvvavsUj_q7IW3BChqfLix-AM5ub9LUo7n5UcdWb8MCKrydxMFT7lNPr3f9SS0ADv6WAj649vieusW3t4H0BOfVhtpRLgGC1to9lI/ALBNUaYAAAAAY1ALUBNJp9gAOX0iy4-qHg0MdzNt1brr/"

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
"""
url3 = "https://www.virustotal.com/api/v3/files/"+stringedRes+"/analyse"

headers2 = {
    "accept": "application/json",
    "x-apikey": "51bff97d51ac2996b0b64155402f55cc8960cdfbfcd3f5361eff4fd9f2dc65b2"
}

response2 = requests.post(url3, headers=headers)

print(response2.text)
"""