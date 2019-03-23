from socketIO_client import SocketIO, BaseNamespace
import requests, json
import threading

#serverip = 'http://127.0.0.1:5000'
serverip = 'http://nginx-server:5001'
socket = SocketIO('nginx-server',5001)

#serverip = 'http://61.139.64.108:18080'
#socket = SocketIO('http://61.139.64.108',18080)
#socket = SocketIO('',5001)
apiurl =  serverip + '/api/v1/login'
apigetmonitorurl = serverip + '/api/v1/zabbixmonitor'
#payload = {"password": "ppy6rQ3iAMKNzpDjpqYdP29g1STvoz6t0", "mobile": "c2YDSc5nIO7u0Bxjy7JHj0VOy"}
payload = {"password": "i8Ts9fJeBa5Q3AU2Ift74g==", "mobile": "youke-chatbot"}
header = {'Content-Type': 'application/json'}

loginrs = requests.post(apiurl, data=json.dumps(payload), headers=header)
print("login...")
token = loginrs.json()['token']
print(token)
companyid = None
print(companyid)

#机器人登录
def botjoinroot(message):
    sendmsg = {'token': token,'role':'chatbot', 'companyid':companyid, 'msg': message}
    socket.emit('talk', sendmsg)


#连接响应
def conn_response(*args):
    print(args[0])

#谈论响应
def talk_response(*args):
    print('talk zzzzzzzzzzz')
    print(args[0])


#机器人响应命令类型
def botsendmsgtype2(username):
    sendmsgtype2 = {'data': {'type': 2,'companyid':companyid, 'token': token, 'rootbean':
            {'msg': '你好，'+ username + ' 需要我帮你做点什么？', 'actions':
                [{'name': '查看主机CPU', 'type': '3'},
                 {'name': '查看主机内存', 'type': '4'},
                 {'name': '查看磁盘状态', 'type': '6'},
                 {'name': '查看网络流量', 'type': '8'},
                 {'name': '重启主机', 'type': '10'}
                 ]}}}
    socket.emit('chatbot', sendmsgtype2)
    print('ooooooh yes')


#发送查询cpu信息
def botsendmsgtype3(host):

    sendmsgtype3 = {
        "data": {
            "type": 3,
            "token": token,
            'companyid': companyid,
            "rootbean": {
                "msg": "当前" + host + "(ip:" + host + "）CPU运行情况：",
                "actions": [
                    {
                        "title": "CPU",
                        "ratio": '89',
                    }
                ]}}}

    socket.emit('chatbot', sendmsgtype3)
    print('ooooooh yes')


#发送查询内存消息
def botsendmsgtype4(host):
    sendmsgtype4 = {
        "data": {
            "type": 4,
            "token": token,
            'companyid': companyid,
            "rootbean": {
            "msg": "当前" + host + "(ip:" + host + "）内存运行情况：",
            "actions": [
                {
                "title": "内存",
                "ratio": '66',
                }
            ]}}}

    socket.emit('chatbot', sendmsgtype4)
    print('ooooooh yes')

#发送查询网络状况消息
def botsendmsgtype8(host):
    sendmsgtype8 = {
        "data": {
            "type": 8,
            "token": token,
            'companyid': companyid,
            "rootbean": {
            "msg": "当前" + host + "(ip:" + host + "）网络状况：",
            "actions": [
                {
                "netDrive": "eth0",
                "outNet": "55",
                "inNet": '22',
                },
                {
                    "netDrive": "eth1",
                    "outNet": "552",
                    "inNet": '223',
                }
            ]}}}

    socket.emit('chatbot', sendmsgtype8)
    print('ooooooh yes')


def botsendmsgtype6(host):
    sendmsgtype6 = {
        "data": {
            "type": 4,
            "token": token,
            'companyid': companyid,
            "rootbean": {
            "msg": "当前" + host + "(ip:" + host + "）磁盘运行情况：",
            "actions": [
                {
                "title": "磁盘",
                "ratio": '24.36',
                }
            ]}}}

    socket.emit('chatbot', sendmsgtype6)
    print('ooooooh yes')

#发送打招呼信息
def botsendmsgtype1(username):
    sendmsgtype1 = {'data': {'type':1, 'token': token,'companyid':companyid, 'rootbean':{'msg': '你好，'+ username}}}
    socket.emit('chatbot', sendmsgtype1)
    print('ooooooh yes')


#机器人针对不同命令类型进行响应
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




#监控chatbotstatus
def chatbots():
    while True:
        socket.on('chatbotstatus', chatbot_response)
        socket.wait(seconds=1)


tada = threading.Thread(target=chatbots)
tada.start()


#监控constatus
def conn():
    print("hehe")
    socket.emit('conn', 'test')
    botjoinroot('join room')
    socket.on('connstatus', conn_response)
    socket.wait(seconds=1)


def botsendmsgtypehello():
    sendmsgtype1 = {'data': {'type':1, 'token': token,'companyid': companyid, 'rootbean':{'msg': 'joinchatbotroom'}}}
    socket.emit('chatbot', sendmsgtype1)
    print('ooooooh yes')


print('ssss')
conn()
botsendmsgtypehello()


