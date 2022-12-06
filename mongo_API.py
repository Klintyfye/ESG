import constants
import requests
import json
from typing import Literal

APIKEY = constants.APIKEY

#Insert json
def insertOne(object: dict) -> Literal[-1,1]:
    """Insert json into database.
    Args:
        object (dict): json to be inserted loaded as a dict.
    Returns:
        Literal[-1,1]: returns 1 on success, -1 if file with hash already exists.
    """
        
    #Check if document with identical hash exists in db
    if getByHash(object["hash"]) != None:
        return -1

    url = "https://data.mongodb-api.com/app/data-jkbjv/endpoint/data/v1/action/insertOne"
    headers = {
    'Content-Type': 'application/json',
    'Access-Control-Request-Headers': '*',
    'api-key': APIKEY,
    }

    payload = json.dumps({
        "collection": "Results",
        "database": "ESG",
        "dataSource": "ESG-DB",

        #json to be inserted
        "document": object
    })

    requests.request("POST", url, headers=headers, data=payload)
    return 1

def getByHash(hash: str) -> dict|None:
    """Fetches single (first) json with matching hash value.
    (should only ever be one not accounting for errors.)
    Args:
        hash (str): hash of crx.
    Returns:
        dict: Returns dict of item on success.
        None: returns None if no matches found.
    """

    url = "https://data.mongodb-api.com/app/data-jkbjv/endpoint/data/v1/action/findOne"
    headers = {
    'Content-Type': 'application/json',
    'Access-Control-Request-Headers': '*',
    'api-key': APIKEY,
    }

    payload = json.dumps({
        "collection": "Results",
        "database": "ESG",
        "dataSource": "ESG-DB",
        "filter": {
            "hash":hash
        },
        "projection": {
            "_id":0
        }
    })
    response = requests.request("POST", url, headers=headers, data=payload)
    return json.loads(response.text)["document"]

def getById(cwsId: str) -> list:
    """Fetches a dictionary with a list of json with matching cwsId.
    Args:
        cwsId (str): Chrome Web Store Id.
    Returns:
        list: returns list of items (dicts) with matching [cwsId].
        list: returns [] on failure.
    """

    #Check if cwsId is None indiciating that it's a local extension and doesn't have a history
    if cwsId == "None":
        return []

    url = "https://data.mongodb-api.com/app/data-jkbjv/endpoint/data/v1/action/find"
    headers = {
    'Content-Type': 'application/json',
    'Access-Control-Request-Headers': '*',
    'api-key': APIKEY,
    }

    payload = json.dumps({
        "collection": "Results",
        "database": "ESG",
        "dataSource": "ESG-DB",
        "filter": {
            "cwsId": cwsId
        },
        "projection": {
            "_id":0
        }
    })
    response = requests.request("POST", url, headers=headers, data=payload)
    return json.loads(response.text)["documents"]

#Drop json by filter
def deleteOne(hash: str) -> Literal[0,1]:
    """Drops json with hash value matching hash.
    Args:
        hash (str): hash value of crx.
    Returns:
        Literal[0,1]: returns 1 on success, 0 on failure
    """

    url = "https://data.mongodb-api.com/app/data-jkbjv/endpoint/data/v1/action/deleteOne"
    headers = {
    'Content-Type': 'application/json',
    'Access-Control-Request-Headers': '*',
    'api-key': APIKEY,
    }

    payload = json.dumps({
        "collection": "Results",
        "database": "ESG",
        "dataSource": "ESG-DB",
        "filter": {
            #Filter of what to find (out of order)
            "hash":hash
        }
    })
    response = requests.request("POST", url, headers=headers, data=payload)
    return json.loads(response.text)["deletedCount"]

if __name__ == '__main__':
    print("Start demo:\n")
    while 1:
        usrInput = input("1:insert\n2:find\n3:find multiple\n4:delete\nq:quit\n")
        match usrInput:
            case "1":
                cwsId = input("Insert cwsId: ")
                hash = input("Insert hash: ")
                object = {"cwsId":cwsId, "hash": hash}
                print("Result:")
                print(insertOne(object))
            case "2":
                hash = input("Insert hash: ")
                print("Result:")
                print(getByHash(hash))
            case "3":
                cwsId = input("Insert cwsId: ")
                print("Result:")
                print(getById(cwsId))
            case "4":
                hash = input("Insert hash: ")
                print("Result:")
                print(deleteOne(hash))
            case "q":
                break
            case _:
                print("please choose 1,2,3, or 4")
