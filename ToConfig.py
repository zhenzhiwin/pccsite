# coding=utf-8
# author zhi.zhen
import os
import time

import xlwt

import processL347


def gen_api(config_file):
    config = []
    path = os.path.abspath('.')
    flag = True
    try:
        with open(config_file) as file:
            for line in file:
                if len(line.strip()) != 0:
                    config.append(line.strip('\n'))
    except:
        with open(config_file, encoding='UTF-8') as file:
            for line in file:
                if len(line.strip()) != 0:
                    config.append(line.strip('\n'))

    l_time = time.strftime('%Y%m%d_%H%M%S', time.localtime(time.time()))
    for ne_name in config:
        if ne_name.find('name "') != -1 and ne_name.find('BNK"') != -1:
            start = ne_name.find('"')
            end = ne_name.find('"', start + 1)
            ne_name = ne_name[start + 1:end]
            path = path + '\\' + 'Generated\\' + ne_name + '\\' + l_time
            processL347.mkdir(path)
            path = path + '\\' + ne_name + '_config.xls'
            flag = False
            break
    if flag:
        path = path + '\\' + 'Generated\\' + 'unknownNE' + '\\' + l_time
        processL347.mkdir(path)
        path = path + '\\' + 'unknownNE_config.xls'

    EX_gen(config, path)


def _gen_style():
    styleblue = xlwt.easyxf('pattern: pattern solid, fore_colour ice_blue;')
    stylegrey = xlwt.easyxf('pattern: pattern solid, fore_colour silver_ega;')
    styleindigo = xlwt.easyxf('pattern: pattern solid, fore_colour ivory;')
    styleorange = xlwt.easyxf('pattern:pattern solid, fore_colour orange;align:horiz center,')
    styleyellow = xlwt.easyxf('pattern:pattern solid, fore_colour yellow;align:horiz center,')
    borders = xlwt.Borders()
    borders.left = 1
    borders.right = 1
    borders.top = 1
    borders.bottom = 1
    styleblue.borders = borders
    stylegrey.borders = borders
    styleindigo.borders = borders
    styleorange.borders = borders
    styleyellow.borders = borders
    return styleblue, stylegrey, styleindigo, styleorange, styleyellow


def EX_gen(config, path):
    prb_list = []
    pr_list = []
    non_pdn_cfg = []
    prb_dic = {}
    for c in range(0, len(config)):
        if config[c].find('pdn 1') != -1:
            non_pdn_cfg = config[:c]

    for j in range(0, len(non_pdn_cfg)):
        if non_pdn_cfg[j].find('policy-rule-base "') != -1:
            start = non_pdn_cfg[j].find('"')
            end = non_pdn_cfg[j].find('"', start + 1)
            prb = non_pdn_cfg[j][start + 1:end]
            prb_list.append(prb)
            for pr in non_pdn_cfg[j:]:
                if pr.find('policy-rule "') != -1:
                    start = pr.find('"')
                    end = pr.find('"', start + 1)
                    pr_list.append(pr[start + 1:end])
                if pr.find('exit') != -1:
                    prb_dic[prb] = pr_list
                    pr_list = []
                    break

    w = xlwt.Workbook()
    styleblue = _gen_style()[0]
    stylegrey = _gen_style()[1]
    styleindigo = _gen_style()[2]
    styleorange = _gen_style()[3]
    styleyellow = _gen_style()[4]
    ws = w.add_sheet('PRB')
    for i in range(0, len(prb_list)):
        ws.col(i).width = 256 * 20
        ws.write(0, i, prb_list[i], styleblue)
        for j in range(0, len(prb_dic[prb_list[i]])):
            ws.write(j + 1, i, prb_dic[prb_list[i]][j], styleindigo)

    wpr = w.add_sheet('PR')
    wpr.col(0).width = 256 * 20
    wpr.col(1).width = 256 * 20
    wpr.col(2).width = 256 * 20
    wpr.col(3).width = 256 * 20
    wpr.write(0, 0, 'PR NAME', styleorange)
    wpr.write(0, 1, 'PRU NAME', styleyellow)
    wpr.write(0, 2, 'CRU NAME', styleorange)
    wpr.write(0, 3, 'PRECEDENCE', styleyellow)
    pr_col = 1
    for pr in non_pdn_cfg:
        if pr.find('policy-rule "') != -1 and pr.find('precedence') != -1:
            start = pr.find('"')
            end = pr.find('"', start + 1)
            wpr.write(pr_col, 0, pr[start + 1:end], styleindigo)
            start = pr.find('"', end + 1)
            end = pr.find('"', start + 1)
            wpr.write(pr_col, 1, pr[start + 1: end], styleblue)
            start = pr.find('"', end + 1)
            end = pr.find('"', start + 1)
            wpr.write(pr_col, 2, pr[start + 1: end], styleindigo)
            start = pr.find('precedence')
            wpr.write(pr_col, 3, pr[start + 10:], styleblue)
            pr_col += 1

    pru_list = []
    flow_list = []
    pru_dic = {}
    for p in range(0, len(non_pdn_cfg)):
        if non_pdn_cfg[p].find('policy-rule-unit "') != -1 and non_pdn_cfg[p].find('precedence') == -1:
            start = non_pdn_cfg[p].find('"')
            end = non_pdn_cfg[p].find('"', start + 1)
            pru = non_pdn_cfg[p][start + 1:end]
            pru_list.append(pru)
            for f in range(p+1, len(non_pdn_cfg)):
                if non_pdn_cfg[f].find('policy-rule-unit "') != -1:
                    break
                if non_pdn_cfg[f].find('match') != -1:
                    for flow in non_pdn_cfg[f + 1:]:
                        if flow.find('exit') != -1:
                            break
                        else:
                            flow_list.append(flow)
            pru_dic[pru] = flow_list
            flow_list = []

    wpru = w.add_sheet('PRU')
    for p in range(0, len(pru_list)):
        wpru.col(p).width = 350 * 20
        wpru.write(0, p, pru_list[p], styleorange)
        for j in range(0, len(pru_dic[pru_list[p]])):
            wpru.write(j + 1, p, pru_dic[pru_list[p]][j].strip(), styleblue)

    cru_list = []
    flow_list = []
    cru_dic = {}
    for p in range(0, len(non_pdn_cfg)):
        if non_pdn_cfg[p].find('charging-rule-unit "') != -1 and non_pdn_cfg[p].find('precedence') == -1:
            start = non_pdn_cfg[p].find('"')
            end = non_pdn_cfg[p].find('"', start + 1)
            cru = non_pdn_cfg[p][start + 1:end]
            cru_list.append(cru)
            for flow in non_pdn_cfg[p + 1:]:
                if flow.find('exit') != -1:
                    break
                else:
                    flow_list.append(flow)
            cru_dic[cru] = flow_list
            flow_list = []

    wcru = w.add_sheet('CRU')
    wcru.col(0).width = 200 * 20
    wcru.write(0, 0, 'CRU NAME', styleyellow)
    wcru.col(1).width = 300 * 20
    wcru.write(0, 1, 'RATING GROUP', styleyellow)
    wcru.col(2).width = 350 * 20
    wcru.write(0, 2, 'SERVICE ID', styleyellow)
    wcru.col(3).width = 350 * 20
    wcru.write(0, 3, 'OTHERS', styleyellow)
    wcru.col(4).width = 350 * 20
    wcru.write(0, 4, 'OTHERS', styleyellow)
    for p in range(0, len(cru_list)):
        wcru.write(p + 1, 0, cru_list[p], styleindigo)
        for j in range(0, len(cru_dic[cru_list[p]])):
            wcru.write(p + 1, j + 1, cru_dic[cru_list[p]][j].strip(), styleindigo)

    for c in range(0, len(config)):
        if config[c].find('app-qos-policy') != -1:
            non_pdn_cfg1 = config[:c]

    entry_list = []
    flow_list = []
    entry_dic = {}
    for p in range(0, len(non_pdn_cfg1)):
        if non_pdn_cfg1[p].find('entry ') != -1 and non_pdn_cfg1[p].find(' create') != -1:
            start = non_pdn_cfg1[p].find('entry ')
            end = non_pdn_cfg1[p].find(' create')
            entry = non_pdn_cfg1[p][start:end]
            entry_list.append(entry)
            for flow in non_pdn_cfg1[p + 1:]:
                if flow.find('exit') != -1:
                    break
                else:
                    flow_list.append(flow)
            entry_dic[entry] = flow_list
            flow_list = []

    wer = w.add_sheet('ENTRY')
    wer.col(0).width = 200 * 20
    wer.col(1).width = 512 * 20
    wer.col(2).width = 512 * 20
    wer.col(3).width = 512 * 20
    wer.col(4).width = 512 * 20
    wer.col(5).width = 400 * 20
    wer.write(0, 0, 'ENTRY', styleyellow)
    wer.write(0, 1, 'AGRS1', styleyellow)
    wer.write(0, 2, 'AGRS2', styleyellow)
    wer.write(0, 3, 'AGRS3', styleyellow)
    wer.write(0, 4, 'AGRS4', styleyellow)
    wer.write(0, 5, 'AGRS5', styleyellow)

    for p in range(0, len(entry_list)):
        wer.write(p + 1, 0, entry_list[p], styleindigo)
        for j in range(0, len(entry_dic[entry_list[p]])):
            wer.write(p + 1, j + 1, entry_dic[entry_list[p]][j].strip(), styleindigo)

    app_list = []
    flow_list = []
    app_dic = {}
    for p in range(0, len(non_pdn_cfg)):
        if non_pdn_cfg[p].find('application "') != -1 and non_pdn_cfg[p].find('" create') != -1:
            start = non_pdn_cfg[p].find('"')
            end = non_pdn_cfg[p].find('"', start + 1)
            app = non_pdn_cfg[p][start + 1:end]
            app_list.append(app)
            for flow in non_pdn_cfg[p + 1:]:
                if flow.find('exit') != -1:
                    break
                else:
                    flow_list.append(flow)
            app_dic[app] = flow_list
            flow_list = []

    wa = w.add_sheet('APP')
    wa.col(0).width = 200 * 20
    wa.write(0, 0, 'APP NAME', styleorange)
    wa.col(1).width = 300 * 20
    wa.write(0, 1, 'ARGS1', styleorange)
    wa.col(2).width = 350 * 20
    wa.write(0, 2, 'ARGS2', styleorange)

    for p in range(0, len(app_list)):
        wa.write(p + 1, 0, app_list[p], styleindigo)
        for j in range(0, len(app_dic[app_list[p]])):
            wa.write(p + 1, j + 1, app_dic[app_list[p]][j].strip(), styleindigo)

    chg_list = []
    flow_list = []
    chg_dic = {}
    for p in range(0, len(non_pdn_cfg)):
        if non_pdn_cfg[p].find('charging-group "') != -1 and non_pdn_cfg[p].find('" create') != -1:
            start = non_pdn_cfg[p].find('"')
            end = non_pdn_cfg[p].find('"', start + 1)
            chg = non_pdn_cfg[p][start + 1:end]
            chg_list.append(chg)
            for flow in non_pdn_cfg[p + 1:]:
                if flow.find('exit') != -1:
                    break
                else:
                    flow_list.append(flow)
            chg_dic[chg] = flow_list
            flow_list = []

    wcg = w.add_sheet('CHG')
    wcg.col(0).width = 200 * 20
    wcg.write(0, 0, 'CHG NAME', styleorange)
    wcg.col(1).width = 300 * 20
    wcg.write(0, 1, 'ARGS', styleorange)

    for p in range(0, len(chg_list)):
        wcg.write(p + 1, 0, chg_list[p], styleindigo)
        for j in range(0, len(chg_dic[chg_list[p]])):
            wcg.write(p + 1, j + 1, chg_dic[chg_list[p]][j].strip(), styleindigo)

    ipl_list = []
    flow_list = []
    ipl_dic = {}
    for p in range(0, len(non_pdn_cfg)):
        if non_pdn_cfg[p].find('ip-prefix-list "') != -1 and non_pdn_cfg[p].find('" create') != -1:
            start = non_pdn_cfg[p].find('"')
            end = non_pdn_cfg[p].find('"', start + 1)
            ipl = non_pdn_cfg[p][start + 1:end]
            ipl_list.append(ipl)
            for flow in non_pdn_cfg[p + 1:]:
                if flow.find('exit') != -1:
                    break
                else:
                    flow_list.append(flow)
            ipl_dic[ipl] = flow_list
            flow_list = []

    wip = w.add_sheet('IP PREFIX LIST')

    for p in range(0, len(ipl_list)):
        wip.col(p).width = 256 * 20
        wip.write(0, p, ipl_list[p], styleorange)
        for j in range(0, len(ipl_dic[ipl_list[p]])):
            wip.write(j + 1, p, ipl_dic[ipl_list[p]][j].strip(), styleindigo)

    ptl_list = []
    flow_list = []
    ptl_dic = {}
    for p in range(0, len(non_pdn_cfg)):
        if non_pdn_cfg[p].find('port-list "') != -1 and non_pdn_cfg[p].find('" create') != -1:
            start = non_pdn_cfg[p].find('"')
            end = non_pdn_cfg[p].find('"', start + 1)
            ptl = non_pdn_cfg[p][start + 1:end]
            ptl_list.append(ptl)
            for flow in non_pdn_cfg[p + 1:]:
                if flow.find('exit') != -1:
                    break
                else:
                    flow_list.append(flow)
            ptl_dic[ptl] = flow_list
            flow_list = []

    wpt = w.add_sheet('PORT LIST')

    for p in range(0, len(ptl_list)):
        wpt.col(p).width = 256 * 20
        wpt.write(0, p, ptl_list[p], styleorange)
        for j in range(0, len(ptl_dic[ptl_list[p]])):
            wpt.write(j + 1, p, ptl_dic[ptl_list[p]][j].strip(), styleindigo)

    for c in range(0, len(config)):
        if config[c].find('app-qos-policy') != -1:
            non_pdn_cfg2 = config[c:]

    aqp_e_list = []
    ma_list = []
    aqp_dic = {}
    aqp = ''
    for p in range(0, len(non_pdn_cfg2)):
        if non_pdn_cfg2[p].find('entry ') != -1 and non_pdn_cfg2[p].find(' create') != -1:
            start = non_pdn_cfg2[p].find('entry ')
            end = non_pdn_cfg2[p].find(' create')
            aqp = non_pdn_cfg2[p][start:end]
            aqp_e_list.append(aqp)
            for f in range(p + 1, len(non_pdn_cfg2[p + 1:])):
                if (non_pdn_cfg2[f].find('entry ') != -1 and non_pdn_cfg2[f].find(' create') != -1) or non_pdn_cfg2[
                    f].find('echo "Mobile Gateway Configuration"') != -1:
                    # ma_list.append(mt_list)
                    # ma_list.append(ac_list)
                    aqp_dic[aqp] = ma_list
                    ma_list = []
                    # ac_list=[]
                    # mt_list=[]
                    break
                if non_pdn_cfg2[f].find('match') != -1:
                    for m in non_pdn_cfg2[f + 1:]:
                        if m.find('exit') != -1:
                            break
                        ma_list.append(m)
                if non_pdn_cfg2[f].find('action') != -1:
                    for a in non_pdn_cfg2[f + 1:]:
                        if a.find('exit') != -1:
                            break
                        ma_list.append(a)

    waqp = w.add_sheet('App Qos Policy')
    waqp.col(0).width = 200 * 20
    waqp.col(1).width = 512 * 20
    waqp.col(2).width = 512 * 20
    waqp.col(3).width = 512 * 20
    waqp.col(4).width = 512 * 20
    waqp.write(0, 0, 'ENTRY', styleyellow)
    waqp.write(0, 1, 'AGRS1', styleyellow)
    waqp.write(0, 2, 'AGRS2', styleyellow)
    waqp.write(0, 3, 'AGRS3', styleyellow)
    waqp.write(0, 4, 'AGRS4', styleyellow)
    for p in range(0, len(aqp_e_list)):
        waqp.write(p + 1, 0, aqp_e_list[p], styleindigo)
        for j in range(0, len(aqp_dic[aqp_e_list[p]])):
            waqp.write(p + 1, j + 1, aqp_dic[aqp_e_list[p]][j].strip(), styleindigo)

    w.save(path)
