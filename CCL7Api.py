

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

def getTheServiceEntryIdList(ServiceEntryList):
    retList = []
    for lst in ServiceEntryList:
        for text in lst:
            if "entry" in text:
                retList.append(int(text.split("entry ")[1].split(" create")[0]))
    if retList:
        retList.sort()
    return retList

def getTheCHGlist(cfg_list,service_name):
    retList = []
    for i in range(0,len(cfg_list)):
        if "charging-group" in cfg_list[i] and service_name in cfg_list[i] and "create" in cfg_list[i]:
            k = i
            for j in range(k,len(cfg_list)):
                retList.append(cfg_list[j].replace(" ",""))
                if "exit" in cfg_list[j]:
                    return retList
    return retList

def getTheAPPlist(cfg_list,service_name):
    retList = []
    for i in range(0,len(cfg_list)):
        if 'application "' in cfg_list[i] and service_name in cfg_list[i] and "create" in cfg_list[i]:
            k = i
            for j in range(k,len(cfg_list)):
                retList.append(cfg_list[j].replace(" ",""))
                if "exit" in cfg_list[j]:
                    return retList
    return retList


def getTheL7UserIpListFromServiceBlock(block_list):
        retList = []
        retDelList = []
        for tup in block_list:
            if tup[1] == "新增":
                layer,change,service_id,service_name,ip,protocol,port,url = tup
                if ip !=None:
                    if "/" not in ip:
                        ip = ip + "/32"
                        tup = layer,change,service_id,service_name,ip,protocol,port,url
                retList.append(tup)
            if tup[1] == "删除":
                layer, change, service_id, service_name, ip, protocol, port, url = tup
                if ip !=None:
                    if "/" not in ip:
                        ip = ip + "/32"
                        tup = layer,change,service_id,service_name,ip,protocol,port,url
                retDelList.append(tup)

        return retList, retDelList

def getTheL7PRUNameList(temp_dict):
    retList = []
    for key in temp_dict:
        if "L7" not in key:
            retList.append(key)
    retList.sort()
    return retList

def PR_L7_in_PRDict(pr_dict):
    if len(pr_dict) == 0:
        return False
    for pr_name in pr_dict:
        if "L7" in pr_name:
            return True
    return False

def PRU_L7_in_PRUDict(pru_dict):
    if len(pru_dict) == 0:
        return False
    for pru_name in pru_dict:
        if "L7" in pru_name:
            return True
    return False

def addL7UserPRPRUCRUAPPCHG2InformationDict(service_configure_dict,user_add_ip_list,service_name):
    service_id_str = user_add_ip_list[0][2]

    for cru_pru_pr_app_chg_key in service_configure_dict:
        if cru_pru_pr_app_chg_key == "CRU":
            if len(service_configure_dict[cru_pru_pr_app_chg_key])==0:
                service_configure_dict["CRU"].append("new_CRU----" + service_id_str)
        if cru_pru_pr_app_chg_key == "PR":
            if PR_L7_in_PRDict(service_configure_dict["PR"]) == False:
                service_configure_dict["PR"]['new_"PR_'+service_name+"_L7"+'"'] = '"PR_'+service_name+"_L7"+'"'
        if cru_pru_pr_app_chg_key == "PRU":
            if PRU_L7_in_PRUDict(service_configure_dict["PRU"]) == False:
                service_configure_dict["PRU"]['new_"PRU_'+service_name+"_L7"+'"'] = '"PRU_'+service_name+"_L7"+'"'
        if cru_pru_pr_app_chg_key == "CHG":
            if len(service_configure_dict[cru_pru_pr_app_chg_key])==0:
                service_configure_dict["CHG"].append('new_"CHG_'+service_name+'"----' + 'description "'+service_name+'"')
        if cru_pru_pr_app_chg_key == "APP":
            if len(service_configure_dict[cru_pru_pr_app_chg_key])==0:
                service_configure_dict["APP"].append('new_"CHG_'+service_name+'"----' + 'description "'+service_name+'"')


def getTheCompatibleEntryId(tup,all_entry_id_list,service_entry_id_list,strat,end):
    retId = -1
    for i in range(strat,end):
        if i not in all_entry_id_list:
            retId = i
            all_entry_id_list.append(retId)
            service_entry_id_list.append(retId)
            break
    return retId

def getTheOneEntryList(tup,entry_id):
    retList = []
    service_name = tup[3]
    ip = tup[4]
    protocol = tup[5]
    port = tup
    url = tup[7]
    #ip-protocol-num eq tcp

    return retList

def addEentry2InformationDict(all_entry_id_lsit,service_entry_id_list,service_entry_list,add_service_tup_list):
    print("------------------------")
    print("all_entry_id_lsit",all_entry_id_lsit)
    print("service_entry_id_list",service_entry_id_list)
    print("service_entry_list",service_entry_list)
    print("add_service_tup_list",add_service_tup_list)
    for add_tup in add_service_tup_list:
        entry_id = getTheCompatibleEntryId(add_tup,all_entry_id_lsit,service_entry_id_list,20501,60000)
        entry_list = getTheOneEntryList(add_tup,entry_id)


