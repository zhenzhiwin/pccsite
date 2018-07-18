# coding=utf-8
# author zhi.zhen

def PRU_assert(configlist):
    log_List_no_match = []
    # log_List_only_protocol=[]
    for i in range(0, len(configlist)):
        if configlist[i].find("flow-description ") != -1 and configlist[i + 1].find("exit") != -1:
            for j in range(i, -1, -1):
                if configlist[j].find('policy-rule-unit "') != -1:
                    log_List_no_match.append(configlist[j].strip() + '中的' + configlist[i] + '未进行match配置')
                    break
        # if configlist[i+2].find("protocol")!=-1:
        #     if configlist[i+3].find("exit"):
        #         for j in range(len(configlist[0:i])-1,-1,-1):
        #             if configlist[j].find('policy-rule-unit "PRU_')!=-1:
        #                 log_List_only_protocol.append(configlist[j])
        #                 break

    return log_List_no_match


def PRB_asser(configlist):
    pr_list = []
    pr_in_prb = []
    pr_log = []
    pr_dif = []
    pr_in_prb_dif = []
    for line in configlist:
        if line.find('policy-rule "') != -1 and line.find('qci * arp * precedence') != -1:
            start = line.find('"')
            end = line.find('"', start + 1)
            pr_list.append(line[start:end])
        if line.find('policy-rule "') != -1 and line.find('qci * arp * precedence') == -1:
            start = line.find('"')
            end = line.find('"', start + 1)
            pr_in_prb.append(line[start:end])
    dif = set(pr_in_prb).symmetric_difference(set(pr_list))
    if len(dif) == 0:
        pr_log.append("本次检查PR均关联至PRB中,共 " + str(len(pr_list)) + "个PR\n")
    for i in dif:
        if i in pr_in_prb:
            pr_in_prb_dif.append(i)
        if i in pr_list:
            pr_dif.append(i)
    if len(pr_dif) > 0:
        pr_log.append("未在PRB下关联的PR有" + str(pr_dif) + '\n')
    if len(pr_in_prb_dif) > 0:
        pr_log.append('在PRB下关联却未进行创建的PR有' + str(pr_in_prb_dif) + '\n')
    return pr_log


def CRU_assert(configlist):
    log_list = []
    str = ''
    for i in range(0, len(configlist)):
        if configlist[i].find('charging-rule-unit "') != -1 and configlist[i].find('qci * arp * precedence') == -1:
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

    for line_num in range(0,len(configlist)):
        if configlist[line_num].find('echo "Application-assurance Configuration"')!=-1:
            configlist=configlist[line_num:]
            break

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
                    if str.find('expression ') == -1 and str.find('server-address eq ') == -1 and str.find(
                            'protocol eq "'):
                        tmp = configlist[i].strip()
                        log_list.append(tmp.replace("create", "缺少expression or server address or protocol配置"))
                    str = ''
                    break
    return log_list


def APP_assert(configlist):
    log_list = []
    str = ''
    tmp = ''
    for i in range(0, len(configlist)):
        if configlist[i].find('application "') != -1 and configlist[i].find('create') != -1:
            for j in range(i, len(configlist[i:])):
                if configlist[j].find('exit') != -1:
                    for k in configlist[i:j]:
                        str = str + k
                    if str.find('app-group "') == -1:
                        tmp = configlist[i].strip()
                        log_list.append(tmp.replace("create", "未关联APP_GROUP"))
                    if str.find('charging-group "') == -1:
                        tmp = configlist[i].strip()
                        log_list.append(tmp.replace("create", "未关联CHG"))
                    str = ''
                    break

    return log_list


def app_chg_assertion(configlist):
    chg_list = []
    app_list = []
    chg_in_pru = []
    chg_in_app = []
    app_in_entry = []
    chg_log_list = []
    app_log_list = []
    in_chglist = []
    in_chglist_tmp = []
    in_chgprulist = []
    in_chgapplist = []
    in_appentrylist = []
    in_applist = []
    for line_num in range(0,len(configlist)):
        if configlist[line_num].find('echo "Application-assurance Configuration"')!=-1:
            configlist=configlist[line_num:]
            break


    for chg in configlist:
        if chg.find('charging-group "') != -1 and chg.find(' create') != -1:
            start = chg.find('"')
            end = chg.find('"', start + 1)
            chg_list.append(chg[start:end])

    for line in configlist:
        if line.find('application "') != -1 and line.find(' create') != -1:
            start = line.find('"')
            end = line.find('"', start + 1)
            app_list.append(line[start:end])

    for line in configlist:
        if line.find('aa-charging-group "') != -1:
            start = line.find('"')
            end = line.find('"', start + 1)
            chg_in_pru.append(line[start:end])

    for line in configlist:
        if line.find('aa-charging-group "') == -1 and line.find('charging-group "') != -1 and line.find(
                ' create') == -1:
            start = line.find('"')
            end = line.find('"', start + 1)
            chg_in_app.append(line[start:end])

    for line in configlist:
        if line.find('application "') != -1 and line.find(' create') == -1:
            start = line.find('"')
            end = line.find('"', start + 1)
            app_in_entry.append(line[start:end])
    # print(len(chg_list))
    chg_dif = set(chg_in_pru).symmetric_difference(set(chg_list))
    chg_dif_app = set(chg_in_app).symmetric_difference(set(chg_list))
    app_dif = set(app_list).symmetric_difference(set(app_in_entry))
    if len(chg_dif) == 0:
        chg_log_list.append("本次检查PRU关联的CHG数量与CREATE数量一致,共 " + str(len(chg_list)) + " 个\n")
    if len(chg_dif_app) == 0:
        chg_log_list.append("本次检查PRU关联的CHG数量与CREATE数量一致,共 " + str(len(chg_list)) + " 个\n")
    # else:
    #     chg_log_list.append("本次检查PRU下关联的CHG有 " + str(len(chg_in_pru)) + "个,CREATE的CHG有 " + str(len(chg_list)) + " 个\n")
    for i in chg_dif:
        if i in chg_list:
            in_chglist.append(i)
        if i in chg_in_pru:
            in_chgprulist.append(i)
    # chg_log_list.append("本次检查PRU下关联的CHG有 " + str(len(chg_in_pru)) + "个,CREATE的CHG有 " + str(len(chg_list)) + " 个\n")
    if len(in_chgprulist) > 0:
        chg_log_list.append("本次检查PRU下关联的CHG有 " + str(len(chg_in_pru)) + "个,CREATE的CHG有 " + str(
            len(chg_list)) + " 个,\nPRU下关联却未进行CREATE的有:" + str(in_chgprulist) + "\n")
    if len(in_chglist) > 0:
        chg_log_list.append("本次检查PRU下关联的CHG有 " + str(len(chg_in_pru)) + "个,CREATE的CHG有 " + str(
            len(chg_list)) + " 个,\nCREATE却未在PRU下关联的有:" + str(in_chglist) + "\n")
    for i in chg_dif_app:
        if i in chg_list:
            in_chglist_tmp.append(i)
        if i in chg_in_app:
            in_chgapplist.append(i)
    if len(in_chgapplist) > 0:
        chg_log_list.append("本次检查APP下关联的CHG有 " + str(len(chg_in_app)) + "个,CREATE的CHG有 " + str(
            len(chg_list)) + " 个,\nAPP下关联却未进行CREATE的有:" + str(in_chgapplist) + "\n")
    if len(in_chglist_tmp) > 0:
        chg_log_list.append("本次检查APP下关联的CHG有 " + str(len(chg_in_app)) + "个,CREATE的CHG有 " + str(
            len(chg_list)) + " 个,\nCREATE却未在APP下关联的有:" + str(in_chglist_tmp) + "\n")
    if len(app_dif) == 0:
        app_log_list.append("本次检查所有entry关联的APP与CREATE APP数量一致,共 " + str(len(app_list)) + " 个\n")
    for i in app_dif:
        if i in app_list:
            in_applist.append(i)
        if i in app_in_entry:
            in_appentrylist.append(i)
    if len(in_appentrylist) > 0:
        app_log_list.append("本次检查ENTRY下关联的APP有 " + str(len(app_in_entry)) + "个,CREATE的APP有 " + str(
            len(app_list)) + " 个,\nENTRY下关联却未进行CREATE的有:" + str(in_appentrylist) + "\n")
    if len(in_applist) > 0:
        app_log_list.append("本次检查ENTRY下关联的APP有 " + str(len(app_in_entry)) + "个,CREATE的APP有 " + str(
            len(app_list)) + " 个,\nCREATE却未在ENTRY下关联的有:" + str(in_applist) + "\n")
    return chg_log_list, app_log_list


def enrichment_assertion(configlist):
    er_applist = []
    er_aqplist = []
    s = 0
    e = 0
    er_list = []
    tmp = []
    entry = []
    out_list = []
    for i in range(0, len(configlist)):
        # if configlist[i].find('application "') != -1 and configlist[i].find('_HeaderEnrich" create') != -1:
        #     start = configlist[i].find('"')
        #     end = configlist[i].find('"', start + 1)
        #     er_applist.append(configlist[i][start:end + 1])
        if configlist[i].find('app-qos-policy') != -1:
            s = i
        if configlist[i].find('echo "Mobile Gateway Configuration"') != -1:
            e = i
            er_list = configlist[s:e]
            break
    # for er in er_list:
    #     if er.find('application eq "') != -1:
    #         start = er.find('"')
    #         end = er.find('"', start + 1)
    #         er_aqplist.append(er[start:end + 1])

    for i in range(0, len(er_list)):
        if er_list[i].find('entry') != -1:
            for entry_next in er_list[i + 1:]:
                if entry_next.find('entry') == -1:
                    tmp.append(entry_next)
                else:
                    tmp.append(er_list[i])
                    entry.append(tmp)
                    tmp = []
                    break

    entry.append(tmp)

    for e in entry:
        m_flag = False
        a_flag = False
        s_flag = False
        for i in e:
            if i.find('match') != -1:
                m_flag = True
            if i.find('action') != -1:
                a_flag = True
            if i.find('no shutdown') != -1:
                s_flag = True
        if m_flag == False:
            out_list.append(e[-1].strip().replace(' create', '') + '未进行match配置\n')
        if a_flag == False:
            out_list.append(e[-1].strip().replace(' create', '') + '未进行action配置\n')
        if s_flag == False:
            out_list.append(e[-1].strip().replace(' create', '') + '未进行no shutdown\n')

    # for app in er_applist:
    #     if app not in er_aqplist:
    #         out_list.append(app + '未在app qos policy中创建对应entry\n')

    return out_list


def gen_assertion_api(config_file):
    configlist = []
    try:
        with open(config_file) as file:
            for line in file:
                if len(line.strip()) != 0:
                    configlist.append(line.strip('\n'))
    except:
        with open(config_file, encoding='UTF-8') as file:
            for line in file:
                if len(line.strip()) != 0:
                    configlist.append(line.strip('\n'))
    PRU_list = PRU_assert(configlist)
    CRU_list = CRU_assert(configlist)
    entry_list = entry_assert(configlist)
    APP_list = APP_assert(configlist)
    return_list = app_chg_assertion(configlist)
    PR_list = PRB_asser(configlist)
    ER_list = enrichment_assertion(configlist)

    # print(APP_list)
    return PRU_list, CRU_list, entry_list, APP_list, return_list[0], return_list[1], PR_list, ER_list
