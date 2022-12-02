import http.client # Required for communication with API
import json # Required for JSON conversion

def autocomplete(extension_name):
    """Get autocomplete suggestions from the chrome webstore.
    Parameter: String
    Return: Array
    """
    conn = http.client.HTTPSConnection("chrome.google.com")
    headers = { 'cookie': "NID=511%3DLiws3dmziXl-QBqvTLHF-h8I-KY49YqO-vOsxEVAQ7llUOdXBj9RdDFK8MJslTvgezpvoE8ueo_x2dl4a3cC1cWne60X29sLzwWVJALTz88prWW0-H1pN0nikP3WtURYRftbfmvSsqvZxjXuEVnrU3sVDymPDyVaPlDykJQNTmI; CONSENT=PENDING%2B895" }
    conn.request("POST", "/webstore/search/autocomplete?pv=20210820&q=" + extension_name, "", headers)

    res = conn.getresponse()
    data = res.read()

    string = data.decode("utf-8").replace(")]}'\n\n", "", 1)
    alist = json.loads(string)[1][2]

    return alist

def get_item(alist):
    """Retrieves basic extension information.
    Parameter: String (Extension name)
    Return: Array (Link to extension, Extension ID, Full extension name, Image link, Description, Amount of reviews, Score our of 5)
    """
    alist =  " ".join(alist.split())
    alist = alist.replace(" ", ',')
    print(alist)
    conn = http.client.HTTPSConnection("chrome.google.com")
    headers = { 'cookie': "NID=511%3Dcy1Y33x_e4r3px-iJ6uv1Mvh6gccjaOXC3x_USnO7gLk5JczW3vkTmtk97s_dG9fhU2oVKzI4rqkbTXSQe02VnxT9RXaLmTljAx8V4y0G9pAMoua1jZWBe7J_ovwwO-YsFyny6bVC6i9gF1iUQ3kZ7JKRQ7pv1YPu3ypjawopbMtRMXgJhQwwTAgS16NbAEwI_NvjAgW; CONSENT=PENDING%2B895" }
    conn.request("POST", "/webstore/ajax/item?pv=20210820&count=112&searchTerm="+ alist,"", headers)

    res = conn.getresponse()
    data = res.read()

    string = data.decode("utf-8").replace(")]}'\n\n", "", 1)
    alist = json.loads(string)

    blist = []
    listlen = len(alist[1][1])
    if (listlen < 4):
        loop_nr = listlen
    else:
        loop_nr = 4

    for i in range(loop_nr):
                blist.append([])
                blist[i].append(alist[1][1][i][37])
                blist[i].append(alist[1][1][i][1])
                blist[i].append(alist[1][1][i][3])
                blist[i].append(alist[1][1][i][6])
                blist[i].append(alist[1][1][i][22])
                blist[i].append(alist[1][1][i][12])

    return blist


# Add other get api for combining with the json to be stored in the database. must be a dictiorary so that we can mark what each field is.
# VT interner error handling
# solve: app = flask(__name__)
# crx download
# Standardisera var_namn