import os
# import json
def retireJS(path2):
    path = path2
    print("Scanning, please wait...")

    os.system("retire --outputpath temp.json --outputformat json --path " + path)
    print("Scan successful!")

    print("\nCleaning, please wait...")

   
    print("Clean successful!")