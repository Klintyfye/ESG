import requests
import json

#Insert json
def insertOne(object):
    url = "https://data.mongodb-api.com/app/data-jkbjv/endpoint/data/v1/action/insertOne"
    headers = {
    'Content-Type': 'application/json',
    'Access-Control-Request-Headers': '*',
    'api-key': "srBukkVkfUToW1UYxdU4XCBq92vK5Su9IRzsf1spNX4i4IX5j3Cw5BNbIysuavqL", 
    }
    
    payload = json.dumps({
        "collection": "Results",
        "database": "ESG",
        "dataSource": "ESG-DB",

        #json to be inserted
        "document": object
    })
    
    requests.request("POST", url, headers=headers, data=payload)

#Find json by filter
def findOne(object):
    url = "https://data.mongodb-api.com/app/data-jkbjv/endpoint/data/v1/action/findOne"
    headers = {
    'Content-Type': 'application/json',
    'Access-Control-Request-Headers': '*',
    'api-key': "srBukkVkfUToW1UYxdU4XCBq92vK5Su9IRzsf1spNX4i4IX5j3Cw5BNbIysuavqL", 
    }

    payload = json.dumps({
        "collection": "Results",
        "database": "ESG",
        "dataSource": "ESG-DB",
        "filter": {
            #Filter of what to find (out of order)
            object[0]:object[1]
        }
    })
    response = requests.request("POST", url, headers=headers, data=payload)
    return response.text

print("Start")

object = {"x":"2"}

key = "x"
value = "2"


with open('json.json', 'r') as f:
  data = json.load(f)

#print(data)
insertOne(data)


print(object)

#print(findOne(object))

print("Finish")