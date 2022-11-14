import os
import json

print("Scanning, please wait...")

os.system("retire --outputpath temp.json --outputformat json")

print("Scan successful!")

print("\nCleaning, please wait...")

f = open("humanOutput.txt", "w")
with open("temp.json") as json_file:
    file = json.load(json_file)
    
    # Print the file of dictionary
    for object in file["data"]:
        f.write("////////////////////////////\n")
        f.write("Vulnerable file:"+ object["file"]+"\n")
        for results in object["results"]:
            f.write("\tComponent:"+ results["component"]+"\n")
            for vulnerabilities in results["vulnerabilities"]:
                f.write("\t\tSummary:"+ vulnerabilities["identifiers"]["summary"]+"\n")
                f.write("\t\t\tCVE:"+ vulnerabilities["identifiers"]["CVE"][0]+"\n")
                f.write("\t\t\tSeverity:"+ vulnerabilities["severity"]+"\n")

f.close()
print("Clean successful!")