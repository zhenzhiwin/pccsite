# coding:utf-8
import openpyxl,ccl34,ccl7_iplist,ccL7,os,time


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

        retList.append((changeLag, serviceId, serviceName, ipAddressL3, protocolNumber, portNumberL4, urlL7))

    return retList


def arrangeTheList(lst, configureList):
    sList = []
    retList = []
    tempList = []
    for tup in lst:
        changeLag, serviceId, serviceName, ipAddress, protocolNumber, portNumber, url = tup
        sList.append(serviceId)
    # print(sList)
    sList = list(set(sList))
    # print(sList)
    for sValue in sList:
        for tup in lst:
            changeLag, serviceId, serviceName, ipAddress, protocolNumber, portNumber, url = tup
            if sValue == serviceId:
                tempList.append(tup)
        retList.append(tempList)
        tempList = []
    # print(retList)
    newRetList = []
    tlst = []
    for retline in retList:
        # print(retline[0][2])
        layerLag = selectL347lag(retline, configureList)
        for tup in retline:
            changeLag, serviceId, serviceName, ipAddress, protocolNumber, portNumber, url = tup
            tlst.append((layerLag, changeLag, serviceId, serviceName, ipAddress, protocolNumber, portNumber, url))
        newRetList.append(tlst)
        tlst = []
    return newRetList


def selectL347lag(tupList, cfgLst):
    # print(tupList[0][2])

    for text in cfgLst:
        if 'policy-rule-unit "PRU_' + tupList[0][2] + '_' in text and "qci * arp * precedence" not in text:
            if "L3" in text:
                return "L3"
            if "L4" in text:
                return "L4"
            if "L7" in text:
                return "L7"

    for tup in tupList:
        if tup[6] != None:
            return "L7"
    # print("++",tupList)
    for tup in tupList:
        if tup[4] != None or tup[5] != None:
            return "L4"

    return "L3"


def writeRowInExcel(sheet, px, py, writetup):
    sheet.cell(row=py, column=1, value=writetup[0])
    sheet.cell(row=py, column=3, value=writetup[1])
    sheet.cell(row=py, column=8, value=writetup[2])
    sheet.cell(row=py, column=10, value=writetup[3])
    sheet.cell(row=py, column=13, value=writetup[4])
    sheet.cell(row=py, column=14, value=writetup[5])
    sheet.cell(row=py, column=15, value=writetup[6])
    sheet.cell(row=py, column=16, value=writetup[7])


def getUrlTimes(tups7, urlstr):
    t = 0
    for line in tups7:
        if line[7] == urlstr:
            t += 1
    return t


def isIpList(serviceName, cfglist, http_host):
    http_host = http_host.replace("http://", "").replace("https://", "").replace("/*", "").replace(":*", "").split("/")[
        0]
    # print(serviceName,http_host)
    for i in range(0, len(cfglist)):
        if http_host in cfglist[i]:  # 先判断http_host 再判断下面的server-address eq ....来确认是否是iplist
            k = i
            for j in range(k, len(cfglist)):
                if "no shutdown" in cfglist[j]:
                    break
                if 'server-address eq ip-prefix-list "app_' + serviceName in cfglist[j]:
                    return True
    return False


def getIPlistServiceTupList(tupLst7, configList):
    L7list = []
    urlList = []
    #url_times = []
    for tup in tupLst7:
        if tup[7] != None:
            L7list.append(tup)
            urlList.append(tup[7])
    # print(list(set(urlList)))
    urlList = list(set(urlList))
    serviceDict = {}
    iplist = []

    for tup in L7list:
        if isIpList(tup[3], configList, tup[7]) == True:
            iplist.append(tup)

    for url in urlList:
        urlTime = getUrlTimes(tupLst7, url)
        # print(url + "出现次数:" + str(urlTime))
        #url_times.append(url + " APPEARS:" + str(urlTime)+" TIME(S)")
        if urlTime > 5:
            for tup in tupLst7:
                if tup[7] == url:
                    iplist.append(tup)

    # for line in iplist:
    #    print(line)
    return list(set(iplist))


def writeExcel(lst, configList,path):
    tupListL34 = []
    # tupListL4 = []
    tupListL7 = []
    #url_times = []
    for llst in lst:
        if llst[0][0] == "L3":
            for tup in llst:
                tupListL34.append(tup)

    for llst in lst:
        if llst[0][0] == "L4":
            for tup in llst:
                tupListL34.append(tup)

    for llst in lst:
        if llst[0][0] == "L7":
            for tup in llst:
                tupListL7.append(tup)

    # print("所有L7:",tupListL7)
    if len(tupListL34) != 0:
        wb = openpyxl.Workbook()
        sheet = wb.active
        sheet.title = "L34"
        x = 1
        y = 3
        for tup in tupListL34:
            writeRowInExcel(sheet, x, y, tup)
            y += 1
        fPath = path + "\\内容计费整理L34" + ".xlsx"
        wb.save(fPath)
        wb.close()

    '''
    if len(tupListL4) !=0:
        wb = openpyxl.Workbook()
        sheet = wb.active
        sheet.title = "L4"
        x = 1
        y = 3
        for tup in tupListL4:
            writeRowInExcel(sheet, x, y, tup)
            y += 1
        fPath = "./" + "内容计费整理L4" + ".xlsx"
        wb.save(fPath)
        wb.close()
    '''
    ip_list_tupList = []

    if len(tupListL7) != 0:
        ip_list_tupList = getIPlistServiceTupList(tupListL7, configList)
        #url_times = getIPlistServiceTupList(tupListL7, configList)[1]
        # print("iplist+++",ip_list_tupList)
        # print("+++++++++++")
        for line in ip_list_tupList:
            # print(line)
            tupListL7.remove(line)

    if len(tupListL7) != 0:
        wb = openpyxl.Workbook()
        sheet = wb.active
        sheet.title = "L7"
        x = 1
        y = 3
        for tup in tupListL7:
            writeRowInExcel(sheet, x, y, tup)
            y += 1
        fPath = path + "\\内容计费整理L7" + ".xlsx"
        wb.save(fPath)
        wb.close()

    # print("+++",ip_list_tupList)
    del_ip_list_tupList = []
    add_ip_list_tupList = []
    for tup in ip_list_tupList:
        if tup[1] == "删除":
            del_ip_list_tupList.append(tup)
        if tup[1] == "新增":
            add_ip_list_tupList.append(tup)

    # print("+",add_ip_list_tupList)
    # print("-", del_ip_list_tupList)
    # for tup in del_ip_list_tupList:
    # print("    ",tup)
    if len(add_ip_list_tupList) != 0:
        wb = openpyxl.Workbook()
        sheet = wb.active
        sheet.title = "ip_prefix_list_add"
        sheet_del = wb.create_sheet("ip_prefix_list_del")

    if len(add_ip_list_tupList) != 0:
        #wb = openpyxl.Workbook()
        #sheet = wb.active
        #sheet.title = "ip_prefix_list"
        x = 1
        y = 3
        for tup in add_ip_list_tupList:
            writeRowInExcel(sheet, x, y, tup)
            y += 1
        fPath = path + "\\ip_prefix_list_L7" + ".xlsx"
        # wb.save(fPath)
        # wb.close()

    if len(del_ip_list_tupList) != 0:
        # del sheet
        #wb = openpyxl.Workbook()
        #sheet = wb.active
        #sheet.title = "ip_prefix_list_del"
        x = 1
        y = 3
        for tup in del_ip_list_tupList:
            writeRowInExcel(sheet_del, x, y, tup)
            y += 1
        fPath = path + "\\ip_prefix_list_L7" + ".xlsx"
        # fPath = "./" + "ip_prefix_list_del" + ".xlsx"
    wb.save(fPath)
    wb.close()
    return tupListL34,tupListL7,del_ip_list_tupList,add_ip_list_tupList


def gen_origin_api(*args):
    serviceDi = []
    path=''
    path=os.path.abspath('.')
    configFile = open(args[1], 'r', encoding='utf-8')
    configList = configFile.readlines()
    configFile.close()
    for ne_name in configList:
        if ne_name.find('BNK')!=-1:
            ne_name=ne_name[14:-2]
            l_time = time.strftime('%Y%m%d', time.localtime(time.time()))
            path=path+'\\'+'Generated\\'+ne_name+'\\'+l_time
            mkdir(path)
            break
    excel = openpyxl.load_workbook(args[0])
    sheet = excel["本次变更"]
    serviceList = []
    serviceList = getServiceListByList(sheet, 3)

    resultList = arrangeTheList(serviceList, configList)

    statistics_list = writeExcel(resultList, configList,path)
    if os.path.exists(path + "\\内容计费整理L34.xlsx"):
        ccl34.gen_l34(configList,path)
    if os.path.exists(path+"\\内容计费整理L7.xlsx"):
        serviceDi=ccL7.gen_l7(configList,path)
    if os.path.exists(path+"\\ip_prefix_list_L7.xlsx"):
        ccl7_iplist.gen_iplist(configList,path)
    return serviceDi

def mkdir(path):
    path = path.strip()
    # path = path.rstrip("\\")
    isExists = os.path.exists(path)
    if not isExists:
        os.makedirs(path)
        return True
    else:
        # print(path + ' 目录已存在,将直接覆盖旧文件...')
        return False
