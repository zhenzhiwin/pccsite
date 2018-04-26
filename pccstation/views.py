# coding:utf-8
from django.shortcuts import render, HttpResponse, redirect
import os, ccL7, ccl7_iplist, ccl34, processL347
from pccstation import models
from django.conf import settings


def upload(request):
    if request.method == 'GET':
        return render(request, 'home.html')
    elif request.method == 'POST':
        e_obj = request.FILES.get('excel')
        f = open(e_obj.name, 'wb')
        for line in e_obj.chunks():
            f.write(line)
        f.close()
        l_obj = request.FILES.get('log')
        f = open(l_obj.name, 'wb')
        for line in l_obj.chunks():
            f.write(line)
        f.close()
        processL347.gen_origin_api(e_obj.name, l_obj.name)
        HttpResponse.charset = 'utf-8'
        # return HttpResponse(url_times,'上传成功,初级分类文件已生成，请查看目录！')
        #return render(request, 'generation.html', {'l34': l34_list}, {'l7': l7_list}, {'del': del_list}, {'add': add_list})
        return render(request, 'generation.html')

def get_log(request):
    log_file = open('processL347.log', 'r')
    pro_list = log_file.readlines()
    log_file.close()

    log_file = open('L34.log', 'r')
    l34_list = log_file.readlines()
    log_file.close()

    log_file = open('L7.log', 'r')
    l7_list = log_file.readlines()
    log_file.close()

    log_file = open('ip_prefix_list_add.log', 'r')
    ipradd_list = log_file.readlines()
    log_file.close()

    log_file = open('ip_prefix_list_del.log', 'r')
    iprdel_list = log_file.readlines()
    log_file.close()
    return render(request,'createlog.html',{'pro':pro_list,'l34':l34_list,'l7':l7_list,'ipadd':ipradd_list,'ipdel':iprdel_list})

def index(request):
    # return HttpResponse("欢迎使用PCC智能工具")
    return render(request, 'home.html')


