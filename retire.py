import os
import json

def runRetire(targetDir: str):
    """Scans targetDir with retireJS and writes a result file "retireResult.json" in current directory.

    Args:
        targetDir (str): path of directory to scan. Either relative or absolute
    """

    #print(f"retire --outputpath retireResult.json --outputformat json --path {target}")
    os.system(f"retire --outputpath retireResult.json --outputformat json --path {targetDir}")


def runRetireDemo(outputPath: str, outputFormat: str, target: str):

    print("Scanning, please wait...")
    if len(outputPath.split(" ")) > 1:
        outputPath = outputPath.split(" ")[1]
    
    if len(outputFormat.split(" ")) > 1:
        outputFormat = outputFormat.split(" ")[1]

    if len(target.split(" ")) > 1:
        target = target.split(" ")[1]
    
    print(f"retire --outputpath {outputPath} --outputformat {outputFormat} --path {target}")
    #os.system(f"retire {outputPath} {outputFormat} {target}")

    print(f"Scan successful!")

def printKey(outputPath: str):

    print("\nCleaning, please wait...")
    with open(outputPath) as f:
        file = json.load(f)
        # Print the file of dictionary

        for object in file["data"]:

            print("\n","{:/^50}".format("/").center(os.get_terminal_size().columns))

            print("Vulnerable file:", object["file"])

            for results in object["results"]:

                print("\tComponent:", results["component"])

                for vulnerabilities in results["vulnerabilities"]:

                    print("\t\tSummary:", vulnerabilities["identifiers"]["summary"])

                    print("\t\t\tCVE:", vulnerabilities["identifiers"]["CVE"][0])

                    print("\t\t\tSeverity:", vulnerabilities["severity"])



        print("\n","{:/^50}".format("/").center(os.get_terminal_size().columns))

        print("Clean successful!")


if __name__ == '__main__':
    print("Start demo:\n")

    target = ""
    outputFormat = ""
    outputPath = ""

    while 1:

        temp = input("Custom scanning path (y/n): ")

        if temp.lower() == "y":

            temp = input("Input target path: ")

            target = f"--path {temp}"

            break

        elif temp.lower() == "n":

            break

    while 1:

        temp = input("Custom output path (y/n): ")

        if temp.lower() == "y":

            temp = input("Input output path: ")

            flagOutputPath = f"--outputpath {temp}"

            outputPath = temp

            break

        elif temp.lower() == "n":

            break

    formats = ["text", "json", "jsonsimple", "depcheck", "cyclonedx", "cyclonedxJSON"]

    while 1:

        temp = input("Custom output format (y/n): ")

        if temp.lower() == "y":

            print(f"Valid formats: {formats}")

            temp = input("Input output format: ")

            if temp in formats:

                outputFormat = f"--outputformat {temp}"

                break

            print("Invalid format!")

        elif temp.lower() == "n":

            break
    runRetireDemo(flagOutputPath, outputFormat, target)