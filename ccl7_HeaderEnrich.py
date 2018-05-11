import openpyxl



def gen_hearderenrich(path,confgList):
    global log_list
    log_list = []
    global configList
    configList = []
    configList = confgList
    commandList = []
    allEntryIdList = []
    global serviceDict
    serviceDict = {}
    global serviceEntryIdDict
    serviceEntryIdDict = {}
    global allEntryIdDict
    allEntryIdDict = {}
    ccl7_cfg = open(path+'\\configureL7.log', 'r')
    ccl7_cfg_list = ccl7_cfg.readlines()
    ccl7_cfg.close()
    allEntryIdList = eval(ccl7_cfg_list[0])
    serviceDict = eval(ccl7_cfg_list[1])
    serviceEntryIdDict = eval(ccl7_cfg_list[2])
    allEntryIdDict = eval(ccl7_cfg_list[3])
    #print(allEntryIdList)
    #print(serviceDict)
    #print(serviceEntryIdDict)

    #chargingContextLog_path = "E:\processL347\内容计费text\sae133-config-20180330.txt"
    #configFile = open(chargingContextLog_path, 'r')
    #configList = configFile.readlines()
    #configFile.close()

    excel_path = path+"\\内容计费整理L7_headEnrich.xlsx"
    excel = openpyxl.load_workbook(excel_path)
    sheet = excel["L7"]
    serviceList = []
    # 该函数会根据分割符来把一条条目中包含port range的分成若干条
    serviceList = getServiceListByList(sheet, 3)
    resultList = arrangeTheList(serviceList)
    resultList = arrangeTheList_2(resultList)


    for resultlst in resultList:

        commandList.append(resultlst[0][3]+"业务进行增删操作\n")
        commandList.append("exit all\n")
        commandList.append("configure application-assurance group 1:1 policy\n")
        commandList.append("begin\n")
        commandList.append("app-filter\n")
        setPRUCRUtoServiceDict(resultlst[0], configList)
        chg_app_create(resultlst[0][3], commandList)
        #print("+++++++++++",resultlst[0])
        dnsMatchList = []
        #dnsMatchList = getNDSMatchListByConfigureLog(resultlst,configList)
        #addNDSMatch2CommandList(commandList,dnsMatchList)
        addEntryIdtoserviceEntryIdDict(resultlst[0][3],configList)
        for tupline in resultlst:
            if tupline[1] == "新增":
                entryId = getTheCompatibleEntryIdByDict()
                addTheCommandtoList_Entry(commandList,tupline,entryId)
            #else:
                #删除entry
                #pass
                #获取该业务的所有entry存于字典中,用来判断该业务是否删干净

                #deleteEntryId = getTheDeleteEntryId(tupline,configList)
                #DeleteTheEntry(commandList,tupline,deleteEntryId)
                #LimitTheServiceSpeed(commandList,tupline)

                #break

        PR_PRU_CRU_Process(commandList, resultlst[0], configList)
        #PR_PRU_CRU_Delete(commandList, resultlst[0], configList)

        commandList.append("\n\n")
    text_cfg = []
    text_cfg.append(str(allEntryIdList) + "\n")
    text_cfg.append(str(serviceDict) + "\n")
    text_cfg.append(str(serviceEntryIdDict) + "\n")
    text_cfg.append(str(allEntryIdDict) + "\n")

    file = open(path + "\\configureL7.log", "w")
    file.writelines(text_cfg)
    file.close()
    fo = open(path+"\\ccL7_HeaderEnrich.txt", "w")
    fo.writelines(commandList)
    fo.close()

def getServiceListByList(sheet,startRow):
    changeLag_col = 3
    serviceId_col = 8
    serviceName_col = 10
    ipAddressL3_col = 13
    protocolNumber_col = 14
    portNumberL4_col = 15
    urlL7_col = 16
    #firstLineServiceId = sheet.cell(row=startRow, column=serviceId_col).value
    retList = []

    for rowNumber in range(startRow,sheet.max_row + 1):
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
            #print(portL4List)
            for p in portL4List:
                retList.append((layerLag, changeLag, serviceId, serviceName, ipAddressL3, protocolNumber, p, urlL7))
        else:
            retList.append((layerLag, changeLag, serviceId, serviceName, ipAddressL3, protocolNumber, portNumberL4, urlL7))
    retList = list(set(retList))

    return  retList

def arrangeTheList(lst):
    sList = []
    retList = []
    tempList = []
    for tup in lst:
        layerLag, changeLag, serviceId, serviceName, ipAddress, protocolNumber, portNumber, url = tup
        sList.append(serviceId)
    sList = list(set(sList))
    for sValue in sList:
        for tup in lst:
            layerLag, changeLag, serviceId, serviceName, ipAddress, protocolNumber, portNumber, url = tup
            if sValue == serviceId:
                tempList.append(tup)
        retList.append(tempList)
        tempList = []
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

def setPRUCRUtoServiceDict(tup,cfglst):

    global serviceDict
    #serviceId = tup[2]
    serviceName = tup[3]
    if "PR_"+serviceName+"_HeaderEnrich" not in serviceDict:
        serviceDict["PR_"+serviceName+"_HeaderEnrich"] = False
    if "PRU_"+serviceName+"_HeaderEnrich"+"_"+tup[0] not in serviceDict:
        serviceDict["PRU_"+serviceName+"_HeaderEnrich"+"_"+tup[0]] = False
    if "APP_" + serviceName+"_HeaderEnrich" not in serviceDict:
        serviceDict["APP_" + serviceName+"_HeaderEnrich"] = False
    if "CHG_" + serviceName+"_HeaderEnrich" not in serviceDict:
        serviceDict["CHG_" + serviceName+"_HeaderEnrich"] = False
    #头增强不需要添加CRU
    #if "CRU_"+serviceName not in serviceDict:
     #   serviceDict["CRU_"+serviceName] = False

    #判断PR是否存在
    prStr = 'policy-rule "PR_'+serviceName+"_HeaderEnrich"+'"'
    if PR_str_isExist(prStr,cfglst) == True:
        serviceDict["PR_" + serviceName+"_HeaderEnrich"] = True

    #判断PRU是否存在
    pruStr = 'policy-rule-unit "PRU_'+serviceName+"_HeaderEnrich"+'_'+tup[0]+'"'
    if PRU_str_isExist(pruStr,cfglst) == True:
        serviceDict["PRU_"+serviceName+"_HeaderEnrich"+"_"+tup[0]] = True
        #print(serviceName+"_PRU",serviceDict[serviceName+"_PRU"])

    #判断CRU是否存在
    #cruStr = 'charging-rule-unit "CRU_'+serviceName+'"'
    #if CRU_str_isExist(cruStr,serviceId,cfglst) == True:
    #    serviceDict["CRU_"+serviceName] = True
    appStr = 'application "APP_' + serviceName+"_HeaderEnrich" + '"'
    if APP_str_isExist(appStr, cfglst) == True:
        serviceDict["APP_" + serviceName+"_HeaderEnrich"] = True

    chgStr = 'application "CHG_' + serviceName+"_HeaderEnrich" + '"'
    if CHG_str_isExist(chgStr, cfglst) == True:
        serviceDict["CHG_" + serviceName+"_HeaderEnrich"] = True


def PR_str_isExist(pr_str,cfglst):
    i = 0
    for text in cfglst:
        if pr_str in text and "qci * arp * precedence" not in text:
            i+=1
    if i == 2:
        return True
    else:
        return False

def PRU_str_isExist(pru_str,cfglst):
    for text in cfglst:
        if pru_str in text and "qci * arp * precedence" not in text:
            return True
    return False

def CRU_str_isExist(cru_str,sid,cfglst):
    global commandList

    for i in range(0,len(cfglst)):
        if cru_str in cfglst[i] and "qci * arp * precedence" not in cfglst[i]:
            #print(i,cfglst[i+1])
            try:
                if cfglst[i+1].split("rating-group ")[1].replace("\n","") != str(sid):
                    #print(cfglst[i+1].split("rating-group ")[1].replace("\n",""))
                    print(cru_str+"该ID："+str(sid)+"匹配不对")
                    commandList.append("注意\n")
                    commandList.append(cru_str+"该ID："+str(sid)+"匹配不对\n")
            except:
                pass
            return True

def PRU_CRU_is_Associate(serviceName,prStr,pruStr,clst):

    #print(serviceName)
    #print(pruStr)
    prStr = 'policy-rule "'+prStr+'"'
    prustr = 'policy-rule-unit "'+pruStr+'"'
    cruStr = 'charging-rule-unit "CRU_'+serviceName+'"'
    #print("+++++",prStr,prustr,cruStr)
    for text in clst:
        if prStr in text and prustr in text and cruStr in text:
            #print(True)
            return True
    #print(False)
    return False

def getTheCompatibleEntryIdByDict():
    global serviceEntryIdDict
    global allEntryIdList
    global allEntryIdDict

    serviceCaseStr = "head"
    retId = -1

    for i in range(2000,20000):
        if i not in allEntryIdDict[serviceCaseStr]:
            retId = i
            allEntryIdDict[serviceCaseStr].append(retId)
            break


    return retId



def addTheCommandtoList_Entry(comLst,tup,enId):
    #print(tup)
    layerLag, changeLag, serviceId, serviceName, ipAddress, protocolNumber, portNumber, url = tup

    comLst.append("entry "+str(enId)+" create\n")
    expression_1 = ""
    expression_2 = ""
    http_port = ""
    if url != None:
        url = url.replace("http://", "").replace("https://", "")
        if url[0] != "*":
            url = "^" + url
        if url[-1]!= "*":
            url = url + "$"

        prefix = ""
        suffix = ""
        if "/*" in url:
            suffix = "/*"
            url = url.replace("/*","")
            url = url + "$"
            expression_2 = "^/*"

        expression_1 = url
        if ":*" not in url and ":" in url:
            expression_1 = url.split(":")[0]+"$"
            expression_2 = "^"+url.split(":")[1][url.split(":")[1].index("/"):len(url.split(":")[1])].replace("$","")+"/*"
            http_port = url.split(":")[1][0:url.split(":")[1].index("/")]

        comLst.append('expression 1 http-host eq "'+expression_1+'"\n')
    if expression_2 != "":
        comLst.append('expression 2 http-uri eq "'+expression_2+'"\n')
    if ipAddress == None:
        comLst.append("server-address eq 10.0.0.172/32\n")
    else:
        if "/" not in ipAddress:
            ipAddress = ipAddress+"/32"
        comLst.append('server-address eq '+ipAddress+'\n')
    if portNumber != None:
        if " " in str(portNumber):
            comLst.append('server-port range ' + str(portNumber) + '\n')
        else:
            comLst.append('server-port eq '+str(portNumber)+'\n')
    if http_port != "":
        comLst.append('http-port eq ' + str(http_port) + '\n')
    comLst.append('application "APP_'+serviceName+"_HeaderEnrich"+'"\n')
    comLst.append("no shutdown\n")
    comLst.append("exit\n")
    comLst.append("\n")
    #纯7L的地址（网址应该创建dns-catch）
    global max_entry_id
    #if ipAddress == None and portNumber == None and tup[7].upper() != tup[7].lower():
    if ipAddress == None and portNumber == None and tup[7] != None:
        dns_entry_id = getTheCompatibleEntryIdByDict()
        comLst.append("exit all\n")
        comLst.append("configure application-assurance group 1:1 policy\n")
        comLst.append("begin\n")
        comLst.append("app-filter\n")
        comLst.append("entry " + str(dns_entry_id) + " create\n")
        if url != None:
            url = url.replace("http://", "").replace("https://", "").replace("^","")
            if url[0] != "*":
                url = "^" + url
            if url[-1]!= "*":
                #print(url)
                url = url.replace("$","") + "$"

            prefix = ""
            suffix = ""
            if "/*" in url:
                suffix = "/*"
                url = url.replace("/*","")
                #url = url + "$"
                expression_2 = "^/*"

            expression_1 = url
            #print(expression_1)
            if ":*" not in url and ":" in url:
                expression_1 = url.split(":")[0]+"$"
                expression_2 = "^"+url.split(":")[1][url.split(":")[1].index("/"):len(url.split(":")[1])].replace("$","")+"/*"
                http_port = url.split(":")[1][0:url.split(":")[1].index("/")]

            comLst.append('expression 1 http-host eq"'+expression_1+'"\n')
        if expression_2 != "":
            comLst.append('expression 2 http-uri eq "'+expression_2+'"\n')

        comLst.append('server-address eq dns-ip-cache "TrustedCache"\n')
        if portNumber != None:
            if " " in str(portNumber):
                comLst.append('server-port range ' + str(portNumber) + '\n')
            else:
                comLst.append('server-port eq '+str(portNumber)+'\n')
        if http_port != "":
            comLst.append('http-port eq ' + str(http_port) + '\n')
        comLst.append('application "APP_'+serviceName+"_HeaderEnrich"+'"\n')
        comLst.append("no shutdown\n")
        comLst.append("exit\n")
        comLst.append("\n\n")
        #因为要添加dns-catch得有两entry所以得添加2次,这里先添加一次
    serviceEntryIdDict[tup[3]].append(enId)


def PR_PRU_CRU_Process(lst,tup,cfglst):
    #print(tup)
    #检测CRU是否存在，不存在则创建
    '''
    if serviceDict["CRU_"+tup[3]] == False:
        # 创建CRU
        lst.append('exit all' + "\n")
        lst.append("configure mobile-gateway profile policy-options " + "\n")
        lst.append('charging-rule-unit "CRU_' + tup[3] + '" ' + "\n")
        lst.append('rating-group ' + str(tup[2]) + "\n")
        lst.append('service-identifier ' + str(tup[2]) + "\n")
        lst.append('reporting-level service-id' + "\n")
        lst.append('exit' + "\n")
        lst.append("\n")
        serviceDict["CRU_" + tup[3]] = True
    '''
    '''
    #检测PR是否存在，不存在则创建
    if serviceDict["PR_" + tup[3]] == False:
        lst.append("该业务需要创建PR\n")
        lst.append('exit all' + "\n")
        lst.append("configure mobile-gateway profile policy-options " + "\n")
        lst.append("该创建PR的命令\n")
        lst.append("\n")
        serviceDict["PR_" + tup[3]] = True
    '''


    # 检测PRU是否存在
    if serviceDict["PRU_" + tup[3]+"_HeaderEnrich"+'_'+tup[0]] == False:
        lst.append('exit all' + "\n")
        lst.append("configure mobile-gateway profile policy-options " + "\n")
        lst.append("begin" + "\n")
        pruKey = "PRU_" + tup[3]+'_'+tup[0]
        #pruStr = 'policy-rule-unit "' + pruKey + '" create' + "\n"
        pruStr = 'policy-rule-unit "' + pruKey + "\n"
        lst.append(pruStr)
        lst.append('flow-description ' + str(1) + "\n")
        lst.append('match' + "\n")
        lst.append('aa-charging-group "CHG_'+tup[3]+'"' + "\n")
        lst.append('exit' + "\n")
        lst.append('exit' + "\n")
        lst.append("\n")
        serviceDict["PRU_" + tup[3] + '_' + tup[0]] = True


    #检测PRU,CRU是否关联到PR
    if serviceDict["PR_" + tup[3]+"_HeaderEnrich"] == False :
        serviceDict["PR_" + tup[3]+"_HeaderEnrich"] = True
        #if PRU_CRU_is_Associate(tup,cfglst) == False:
        #print(tup[3],"需要关联PR,PRU,CRU")
        precedenceId = 10000
        pruKey = "PRU_" + tup[3]+"_HeaderEnrich" + '_' + tup[0]
        pruStr = 'policy-rule-unit "' + pruKey + '"'
        cmpstr = 'policy-rule "PR_' + tup[3]+"_HeaderEnrich" + '" ' + pruStr + ' charging-rule-unit "CRU_' + tup[3] + '" qci * arp * precedence ' + str(precedenceId)
        lst.append(cmpstr)
        lst.append('\n')


def addEntryIdtoserviceEntryIdDict(serviceName,cfglst):
    global serviceEntryIdDict
    entryIdList = []
    if serviceName in serviceEntryIdDict:
        return ""

    for i in range(0,len(cfglst)):
        if 'application "APP_'+serviceName+'"' in cfglst[i] and "create" not in cfglst[i]:
            k = i
            #print(serviceName,k)
            for j in range(k,0,-1):
                if 'server-address eq ip-prefix-list "app_'+serviceName in cfglst[j]:
                    break
                if "entry" in cfglst[j]:
                    #print(cfglst[j])
                    entryIdList.append(int(cfglst[j].split("entry ")[1].split(" create")[0]))
                    break
    serviceEntryIdDict[serviceName] = entryIdList


def APP_str_isExist(app_str, cfglst):
    for text in cfglst:
        if app_str in text:
            return True
    return False


def CHG_str_isExist(chg_str, cfglst):
    for text in cfglst:
        if chg_str in text:
            return True
    return False

def chg_app_create(service_name, cmd_list):
    global log_list
    if serviceDict["CHG_" + service_name+"_HeaderEnrich"] == False:
        log_list.append("创建该业务:"+service_name+"_HeaderEnrich" + "的CHG" + "\n")
        cmd_list.append('exit all\n')
        cmd_list.append('configure application-assurance group 1:1 policy\n')
        cmd_list.append('charging-group "CHG_' + service_name+"_HeaderEnrich" + '" create\n')
        cmd_list.append('description "' + service_name+"_HeaderEnrich" + '_00"\n\n')

    if serviceDict["APP_" + service_name+"_HeaderEnrich"] == False:
        log_list.append("创建该业务:" + service_name+"_HeaderEnrich" + "的APP" + "\n")
        cmd_list.append('exit all\n')
        cmd_list.append('configure application-assurance group 1:1 policy\n')
        cmd_list.append('application "' + service_name+"_HeaderEnrich" + '" create\n')
        cmd_list.append('app-group "APP_GROUP_1"\n')
        cmd_list.append('charging-group "CHG_' + service_name+"_HeaderEnrich" + '"\n\n')


