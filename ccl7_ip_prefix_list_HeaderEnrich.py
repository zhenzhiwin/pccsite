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
        if layerLag == "L7" and serviceName == None:
            print("所在行数", rowNumber)
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


def arrangeTheList_2(rtList):
    new_ret_list = []
    for lst in rtList:
        tmplist = []
        for tup in lst:
            if tup[1] == "新增":
                tmplist.append(tup)
        for tup in lst:
            if tup[1] == "删除":
                tmplist.append(tup)
        new_ret_list.append(tmplist)
    return new_ret_list


def getTheAllServiceUrl(service_name):
    global configList
    retList = []

    return retList


def addServiceUrlIpListToDict(lst):
    global serviceUrlIpListDict
    urlIpListDict = {}
    # print(lst)

    serviceName = lst[0][3]
    # print(serviceName,lst)

    urlList = []
    for tup in lst:
        urlList.append(tup[7])
    # urlList = getTheAllServiceUrl(serviceName)
    urlList = list(set(urlList))
    # print(serviceName,urlList)
    for url in urlList:
        urlIpListDict[url] = []
    serviceUrlIpListDict[serviceName] = urlIpListDict
    # print(serviceUrlIpListDict)
    for urlKey in serviceUrlIpListDict[serviceName]:
        ipPrefixList = []
        ipPrefixList = getIpPrefixListByUrl_serviceName(urlKey, serviceName)
        # print(urlKey,ipPrefixList)
        urlIpListDict[urlKey] = ipPrefixList


def getIpPrefixListByUrl_serviceName(url, service_name):
    global configList
    retList = []
    # print(url)
    http_host = url.replace("http://", "").replace("/*", "").replace(":*", "")
    # print(http_host)
    if http_host[0] != "*":
        http_host = '^' + http_host
    if http_host[-1] != "*":
        http_host = http_host + '$'
    http_host = 'expression 1 http-host eq "' + http_host + '"'
    # print(http_host)
    for i in range(0, len(configList)):
        if http_host in configList[i]:
            k = i
            tmplist = []
            for j in range(k, len(configList)):
                if 'no shutdown' in configList[j]:
                    break
                if 'server-address eq ip-prefix-list "app_' + service_name in configList[j] and "_HeaderEnrich" in \
                        configList[j]:
                    ipListStr = configList[j].split("server-address eq ")[1].replace("\n", "")
                    # print(ipListStr)
                    tmplist = getTheIpPrefixList(ipListStr)
            if len(tmplist) != 0:
                retList.append(tmplist)
    return retList


def getTheIpPrefixList(ip_list_str):
    global configList
    retList = []
    retList.append(ip_list_str)
    for i in range(0, len(configList)):
        if ip_list_str + ' create' in configList[i]:
            f = i
            # print(ip_list_str,":",k)
            for j in range(f, len(configList)):
                if "exit" in configList[j]:
                    e = j
                    break
    # print(ip_list_str,f,e)
    for i in range(f, e):
        if 'prefix ' in configList[i]:
            ipstr = configList[i].replace("\n", "").split("prefix ")[1].split(" name")[0].replace("/32", "")
            # print(ipstr)
            retList.append(ipstr)
    return retList


def setServicePostFixNum(service_name, postList):
    global configList
    for text in configList:
        if 'ip-prefix-list "app_' + service_name + '_' in text and "create" in text and "_HeaderEnrich" in text:
            postfixnumstr = text.split('ip-prefix-list "app_' + service_name + '_')[1].split('" create')[0]
            # print("========",service_name,postfixnumstr)
            postList.append(int(postfixnumstr))


def addServiceUrlIpListToUserDict(lst):
    global serviceUrlIpListUserDict
    global del_serviceUrlIpListUserDict
    global servce_ipostfix_num
    serviceName = lst[0][3]

    if serviceName not in servce_ipostfix_num:
        servce_ipostfix_num[serviceName] = []
        setServicePostFixNum(serviceName, servce_ipostfix_num[serviceName])
    # print("====",servce_ipostfix_num)

    urlIpListDict = {}
    urlList = []
    for tup in lst:
        urlList.append(tup[7])
    urlList = list(set(urlList))
    # print(serviceName,urlList)
    for url in urlList:
        urlIpListDict[url] = []
    # for url in del_urlIpListDict:
    #   del_urlIpListDict[url] = []
    # print(serviceName, urlIpListDict)
    for url in urlList:
        # print(url)
        # tmpdict = {}
        tmplst = []
        delTmplst = []
        for tup in lst:
            if tup[7] == url and tup[1] == "新增":
                tmplst.append(tup[4])
            # if tup[7] == url and tup[1]=="删除":
            #   delTmplst.append(tup[4])
        # print(serviceName,url,tmplst)
        urlIpListDict[url] = tmplst
        # del_urlIpListDict[url] = delTmplst
    # print('+++++',urlIpListDict)
    serviceUrlIpListUserDict[serviceName] = urlIpListDict
    # del_serviceUrlIpListUserDict[serviceName] = del_urlIpListDict
    # print(serviceUrlIpListUserDict)


def addCommandTocommandList(comlst, serverName, url, addList):
    # print(serverName, url,addList)
    global serviceUrlIpListDict
    global ip_prefix_list_max_number
    global servce_ipostfix_num

    '''
    if len(servce_ipostfix_num[serverName])==0:
        postfix_num = 1
    else:
        postfix_num = max(servce_ipostfix_num[serverName])
    '''
    config_ipPrefixList = serviceUrlIpListDict[serverName][url]

    # 若配置列表为空则表示配置文件中无该业务的ip_prefix_list

    if len(config_ipPrefixList) == 0:
        # print("aaaaaaaaa+++", serverName, url, config_ipPrefixList)
        tl = []
        if len(servce_ipostfix_num[serverName]) == 0:
            postFixNum = 1
            servce_ipostfix_num[serverName].append(postFixNum)
        else:
            postFixNum = max(servce_ipostfix_num[serverName]) + 1
            servce_ipostfix_num[serverName].append(postFixNum)
        # print("bbbbbbb+++",serverName,servce_ipostfix_num)
        # postFixNum = postfix_num
        # postfix_num+=1
        # servce_ipostfix_num[serverName].append(postfix_num)
        if postFixNum < 10:
            ipliststr = 'ip-prefix-list "app_' + serverName + '_0' + str(postFixNum) + '_HeaderEnrich"'
        else:
            ipliststr = 'ip-prefix-list "app_' + serverName + '_' + str(postFixNum) + '_HeaderEnrich"'
        tl.append(ipliststr)
        entryId = getTheCompatibleEntryId()

        createIpPrefixListEntry(comlst, serverName, url, ipliststr, entryId)
        config_ipPrefixList.append(tl)
        while len(addList) != 0:
            for lst in config_ipPrefixList:
                # print("---",lst)
                if len(lst) < ip_prefix_list_max_number + 1:
                    # print("----------",addList)
                    addIpStr = addList[0]
                    lst.append(addList[0])
                    addList.remove(addList[0])
                    # print("-----", lst[0], addList[0])
                    addIpPrefixListCommand(comlst, serverName, lst[0], addIpStr)
                    if len(addList) == 0:
                        break
                    # print("+++++",lst[0],addIpStr)
                    # addIpPrefixListCommand(comlst,serverName,lst[0],addIpStr)

            # 若所有列表都满了则需创建新的列表
            if ip_prefix_list_is_full(config_ipPrefixList) == True:
                tl = []
                if len(servce_ipostfix_num[serverName]) != 0:
                    postFixNum = max(servce_ipostfix_num[serverName]) + 1
                    servce_ipostfix_num[serverName].append(postFixNum)
                if postFixNum < 10:
                    ipliststr = 'ip-prefix-list "app_' + serverName + '_0' + str(postFixNum) + '_HeaderEnrich"'
                else:
                    ipliststr = 'ip-prefix-list "app_' + serverName + '_' + str(postFixNum) + '_HeaderEnrich"'
                # print("++++++++",ipliststr)
                tl.append(ipliststr)
                entryId = getTheCompatibleEntryId()
                createIpPrefixListEntry(comlst, serverName, url, ipliststr, entryId)
                config_ipPrefixList.append(tl)
    else:
        # 循环直到用户需要添加iplist(addList)列表中的数据添加完才跳出循环
        while len(addList) != 0:
            for lst in config_ipPrefixList:
                if len(lst) < ip_prefix_list_max_number + 1:
                    addIpStr = addList[0]
                    lst.append(addList[0])
                    addList.remove(addList[0])
                    addIpPrefixListCommand(comlst, serverName, lst[0], addIpStr)
                    if len(addList) == 0:
                        break
                    # addIpPrefixListCommand(comlst,serverName,lst[0],addIpStr)

            # 若所有列表都满了则需创建新的列表
            if ip_prefix_list_is_full(config_ipPrefixList) == True:
                tl = []
                if len(servce_ipostfix_num[serverName]) != 0:
                    postFixNum = max(servce_ipostfix_num[serverName]) + 1
                    servce_ipostfix_num[serverName].append(postFixNum)
                # postFixNum = postfix_num
                # postfix_num += 1
                if postFixNum < 10:
                    ipliststr = 'ip-prefix-list "app_' + serverName + '_0' + str(postFixNum) + '_HeaderEnrich"'
                else:
                    ipliststr = 'ip-prefix-list "app_' + serverName + '_' + str(postFixNum) + '_HeaderEnrich"'
                tl.append(ipliststr)
                entryId = getTheCompatibleEntryId()
                createIpPrefixListEntry(comlst, serverName, url, ipliststr, entryId)
                config_ipPrefixList.append(tl)


def createIpPrefixListEntry(clst, service_name, url, ip_list_str, enId):
    # print("+++++++",service_name,url)
    clst.append("exit all\n")
    clst.append("configure application-assurance group 1:1 policy\n")
    # clst.append("begin\n")
    clst.append("app-filter\n")
    clst.append("entry " + str(enId) + " create\n")
    expression_1 = ""
    expression_2 = ""
    http_port = ""
    if url != None:
        url = url.replace("http://", "").replace("https://", "")
        if url[0] != "*":
            url = "^" + url
        if url[-1] != "*":
            url = url + "$"

        prefix = ""
        suffix = ""
        if "/*" in url:
            suffix = "/*"
            url = url.replace("/*", "")
            url = url + "$"
            expression_2 = "^/*"

        expression_1 = url
        if ":*" not in url and ":" in url:
            expression_1 = url.split(":")[0] + "$"
            expression_2 = "^" + url.split(":")[1][url.split(":")[1].index("/"):len(url.split(":")[1])].replace("$",
                                                                                                                "") + "/*"
            http_port = url.split(":")[1][0:url.split(":")[1].index("/")]

        clst.append('expression 1 http-host eq "' + expression_1 + '"\n')
    if expression_2 != "":
        clst.append('expression 2 http-uri eq "' + expression_2 + '"\n')

    clst.append("server-address eq " + ip_list_str + '"\n')
    clst.append('application "APP_' + service_name + '_HeaderEnrich"\n')
    clst.append("no shutdown\n")
    clst.append("exit\n")

    ''''''
    clst.append('exit all\n')
    clst.append('configure application-assurance group 1:1\n')
    clst.append(ip_list_str + "\n")

    clst.append("\n")


def getTheCompatibleEntryId():
    retId = 30000

    return retId


def addIpPrefixListCommand(clst, sName, ipPrefixListStr, ipStr):
    # clst.append('exit all\n')
    # clst.append('configure application-assurance group 1:1\n')
    # clst.append(ipPrefixListStr+"\n")
    if "/" not in ipStr:
        ipStr = ipStr + "/32"
    clst.append("prefix " + ipStr + ' name "' + sName + '_HeaderEnrich"' + "\n")
    # clst.append("\n")


def ip_prefix_list_is_full(cfg_ipPrefixList):
    global ip_prefix_list_max_number
    for lst in cfg_ipPrefixList:
        if len(lst) < ip_prefix_list_max_number + 1:
            return False
    return True


def DeleteTheIpPrefixList(comlst, server_name, url, del_list):
    pass


def getTheServicePostFixNum():
    pass


def getTheServiceUrlIpListDict_Delete(List_del):
    print("11111", List_del)


def gen_prefix_enrich(path, confgList):
    global configList
    configList = []
    configList = confgList
    log_list = []
    global serviceUrlIpListDict
    global serviceUrlIpListUserDict
    global del_serviceUrlIpListUserDict
    # 用个全局变量来存储ip_prefix_list的最大值
    global ip_prefix_list_max_number
    ip_prefix_list_max_number = 50

    serviceUrlIpListDict = {}
    serviceUrlIpListUserDict = {}
    del_serviceUrlIpListUserDict = {}
    commandList = []
    # print("把excel表拖入cmd窗口\n")
    # excel_path = input()
    # excel_path = "C:\L7chargingcontext.xlsx"
    excel_path = path + "\\ip_prefix_list_L7_headEnrich.xlsx"
    # print("把内容计费的配置log表拖入cmd窗口\n")
    # chargingContextLog_path = input()
    # chargingContextLog_path = "E:\processL347\内容计费text\sae133-config-20180330.txt"
    # configFile = open(chargingContextLog_path, 'r')
    # configList = configFile.readlines()
    # configFile.close()

    global servce_ipostfix_num
    servce_ipostfix_num = {}
    global servicePostFixNumDict
    servicePostFixNumDict = {}

    excel = openpyxl.load_workbook(excel_path)
    try:
        sheet = excel["ip_prefix_list_add"]
    except Exception as err:
        print(err)

    serviceList = []
    # 该函数会根据分割符来把一条条目中包含port range的分成若干条
    serviceList = getServiceListByList(sheet, 3)
    # for tup in serviceList:
    #   print("---",tup)
    # print(serviceList)
    resultList = []
    resultList = arrangeTheList(serviceList)
    # resultLis = list(set(resultList))
    # for lint in resultList:
    #   print("---",len(lint),lint)
    #   time.sleep(1)
    resultList = arrangeTheList_2(resultList)
    # print(resultList)
    for resultLine in resultList:
        # print("++",resultLine)
        if len(resultLine) == 0:
            resultList.remove(resultLine)
    # exit(7)
    # print(len(resultList))
    for resultlst in resultList:
        # print("++", resultlst)
        addServiceUrlIpListToDict(resultlst)
    # print(serviceUrlIpListDict)
    # 添加业务url列表（该业务对应的url所有的需要添加的IP）
    for resultlst in resultList:
        addServiceUrlIpListToUserDict(resultlst)

    # exit(7)
    # print(serviceUrlIpListUserDict)

    # print(serviceUrlIpListDict)
    log_list.append("这是配置文件中相关业务的数据:\n")
    for sNameKey in serviceUrlIpListDict:
        log_str = sNameKey
        for urlKey in serviceUrlIpListDict[sNameKey]:
            log_str = log_str + "  " + urlKey
            for linelst in serviceUrlIpListDict[sNameKey][urlKey]:
                log_str = log_str + "    " + str(linelst) + "\n"
                log_list.append(log_str)
                log_str = ""

    log_list.append("这是用户添加的数据:\n")
    # print(serviceUrlIpListUserDict)
    for sNameKey in serviceUrlIpListUserDict:
        log_str = sNameKey
        for urlKey in serviceUrlIpListUserDict[sNameKey]:
            log_str = log_str + "  " + urlKey
            # for linelst in serviceUrlIpListUserDict[sNameKey][urlKey]:
            log_str = log_str + "    " + str(len(serviceUrlIpListUserDict[sNameKey][urlKey])) + str(
                serviceUrlIpListUserDict[sNameKey][urlKey]) + "\n"
            log_list.append(log_str)
            log_str = ""

    log_list.append("这是配置文件中相关业务的数据(添加前):\n")
    for sNameKey in serviceUrlIpListDict:
        log_str = sNameKey
        for urlKey in serviceUrlIpListDict[sNameKey]:
            log_str = log_str + "  " + urlKey
            for linelst in serviceUrlIpListDict[sNameKey][urlKey]:
                log_str = log_str + "    " + str(len(linelst) - 1), str(linelst) + "\n"
                log_list.append(log_str)
                log_str = ""

    # 先对业务进行增加操作
    commandList.append("exit all\n")
    commandList.append("configure application-assurance group 1:1 policy\n")
    # commandList.append("begin\n")
    for sNameKey in serviceUrlIpListUserDict:
        log_list.append("************"+sNameKey+str(serviceUrlIpListUserDict))
        commandList.append("对" + sNameKey + "业务进行新增操作\n")
        for urlKey in serviceUrlIpListUserDict[sNameKey]:
            # print(sNameKey, urlKey,serviceUrlIpListUserDict[sNameKey][urlKey])
            addCommandTocommandList(commandList, sNameKey, urlKey, serviceUrlIpListUserDict[sNameKey][urlKey])

    log_list.append("这是配置文件中相关业务的数据(添加后):\n")
    for sNameKey in serviceUrlIpListDict:
        log_str = sNameKey
        for urlKey in serviceUrlIpListDict[sNameKey]:
            log_str = log_str + "  " + urlKey
            for linelst in serviceUrlIpListDict[sNameKey][urlKey]:
                log_str = log_str + "    " + str(len(linelst) - 1)+str(linelst) + "\n"
                log_list.append(log_str)
                log_str = ""

    fo = open(path + "\\ip_prefix_list_HeaderEnrich.txt", "w")
    fo.writelines(commandList)
    fo.close()

    if log_list:
        fo = open(path + "\\ip_prefix_list_HeaderEnrich.log", "w")
        fo.writelines(log_list)
        fo.close()

        # fo = open("ip_prefix_list_HeaderEnrich.log", "w")
        # fo.writelines(log_list)
        # fo.close()

    # exit(7)
