import http.client # Required for communication with API
import json # Required for JSON conversion

def autocomplete(extension_name):
    """Get autocomplete suggestions from the chrome webstore.
    Parameter: String
    Return: Array
    """
    extension_name = extension_name.replace(" ", "%20") # Support for space
    extension_name  = extension_name.replace("\"", "") # Not a good solution but it works.

    conn = http.client.HTTPSConnection("chrome.google.com")
    headers = { 'cookie': "NID=511%3Dcy1Y33x_e4r3px-iJ6uv1Mvh6gccjaOXC3x_USnO7gLk5JczW3vkTmtk97s_dG9fhU2oVKzI4rqkbTXSQe02VnxT9RXaLmTljAx8V4y0G9pAMoua1jZWBe7J_ovwwO-YsFyny6bVC6i9gF1iUQ3kZ7JKRQ7pv1YPu3ypjawopbMtRMXgJhQwwTAgS16NbAEwI_NvjAgW; CONSENT=PENDING%2B895" }
    conn.request("POST", "/webstore/search/autocomplete?pv=20210820&q=" + str(extension_name), "", headers)

    res = conn.getresponse()
    data = res.read()

    # String manipulation
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
                blist[i].append(alist[1][1][i][37])   # Extension link
                blist[i].append(alist[1][1][i][1])    # Name
                blist[i].append(alist[1][1][i][3])    # Image link
                blist[i].append(alist[1][1][i][6])    # Description
                blist[i].append(alist[1][1][i][22])   # Nr. of ratings
                blist[i].append(alist[1][1][i][12])   # Rating out of 5
                blist[i].append(alist[1][1][i][0])    # ID

    return blist
