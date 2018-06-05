import gc
import openpyxl
import gc,time,os,processL347

import openpyxl


def getWholeChargingListByfile(loglist):
    front = -1
    end = -1
    lst = []
    for a in range(0,len(loglist)):
        #print(loglist[a])
        try:
            if ("]#" in loglist[a] or "]$" in loglist[a]) and ">pGWRecord(79)" in loglist[a + 1]:
                front = a
        except:
            pass
        try:
            if "consolidationResult" in loglist[a] and ("]#" in loglist[a + 2] or"]$" in loglist[a+2]):
                end = a
                lst.append((front,end))
                front = -1
                end = -1
        except:
            pass

        #loglist[a]
    #print(lst)
    return  lst


def getRecordList(lst,front,end):

    allrecordlist = []
    ltemp = []
    #if ">" in lst[199]:
     #   print("recode")
    #if "101" in lst[69] or "consolidationResult" in lst[i]:
     #   print("recode")
    for i in range(front,end):
        if ">" in lst[i]:
            #print(lst[i])
            ltemp.append(lst[i])
            #consolidationResult
        #if "consolidationResult" in lst[i]:
        #print(lst[i])
        #if "101" in lst[i] or "consolidationResult" in lst[i]:
        if "consolidationResult" in lst[i]:
            #print("+++++"+str(i))
            #ltemp.append(lst[i])
            allrecordlist.append(ltemp)
            ltemp = []
            #print("有空格"+lst[i])
            #prin(i)
        #print(ltemp)
        #print(allrecordlist)
        #time.sleep(1)
        #print("======"+str(i))
    #print(allrecordlist)
    return allrecordlist



def getBillFileName(billstr):
    #billstr.split(" ")[3].replace("/tmp","").replace("/","").replace(".res","").replace(".txt","")
    #print(billstr)
    for line in billstr.split(" "):
        if "cg" in line and ".dat" in line:
            #print(line)
            return line.replace("/tmp","").replace("/","").replace(".res","").replace(".txt","")



def write07Excel(fname,dictlist):
    path = os.path.abspath('.')
    wb = openpyxl.Workbook()
    sheet = wb.active
    sheet.title = "text"
    titlelist = ["序号","话单类型","测试号码","IMSI","APN","RAT Type","startTime","stopTime","RG开始时间","RG结束时间","上行流量","下行流量","SERVICE_ID","话单文件","CG IP地址"]
    x = 1
    for v in titlelist:
        sheet.cell(row=1, column=x, value=v)
        x+=1
    #y=1
    for key in dictlist:
        #print(key)
        for keyValueList in dictlist[key]:
            writeRowInExcel(sheet,key,keyValueList)
            #y+=1
            #print(keyValueList)
    l_time = time.strftime('%Y%m%d_%H%M%S', time.localtime(time.time()))
    path =  path+'\\' + 'Generated\\' + l_time
    processL347.mkdir(path)
    path =  path+'\\'+l_time+'.xlsx'
    wb.save(path)
    wb.close()

    #print("写入数据成功！")


def getnumber(str):
    #print(str)
    retstr = ""
    for n in range(0,len(str),2):
        if n % 2 == 0:
            tstr = str[n+1] + str[n]
            retstr += tstr
    #print(retstr.replace("f",""))
    return retstr.replace("f","")


def getRGlist(lst):
    rtlist = []
    tmplist = []
    for text in lst:
        if "serviceIdentifier" in text:
            tmplist.append(text.split("value:")[1])
            rtlist.append(tmplist)
            tmplist = []
        else:
            #获取rg开始时间
            if "timeOfFirstUsage" in text:
                tmplist.append(text.split("value:")[1])
            if "timeOfLastUsage" in text:
                tmplist.append(text.split("value:")[1])
            if "datavolumeFBCUplink" in text:
                tmplist.append(text.split("value:")[1])
            if "datavolumeFBCDownlink" in text:
                tmplist.append(text.split("value:")[1])
    #print(rtlist)
    return rtlist

def handleOneRecord(wlist):
    #该函数把需要填的验证内容存入列表
    rList = []
    rglist = []
    retList = []
    #获取话单类型
    for text in wlist:
        if "recordType" in text:
            rList.append(text.split(":")[1])
            break
    #获取msisdn
    for text in wlist:
        if "servedMSISDN" in text:
            numstr = text.split(":")[1].replace(" 0x","")
            msisdn = getnumber(numstr)
            rList.append(msisdn)
            break
    # 获取imsi
    for text in wlist:
        if "servedIMSI" in text:
            numstr = text.split(":")[1].replace(" 0x","")
            imsi = getnumber(numstr)
            rList.append(imsi)
            break
    # 获取APN
    for text in wlist:
        if "accessPointNameNI" in text:
            rList.append(text.split(":")[1])
            break

    # 获取基站类型
    for text in wlist:
        if "rATType" in text:
            rList.append(text.split(":")[1])
            break
    # 获取记录开始时间
    for text in wlist:
        if "recordOpeningTime" in text:
            rList.append(text.split("value:")[1])
            break
    # 获取记录结束时间(stoptime)
    for text in wlist:
        if "timeOfReport" in text:
            stoptime = text.split("value:")[1]
    rList.append(stoptime)
    #print(rList)
    rglist = getRGlist(wlist)
    #print(rglist)
    for rl in rglist:
        t = []
        t.extend(rList)
        t.extend(rl)
        retList.append(t)
        #print(t)
    #for onecontext in retList:
    #    print(onecontext)
    return retList
    #exit(2)


def writeRowInExcel(sheet,billFileName,writeList):

    py = sheet.max_row + 1
    contextList = []
    contextList = handleOneRecord(writeList)
    for onecontext in contextList:
        onecontext.append(billFileName)
        px = 2
        for value in onecontext:
            sheet.cell(row=py, column=px, value=value)
            px+=1
        py+=1
        #print(onecontext)

    '''
    for row in contextList:
        sheet.cell(row=py, column=px, value=text)
        px+= 1
    '''



#G:\LOG\log_20180207\CG29_20180207.txt
def gen_CHG(filepath):
    #filepath = input("输入话单log文件")
    #filepath = "G:\LOG\log_20180126\CG29_20180126_0.txt"
    #filepath = "G:\LOG\log_20180126\CG48_20180126_0.log"
    #filepath = "G:\LOG\log_20180201\CG29_20180202_02.log"
    #filepath = "G:\LOG\log_20180201\CG29_20180201_01.log"
    chargingDict = {}
    list = []
    file = open(filepath)

    #print(file.read())
    lt = file.readlines()
    l = []
    for linestr in lt:
        #print(linestr)
        l.append(linestr.split('\n')[0])
    lt = []
    #for linestr in l:
     #   print(linestr)
    #print(len(l))
    #exit(1)
    list = getWholeChargingListByfile(l)
    #print(list)
    for bill in list:
        recordlist = []
        f,e = bill
        billfile = getBillFileName(l[f])
        #if billfile == "cg29_pgw2_20180202012627_00061886.dat":
        #print(f,e)
        recordlist = getRecordList(l,f+1,e+1)
        chargingDict[billfile] = recordlist
        #print(billfile)
        #print(recordlist)
    del l
    del lt
    del list
    gc.collect()
    file.close()
    write07Excel("话单验证", chargingDict)