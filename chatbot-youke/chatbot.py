from socketIO_client import SocketIO, BaseNamespace
from datetime import datetime
import threading
import requests
import json
import time
import random
import string

#serverip = 'http://127.0.0.1:5000'
serverip = 'http://nginx-server:5001'
socket = SocketIO('nginx-server',5001)
apiurl =  serverip + '/api/v1/login'
apigetmonitorurl = serverip + '/api/v1/zabbixmonitor'
#apiurl = 'http://139.196.107.14:5000/api/v1/login'
#payload = {"password": "ppy6rQ3iAMKNzpDjpqYdP29g1STvoz6t0", "mobile": "c2YDSc5nIO7u0Bxjy7JHj0VOy"}
payload = {"password": "i8Ts9fJeBa5Q3AU2Ift74g==", "mobile": "cHTqfKpMkfZaD1AuNWxJVVXDx"}
header = {'Content-Type': 'application/json'}

#产生一个随机字符串
def generate_random_str(randomlength=16):
    """
    生成一个指定长度的随机字符串，其中
    string.digits=0123456789
    string.ascii_letters=abcdefghigklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ
    """
    str_list = [random.choice(string.digits + string.ascii_letters) for i in range(randomlength)]
    random_str = ''.join(str_list)
    return random_str


loginrs = requests.post(apiurl, data=json.dumps(payload), headers=header)
print("login...")
print(loginrs.json())
token = loginrs.json()['token']
companyid = loginrs.json()['companyid']

#机器人登录
def botjoinroot(message):
    msgid = generate_random_str(48)
    sendmsg = {'token': token,'role':'chatbot', 'companyid':companyid, 'msg': message, 'msgid':msgid}
    socket.emit('talk', sendmsg)

#发送消息
def sendmsg(message):
    msgid = generate_random_str(48)
    sendmsg = {'token': token, 'companyid':companyid, 'msg': message, 'msgid':msgid}
    socket.emit('talk', sendmsg)


#连接响应
def conn_response(*args):
    print(args[0])


#talk响应
def talk_response(*args):
    print('talk zzzzzzzzzzz')
    print(args[0])

#发送消息类型2
def botsendmsgtype2(username):
    msgid = generate_random_str(48)
    sendmsgtype2 = {'data': {'type': 2,'companyid':companyid,'msgid':msgid, 'token': token, 'rootbean':
            {'msg': '你好，'+ username + ' 需要我帮你做点什么？', 'actions':
                [{'name': '查看主机CPU', 'type': '3'},
                 {'name': '查看主机内存', 'type': '4'},
                 {'name': '查看磁盘状态', 'type': '6'},
                 {'name': '查看网络流量', 'type': '8'},
                 {'name': '重启主机', 'type': '10'}
                 # {'name': '查看磁盘读写', 'type': '12'},
                 ]}}}
    socket.emit('chatbot', sendmsgtype2)
    print('ooooooh yes')


#发送查询主机cpu消息
def botsendmsgtype3(host):
    msgid = generate_random_str(48)
    getinfo = requests.get(apigetmonitorurl + '/' + host + '?token=' + token + '&companyid=' + companyid, headers=header)
    if getinfo.status_code != 200:
        print("你们先过了我这一关！！！！！")
    else:
        print('hhhhhhhhhhh', getinfo.json())
        if 'status' in getinfo.json():
            print('不存在host', host)
            #sendmsgtype3 = {
               # 'data': {'type': 1, 'token': token,'msgid':msgid, 'companyid': companyid, 'rootbean':
                   # {'msg': "Ooops，未找到此主机：" + host + "，请检查输入的hostid/hostname/hostip"}}}
            sendmsgtype3 = {
               'data': {'type': 1, 'token': token,'msgid':msgid, 'companyid': companyid, 'rootbean':
                   {'msg': "没有查询到相关信息、请检查输入信息是否正确。"}}}

        else:
            lastvalue_str = getinfo.json()['cpu'][0]['lastvalue']
            lastvalue_float = float(lastvalue_str)
            lastvalue_float2 = round(lastvalue_float, 2)
            hostip = getinfo.json()['hostip']

            sendmsgtype3 = {
            "data": {
                "type": 3,
                "msgid":msgid,
                "token": token,
                'companyid': companyid,
                "rootbean": {
                "msg": "当前" + host + "(ip:" + hostip + "）CPU运行情况：",
                "actions": [
                    {
                    "title": "CPU",
                    "ratio": lastvalue_float2,
                    }
                ]}}}

        socket.emit('chatbot', sendmsgtype3)

        print('ooooooh yes')


#发送查询主机内存消息
def botsendmsgtype4(host):
    msgid = generate_random_str(48)
    getinfo = requests.get(apigetmonitorurl + '/' + host + '?token=' + token + '&companyid=' + companyid, headers=header)
    print('hhhhhhhhhhh', getinfo.json())
    if 'status' in getinfo.json():
        print('不存在host', host)
        """
        sendmsgtype4 = {
            'data': {'type': 1, 'token': token, 'msgid':msgid,'companyid': companyid, 'rootbean':
                {'msg': "Ooops，未找到此主机：" + host + "，请检查输入的hostid/hostname/hostip"}}}
        """
        sendmsgtype4 = {
               'data': {'type': 1, 'token': token,'msgid':msgid, 'companyid': companyid, 'rootbean':
                   {'msg': "没有查询到相关信息、请检查输入信息是否正确。"}}}
    else:
        total_memory_lastvalue = getinfo.json()['total_memory'][0]['lastvalue']
        available_memory_lastvalue = getinfo.json()['available_memory'][0]['lastvalue']
        used_memory_lastvalue = total_memory_lastvalue - available_memory_lastvalue
        print(total_memory_lastvalue)
        print(available_memory_lastvalue)
        ratiolastvalue_float = used_memory_lastvalue / total_memory_lastvalue * 100
        ratiolastvalue = round(ratiolastvalue_float, 2)
        hostip = getinfo.json()['hostip']

        sendmsgtype4 = {
        "data": {
            "type": 4,
            "token": token,
            "msgid":msgid,
            'companyid': companyid,
            "rootbean": {
            "msg": "当前" + host + "(ip:" + hostip + "）内存运行情况：",
            "actions": [
                {
                "title": "内存",
                "ratio": ratiolastvalue,
                }
            ]}}}

    socket.emit('chatbot', sendmsgtype4)
    print('ooooooh yes')


#发送查询主机网络消息
def botsendmsgtype8(host):
    msgid = generate_random_str(48)
    getinfo = requests.get(apigetmonitorurl + '/' + host + '?token=' + token + '&companyid=' + companyid, headers=header)
    print('hhhhhhhhhhh', getinfo.json())
    if 'status' in getinfo.json():
        print('不存在host', host)
        sendmsgtype8 = {
               'data': {'type': 1, 'token': token,'msgid':msgid, 'companyid': companyid, 'rootbean':
                   {'msg': "没有查询到相关信息、请检查输入信息是否正确。"}}}
    else:
        monitorinfo = getinfo.json()
        hostip = getinfo.json()['hostip']
        innetworkinfo_list = monitorinfo['in_network']
        outnetworkinfo_list = monitorinfo['out_network']
        print(innetworkinfo_list)
        print(outnetworkinfo_list)

        allinnetworkinfo_list = []
        for innetworkinfo in innetworkinfo_list:
            allinnetworkinfo_dict = {}
            drivename_source = innetworkinfo['key_']
            wangkalastvalue = innetworkinfo['lastvalue']
            drivename = drivename_source.strip('net.if.in').strip('[').strip(']')
            allinnetworkinfo_dict['netDrive'] = drivename
            allinnetworkinfo_dict['inNet'] = wangkalastvalue
            allinnetworkinfo_list.append(allinnetworkinfo_dict)

        alloutnetworkinfo_list = []
        for outnetworkinfo in outnetworkinfo_list:
            alloutnetworkinfo_dict = {}
            outdrivename_source = outnetworkinfo['key_']
            outwangkalastvalue = outnetworkinfo['lastvalue']
            outdrivename = outdrivename_source.strip('net.if.out').strip('[').strip(']')
            alloutnetworkinfo_dict['netDrive'] = outdrivename
            alloutnetworkinfo_dict['outNet'] = outwangkalastvalue
            alloutnetworkinfo_list.append(alloutnetworkinfo_dict)

        print(alloutnetworkinfo_list)
        print(allinnetworkinfo_list)

        allnetworkinfo_list = []
        for networkinfo in allinnetworkinfo_list:
            innetworkdrivename = networkinfo['netDrive']
            for outnetworkinfo_check in alloutnetworkinfo_list:
                if outnetworkinfo_check['netDrive'] == innetworkdrivename:
                    print('1111111', outnetworkinfo_check)

                    print('networkinfo', networkinfo)
                    print('outnetworkinfo_check[outNet]', outnetworkinfo_check['outNet'])
                    outnetvalue = outnetworkinfo_check['outNet']
                    networkinfo['outNet'] = outnetvalue
                    allnetworkinfo_list.append(networkinfo)

        print(allnetworkinfo_list)
        sendmsgtype8 = {
        "data": {
            "type": 8,
            "token": token,
            "msgid":msgid,
            'companyid': companyid,
            "rootbean": {
            "msg": "当前" + host + "(ip:" + hostip + "）网络状况：",
            "actions": allnetworkinfo_list
            }}}

    socket.emit('chatbot', sendmsgtype8)
    print('ooooooh yes')

#发送查询主机磁盘状态消息
def botsendmsgtype6(host):
    msgid = generate_random_str(48)
    getinfo = requests.get(apigetmonitorurl + '/' + host + '?token=' + token + '&companyid=' + companyid, headers=header)
    print('hhhhhhhhhhh', getinfo.json())
    hostip = getinfo.json()['hostip']
    if 'status' in getinfo.json():
        print('不存在host', host)
        sendmsgtype6 = {
               'data': {'type': 1, 'token': token,'msgid':msgid, 'companyid': companyid, 'rootbean':
                   {'msg': "没有查询到相关信息、请检查输入信息是否正确。"}}}
    else:
        monitorinfo = getinfo.json()
        diskinfo_list = monitorinfo['disk']
        print(diskinfo_list)
        useddiskinfo_list = []
        for diskinfo in diskinfo_list:
            useddiskinfo_dict = {}
            drivename_source = diskinfo['key_']
            drivename = drivename_source.strip('vfs.fs.size').strip('[').strip(']')
            diskdrivename = drivename.split(',')

            if drivename.find('used') != -1:
                diskuseddrivelastvalue = diskinfo['lastvalue']
                useddiskinfo_dict['usedSize'] = diskuseddrivelastvalue
                useddiskinfo_dict['title'] = diskdrivename[0]
                useddiskinfo_list.append(useddiskinfo_dict)

        totaldiskinfo_list = []
        for totaldiskinfo in diskinfo_list:
            totaldiskinfo_dict = {}
            totaldrivename_source = totaldiskinfo['key_']
            totaldrivename = totaldrivename_source.strip('vfs.fs.size').strip('[').strip(']')
            diskdrivename = totaldrivename.split(',')
            if totaldrivename.find('total') != -1:
                disktotaldrivelastvalue = totaldiskinfo['lastvalue']
                totaldiskinfo_dict['totalSize'] = disktotaldrivelastvalue
                totaldiskinfo_dict['title'] = diskdrivename[0]
                totaldiskinfo_list.append(totaldiskinfo_dict)

        alldisknfo_list = []
        for lastuseddiskinfo in useddiskinfo_list:
            lastuseddiskdrivename = lastuseddiskinfo['title']
            for lasttotaldiskinfo_check in totaldiskinfo_list:
                if lasttotaldiskinfo_check['title'] == lastuseddiskdrivename:

                    alldiskvalue = lasttotaldiskinfo_check['totalSize']
                    useddiskvalue = lastuseddiskinfo['usedSize']
                    diskratio = useddiskvalue / alldiskvalue * 100

                    int_diskratio = int(diskratio)
                    float_alldiskvalue = '%.2f' % alldiskvalue
                    float_useddiskvalue = '%.2f' % useddiskvalue

                    totalSize = str(float_alldiskvalue) + 'G'
                    usedSize = str(float_useddiskvalue) + 'G'
                    lastuseddiskinfo['ratio'] = int_diskratio
                    lastuseddiskinfo['totalSize'] = totalSize
                    lastuseddiskinfo['usedSize'] = usedSize
                    alldisknfo_list.append(lastuseddiskinfo)

        print(alldisknfo_list)

        sendmsgtype6 = {
        "data": {
            "type": 6,
            "token": token,
            "msgid": msgid,
            'companyid': companyid,
            "rootbean": {
            "msg": "当前" + host + "(ip:" + hostip + "）磁盘状况：",
            "actions": alldisknfo_list
            }}}

    socket.emit('chatbot', sendmsgtype6)
    print('ooooooh yes')

def botsendmsgtype1(username):
    msgid = generate_random_str(48)
    sendmsgtype1 = {'data': {'type':1, 'token': token,'msgid':msgid,'companyid':companyid, 'rootbean':{'msg': '你好，'+ username}}}
    socket.emit('chatbot', sendmsgtype1)
    print('ooooooh yes')



#审核不同类型的消息
def botsendmsgtype11(host ,role, oprole, action, commandType):
    msgid = generate_random_str(32)
    
    sendmsgtype11 = {'data':"333333333333"}
    socket.emit('chatbot', sendmsgtype11)
    if role == '8':
        botjoinroot("Oooops, 用户已被禁用Oooops")

    elif oprole == '4' or oprole == '6' or oprole == '3':
        if action == 'agree' or action == 'request':
            if commandType == 10:
                print('重启执行中...')

                rebooturl = serverip + '/api/v1/salt/command'
                usertoken = token.split('-')[1]
                userid = token.split('-')[0]
                payload = {"usertoken": usertoken,
                           "userid":userid,
                            "clientip":host,
                            "command":"reboot",
                            "companyid":companyid}

                rebootrs = requests.post(url=rebooturl, data=json.dumps(payload), headers=header)

                if rebootrs.status_code == 200:
                    #rebootrs_dict_str = rebootrs.json()
                    #print(rebootrs_dict_str)
                    # rebootrs_dict = eval(rebootrs_dict_str)a
                    rebootrs_dict = rebootrs.json()
                    status = rebootrs_dict['status']
                    if status == 0:
                        sendmsg(host + " 重启成功!")
                    else:
                        sendmsg(host + " 重启失败!, " + rebootrs_dict['result'])
            elif commandType == 3:

                print('查看主机cpu执行中...')
                print(host)
                botsendmsgtype3(host)
                print('主机cpu执行完成')
            elif commandType == 4:
                print('查看主机内存执行中...')
                print(host)
                botsendmsgtype4(host)
            elif commandType == 6:
                print(host)
                botsendmsgtype6(host)
            elif commandType == 8:
                print('查看主机网络流量执行中...')
                print(host)
                botsendmsgtype8(host)

        else:
            print('已拒绝...')
            if commandType == 10:
                sendmsg(host + " ： 此主机重启申请已被拒绝!")
            elif commandType == 3:
                sendmsg(host + " ： 查看此主机CPU已被拒绝!")
            elif commandType == 4:
                sendmsg(host + " ： 查看此主机内存已被拒绝")
            elif commandType == 6:
                sendmsg(host + " ： 查看此主机磁盘状态已被拒绝!")
            elif commandType == 8:
                sendmsg(host + " ： 查看此主机网络流量已被拒绝!")


    print('ooooooh yes')


def botsendmsgtype12(host, role, oprole):
    msgid = generate_random_str(48)
    getinfo = requests.get(apigetmonitorurl + '/' + host + '?token=' + token + '&companyid=' + companyid, headers=header)
    print('hhhhhhhhhhh', getinfo.json())
    if 'status' in getinfo.json():
        print('不存在host', host)
        sendmsgtype12 = {
               'data': {'type': 1, 'token': token,'msgid':msgid, 'companyid': companyid, 'rootbean':
                   {'msg': "没有查询到相关信息、请检查输入信息是否正确。"}}}
    else:
        hostip = getinfo.json()['hostip']
        #
        # if action == 'agree' or action == 'request':
        print('执行中...')
        diskperformanceurl = serverip + '/api/v1/salt/diskperformance'
        data = {

            "token": token,
            "oprole": oprole,
            "role": role,
            "clientip": host,
            "commandid": "4",
            "companyid": companyid
        }

        diskperformance_request = requests.post(url=diskperformanceurl, data=json.dumps(data), headers=header)

        assert diskperformance_request.status_code == 200
        command_result = diskperformance_request.json()
        print(command_result)
        if command_result["status"] == 0:
            result_temp = command_result["result"]["command_result"]
            socket.emit('chatbot', result_temp)
        else:
            result_temp = command_result["msg"]
            socket.emit('chatbot', result_temp)

        sendmsgtype12 = {
            "data": {
                "type": 12,
                "token": token,
                "msgid": msgid,
                'companyid': companyid,
                "rootbean": {
                    "msg": "当前" + host + "(ip:" + hostip + "）磁盘IO：",
                    "actions": result_temp
                }}}
    print(sendmsgtype12)
    socket.emit('chatbot', sendmsgtype12)
    print('ooooooh yes')


#机器人响应
def chatbot_response(*args):
    try:
        print('chatbot zzzzzzzzzzz')
        botmsgdict = args[0]
        print(botmsgdict)
        username = botmsgdict['data']['username']


        if botmsgdict['data']['oprole'] != '5' and botmsgdict['data']['type'] == 1:
            botsendmsgtype1(username)
        elif botmsgdict['data']['oprole'] != '5' and botmsgdict['data']['type'] == 2:
            botsendmsgtype2(username)
        elif botmsgdict['data']['oprole'] != '5' and botmsgdict['data']['type'] == 10:
                host = botmsgdict['data']['rootbean']['hostip']
                role = botmsgdict['data']['role']
                oprole = botmsgdict['data']['oprole']
                action = botmsgdict['data']['rootbean']['action']
                commandType = botmsgdict['data']['commandType']
                print(host, role, oprole, action,commandType)
                botsendmsgtype11(host,role, oprole, action,commandType)

                #保存操作记录
                if commandType == 3:
                    exec_com = "cpu"
                elif commandType == 4:
                    exec_com = "memory"
                elif commandType == 6:
                    exec_com = "iostat -d |egrep -v '$^|Linux' |awk '{print $1,$3,$4}'"
                elif commandType == 8:
                    exec_com = "network"
                elif commandType == 10:
                    exec_com = "reboot"
                ip = host
                hostname = host
                exec_time = datetime(datetime.today().year, datetime.today().month, datetime.today().day,datetime.today().hour,datetime.today().minute,datetime.today().second)
                exec_time = exec_time.strftime("%Y-%m-%d %H:%M:%S")
                addoperation_payload = {"username":username,"companyid":companyid,"exec_com":exec_com,"ip":ip,"hostname":hostname,"exec_time":exec_time}
                url_s = serverip + '/api/v1/operation/operation_log_save'
                saveoperation_rs = requests.post(url=url_s, data=json.dumps(addoperation_payload), headers=header)

    except Exception as e:
        print(e)
        print("Ooops, somethings waring")

#监控constatus消息
def conn():
    socket.emit('conn', 'test')
    botjoinroot('join room')
    socket.on('connstatus', conn_response)
    socket.wait(seconds=1)

def onlyconn():
    socket.emit('conn', 'test')
    socket.on('connstatus', conn_response)
    socket.wait(seconds=1)

def chatbots():
    while True:
        socket.on('chatbotstatus', chatbot_response)
        socket.wait(seconds=1)

def talks():
    while True:
        socket.on('talkstatus', talk_response)
        socket.wait(seconds=1)

def botjoinroot(message):
    msgid = generate_random_str(48)
    sendmsg = {'token': token,'role':'chatbot', 'companyid':companyid, 'msg': message, 'msgid':msgid}
    socket.emit('talk', sendmsg)

def sendmsg(message):
    msgid = generate_random_str(48)
    sendmsg = {'token': token, 'companyid':companyid, 'msg': message, 'msgid':msgid}
    socket.emit('talk', sendmsg)


def conn_response(*args):
    print(args[0])


def talk_response(*args):
    print('talk zzzzzzzzzzz')
    print(args[0])

tada = threading.Thread(target=chatbots)
tada.start()

talk_thread = threading.Thread(target=talks)
talk_thread.start()

conn()
def connthreading():
    while True:
        time.sleep(2)
        onlyconn()
connth = threading.Thread(target=connthreading)
connth.start()
