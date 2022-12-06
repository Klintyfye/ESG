from zipfile import ZipFile
from typing import Literal
import mongo_API
import result_compile
import retire
import virustotal

def scan(crxDir: str, meta: dict) -> Literal[-1,1]:
    """Takes path of crx and its cwsId and scans, compiles results, and uploads to database

    Args:
        crxDir (str): Relative or absolute path of crx to scan.
        meta (dict): dictionary of meta data including: cwsId (chrome web store id), extension name etc...

    Returns:
        Literal[0,1]: returns 1 on databse upload success or local extension scan, or -1 on database upload failure.
    """

    print("Börja vt")
    #how ever tf you run the virus total api idk how to make it work nicely.
    vtDir = "vtResult.json"
    virustotal.virustotal(crxDir)


    #Name of folder which the crx extracts into
    extractedDir = "temp"
    #extracts crx file to allow for retireJS scan
    with ZipFile(crxDir, 'r') as f:
        f.extractall(extractedDir)

    print("Börja retire")
    #Run retireJS scan on folder and create result json "retireResult.json"
    retire.runRetire(extractedDir)
    jsDir = "retireResult.json"

    print("Börja compile")
    #Compiles results from retireJS and virusTotal
    object = result_compile.compileResult(jsDir, vtDir, meta)

    #Inserts result json into db
    print(object)
    #Check if cwsId is None indiciating that it's a local extension and not to be uploaded
    if object["meta"]["cwsId"] == "None":
        return 1

    return mongo_API.insertOne(object)


if __name__ == '__main__':
    #crxDir = "crx.crx"
    #cwsId = "123"
    crxDir = input("crxDir: ")
    cwsId = input("cwsId: ")
    meta = {"cwsId":cwsId}

    print(scan(crxDir, meta))
    print("Done")
