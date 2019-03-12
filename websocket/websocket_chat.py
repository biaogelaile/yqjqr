# coding=utf-8
from flask import Flask, render_template
from flask_socketio import SocketIO, emit
import requests
import json
import random, string



from APISender import APISender
from base.APIMessage import *
from base.APIConstants import *
from APITools import *
from APISubscribe import *
import sys

#from push_msg import *


app = Flask(__name__)
socketio = SocketIO(app)
Constants.use_official() 
from flask_socketio import join_room, leave_room


#apiserver = 'http://127.0.0.1:5000'
apiserver = 'http://chatapi:5000'
#apiserver = 'http://139.196.107.14:5000'
header = {'Content-Type': 'application/json'}

#生成一个随机字符串
def generate_random_str(randomlength=16):
    """
    生成一个指定长度的随机字符串，其中
    string.digits=0123456789
    string.ascii_letters=abcdefghigklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ
    """
    str_list = [random.choice(string.digits + string.ascii_letters) for i in range(randomlength)]
    random_str = ''.join(str_list)
    return random_str

#监控conn
@socketio.on('conn')
def on_connect(msg):
    print('msg is :', msg)
    emit('connstatus', {'data': 'Connected'})

#监控talk
@socketio.on('talk')
def talk_connect(msg):
    print(msg)
    print(msg)
    jieshoumessage = msg['msg']
    print(type(msg))
    if 'msgid' in msg:
        msgid = msg['msgid']
    else:
        msgid = None
    if "ids" in msg:
        ids = msg["ids"]
        result = push_msg_to_android(ids[0],'jjjbbbkjjk', 'com.domain.operationrobot', '消息通知', '有人@你', 0,'payload')
        push_msg_to_ios(ids[0],'dddasdadad', 'com.domain.operationrobot', '消息通知', '有人@你', 'body')
        print("推送结果：",result)
        print("用户id",ids)
        print("用户id",ids)
        print("用户id",ids)
    #else:
       #ids = None
    token = msg['token']
    companyid = msg['companyid']
    print('token is', token)
    if companyid:
        user_profile_rs = requests.get(apiserver + '/api/v1/user?token=' + token + '&companyid=' + companyid, headers=header)
    else:
        user_profile_rs = requests.get(apiserver + '/api/v1/youke?token=' + token,headers=header)

    print(user_profile_rs.json())

    user_role = user_profile_rs.json()['role']
    user_companyrole = user_profile_rs.json()['companyrole']
    if user_role == '1' or user_role == '2':
        room = generate_random_str(24)
    else:
        room = user_profile_rs.json()['companyname']

    msg['imageUrl'] = user_profile_rs.json()['imageUrl']
    msg['mobile'] = user_profile_rs.json()['mobile']
    msg['username'] = user_profile_rs.json()['opuser_name']
    msg['userid'] = user_profile_rs.json()['userid']
    del msg['token']
    join_room(room)
    print('room is:', room)
    if 'role' in msg or jieshoumessage == 'joinroom':
        print('ccccccccccccc')
        pass
    else:
        response = {'data': msg}
        print('uuuuuuuuuuuuu')

        if user_role != '1' and user_role != '2':
            if msgid:
                addlixianmessage_payload = {'token':token, 'companyid':companyid, 'msgid':msgid, 'message': msg}
                addlixianmessage_rs = requests.post(apiserver + '/api/v1/message',data=json.dumps(addlixianmessage_payload),
                                           headers=header)
                if addlixianmessage_rs.status_code == 200:
                    pass
                else:
                    print("Something worang")

        emit('talkstatus', response, room=room)



#监控机器人
@socketio.on('chatbot')
def chatbot_connect(msg):
    print('chatbot msg', msg)
    print("$"*100)
    print("6666666666666666666")
    print(type(msg))
    print(type(msg))
    print(type(msg))
    print(type(msg))
    print(type(msg))
    print(type(msg))
    print("&"*100)
    token = msg['data']['token']
    if 'companyid' in msg['data']:
        companyid = msg['data']['companyid']
    else:
        companyid = None
    #company_info_rs = requests.get(apiserver + '/backstage/companymanage/companyinfo?token=' + token + '&companyid=' + companyid,headers=header)
    #print(company_info_rs.json())

    if 'msgid' in msg['data']:
        msgid = msg['data']['msgid']
    else:
        msgid = None
    """ 
    if 'type' in msg['data']:
        type = msg['data']['type']
    else:
        type = None
    """
    chatbottype = msg['data']['type']
    if companyid:
        user_profile_rs = requests.get(apiserver + '/api/v1/user?token=' + token + '&companyid=' + companyid, headers=header)
    else:
        user_profile_rs = requests.get(apiserver + '/api/v1/youke?token=' + token,headers=header)
    print(user_profile_rs.json())
    print(user_profile_rs.json())
    if 'role' in user_profile_rs.json():
        role = user_profile_rs.json()['role']
    if 'oprole' in user_profile_rs.json():
        oprole = user_profile_rs.json()['oprole']
    user_companyrole = user_profile_rs.json()['companyrole']
    print(role)
   
    if chatbottype == 11:
        if companyid:
        
            company_info_rs = requests.get(apiserver + '/backstage/companymanage/opusersinfo?token=' + token + '&companyid=' + companyid,headers=header)
            company_info_rs = company_info_rs.json()
            print(company_info_rs)
            applyopusername = user_profile_rs.json()['opuser_name']
            host = msg["data"]["rootbean"]["hostip"]
            msg1 = "%s申请重启服务器%s"%(applyopusername,host)
            print(msg1*10)
            #这个地方还要加上审核员
            for temp in company_info_rs["opuserinfo"]:
                result1 = push_msg_to_android(temp["opuserid"], token, 'com.domain.operationrobot', '消息通知', msg1, 0, 'payload')
                print(result1)
                result2 =push_msg_to_ios(temp["opuserid"], token, 'com.domain.operationrobot', '消息通知', msg1, 'body')
                print(result2)
  
    if role == '1' or role == '2':
        room = 'chatbotyouke11111'
    else:
        room = user_profile_rs.json()['companyname']
    join_room(room)
    print('room is:', room)
    #chatbottype = msg['data']['type']
    if chatbottype == 1:
        print('11111111111111111')
        if 'rootbean' in msg['data'] and msg['data']['rootbean']['msg'] == 'joinchatbotroom':
            print('检查rootbean 是否存在', msg['data']['rootbean']['msg'])
            pass
        else:
            msg['data']['role'] = role
            msg['data']['oprole'] = oprole
            msg['data']['imageUrl'] = user_profile_rs.json()['imageUrl']
            msg['data']['mobile'] = user_profile_rs.json()['mobile']
            msg['data']['username'] = user_profile_rs.json()['opuser_name']
            msg['data']['userid'] = user_profile_rs.json()['userid']
            msg['data']['companyid'] = user_profile_rs.json()['companyid']
            del msg['data']['token']
        #response = {'data': {'type':1, 'rootbean':{'msg': '你好'}}}
            if role != '1' and role != '2':
                if msgid:
                    print("到底有没有")
                    addlixianmessage_payload = {'token': token, 'companyid': companyid, 'msgid': msgid, 'message': msg}
                    addlixianmessage_rs = requests.post(apiserver + '/api/v1/message',
                                                        data=json.dumps(addlixianmessage_payload),
                                                        headers=header)
                    if addlixianmessage_rs.status_code == 200:
                        pass
                    else:
                        print("Something worang")
            print('发送数据中')
            emit('chatbotstatus', msg, room=room)
    elif chatbottype == 2:
        print('2222222222222')
        msg['data']['role'] = role
        msg['data']['oprole'] = oprole
        msg['data']['imageUrl'] = user_profile_rs.json()['imageUrl']
        msg['data']['mobile'] = user_profile_rs.json()['mobile']
        msg['data']['username'] = user_profile_rs.json()['opuser_name']
        msg['data']['userid'] = user_profile_rs.json()['userid']
        msg['data']
        del msg['data']['token']
        print(msg)
        print('msgid', msgid)
        if role != '1' and role != '2':
            if msgid:
                print("到底有没有")
                addlixianmessage_payload = {'token':token, 'companyid':companyid, 'msgid':msgid, 'message': msg}
                addlixianmessage_rs = requests.post(apiserver + '/api/v1/message',data=json.dumps(addlixianmessage_payload),
                                               headers=header)
                if addlixianmessage_rs.status_code == 200:
                    pass
                else:
                    print("Something worang")
        emit('chatbotstatus', msg, room=room)


    elif chatbottype >= 3:
        print('333333333')
        print(msg)
        print("$"*100)
        print(type(msg))
        print(type(msg))
        print(type(msg))
        print(type(msg))
        print(type(msg))
        print(type(msg))
        print("&"*100)
        msg['data']['role'] = role
        msg['data']['oprole'] = oprole
        msg['data']['imageUrl'] = user_profile_rs.json()['imageUrl']
        msg['data']['mobile'] = user_profile_rs.json()['mobile']
        msg['data']['username'] = user_profile_rs.json()['opuser_name']
        msg['data']['userid'] = user_profile_rs.json()['userid']
        del msg['data']['token']
        if role != '1' and role != '2':
            if msgid:
                addlixianmessage_payload = {'token':token, 'companyid':companyid, 'msgid':msgid, 'message': msg}
                addlixianmessage_rs = requests.post(apiserver + '/api/v1/message',data=json.dumps(addlixianmessage_payload),
                                               headers=header)
                if addlixianmessage_rs.status_code == 200:
                    pass
                else:
                    print("Something worang")
        emit('chatbotstatus', msg, room=room)

#推送安卓消息
def push_msg_to_android(userid,usertoken, package_name, title, description, pass_through,payload):
    APP_SecKey = r"lsoNVMUZH69YvcsLR6SHNQ=="
    result_code = 0
    try:


        # build android message
        message = PushMessage() \
            .restricted_package_name(package_name) \
            .title(title).description(description) \
            .pass_through(pass_through).payload(payload) \
            .extra({Constants.extra_param_notify_effect: Constants.notify_launcher_activity})

    except:
        print("get parameters value error ! ", sys.exc_info()[0])
        msg = "get parameters value error "
        result = {
            "msg": msg,
            "status": result_code
        }
        return result

    try:
        sender = APISender(APP_SecKey)
        recv = sender.send_to_user_account(message.message_dict(), userid)
        print(recv)

    except:
        print("send msg was failed ! ", sys.exc_info()[0])
        result_code = 1
        msg = "send msg was failed "
    finally:
        msg = "succecss"
        result = {
            "msg": msg,
            "status": result_code
        }
        return result



#推送ios消息
def push_msg_to_ios(userid,usertoken, package_name, title, subtitle, body):
    APP_SecKey = r"XWd6+oOcSmliC4jJJsdrcw=="
    result_code = 0
    try:
        message_ios10 = PushMessage() \
            .restricted_package_name(package_name) \
            .aps_title(title) \
            .aps_subtitle(subtitle) \
            .aps_body(body) \
            .aps_mutable_content("1") \
            .sound_url("default") \
            .badge(1) \
            .category("action") \
            .extra({"key": "value"})

    except:
        print("get parameters value error ! ", sys.exc_info()[0])
        result_code = 1
        msg = "get parameters value error "
        result = {
            "msg": msg,
            "status": result_code
        }
        return result

    try:
        sender = APISender(APP_SecKey)

        recv_ios = sender.send_to_user_account(message_ios10.message_dict_ios(), userid)
        print(recv_ios)


        tools = APITools(APP_SecKey)
    except:
        print("send msg was failed ! ", sys.exc_info()[0])
        result_code = 1
        msg = "send msg was failed "
    finally:
        msg = "succecss"
        result = {
            "msg": msg,
            "status": result_code
        }
        return result

#result = push_msg_to_android('uz1NFGfV0Kp64WloxTNq5zmCU','jjjbbbkjjk', 'com.domain.operationrobot', '消息通知', '有人@你', 0,'payload')
#print(result)

if __name__ == '__main__':
    socketio.run(app, host='0.0.0.0',port=5002)
