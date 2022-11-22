import http.client # Required for communication with API
import json # Required for JSON conversion
from werkzeug.utils import secure_filename
def autocomplete(extension_name):
    """Get autocomplete suggestions from the chrome webstore.
    Parameter: String
    Return: Array
    """
    # conn = http.client.HTTPSConnection("chrome.google.com")
    # headers = { 'cookie': "NID=511%3DLiws3dmziXl-QBqvTLHF-h8I-KY49YqO-vOsxEVAQ7llUOdXBj9RdDFK8MJslTvgezpvoE8ueo_x2dl4a3cC1cWne60X29sLzwWVJALTz88prWW0-H1pN0nikP3WtURYRftbfmvSsqvZxjXuEVnrU3sVDymPDyVaPlDykJQNTmI; CONSENT=PENDING%2B895" }
    # conn.request("POST", "/webstore/search/autocomplete?pv=20210820&q=" + extension_name, "", headers)

    # res = conn.getresponse()
    # data = res.read()

    # string = data.decode("utf-8").replace(")]}'\n\n", "", 1)
    # alist = json.loads(string)[1][2]
    # return alist


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
    if alist[1][1]:
        listlen = len(alist[1][1])
        if listlen >= 4:
            for i in range(4):
                blist.append([])
                blist[i].append(alist[1][1][i][37]) 
                blist[i].append(alist[1][1][i][1]) 
                blist[i].append(alist[1][1][i][4])
                blist[i].append(alist[1][1][i][6]) 
                blist[i].append(alist[1][1][i][22]) 
                blist[i].append(alist[1][1][i][12])
            # print(blist)
        elif listlen == 3:
            for i in range(3):
                blist.append([])
                # print('\n''####################################################')
                blist[i].append(alist[1][1][i][37]) 
                blist[i].append(alist[1][1][i][1]) 
                blist[i].append(alist[1][1][i][4])
                blist[i].append(alist[1][1][i][6]) 
                blist[i].append(alist[1][1][i][22]) 
                blist[i].append(alist[1][1][i][12])
            # print(blist)
        elif listlen == 2:
            for i in range(2):
                blist.append([])
                # print('\n''####################################################')
                blist[i].append(alist[1][1][i][37]) 
                blist[i].append(alist[1][1][i][1]) 
                blist[i].append(alist[1][1][i][4])
                blist[i].append(alist[1][1][i][6]) 
                blist[i].append(alist[1][1][i][22]) 
                blist[i].append(alist[1][1][i][12])
            # print(blist)
        elif listlen == 1:
            for i in range(1):
                blist.append([])
                # print('\n''####################################################')
                blist[i].append(alist[1][1][i][37]) 
                blist[i].append(alist[1][1][i][1]) 
                blist[i].append(alist[1][1][i][4])
                blist[i].append(alist[1][1][i][6]) 
                blist[i].append(alist[1][1][i][22]) 
                blist[i].append(alist[1][1][i][12])
            # print(blist)
        return blist
    return blist
            # print('\n''####################################################')

    


# # For testing
# test_value = 'adblock'


# autocomplete(test_value)

# get_item(test_value)

# ['adblock plus', 'adblock for youtube']

# tlist = [['https://chrome.google.com/webstore/detail/adblock-%E2%80%94-best-ad-blocker/gighmmpiobklfepjocnamgkkbiglidom', 'AdBlock — den bästa annonsblockeraren', 'https://lh3.googleusercontent.com/3WssruYpy1oFSsMEQol5IZFGPYI7uYgwfekPl85NqKaUxu2bJsveNdO9oII2fYeBgznWbL-X5AtBidNa9ddFowwd7pM=w220-h140-e365-rj-sc0x00ffffff', 'Blockera reklam, pop-ups på YouTube, Facebook, Twitch och dina andra favoritsidor.', 296928, 4.520779448216403], ['https://chrome.google.com/webstore/detail/adblock-for-youtube/cmedhionkhpnakcndndgjdbohmhepckk', 'Adblock for Youtube™', 'https://lh3.googleusercontent.com/s461fSyCaZWFkKsCvs8jsZV-SW_szvxsJwKFN8CgVpNXNE4DBM_ZpGa7glQrVEDemSTkTQMx3KqA_DBEtkJHR-DXSA=w220-h140-e365-rj-sc0x00ffffff', 'Tar bort annonser från Youtube.', 260125, 4.396790004805382], ['https://chrome.google.com/webstore/detail/adblock-plus-free-ad-bloc/cfhdojbkjhnklbpkdaibdccddilifddb', 'Adblock Plus - gratis annonsblockerare', 'https://lh3.googleusercontent.com/5KhDb_CYPuUIBdZgLu4AOFIRjerLSQdC9Jrbv5ReXPQudO7_RlcNHZZJDqNrWQpoN2-xMg20j2uASzVdBoI1sq0kECo=w220-h140-e365-rj-sc0x00ffffff', 'Blockera YouTube™-annonser, popup-fönster & bekämpa mot skadlig kod!', 181687, 4.455134379454776], ['https://chrome.google.com/webstore/detail/crystal-ad-block/lklmhefoneonjalpjcnhaidnodopinib', 'Crystal Ad block', 'https://lh3.googleusercontent.com/CI44xBkM86uYrI7vSKAGpyXvI8P_gZon17lLhdf6SwbkukAH_ihgHMucufqPl1mx0L2BWhMLz23n-NGjGBTY3nOtpA=w220-h140-e365-rj-sc0x00ffffff', 'Crystal ad block - Open source and transparent ad block software.', 30, 4.2]]

# for i in tlist:
#     print(i[0].split('/')[-1])