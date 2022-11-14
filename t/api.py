import http.client # Required for communication with API
import json # Required for JSON conversion
from werkzeug.utils import secure_filename
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
    if len(alist) <= 4:
        return get_item(alist)
    else:
        return get_item(alist[0:4])


def get_item(alist):
    """Retrieves basic extension information.
    Parameter: String (Extension name)
    Return: Array (Link to extension, Extension ID, Full extension name, Image link, Description, Amount of reviews, Score our of 5)
    """
    clist = []
    for i in alist:
        blist = []
        i = secure_filename(i)
        conn = http.client.HTTPSConnection("chrome.google.com")
        headers = { 'cookie': "NID=511%3Dcy1Y33x_e4r3px-iJ6uv1Mvh6gccjaOXC3x_USnO7gLk5JczW3vkTmtk97s_dG9fhU2oVKzI4rqkbTXSQe02VnxT9RXaLmTljAx8V4y0G9pAMoua1jZWBe7J_ovwwO-YsFyny6bVC6i9gF1iUQ3kZ7JKRQ7pv1YPu3ypjawopbMtRMXgJhQwwTAgS16NbAEwI_NvjAgW; CONSENT=PENDING%2B895" }
        conn.request("POST", "/webstore/ajax/item?pv=20210820&count=112&searchTerm="+ i,"", headers)

        res = conn.getresponse()
        data = res.read()

        string = data.decode("utf-8").replace(")]}'\n\n", "", 1)
        alist = json.loads(string)
        for j in (alist[1][1][0][37], alist[1][1][0][1], alist[1][1][0][4], alist[1][1][0][6], alist[1][1][0][22], alist[1][1][0][12]):
            blist.append(j)
        clist.append(blist)

    return clist


# # For testing
# test_value = 'adblock'

# autocomplete(test_value)

# ['adblock plus', 'adblock for youtube']

