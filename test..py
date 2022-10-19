import requests


url3 = "https://www.virustotal.com/api/v3/files/upload_url"
refined_url = ""
cnt = 15
headers = {
    "accept": "application/json",
    "x-apikey": "51bff97d51ac2996b0b64155402f55cc8960cdfbfcd3f5361eff4fd9f2dc65b2"
}

response3 = requests.get(url3, headers=headers)
while (response3.text[cnt] != '"'):
    refined_url += response3.text[cnt]
    cnt += 1

print(refined_url)