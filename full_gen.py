# coding=utf-8
"""
@Author:zhi.zhen
email:zhi.zhen@nokia.com
"""


def gen_begining(configlist, path):
    cmdlist = []
    flag = True
    for line in configlist:
        if line.find("primary 10/2") != -1:
            flag = False
            break
    if flag:
        cmdlist.append("configure isa application-assurance-group 1 aa-sub-scale mobile-gateway create\n")
        cmdlist.append("primary 1/2\n")
        cmdlist.append("primary 2/2\n")
        cmdlist.append("primary 3/2\n")
        cmdlist.append("primary 4/2\n")
        cmdlist.append("primary 5/2\n")
        cmdlist.append("primary 6/2\n")
        cmdlist.append("primary 7/2\n")
        cmdlist.append("primary 8/2\n")
        cmdlist.append("primary 9/2\n")
        cmdlist.append("primary 10/2\n")
        cmdlist.append("shared-resources\n")
        cmdlist.append("tcp-adv-func 0\n")
        cmdlist.append("exit\n")
        cmdlist.append("partitions\n")
        cmdlist.append("statistics\n")
        cmdlist.append("performance\n")
        cmdlist.append("collect-stats\n")
        cmdlist.append("exit\n")
        cmdlist.append("exit\n")
        cmdlist.append("no shutdown\n")
        cmdlist.append("exit all\n")

        cmdlist.append("/configure application-assurance group 1:1 policy begin\n")
        cmdlist.append(
            '/configure application-assurance group 1:1 policy app-profile "default-app-profile" create description "Global App-profile"\n')
        cmdlist.append('/configure application-assurance group 1:1 policy app-profile "default-app-profile" divert\n')
        cmdlist.append('/configure application-assurance group 1:1 policy commit\n')
        cmdlist.append('exit all\n')

        file = open(path + "\\AA Partitions.txt", "w")
        file.writelines(cmdlist)
        file.close()
