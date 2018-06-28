def getServiceEntryList(serviceName, cLst):
    retLst = []
    tmpLst = []
    for i in range(0, len(cLst)):
        if 'application "APP_' + serviceName + '"' in cLst[i] and "create" not in cLst[i]:
            p = i
            for j in range(p, 0, -1):
                if "entry " in cLst[j]:
                    for t in range(j, p + 2):
                        tmpLst.append(cLst[t])
                    break
            retLst.append(tmpLst)
            tmpLst = []

    return retLst



def processUrl(url):
    e_host = None
    e_url = None
    h_port = None
    if url == None:
        return None,None,None
    url = url.replace("http://", "").replace("https://", "")
    if url[-2]+url[-1] == "/*":
        if url[-2]+url[-1] == "/*" and url.count("/*") == 1:
            url = url.replace("/*","")
            e_url = "/*"
            e_host = url

            if "/" in url:
                e_url = url[url.find("/"):len(url)] + e_url
                e_host = url[0:url.find("/")]

            if ":" in e_host:
                h_port = e_host.split(":")[1]
                e_host = e_host.split(":")[0]
        elif url[-2]+url[-1] == "/*" and url.count("/*") > 1:
            url = url[0:-2]
            e_url = "/*"
            if "/" in url:
                e_url = url[url.find("/"):len(url)] + e_url
                e_host = url[0:url.find("/")]
            if ":" in e_host:
                h_port = e_host.split(":")[1]
                e_host = e_host.split(":")[0]

    if ":*" in url:
        if "/" in url:
            e_url = url[url.find("/"):len(url)]
            e_host = url[0:url.find("/")]
        else:
            e_host = url

    if ":*" not in url and url[-2]+url[-1] == "/*":
        e_host = url
        if "/" in url:
            e_url = url[url.find("/"):len(url)]
            e_host = url[0:url.find("/")]
        if ":" in e_host:
            h_port = e_host.split(":")[1]
            e_host = e_host.split(":")[0]
    if ":*" not in url and url[-2] + url[-1] != "/*":
        e_host = url
    if e_host != None:
        if e_host[0]!= "*":
            e_host = "^" + e_host
        if e_host[-1] != "*":
            e_host = e_host + "$"
    if e_url!= None:
        if e_url[0]!= "*":
            e_url = "^" + e_url
        if e_url[-1] != "*":
            e_url = e_url + "$"

    return e_host,e_url,h_port

def DeleteEntryIsTrue(service_name,service_port,http_host,http_uri,http_port,ip_address,entryCfgList):
    entry_cfg_list = []
    for text in entryCfgList:
        entry_cfg_list.append(text.replace("\n", "").replace(" ", ""))
    if "/" not in ip_address:
        ip_address = ip_address + "/32"
    entry_str_list = []
    if http_host != None:
        text = 'expression 1 http-host eq "' + http_host + '"'
        entry_str_list.append(text.replace(" ", ""))
    if http_uri != None:
        text = 'expression 2 http-uri eq "' + http_uri + '"'
        entry_str_list.append(text.replace(" ", ""))
    if ip_address !=None:
        text = 'server-address eq ' + str(ip_address)
        entry_str_list.append(text.replace(" ", ""))
    if http_port !=None:
        text = 'http-port eq ' + str(http_port)
        entry_str_list.append(text.replace(" ", ""))
    if service_port != None:
        text = 'server-port eq ' + str(service_port)
        entry_str_list.append(text.replace(" ", ""))
    if service_name != None:
        text = 'application "APP_' + service_name + '"'
        entry_str_list.append(text.replace(" ", ""))

    for text in entry_str_list:
        if text not in entry_cfg_list:
            return False
    return True



def EntryIsTrue(service_name,service_port,http_host,http_uri,http_port,cfglst,start_bit,end_bit):
    entry_cfg_list = []
    for i in range(start_bit,end_bit):
        entry_cfg_list.append(cfglst[i].replace("\n","").replace(" ",""))
    entry_str_list = []
    if http_host != None:
        text = 'expression 1 http-host eq "'+http_host+'"'
        entry_str_list.append(text.replace(" ",""))
    if http_uri != None:
        text = 'expression 2 http-uri eq "'+http_uri+'"'
        entry_str_list.append(text.replace(" ",""))
    if service_port !=None:
        text = 'server-port eq '+str(service_port)
        entry_str_list.append(text.replace(" ",""))
    if service_name !=None:
        text = 'application "APP_'+service_name+'"'
        entry_str_list.append(text.replace(" ",""))
    #print("-------------")
    #print(entry_str_list)
    #print(entry_cfg_list)
    for text in entry_str_list:
        if text not in entry_cfg_list:
            return False
    #print("True:",service_name,service_port,http_host,http_uri)
    return True