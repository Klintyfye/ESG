import http.client # Required for communication with API
import json # Required for JSON conversion
from werkzeug.utils import secure_filename

def get_item(alist):
    """Retrieves basic extension information.
    Parameter: String (Extension name)
    Return: Array (Link to extension, Extension ID, Full extension name, Image link, Description, Amount of reviews, Score our of 5)
    """
    # clist = []
    # for i in alist:
    blist = [[], [], [], []]
    alist = secure_filename(alist)
    conn = http.client.HTTPSConnection("chrome.google.com")
    headers = { 'cookie': "NID=511%3Dcy1Y33x_e4r3px-iJ6uv1Mvh6gccjaOXC3x_USnO7gLk5JczW3vkTmtk97s_dG9fhU2oVKzI4rqkbTXSQe02VnxT9RXaLmTljAx8V4y0G9pAMoua1jZWBe7J_ovwwO-YsFyny6bVC6i9gF1iUQ3kZ7JKRQ7pv1YPu3ypjawopbMtRMXgJhQwwTAgS16NbAEwI_NvjAgW; CONSENT=PENDING%2B895" }
    conn.request("POST", "/webstore/ajax/item?pv=20210820&count=112&searchTerm="+ alist,"", headers)

    res = conn.getresponse()
    data = res.read()

    string = data.decode("utf-8").replace(")]}'\n\n", "", 1)
    alist = json.loads(string)
    # print(alist)
    if len(alist[1][1]) >4:
        for i in range(4):
            
            # print('\n''####################################################')
            blist[i].append(alist[1][1][i][37]) 
            blist[i].append(alist[1][1][i][1]) 
            blist[i].append(alist[1][1][i][4])
            blist[i].append(alist[1][1][i][6]) 
            blist[i].append(alist[1][1][i][22]) 
            blist[i].append(alist[1][1][i][12])
        # print(blist)
    else:
        for i in range(len(alist[1][1])):
            
            # print('\n''####################################################')
            blist[i].append(alist[1][1][i][37]) 
            blist[i].append(alist[1][1][i][1]) 
            blist[i].append(alist[1][1][i][4])
            blist[i].append(alist[1][1][i][6]) 
            blist[i].append(alist[1][1][i][22]) 
            blist[i].append(alist[1][1][i][12])
        # print(blist)

        # print('\n''####################################################')

    return blist

# # For testing
# test_value = 'adblock'

# autocomplete(test_value)
# ['adblock plus', 'adblock for youtube']

