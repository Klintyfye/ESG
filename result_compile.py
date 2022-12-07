import json
from datetime import datetime
import os

def compile_result(jsDir: str, vtDir: str, meta: dict) -> dict:
    """Uses results from retireJs and virus total along with the cwsId to compile important information.

    Args:
        jsDir (str): directory to result file from retireJS
        vtDir (str): directory to result file from virusTotal
        meta (dict): dictionary of meta data including: cwsId (chrome web store id), extension name etc...

    Returns:
        dict: dict of combined results of
    """

    result = {}

    #read RetireJS data
    with open(jsDir, "r") as f:
        file = json.load(f)

    file = file["data"]

    #add RetireJS data to dict
    for object in file:
        for temp in object["results"]:
            temp.pop("detection", None)

    #Keeps only relative path
    cwd = os.getcwd()
    for object in file:
        object["file"] = os.path.relpath(object["file"], cwd+"/temp")

    #Summarises retireJS vulnerabilities
    severities = {"none":0,"low":0,"medium":0,"high":0,"critical":0}
    result["retireJs"] = file
    # print(file[0]["results"])
    for temp in file:
        for object in temp["results"][0]["vulnerabilities"]:
            for severity in severities:
                if object["severity"] == severity:
                    severities[severity] += 1
                    break


    result["retireSeverity"] = severities

    #read Virus Total data
    with open(vtDir, "r") as f:
        file = json.load(f)

    #add Virus Total data to dict
    sum = 0
    for num in file["data"]["attributes"]["stats"]:
        sum += file["data"]["attributes"]["stats"][num]
    result["virusTotal"] = file["data"]["attributes"]["stats"]
    result["virusTotalSum"] = sum


    #Add meta data to the dict of the json so we can use it as an identifier
    meta["date"] = str(datetime.now())
    result["meta"] = meta
    result["hash"] = file["meta"]["file_info"]["sha256"]

    return result
