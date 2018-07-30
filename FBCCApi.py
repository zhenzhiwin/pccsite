def getTheAllServiceName(configure_list):
    retList = []
    for text in configure_list:
        if "application " in text and "APP_" in text:
            #print(text)
            retList.append(text.split("APP_")[1].split('"')[0])
    return list(set(retList))

def getTheTupListFromEntryList(service_name,entry_list,configure_list):
    retList = []
    urlstr = ""
    express1 = ""
    express2 = ""
    serviceaddress = ""
    serviceport = ""
    httpport = ""
    for text in entry_list:
        if "expression1http-hosteq" in text:
            express1 = text.split('"')[1].replace("^","").replace("$","")
        if "expression2http-urieq" in text:
            express2 = text.split('"')[1].replace("^", "").replace("$", "")
        if "server-addresseq" in text:
            serviceaddress = text.replace("server-addresseq","")
        if "server-porteq" in text:
            serviceport = text.replace("server-porteq","")
        if "http-porteq" in text:
            httpport = text.replace("http-porteq","")
    if serviceport == "443":
        urlstr = "https://"+express1
        serviceport = ""
        if httpport != "":
            urlstr = urlstr + ":"+httpport
        urlstr+=express2
    else:
        urlstr = "http://"+express1
        if httpport != "":
            urlstr = urlstr + ":"+httpport
        urlstr+=express2
    #print("serviceaddress:",serviceaddress,"serviceport:",serviceport,"url:",urlstr)
    if "dns-ip-cache" in serviceaddress:
        retList.append((serviceaddress, serviceport, urlstr))
        return retList
    elif "ip-prefix-list" in serviceaddress:

        retList = getTheTupListFromIpPrefixList(service_name,serviceaddress,serviceport,urlstr,configure_list)
        #print("ip-prefix-list---",retList)
        return retList
    else:
        if urlstr == "http://":
            urlstr = ""
        retList.append((serviceaddress,serviceport,urlstr))
        return retList



def getTheTupListFromIpPrefixList(service_name,prefix_list_name,service_port,url,cfg_list):

    retList = []
    prefix_list_name = prefix_list_name.replace('ip-prefix-list',"")
    #print("--------", prefix_list_name,service_name,service_port,url)
    for i in range(0,len(cfg_list)):
        if prefix_list_name in cfg_list[i] and "create" in cfg_list[i]:
            k = i
            for j in range(k,len(cfg_list)):
                if "exit" in cfg_list[j]:
                    break
                #if "prefix" in cfg_list[j]:
                if "prefix" in cfg_list[j] and "create" not in cfg_list[j]:
                #if "prefix" in cfg_list[j] and service_name in cfg_list[j]:
                    if url == "http://":
                        url = ""
                    retList.append((cfg_list[j].replace("prefix ","").replace(" ",""),service_port,url))
    return retList


def getTheServiceTupList(service_name,service_entry_list,cfg_list):
    retList = []
    for entry_lst in service_entry_list:
        entry_tup_list = getTheTupListFromEntryList(service_name,entry_lst,cfg_list)
        if entry_tup_list:
        # print("entry_lst",entry_lst)
        # print("entry_tup_list",entry_tup_list)
            retList+=entry_tup_list
    return retList