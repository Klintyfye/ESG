from zipfile import ZipFile
from typing import Literal
import mongoAPI
import resultCompile
import runRetire

def scan(crxDir: str, cwsId: str) -> Literal[-1,1]:
    """Takes path of crx and its cwsId and scans, compiles results, and uploads to database

    Args:
        crxDir (str): Relative or absolute path of crx to scan.
        cwsId (str): Chrome Web Store id of extension

    Returns:
        Literal[0,1]: returns 1 on databse upload success or -1 on databse upload failure.
    """

    #how ever tf you run the virus total idk how to make it work nicely.
    vtDir = "vtExample.json"


    #Name of folder which the crx extracts into
    extractedDir = "temp"
    #extracts crx file to allow for retireJS scan
    with ZipFile(crxDir, 'r') as f:
        f.extractall(extractedDir)

    #Run retireJS scan on folder and create result json "retireResult.json"
    runRetire.runRetire(extractedDir)
    jsDir = "retireResult.json"

    #Compiles results from retireJS and virusTotal
    object = resultCompile.compileResult(jsDir, vtDir, cwsId)

    #Inserts result json into db
    #print(object)
    return mongoAPI.insertOne(object)


if __name__ == '__main__':
    crxDir = "crx.crx"
    cwsId = "123"
    scan(crxDir, cwsId)