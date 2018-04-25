import openpyxl


def getServiceListByList(sheet, startRow):
    changeLag_col = 3
    serviceId_col = 8
    serviceName_col = 10
    ipAddressL3_col = 13
    protocolNumber_col = 14
    portNumberL4_col = 15
    urlL7_col = 16
    # firstLineServiceId = sheet.cell(row=startRow, column=serviceId_col).value
    retList = []

    for rowNumber in range(startRow, sheet.max_row + 1):
        changeLag = sheet.cell(row=rowNumber, column=changeLag_col).value
        serviceId = sheet.cell(row=rowNumber, column=serviceId_col).value
        serviceName = sheet.cell(row=rowNumber, column=serviceName_col).value
        ipAddressL3 = sheet.cell(row=rowNumber, column=ipAddressL3_col).value
        protocolNumber = sheet.cell(row=rowNumber, column=protocolNumber_col).value
        portNumberL4 = sheet.cell(row=rowNumber, column=portNumberL4_col).value
        urlL7 = sheet.cell(row=rowNumber, column=urlL7_col).value

        layerLag = "L7"
        portsplit_1 = "|"
        portsplit_2 = "=="
        portL4List = []
        portstr = portNumberL4
        if portNumberL4 != None:
            if portsplit_2 in str(portNumberL4):
                portstr = portNumberL4.split(portsplit_2)[0]
                portL4List.append(portNumberL4.split(portsplit_2)[1])
            else:
                pass
            if portsplit_1 in str(portstr):
                portstr = portstr.split(portsplit_1)
                for p in portstr:
                    portL4List.append(p)
            else:
                portL4List.append(portstr)
            # print(portL4List)
            for p in portL4List:
                retList.append((layerLag, changeLag, serviceId, serviceName, ipAddressL3, protocolNumber, p, urlL7))
        else:
            retList.append(
                (layerLag, changeLag, serviceId, serviceName, ipAddressL3, protocolNumber, portNumberL4, urlL7))
        #if layerLag == "L7" and serviceName == None:
            #print("所在行数", rowNumber)
    retList = list(set(retList))

    return retList


def arrangeTheList(lst):
    sList = []
    retList = []
    tempList = []
    for tup in lst:
        # print("----")
        layerLag, changeLag, serviceId, serviceName, ipAddress, protocolNumber, portNumber, url = tup
        sList.append(serviceId)
    # print(len(sList),sList)
    sList = list(set(sList))
    for sValue in sList:
        for tup in lst:
            layerLag, changeLag, serviceId, serviceName, ipAddress, protocolNumber, portNumber, url = tup
            if sValue == serviceId:
                tempList.append(tup)
        retList.append(tempList)
        tempList = []
    # for line in retList:
    #    print("+++", line)
    return retList


def getTheUrlList(lst):
    retList = []
    for tup in lst:
        retList.append(tup[7])
    retList = list(set(retList))
    return retList


def getTheTupList(url, sLst):
    retList = []
    for tup in sLst:
        if tup[7] == url:
            retList.append(tup)
    return retList


def getTheServiceUrlIpListDict_Delete(List_del):
    # print("11111", List_del)
    # {业务名：{url:[ip]}}
    retDict = {}

    for serviceList in List_del:
        serviceName = serviceList[0][3]
        urlList = getTheUrlList(serviceList)
        urlDict = {}
        # print("11111",serviceName,urlList)
        for url in urlList:
            tupList = getTheTupList(url, serviceList)
            urlDict[url] = tupList
            retDict[serviceName] = urlDict

    return retDict


def getTheiplistStrList(listName, clst):
    retList = []
    for i in range(0, len(clst)):
        if 'ip-prefix-list ' + listName in clst[i] and "create" in clst[i]:
            # retList.append(clst[i])
            k = i
            for j in range(k, len(clst)):
                if "exit" in clst[j]:
                    retList.append(clst[j])
                    break
                else:
                    retList.append(clst[j])
    # print("2222", listName,retList)
    return retList


def getTheIpPrefixListStrList(sName, urlstr, cfglst):
    retList = []
    iplist_name_list = []

    http_host = urlstr.replace("http://", "").replace("/*", "").replace(":*", "")
    for i in range(0, len(cfglst)):
        if 'expression 1 http-host eq' in cfglst[i] and http_host in cfglst[i]:
            k = i
            for j in range(k, len(cfglst)):
                if 'application "APP_' + sName + '"' in cfglst[j]:
                    if 'server-address eq ip-prefix-list' in cfglst[j - 1]:
                        prefixlistname = cfglst[j - 1].split("server-address eq ip-prefix-list ")[1]
                        iplist_name_list.append(prefixlistname.replace("\n", ""))
                    break

    # print("55555",iplist_name_list)
    for iplistName in iplist_name_list:
        iplistStrList = getTheiplistStrList(iplistName, cfglst)
        retList.append(iplistStrList)
        # print("+++",sName,urlstr,iplistStrList)
    return retList


def getTheServiceUrlIpListStrDict_Delete(service_dict, cfglst):
    retDict = {}
    for service_name in service_dict:
        # print("222",service_name)
        urlDict = {}
        for url in service_dict[service_name]:
            # print("333",url)
            iplistStr = []
            iplistStr = getTheIpPrefixListStrList(service_name, url, cfglst)
            # print("444",service_name,url,iplistStr)
            urlDict[url] = iplistStr
            retDict[service_name] = urlDict

    return retDict


def getTheDeleteIpPrefixListName(tup, strList):
    retStr = ""
    ipStr = tup[4].replace(" ", "")
    if "/" not in ipStr:
        ipStr = ipStr + "/32"
    for i in range(0, len(strList)):
        # k = i
        for text in strList[i]:
            if ipStr in text:
                retStr = "ip-prefix-list " + strList[i][0].split("ip-prefix-list ")[1].split(" create")[0]
                return retStr

    return str(tup) + "未找到该条目"


def getTheSplitList(tempList):
    nameList = []
    retList = []
    for c in tempList:
        nameList.append(c[0])
    nameList = list(set(nameList))
    # print("----",nameList)
    for name in nameList:
        tList = []
        tList.append(name)
        for c in tempList:
            if c[0] == name:
                tList.append(c[1])
        retList.append(tList)
    return retList


def DeleteTheUrlIpList(comlst, service_name, url, delete_tup_list, ipListStrList):
    # print(service_name,url)
    # print(delete_tup_list)
    # print(ipListStrList)
    comlst.append("对" + service_name + "的" + url + "进行操作\n")
    comlst.append("exit all\n")
    comlst.append("configure application-assurance group 1:1\n")
    tempList = []
    for tup in delete_tup_list:
        deleteName = getTheDeleteIpPrefixListName(tup, ipListStrList)
        # comlst.append(deleteName+"\n")
        if "未找到该条目" not in deleteName:
            ipStr = tup[4].replace(" ", "")
            if "/" not in ipStr:
                ipStr = ipStr + "/32"
                tempList.append((deleteName, ipStr))
            else:
                tempList.append((deleteName, ipStr))
    SplitList = []
    # print("++++",tempList)
    SplitList = getTheSplitList(tempList)
    print("++++", SplitList)
    for lst in SplitList:
        for line in lst:
            if "ip-prefix-list" in line:
                comlst.append(line + "\n")
            else:
                comlst.append("no prefix " + line + "\n")
        comlst.append("\n")
        # comlst.append("no prefix "+ipStr+"\n")
        # print("+++",deleteName)


def DeleteTheServiceName_iplist(comlist, sName, delete_url_dict, ipListStrDict):
    # comlist.append(sName+"业务进行删除操作")
    #print(sName + "业务进行删除操作")
    for url_key in delete_url_dict:
        # print("+++",url_key)
        DeleteTheUrlIpList(comlist, sName, url_key, delete_url_dict[url_key], ipListStrDict[sName][url_key])


def gen_iplist_del(configList, path):
    commandList = []
    # print("把excel表拖入cmd窗口\n")
    # excel_path = input()
    # excel_path = "C:\L7chargingcontext.xlsx"
    excel_path = path + "\\ip_prefix_list_L7.xlsx"
    # print("把内容计费的配置log表拖入cmd窗口\n")
    # chargingContextLog_path = input()
    # chargingContextLog_path = "E:\processL347\内容计费text\sae133-config-20180330.txt"
    # configFile = open(chargingContextLog_path, 'r')
    # configList = configFile.readlines()
    # configFile.close()

    excel = openpyxl.load_workbook(excel_path)

    try:
        sheet_del = excel["ip_prefix_list_del"]
    except Exception as err:
        print(err)

    # 对ip_prefix_list进行删除操作
    resultList_del = getServiceListByList(sheet_del, 3)
    # for tup in resultList_del:
    #   print(tup)

    resultList_del = arrangeTheList(resultList_del)
    # print(resultList_del)

    # 获取{业务名：{url:[ip]}}该结构的字典，删除操作
    serviceUrlIpListDict_Delete = {}
    serviceUrlIpListDict_Delete = getTheServiceUrlIpListDict_Delete(resultList_del)
    print(serviceUrlIpListDict_Delete)

    # 获取业务名对应的url对应的iplist列表
    # {业务名：{url:[[iplist的字符段]]}}
    serviceUrlIpListStrDict_Delete = {}
    serviceUrlIpListStrDict_Delete = getTheServiceUrlIpListStrDict_Delete(serviceUrlIpListDict_Delete, configList)
    # for key in serviceUrlIpListStrDict_Delete:
    # print("+++", key, serviceUrlIpListDict_Delete[key])
    # for urlKey in serviceUrlIpListStrDict_Delete[key]:
    # print("aaaaaaaa", key, urlKey, serviceUrlIpListStrDict_Delete[key][urlKey])

    # 进行删除操作
    for del_serviceName_key in serviceUrlIpListDict_Delete:
        DeleteTheServiceName_iplist(commandList, del_serviceName_key, serviceUrlIpListDict_Delete[del_serviceName_key],
                                    serviceUrlIpListStrDict_Delete)

    fo = open(path + "\\test_ip_prefix_list_del.txt", "w")
    fo.writelines(commandList)
    fo.close()

    # exit(7)
