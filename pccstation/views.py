# coding:utf-8
import os

from django.shortcuts import render, HttpResponse

import pcc_check,ToConfig
import processL347


def upload(request):
    processL347.mkdir("tmp\\")
    if request.method == 'GET':
        return render(request, 'home.html')
    elif request.method == 'POST':
        e_obj = request.FILES.get('excel')
        l_obj = request.FILES.get('log')
        as_obj = request.FILES.get('log_as')
        ex_obj = request.FILES.get('log_ex')
        if e_obj != None and l_obj != None:
            f = open("tmp\\" + e_obj.name, 'wb')
            for line in e_obj.chunks():
                f.write(line)
            f.close()
            f = open("tmp\\" + l_obj.name, 'wb')
            for line in l_obj.chunks():
                f.write(line)
            f.close()
            try:
                processL347.gen_origin_api("tmp\\" + e_obj.name, "tmp\\" + l_obj.name)
            except UnicodeDecodeError:
                e = '解码错误,配置文件中存在有全角字符,请检查!'
                return render(request, 'errorpage.html', {'error': e})
            except Exception as e:
                return render(request, 'errorpage.html', {'error': e})
            HttpResponse.charset = 'utf-8'
            # return HttpResponse(url_times,'上传成功,初级分类文件已生成，请查看目录！')
            # return render(request, 'generation.html', {'l34': l34_list}, {'l7': l7_list}, {'del': del_list}, {'add': add_list})
            return render(request, 'generation.html')
        if as_obj != None:
            f = open("tmp\\" + as_obj.name, 'wb')
            for line in as_obj.chunks():
                f.write(line)
            f.close()
            try:
                # log_list = pcc_check.app_chg_assertion("tmp\\" + as_obj.name)
                return_list = pcc_check.gen_assertion_api("tmp\\" + as_obj.name)
            except UnicodeDecodeError:
                e = '解码错误,配置文件中存在有全角字符,请检查!'
                return render(request, 'errorpage.html', {'error': e})
            except Exception as e:
                return render(request, 'errorpage.html', {'error': e})
            PRU_list = return_list[0]
            CRU_list = return_list[1]
            entry_list = return_list[2]
            APP_list = return_list[3]
            ER_list = return_list[7]
            if len(PRU_list) == 0:
                PRU_list = ['本次检查PRU中均包含关联项']
            if len(CRU_list) == 0:
                CRU_list = ['本次检查CRU中均包含关联项']
            if len(entry_list) == 0:
                entry_list = ['本次检查entry中均包含关联项']
            if len(APP_list) == 0:
                APP_list = ['本次检查Application中均包含关联项']
            if len(ER_list) == 0:
                ER_list = ['本次检查aqp entry中均包含关联项']
            # print(return_list[5])
            return render(request, 'assertion.html', {'PRU': PRU_list, 'CRU': CRU_list, 'entry': entry_list,
                                                      'APP': APP_list, 'log1': return_list[4], 'log2': return_list[5],
                                                      'PR': return_list[6], 'ER': ER_list})

        if ex_obj != None:
            f = open("tmp\\" + ex_obj.name, 'wb')
            for line in ex_obj.chunks():
                f.write(line)
            f.close()
            try:
                ToConfig.gen_api("tmp\\" + ex_obj.name)
            except UnicodeDecodeError:
                e = '解码错误,配置文件中存在有全角字符,请检查!'
                return render(request, 'errorpage.html', {'error': e})
            except Exception as e:
                return render(request, 'errorpage.html', {'error': e})
            return render(request, 'result.html')

def get_log(request):
    if os.path.exists('tmp\\processL347.log'):
        log_file = open('tmp\\processL347.log', 'r')
        pro_list = log_file.readlines()
        log_file.close()
    else:
        pro_list = ["本次无3/4/7层数据变更"]

    if os.path.exists('tmp\\L34.log'):
        log_file = open('tmp\\L34.log', 'r')
        l34_list = log_file.readlines()
        log_file.close()
    else:
        l34_list = ["本次无3/4层数据变更"]

    if os.path.exists('tmp\\L7.log'):
        log_file = open('tmp\\L7.log', 'r')
        l7_list = log_file.readlines()
        log_file.close()
    else:
        l7_list = ["本次无7层数据变更"]

    if os.path.exists('tmp\\ip_prefix_list_add.log'):
        log_file = open('tmp\\ip_prefix_list_add.log', 'r')
        ipradd_list = log_file.readlines()
        log_file.close()
    else:
        ipradd_list = ["本次无ip prefix list 增加"]

    if os.path.exists('tmp\\ip_prefix_list_del.log'):
        log_file = open('tmp\\ip_prefix_list_del.log', 'r')
        iprdel_list = log_file.readlines()
        log_file.close()
    else:
        iprdel_list = ["本次无ip prefix list 删除"]

    if os.path.exists('tmp\\ip_prefix_list_HeaderEnrich.log'):
        log_file = open('tmp\\ip_prefix_list_HeaderEnrich.log', 'r')
        iprHE_list = log_file.readlines()
        log_file.close()
    else:
        iprHE_list = ["本次无ip prefix 头增强变更"]
    return render(request, 'createlog.html',
                  {'pro': pro_list, 'l34': l34_list, 'l7': l7_list, 'ipadd': ipradd_list, 'ipdel': iprdel_list,
                   'iprHE': iprHE_list})


def index(request):
    # return HttpResponse("欢迎使用PCC智能工具")
    return render(request, 'home.html')
