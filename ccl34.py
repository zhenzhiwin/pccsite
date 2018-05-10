import openpyxl


def getServiceListByList(sheet, startRow):
    changeLag_col = 3
    serviceId_col = 8
    serviceName_col = 10
    ipAddressL3_col = 13
    protocolNumber_col = 14
    portNumberL4_col = 15
    urlL7_col = 16
    layerLag = ""
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
        if protocolNumber == None and portNumberL4 == None:
            layerLag = "L3"
        else:
            layerLag = "L4"
        retList.append((layerLag, changeLag, serviceId, serviceName, ipAddressL3, protocolNumber, portNumberL4, urlL7))

    return retList


def add_pruListtoPRUList(alllist, pruStr, configureList):
    retList = []
    for line in range(0, len(configureList) + 1):
        try:
            if pruStr in configureList[line] and "charging-rule-unit" not in configureList[line]:
                front = line
                for i in range(front, len(configureList) + 1):
                    if "exit" in configureList[i] and (
                            "policy-rule-unit" in configureList[i + 1] or "charging-rule-unit" in configureList[i + 1]):
                        end = i
                        break
        except:
            pass

    try:
        for i in range(front, end + 1):
            retList.append(configureList[i])
    except:
        pass
    if len(retList) != 0:
        alllist.append(retList)


'''
def getPRUlistByConfigureList(tup, configureList):
    layerLag, changeLag, serviceId, serviceName, ipAddress, protocolNumber, portNumber, url = tup
    pruStr = 'policy-rule-unit "PRU_' + serviceName + '_' + layerLag + '"'
    all_ret_list = []
    add_pruListtoPRUList(all_ret_list, pruStr, configureList)
    pruStr = 'policy-rule-unit "PRU_' + serviceName + '_' + layerLag + '_01'+'"'
    add_pruListtoPRUList(all_ret_list, pruStr, configureList)
    pruStr = 'policy-rule-unit "PRU_' + serviceName + '_' + layerLag + '_02' + '"'
    add_pruListtoPRUList(all_ret_list, pruStr, configureList)

    return all_ret_list


def getPRUlistByConfigureList_01(tup, configureList):
    layerLag, changeLag, serviceId, serviceName, ipAddress, protocolNumber, portNumber, url = tup
    pruStr = 'policy-rule-unit "PRU_' + serviceName + '_' + layerLag + '_01"'
    # prStr = 'policy-rule "PR_'+serviceName+'_'+layerLag+'"'
    # print(pruStr)
    exitStr = ""
    findLag = False
    retList = []

    for line in range(0, len(configureList) + 1):
        try:
            if pruStr in configureList[line] and "charging-rule-unit" not in configureList[line]:
                # print("找到PRU:"+str(line))
                # print(configureList[line])
                front = line
                # retList.append(lineValue)
                # exitStr = configureList[line].split('policy-rule-unit "PRU_')[0] + "exit"
                # print(exitStr)
                # findLag = True
                for i in range(front, len(configureList) + 1):
                    if "exit" in configureList[i] and (
                            "policy-rule-unit" in configureList[i + 1] or "charging-rule-unit" in configureList[i + 1]):
                        # print("找到对应的exit:" + str(i))
                        end = i
                        break
        except:
            pass

    try:
        for i in range(front, end + 1):
            retList.append(configureList[i])
    except:
        pass

    return retList
'''


def arrangeTheList(lst):
    sList = []
    retList = []
    tempList = []
    for tup in lst:
        layerLag, changeLag, serviceId, serviceName, ipAddress, protocolNumber, portNumber, url = tup
        sList.append(serviceId)
    # print(sList)
    sList = list(set(sList))
    # print(sList)
    for sValue in sList:
        for tup in lst:
            layerLag, changeLag, serviceId, serviceName, ipAddress, protocolNumber, portNumber, url = tup
            if sValue == serviceId:
                tempList.append(tup)
        retList.append(tempList)
        tempList = []
    # print(retList)
    return retList


def judgePruL4InConfigureList(sName, clst):
    # print("service name is"+sName)
    # print(clst)
    try:
        for i in len(clst):
            if 'policy-rule-unit "PRU_' + sName + '_L4"' in clst[i] and "shallow-inspection-only" in clst[i + 1]:
                return True
    except:
        pass
    return False


def judgeL4Service(lst, clist):
    # print(lst[0])
    pruBool = judgePruL4InConfigureList(lst[0][3], clist)
    if pruBool == True:
        return True

    for text in lst:
        if text[0] == "L4":
            return True
    return False


def handleL4ServiceList(rLst, confList):
    retList = []
    tempList = []
    for serList in rLst:
        # print(serList)
        if judgeL4Service(serList, confList) == True:
            for text in serList:
                layerLag, changeLag, serviceId, serviceName, ipAddress, protocolNumber, portNumber, url = text
                layerLag = "L4"
                tempList.append(
                    (layerLag, changeLag, serviceId, serviceName, ipAddress, protocolNumber, portNumber, url))
            retList.append(tempList)
            tempList = []
        else:
            for text in serList:
                layerLag, changeLag, serviceId, serviceName, ipAddress, protocolNumber, portNumber, url = text
                tempList.append(
                    (layerLag, changeLag, serviceId, serviceName, ipAddress, protocolNumber, portNumber, url))
            retList.append(tempList)
            tempList = []
    return retList


def getTheFlowNumId(serviceName):
    global serviceFlowNumListDict
    # print("+++++",serviceName)
    # print("+++++",serviceFlowNumListDict[serviceName])
    if len(serviceFlowNumListDict[serviceName]) == 0:
        # print(serviceName+"的flow为空")
        if serviceName in serviceFlowNumListDict:
            if len(serviceFlowNumListDict[serviceName]) == 0:
                t = []
                serviceFlowNumListDict[serviceName].append(t)
        return 1
    else:
        # print("+++++",serviceName + "的flow为"+str(serviceFlowNumListDict[serviceName][-1][-1]))
        if serviceFlowNumListDict[serviceName][-1][-1] + 1 > 255:
            # print(serviceName+"该flow超过255了")
            retNum = serviceFlowNumListDict[serviceName][-1][-1] + 1 - 255
            l = []
            l.append(retNum)
            serviceFlowNumListDict[serviceName].append(l)
        else:
            retNum = serviceFlowNumListDict[serviceName][-1][-1] + 1
        return retNum


def addTheCommandtoList(lst, tup, pruLst):
    layerLag, changeLag, serviceId, serviceName, ipAddress, protocolNumber, portNumber, url = tup
    global log_list
    log_list.append("将该条目:"+str(tup)+"加入命令列表中"+"\n")
    # print("+++++++",tup[3],pruLst)
    flowId = getTheFlowNumId(tup[3])
    serviceFlowNumListDict[serviceName][-1].append(flowId)
    # print(tup[3],flowId)
    # return ""
    # 创建PRU
    lst.append('exit all' + "\n")
    lst.append("configure mobile-gateway profile policy-options " + "\n")
    # lst.append("begin" + "\n")
    global serviceDict
    # print(serviceName+"存在着"+str(len(serviceFlowNumListDict[serviceName]))+"个PRU")
    # print(len(serviceFlowNumListDict[serviceName]))
    if len(serviceFlowNumListDict[serviceName]) < 2:
        pruKey = "PRU_" + serviceName + "_" + layerLag
    else:
        pruKey = "PRU_" + serviceName + "_" + layerLag + "_0" + str(len(serviceFlowNumListDict[serviceName]) - 1)
    if serviceDict[pruKey] == True:
        pruStr = 'policy-rule-unit "' + pruKey + '"' + "\n"
    else:
        # pruStr = 'policy-rule-unit "' + pruKey+'" create' + "\n"
        pruStr = 'policy-rule-unit "' + pruKey + "\n"
        serviceDict[pruKey] = True
    # print(pruKey,serviceDict[pruKey])
    # print(pruStr)
    # return ""

    lst.append(pruStr)
    lst.append('shallow-inspection-only' + "\n")
    lst.append('flow-description ' + str(flowId) + "\n")
    lst.append('match' + "\n")
    if layerLag == "L4":
        if protocolNumber != None:
            lst.append('protocol ' + str(protocolNumber) + "\n")
    if "/" in ipAddress:
        ip = ipAddress
    else:
        ip = ipAddress + "/32"
    lst.append('remote-ip ' + ip + "\n")
    if layerLag == "L4":
        if portNumber != None:
            # print("+++++",portNumber)
            if "--" in str(portNumber):
                lst.append('remote-port range ' + str(portNumber).replace("--", " ") + "\n")
            else:
                lst.append('remote-port eq ' + str(portNumber) + "\n")
    #lst.append('exit' + "\n")
    #lst.append('exit' + "\n")
    lst.append("\n")


def getTheFlowNumberList(PruList):
    # print("55555555555555",PruList)
    retList = []
    for pruline in PruList:
        templst = []
        for text in pruline:
            if "flow-description " in text:
                # print("9999999999")
                templst.append(int(text.replace("\n", "").split("flow-description ")[1]))
        # print("555555555",templst)
        retList.append(templst)
    return retList


def getDeletePruStrFlowNumberByList(tup, lst):
    # print("***********",tup,len(lst),lst)
    prustr = None
    retNumber = None
    # print(lst)
    for text in lst:
        pass
    # return (1,2)

    # 有无子网掩码需要处理过
    if "/" in tup[4]:
        ip = tup[4]
    else:
        ip = tup[4] + "/32"
    del_ip_str = ip.replace(" ", "")

    # 端口范围分隔符
    portSplitStr = "--"
    if tup[6] != None:
        if portSplitStr in str(tup[6]):
            portStr = "remote-port range " + tup[6].split(portSplitStr)[0] + " " + tup[6].split(portSplitStr)[1]
        else:
            portStr = "remote-port eq " + str(tup[6])

    '''
    for pruLine in lst:
        for i in range(0, len(pruLine)):
            try:

                if tup[0] == "L3":
                    if "remote-ip " + del_ip_str in lst[i]:

                        retNumber = int(lst[i - 2].split("flow-description ")[1])
                        print("找到",pruLine[0],retNumber)
                        return (pruLine[0].replace("\n", "").split("policy-rule-unit ")[1], retNumber)
                        break
                elif tup[0] == "L4":
                    # print(tup[6])
                    if "protocol " + str(tup[5]) in lst[i] and "remote-ip " + del_ip_str in lst[i + 1] and portStr in \
                            lst[
                                i + 2]:
                        # print("找到协议")
                        retNumber = int(lst[i - 2].split("flow-description ")[1])
                        return (pruLine[0].replace("\n", "").split("policy-rule-unit ")[1], retNumber)
                        break
            except:
                pass
    '''
    # print(del_ip_str)
    for i in range(0, len(lst)):
        # print(lst[i])
        try:

            if tup[0] == "L3":
                if "remote-ip " + del_ip_str in lst[i]:
                    retNumber = int(lst[i - 2].split("flow-description ")[1])
                    #print("找到", retNumber, lst[0])
                    break
            elif tup[0] == "L4":
                # print(tup[6])
                if "protocol " + str(tup[5]) in lst[i] and "remote-ip " + del_ip_str in lst[i + 1] and portStr in lst[
                    i + 2]:
                    # print("找到协议")
                    retNumber = int(lst[i - 2].split("flow-description ")[1])
                    break
        except:
            pass

    if retNumber != None:
        return (lst[0].replace("\n", "").split("policy-rule-unit ")[1], retNumber)

    return (None, None)


def deleteTheFlow(comList, tup, flowStrList):
    # print("+++++++++++",tup,flowStrList)
    global log_list

    prustr, del_num = None, None
    for line in flowStrList:
        prustr, del_num = getDeletePruStrFlowNumberByList(tup, line)
        #log_list.append("删除该条目:" + str(tup) + "获取删除的pru名，flow id"+str(prustr)+","+str(del_num) + "\n")
        if prustr != None:
            log_list.append("删除该条目:" + str(tup) + "获取删除的pru名，flow id" + prustr + "," + str(del_num) + "\n")
            break

    if del_num == None:
        comList.append(str(tup) + "该删除条目在配置文件中不存在\n")
        log_list.append(str(tup) + "该删除条目在配置文件中不存在\n")
    else:
        comList.append('exit all' + "\n")
        comList.append("configure mobile-gateway profile policy-options " + "\n")
        comList.append('policy-rule-unit ' + prustr + "\n")
        comList.append("no flow-description " + str(del_num) + "\n")
        # comList.append(str(tup)+"删除的是:"+prustr+"下的flow "+str(del_num))
        comList.append('\n')
        log_list.append(str(tup) + "删除的是:" + prustr + "下的flow " + str(del_num)+"\n")
    # serviceFlowNumListDict[tup[3]]

    '''
    if pruname == "" and delete_flow_number == -1:
        comList.append(tup[3] + "的" + tup[4] + "在配置Log中不存在")
        return ""

    pruname = pruname.replace('\n', "")
    comList.append('exit all' + "\n")
    comList.append("configure mobile-gateway profile policy-options " + "\n")
    comList.append("begin" + "\n")
    comList.append('policy-rule-unit ' + pruname + "\n")
    comList.append("no flow-description " + str(delete_flow_number) + "\n")
    comList.append("\n\n")

    global serviceFlowNumListDict
    # print(pruname+"删除的flow号："+str(delete_flow_number))
    # print(pruname+str(serviceFlowNumListDict[pruname]))
    if delete_flow_number in serviceFlowNumListDict[pruname]:
        serviceFlowNumListDict[pruname].remove(delete_flow_number)
    # print("删除后"+pruname + str(serviceFlowNumListDict[pruname]))
    if len(serviceFlowNumListDict[pruname]) == 1 and serviceFlowNumListDict[pruname][0] == 0:
        comList.append("删除PRU关联命令\n")
    '''


def setTheFlowNumList(pruLst):
    if len(pruLst) > 0:
        # print(pruLst[0].split("policy-rule-unit ")[1])
        pruKey = pruLst[0].split("policy-rule-unit ")[1].replace('\n', "")

        if pruKey not in serviceFlowNumListDict:
            serviceFlowNumListDict[pruKey] = []
        # 列表中的0 是否有0表示配置log中的flow是否已经记录过,在新增中是动态添加的
        if 0 not in serviceFlowNumListDict[pruKey]:
            serviceFlowNumListDict[pruKey].append(0)
            for pruline in pruLst:
                if "flow-description " in pruline:
                    serviceFlowNumListDict[pruKey].append(int(pruline.split("flow-description ")[1]))
        serviceFlowNumListDict[pruKey] = list(set(serviceFlowNumListDict[pruKey]))


def setPRUCRUtoServiceDict(tup, cfglst):
    global serviceDict
    serviceId = tup[2]
    serviceName = tup[3]
    if "PR_" + serviceName not in serviceDict:
        serviceDict["PR_" + serviceName] = False
    if "PRU_" + serviceName + "_" + tup[0] not in serviceDict:
        serviceDict["PRU_" + serviceName + "_" + tup[0]] = False
    if "PRU_" + serviceName + "_" + tup[0] + "_01" not in serviceDict:
        serviceDict["PRU_" + serviceName + "_" + tup[0] + "_01"] = False
    if "PRU_" + serviceName + "_" + tup[0] + "_02" not in serviceDict:
        serviceDict["PRU_" + serviceName + "_" + tup[0] + "_02"] = False
    if "PRU_" + serviceName + "_" + tup[0] + "_03" not in serviceDict:
        serviceDict["PRU_" + serviceName + "_" + tup[0] + "_03"] = False
    if "CRU_" + serviceName not in serviceDict:
        serviceDict["CRU_" + serviceName] = False

    # 判断PR是否存在
    prStr = 'policy-rule "PR_' + serviceName + '"'
    if PR_str_isExist(prStr, cfglst) == True:
        serviceDict["PR_" + serviceName] = True

    # 判断PRU是否存在
    pruStr = 'policy-rule-unit "PRU_' + serviceName + '_' + tup[0] + '"'
    if PRU_str_isExist(pruStr, cfglst) == True:
        serviceDict["PRU_" + serviceName + "_" + tup[0]] = True
        # print(serviceName+"_PRU",serviceDict[serviceName+"_PRU"])
    pruStr = 'policy-rule-unit "PRU_' + serviceName + '_' + tup[0] + "_01" + '"'
    if PRU_str_isExist(pruStr, cfglst) == True:
        serviceDict["PRU_" + serviceName + "_" + tup[0] + "_01"] = True
    pruStr = 'policy-rule-unit "PRU_' + serviceName + '_' + tup[0] + "_02" + '"'
    if PRU_str_isExist(pruStr, cfglst) == True:
        serviceDict["PRU_" + serviceName + "_" + tup[0] + "_02"] = True
    pruStr = 'policy-rule-unit "PRU_' + serviceName + '_' + tup[0] + "_03" + '"'
    if PRU_str_isExist(pruStr, cfglst) == True:
        serviceDict["PRU_" + serviceName + "_" + tup[0] + "_03"] = True

    # 判断CRU是否存在
    cruStr = 'charging-rule-unit "CRU_' + serviceName + '"'
    if CRU_str_isExist(cruStr, serviceId, cfglst) == True:
        serviceDict["CRU_" + serviceName] = True
        # print(serviceName+"_CRU", serviceDict[serviceName + "_CRU"])


def PR_str_isExist(pr_str, cfglst):
    i = 0
    for text in cfglst:
        if pr_str in text and "qci * arp * precedence" not in text:
            i += 1
    if i == 2:
        return True
    else:
        return False


def PRU_str_isExist(pru_str, cfglst):
    for text in cfglst:
        if pru_str in text and "qci * arp * precedence" not in text:
            return True
    return False


def CRU_str_isExist(cru_str, sid, cfglst):
    global commandList

    for i in range(0, len(cfglst)):
        if cru_str in cfglst[i] and "qci * arp * precedence" not in cfglst[i]:
            # print(i,cfglst[i+1])
            try:
                if cfglst[i + 1].split("rating-group ")[1].replace("\n", "") != str(sid):
                    # print(cfglst[i+1].split("rating-group ")[1].replace("\n",""))
                    print(cru_str + "该ID：" + str(sid) + "匹配不对")
                    commandList.append("注意\n")
                    commandList.append(cru_str + "该ID：" + str(sid) + "匹配不对\n")
            except:
                pass
            return True


def PRU_CRU_is_Associate(serviceName, prStr, pruStr, clst):
    # print(serviceName)
    # print(pruStr)
    prStr = 'policy-rule "' + prStr + '"'
    prustr = 'policy-rule-unit "' + pruStr + '"'
    cruStr = 'charging-rule-unit "CRU_' + serviceName + '"'
    # print("+++++",prStr,prustr,cruStr)
    for text in clst:
        if prStr in text and prustr in text and cruStr in text:
            # print(True)
            return True
    # print(False)
    return False


def getPRUlistByConfigureList(tup, configureList):
    layerLag, changeLag, serviceId, serviceName, ipAddress, protocolNumber, portNumber, url = tup
    # print(layerLag,changeLag,serviceId,serviceName,ipAddress,protocolNumber,portNumber,url)
    # serviceName = "wxcs_03"
    # serviceName = "xgsp_00"
    # pruStr = 'policy-rule-unit "PRU_'+serviceName+'_'+layerLag+'"'
    pruStr = 'policy-rule-unit "PRU_' + serviceName + '_' + layerLag
    # prStr = 'policy-rule "PR_'+serviceName+'_'+layerLag+'"'
    # print(pruStr)
    exitStr = ""
    findLag = False
    retList = []
    tlist = []

    for line in range(0, len(configureList) + 1):
        # print(line)
        try:
            if pruStr in configureList[line] and "charging-rule-unit" not in configureList[line]:
                # print("找到PRU:"+str(line))
                # print(configureList[line])
                front = line
                for i in range(front, len(configureList) + 1):
                    if "exit" in configureList[i] and (
                            "policy-rule-unit" in configureList[i + 1] or "charging-rule-unit" in configureList[i + 1]):
                        # print("找到对应的exit:" + str(i))
                        end = i
                        break
                try:
                    for i in range(front, end + 1):
                        # retList.append(configureList[i])
                        tlist.append(configureList[i])
                    retList.append(tlist)
                    tlist = []
                    front = -1
                    end = -1
                except:
                    pass
        except:
            pass
    '''
    try:
        for i in range(front,end+1):
            #retList.append(configureList[i])
            tlist.append(configureList[i])
        retList.append(tlist)
    except:
        pass
    '''
    return retList


def PR_PRU_CRU_Process(lst, tup, cfglst):
    global log_list

    # print(tup)
    # 检测CRU是否存在，不存在则创建
    if serviceDict["CRU_" + tup[3]] == False:
        # 创建CRU
        log_list.append("创建该业务:"+tup[3]+"的CRU")
        lst.append('exit all' + "\n")
        lst.append("configure mobile-gateway profile policy-options " + "\n")
        lst.append('charging-rule-unit "CRU_' + tup[3] + '" ' + "\n")
        lst.append('rating-group ' + str(tup[2]) + "\n")
        lst.append('service-identifier ' + str(tup[2]) + "\n")
        lst.append('reporting-level service-id' + "\n")
        lst.append('exit' + "\n")
        lst.append("\n")

    '''
    #检测PR是否存在，不存在则创建
    if serviceDict["PR_" + tup[3]] == False:
        lst.append("该业务需要创建PR\n")
        lst.append('exit all' + "\n")
        lst.append("configure mobile-gateway profile policy-options " + "\n")
        lst.append("\n")
    '''

    # 检测PRU是否存在，存在则关联,PRU在创建flow的时候已经创建并标记了,所以只要将现存的PRU关联下就可以了
    log_list.append("创建该业务:" + tup[3] + "的PRU")
    if len(serviceFlowNumListDict[tup[3]]) == 4:
        for i in range(4, 1, -1):
            pruStr = 'PRU_' + tup[3] + '_' + tup[0] + '_0' + str(i - 1)
            prStr = 'PR_' + tup[3] + '_0' + str(i - 1)
            id = 10000
            # print(pruStr, PRU_CRU_is_Associate(tup[3],prStr, pruStr, cfglst))
            if PRU_CRU_is_Associate(tup[3], prStr, pruStr, cfglst) == False:
                cmpstr = 'policy-rule "' + prStr + '" policy-rule-unit "' + pruStr + '" charging-rule-unit "CRU_' + tup[
                    3] + '" qci * arp * precedence ' + str(id)
                lst.append("该业务需要创建PR\n")
                lst.append(cmpstr + '\n')
                lst.append('policy-rule-base  "PRB_cmnet_L3L4"' + "\n")
                lst.append('policy-rule  "' + prStr + '"\n')
                lst.append('policy-rule-base  "PRB_cmwap_L3L4"' + "\n")
                lst.append('policy-rule  "' + prStr + '"\n')
                lst.append('exit all' + "\n")

        pruStr = 'PRU_' + tup[3] + '_' + tup[0]
        prStr = 'PR_' + tup[3]
        id = 10000
        # print(pruStr, PRU_CRU_is_Associate(tup[3], prStr, pruStr, cfglst))
        if PRU_CRU_is_Associate(tup[3], prStr, pruStr, cfglst) == False:
            cmpstr = 'policy-rule "' + prStr + '" policy-rule-unit "' + pruStr + '" charging-rule-unit "CRU_' + tup[
                3] + '" qci * arp * precedence ' + str(id)
            lst.append("该业务需要创建PR\n")
            lst.append(cmpstr + '\n')
            lst.append('policy-rule-base  "PRB_cmnet_L3L4"' + "\n")
            lst.append('policy-rule  "' + prStr + '"\n')
            lst.append('policy-rule-base  "PRB_cmwap_L3L4"' + "\n")
            lst.append('policy-rule  "' + prStr + '"\n')
            lst.append('exit all' + "\n")
    elif len(serviceFlowNumListDict[tup[3]]) == 3:
        # print(tup[3], len(serviceFlowNumListDict[tup[3]]))
        for i in range(3, 1, -1):
            pruStr = 'PRU_' + tup[3] + '_' + tup[0] + '_0' + str(i - 1)
            prStr = 'PR_' + tup[3] + '_0' + str(i - 1)
            id = 10000
            # print(pruStr, PRU_CRU_is_Associate(tup[3],prStr, pruStr, cfglst))
            if PRU_CRU_is_Associate(tup[3], prStr, pruStr, cfglst) == False:
                cmpstr = 'policy-rule "' + prStr + '" policy-rule-unit "' + pruStr + '" charging-rule-unit "CRU_' + tup[
                    3] + '" qci * arp * precedence ' + str(id)
                lst.append("该业务需要创建PR\n")
                lst.append(cmpstr + '\n')
                lst.append('policy-rule-base  "PRB_cmnet_L3L4"' + "\n")
                lst.append('policy-rule  "' + prStr + '"\n')
                lst.append('policy-rule-base  "PRB_cmwap_L3L4"' + "\n")
                lst.append('policy-rule  "' + prStr + '"\n')
                lst.append('exit all' + "\n")
        pruStr = 'PRU_' + tup[3] + '_' + tup[0]
        prStr = 'PR_' + tup[3]
        id = 10000
        # print(pruStr, PRU_CRU_is_Associate(tup[3], prStr, pruStr, cfglst))
        if PRU_CRU_is_Associate(tup[3], prStr, pruStr, cfglst) == False:
            cmpstr = 'policy-rule "' + prStr + '" policy-rule-unit "' + pruStr + '" charging-rule-unit "CRU_' + tup[
                3] + '" qci * arp * precedence ' + str(id)
            lst.append("该业务需要创建PR\n")
            lst.append(cmpstr + '\n')
            lst.append('policy-rule-base  "PRB_cmnet_L3L4"' + "\n")
            lst.append('policy-rule  "' + prStr + '"\n')
            lst.append('policy-rule-base  "PRB_cmwap_L3L4"' + "\n")
            lst.append('policy-rule  "' + prStr + '"\n')
            lst.append('exit all' + "\n")
    elif len(serviceFlowNumListDict[tup[3]]) == 2:
        for i in range(2, 1, -1):
            pruStr = 'PRU_' + tup[3] + '_' + tup[0] + '_0' + str(i - 1)
            prStr = 'PR_' + tup[3] + '_0' + str(i - 1)
            id = 10000
            # print(pruStr, PRU_CRU_is_Associate(tup[3],prStr, pruStr, cfglst))
            if PRU_CRU_is_Associate(tup[3], prStr, pruStr, cfglst) == False:
                cmpstr = 'policy-rule "' + prStr + '" policy-rule-unit "' + pruStr + '" charging-rule-unit "CRU_' + tup[
                    3] + '" qci * arp * precedence ' + str(id)
                lst.append("该业务需要创建PR\n")
                lst.append(cmpstr + '\n')
                lst.append('policy-rule-base  "PRB_cmnet_L3L4"' + "\n")
                lst.append('policy-rule  "' + prStr + '"\n')
                lst.append('policy-rule-base  "PRB_cmwap_L3L4"' + "\n")
                lst.append('policy-rule  "' + prStr + '"\n')
                lst.append('exit all' + "\n")
        pruStr = 'PRU_' + tup[3] + '_' + tup[0]
        prStr = 'PR_' + tup[3]
        id = 10000
        # print(pruStr, PRU_CRU_is_Associate(tup[3], prStr, pruStr, cfglst))
        if PRU_CRU_is_Associate(tup[3], prStr, pruStr, cfglst) == False:
            cmpstr = 'policy-rule "' + prStr + '" policy-rule-unit "' + pruStr + '" charging-rule-unit "CRU_' + tup[
                3] + '" qci * arp * precedence ' + str(id)
            lst.append("该业务需要创建PR\n")
            lst.append(cmpstr + '\n')
            lst.append('policy-rule-base  "PRB_cmnet_L3L4"' + "\n")
            lst.append('policy-rule  "' + prStr + '"\n')
            lst.append('policy-rule-base  "PRB_cmwap_L3L4"' + "\n")
            lst.append('policy-rule  "' + prStr + '"\n')
            lst.append('exit all' + "\n")
    else:
        pruStr = 'PRU_' + tup[3] + '_' + tup[0]
        prStr = 'PR_' + tup[3]
        id = 10000
        # print(pruStr, PRU_CRU_is_Associate(tup[3], prStr, pruStr, cfglst))
        if PRU_CRU_is_Associate(tup[3], prStr, pruStr, cfglst) == False:
            cmpstr = 'policy-rule "' + prStr + '" policy-rule-unit "' + pruStr + '" charging-rule-unit "CRU_' + tup[
                3] + '" qci * arp * precedence ' + str(id)
            lst.append("该业务需要创建PR\n")
            lst.append(cmpstr + '\n')
            lst.append('policy-rule-base  "PRB_cmnet_L3L4"' + "\n")
            lst.append('policy-rule  "' + prStr + '"\n')
            lst.append('policy-rule-base  "PRB_cmwap_L3L4"' + "\n")
            lst.append('policy-rule  "' + prStr + '"\n')
            lst.append('exit all' + "\n")
    lst.append('\n')


def gen_l34(configList,path):
    # 全局变量字典用于存储业务是否已经创建（PRU,CRU）(True,False) 业务名:pru是否存在
    global serviceDict
    serviceDict = {}
    global log_list
    log_list = []
    global serviceFlowStrListDict
    serviceFlowStrListDict = {}
    global serviceFlowNumListDict
    serviceFlowNumListDict = {}

    commandList = []
    #print("把excel表拖入cmd窗口\n")
    # excel_path = input()
    # excel_path = "D:\chargingContext20180403\L347处理\内容计费整理L3.xlsx"
    excel_path = path + "\\内容计费整理L34.xlsx"
    #print("把内容计费的配置log表拖入cmd窗口\n")
    # chargingContextLog_path = input()
    # chargingContextLog_path = "D:\chargingContext20180403\sae133-config-20180330.txt"
    #chargingContextLog_path = "E:\processL347\内容计费text\sae133-config-20180330.txt"
    #configFile = open(chargingContextLog_path, 'r')
    #configList = configFile.readlines()
    #configFile.close()

    excel = openpyxl.load_workbook(excel_path)
    # sheet = excel["本次变更"]
    sheet = excel["L34"]
    # sheet = excel.get_sheet_by_name("本次变更")
    serviceList = []
    serviceList = getServiceListByList(sheet, 3)
    # print(serviceList)
    resultList = []
    resultList = arrangeTheList(serviceList)
    # print(resultList)
    commandList.append('exit all' + "\n")
    commandList.append("configure mobile-gateway profile policy-options " + "\n")
    #commandList.append("begin" + "\n")

    for resultlst in resultList:
        # print(resultlst)
        # continue
        #commandList.append(resultlst[0][3] + "业务进行增删操作\n")
        setPRUCRUtoServiceDict(resultlst[0], configList)

        pruList = []
        if resultlst[0][3] not in serviceFlowStrListDict:
            pruList = getPRUlistByConfigureList(resultlst[0], configList)
            log_list.append("获取该业务："+resultlst[0][3]+"的所有PRU："+str(pruList)+"\n")
            serviceFlowStrListDict[resultlst[0][3]] = pruList
            #print("*********", resultlst[0][3],len(pruList), pruList)

        pruFlowNumList = []
        if resultlst[0][3] not in serviceFlowNumListDict:
            pruFlowNumList = getTheFlowNumberList(pruList)
            log_list.append("获取该业务：" + resultlst[0][3] + "的所有PRU的数字列表：" + str(pruFlowNumList) + "\n")
            serviceFlowNumListDict[resultlst[0][3]] = pruFlowNumList
            #print("///////////",resultlst[0][3], pruFlowNumList)

        # print("*********",serviceFlowNumListDict["aqy_00"])
        for tupline in resultlst:
            if tupline[1] == "新增":
                # continue
                # print("----",serviceFlowNumListDict[tupline[3]])
                addTheCommandtoList(commandList, tupline, serviceFlowNumListDict[tupline[3]])
            else:
                # print("删除")
                deleteTheFlow(commandList, tupline, serviceFlowStrListDict[tupline[3]])

                # for text in pruList:
        # 创建PR,CRU,PRU,关联PR
        PR_PRU_CRU_Process(commandList, resultlst[0], configList)

    '''
    print("000")
    for key in serviceFlowNumListDict:
        #print(key + str(serviceFlowNumListDict[key]))
        print(key+":")
        for line in serviceFlowNumListDict[key]:
            print(line)

    print("111")
    for key in serviceFlowStrListDict:
        print(key + str(serviceFlowStrListDict[key]))
    print("222")
    for key in serviceDict:
        print(key + str(serviceDict[key]))
    # for linetext in pruList:
    #   print(linetext)
    '''
    fo = open(path + "\\L34.txt", "w")
    fo.writelines(commandList)
    fo.close()
    if log_list:
        fo_log = open(path + "\\L34.log", "w")
        fo_log.writelines(log_list)
        fo_log.close()

        fo_log = open("tmp\\L34.log", "w")
        fo_log.writelines(log_list)
        fo_log.close()


'''
global serviceDict
serviceDict = {}

global serviceFlowStrListDict
serviceFlowStrListDict = {}
global serviceFlowNumListDict
serviceFlowNumListDict = {}
'''