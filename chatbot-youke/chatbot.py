from socketIO_client import SocketIO, BaseNamespace
import requests, json
import threading

#serverip = 'http://127.0.0.1:5000'
serverip = 'http://nginx-server:5001'
socket = SocketIO('nginx-server',5001)
#socket = SocketIO('127.0.0.1',5001)
apiurl =  serverip + '/api/v1/login'
apigetmonitorurl = serverip + '/api/v1/zabbixmonitor'
#payload = {"password": "ppy6rQ3iAMKNzpDjpqYdP29g1STvoz6t0", "mobile": "c2YDSc5nIO7u0Bxjy7JHj0VOy"}
payload = {"password": "youke-chatbot", "mobile": "youke-chatbot"}
header = {'Content-Type': 'application/json'}

loginrs = requests.post(apiurl, data=json.dumps(payload), headers=header)
print("login...")
token = loginrs.json()['token']
print(token)
companyid = None
print(companyid)

def botjoinroot(message):
    sendmsg = {'token': token,'role':'chatbot', 'companyid':companyid, 'msg': message}
    socket.emit('talk', sendmsg)


def conn_response(*args):
    print(args[0])


def talk_response(*args):
    print('talk zzzzzzzzzzz')
    print(args[0])

def botsendmsgtype2(username):
    sendmsgtype2 = {'data': {'type': 2,'companyid':companyid, 'token': token, 'rootbean':
            {'msg': '你好，'+ username + ' 需要我帮你做点什么？', 'actions':
                [{'name': '查看主机CPU', 'type': '3'},
                 {'name': '查看主机内存', 'type': '4'},
                 {'name': '查看磁盘状态', 'type': '6'},
                 {'name': '查看网络流量', 'type': '8'}
                 # {'name': '查看磁盘读写', 'type': '12'},
                 ]}}}
    socket.emit('chatbot', sendmsgtype2)
    print('ooooooh yes')



def botsendmsgtype3(host):
    getinfo = requests.get(apigetmonitorurl + '/' + host + '?token=' + token + '&companyid=cHTqfKpMkfZaD1AuNWxJVVXDx', headers=header)
    if getinfo.status_code != 200:
        pass
    else:
        print('hhhhhhhhhhh', getinfo.json())
        if 'status' in getinfo.json():
            print('不存在host', host)
            sendmsgtype3 = {
                'data': {'type': 1, 'token': token, 'companyid': companyid, 'rootbean':
                    {'msg': "Ooops，未找到此主机：" + host + "，请检查输入的hostid/hostname/hostip"}}}

        else:
            lastvalue_str = getinfo.json()['cpu'][0]['lastvalue']
            lastvalue_float = float(lastvalue_str)
            lastvalue_float2 = round(lastvalue_float, 2)
            hostip = getinfo.json()['hostip']

            sendmsgtype3 = {
            "data": {
                "type": 3,
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

def botsendmsgtype4(host):
    getinfo = requests.get(apigetmonitorurl + '/' + host + '?token=' + token + '&companyid=cHTqfKpMkfZaD1AuNWxJVVXDx', headers=header)
    print('hhhhhhhhhhh', getinfo.json())
    if 'status' in getinfo.json():
        print('不存在host', host)
        sendmsgtype4 = {
            'data': {'type': 1, 'token': token, 'companyid': companyid, 'rootbean':
                {'msg': "Ooops，未找到此主机：" + host + "，请检查输入的hostid/hostname/hostip"}}}
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


def botsendmsgtype8(host):
    getinfo = requests.get(apigetmonitorurl + '/' + host + '?token=' + token + '&companyid=cHTqfKpMkfZaD1AuNWxJVVXDx', headers=header)
    print('hhhhhhhhhhh', getinfo.json())
    if 'status' in getinfo.json():
        print('不存在host', host)
        sendmsgtype8 = {
            'data': {'type': 1, 'token': token, 'companyid': companyid, 'rootbean':
                {'msg': "Ooops，未找到此主机：" + host + "，请检查输入的hostid/hostname/hostip"}}}

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
            'companyid': companyid,
            "rootbean": {
            "msg": "当前" + host + "(ip:" + hostip + "）网络状况：",
            "actions": allnetworkinfo_list
            }}}

    socket.emit('chatbot', sendmsgtype8)
    print('ooooooh yes')


def botsendmsgtype6(host):
    getinfo = requests.get(apigetmonitorurl + '/' + host + '?token=' + token + '&companyid=cHTqfKpMkfZaD1AuNWxJVVXDx', headers=header)
    print('hhhhhhhhhhh', getinfo.json())
    hostip = getinfo.json()['hostip']
    if 'status' in getinfo.json():
        print('不存在host', host)
        sendmsgtype6 = {
            'data': {'type': 1, 'token': token,'companyid': companyid, 'rootbean':
                {'msg': "Ooops，未找到此主机：" + host + "，请检查输入的hostid/hostname/hostip"}}}

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
            'companyid': companyid,
            "rootbean": {
            "msg": "当前" + host + "(ip:" + hostip + "）磁盘状况：",
            "actions": alldisknfo_list
            }}}

    socket.emit('chatbot', sendmsgtype6)
    print('ooooooh yes')

def botsendmsgtype1(username):
    sendmsgtype1 = {'data': {'type':1, 'token': token,'companyid':companyid, 'rootbean':{'msg': '你好，'+ username}}}
    socket.emit('chatbot', sendmsgtype1)
    print('ooooooh yes')


def chatbot_response(*args):
    print('chatbot zzzzzzzzzzz')
    botmsgdict = args[0]
    print(botmsgdict)
    username = botmsgdict['data']['username']
    if username is None:
        username = '游客'

    if botmsgdict['data']['userid'] != 'youkechatbot' and botmsgdict['data']['type'] == 1:
        botsendmsgtype1(username)
        print('lalalalalalalalal')
    elif botmsgdict['data']['userid'] != 'youkechatbot' and botmsgdict['data']['type'] == 2:
        botsendmsgtype2(username)
    elif botmsgdict['data']['userid'] != 'youkechatbot' and botmsgdict['data']['commandType'] == 3:
            print(botmsgdict['data'])
            host = botmsgdict['data']['rootbean']['hostip']
            print(host)
            botsendmsgtype3(host)
    elif botmsgdict['data']['userid'] != 'youkechatbot' and botmsgdict['data']['commandType'] == 4:
            print(botmsgdict['data'])
            host = botmsgdict['data']['rootbean']['hostip']
            print(host)
            botsendmsgtype4(host)
    elif botmsgdict['data']['userid'] != 'youkechatbot' and botmsgdict['data']['commandType'] == 6:
            print(botmsgdict['data'])
            host = botmsgdict['data']['rootbean']['hostip']
            print(host)
            botsendmsgtype6(host)
    elif botmsgdict['data']['userid'] != 'youkechatbot' and botmsgdict['data']['commandType'] == 8:
            print(botmsgdict['data'])
            host = botmsgdict['data']['rootbean']['hostip']
            print(host)
            botsendmsgtype8(host)





def chatbots():
    while True:
        socket.on('chatbotstatus', chatbot_response)
        socket.wait(seconds=1)


tada = threading.Thread(target=chatbots)
tada.start()


def conn():
    socket.emit('conn', 'test')
    botjoinroot('join room')
    socket.on('connstatus', conn_response)
    socket.wait(seconds=1)


def botsendmsgtypehello():
    sendmsgtype1 = {'data': {'type':1, 'token': token,'companyid': companyid, 'rootbean':{'msg': 'joinchatbotroom'}}}
    socket.emit('chatbot', sendmsgtype1)
    print('ooooooh yes')



conn()
botsendmsgtypehello()

