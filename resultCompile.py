import json
import hashlib

def compileResult(crxDir, jsDir, vtDir):
    #Load the temp json as a dict
    with open(jsDir, "r") as f:
        data = json.load(f)


    #Get hash of crx
    with open(crxDir ,"rb") as f:
        bytes = f.read()
        hash = hashlib.sha256(bytes).hexdigest()

    #Add virus total data
        ###
        ###
        ###

    #Add the hash to the dict of the json so we can use it as an identifier
    data["hash"] = hash

    return data


jsDir = "tempJS.json"
vtDir = "tempVT.json"
crxDir = "adblock.crx"

result = compileResult(crxDir, jsDir, vtDir)
print(result)