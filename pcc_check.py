# coding=utf-8


def PRU_assert(configlist):
    log_List_no_match = []
    # log_List_only_protocol=[]
    for i in range(0, len(configlist)):
        if configlist[i].find("flow-description ") != -1 and configlist[i + 1].find("exit") != -1:
            for j in range(i, -1, -1):
                if configlist[j].find('policy-rule-unit "PRU_') != -1:
                    log_List_no_match.append(configlist[j].strip() + ' 未进行match配置')
                    break
        # if configlist[i+2].find("protocol")!=-1:
        #     if configlist[i+3].find("exit"):
        #         for j in range(len(configlist[0:i])-1,-1,-1):
        #             if configlist[j].find('policy-rule-unit "PRU_')!=-1:
        #                 log_List_only_protocol.append(configlist[j])
        #                 break

    return log_List_no_match


def CRU_assert(configlist):
    log_list = []
    str = ''
    for i in range(0, len(configlist)):
        if configlist[i].find('charging-rule-unit "CRU_') != -1 and configlist[i].find('qci * arp * precedence') == -1:
            for j in range(i, len(configlist)):
                if configlist[j].find("exit") != -1:
                    for k in configlist[i:j]:
                        str = str + k
                    if str.find('rating-group') == -1:
                        log_list.append(configlist[i].strip() + '未配置rating group')
                    if str.find('service-identifier') == -1:
                        log_list.append(configlist[i].strip() + '未配置service identifier')
                    if str.find('reporting-level service-id') == -1:
                        log_list.append(configlist[i].strip() + '未配置reporting-level')
                    str = ''
                    break

    return log_list


def entry_assert(configlist):
    log_list = []
    str = ''
    tmp = ''
    for i in range(0, len(configlist)):
        if configlist[i].find("app-qos-policy") != -1:
            break
        if configlist[i].find("entry ") != -1 and configlist[i].find(" create") != -1:
            for j in range(i, len(configlist)):
                if configlist[j].find("exit") != -1:
                    for k in configlist[i:j]:
                        str = str + k
                    if str.find("no shutdown") == -1:
                        tmp = configlist[i].strip()
                        log_list.append(tmp.replace("create", "没有no shut down"))
                    if str.find('application "') == -1:
                        tmp = configlist[i].strip()
                        log_list.append(tmp.replace("create", "未关联APP"))
                    if str.find('expression ') == -1 and str.find('server-address eq ') == -1:
                        tmp = configlist[i].strip()
                        log_list.append(tmp.replace("create", "缺少expression或server address配置"))
                    str = ''
                    break
    return log_list


def APP_assert(configlist):
    log_list = []
    str = ''
    tmp = ''
    for i in range(0, len(configlist)):
        if configlist[i].find('application "APP_') != -1 and configlist[i].find('create') != -1:
            for j in range(i, len(configlist[i:])):
                if configlist[j].find('exit') != -1:
                    for k in configlist[i:j]:
                        str = str + k
                    if str.find('app-group "') == -1:
                        tmp = configlist[i].strip()
                        log_list.append(tmp.replace("create", "未关联APP_GROUP"))
                    if str.find('charging-group "CHG_') == -1:
                        tmp = configlist[i].strip()
                        log_list.append(tmp.replace("create", "未关联CHG"))
                    str = ''
                    break

    return log_list


def gen_assertion_api(config_file):
    configlist = []
    with open(str(config_file)) as file:
        for line in file:
            if len(line.strip()) != 0:
                configlist.append(line.strip('\n'))
    PRU_list = PRU_assert(configlist)
    CRU_list = CRU_assert(configlist)
    entry_list = entry_assert(configlist)
    APP_list = APP_assert(configlist)

    # print(APP_list)
    return PRU_list, CRU_list, entry_list, APP_list
