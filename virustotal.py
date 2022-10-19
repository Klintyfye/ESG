from fileinput import filename
import string
import requests
import json
import pathlib
import os


path = "/Users/mossabkadhom/Desktop/Projekt/claroread.crx"
#os.path.dirname(os.path.abspath(__file__))

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

filename = "virustotal_output.json"

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