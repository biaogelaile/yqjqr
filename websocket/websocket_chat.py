# coding=utf-8

from flask import Flask, render_template
from flask_socketio import SocketIO, emit
import requests
import json
import random, string

from APISender import APISender
from base.APIMessage import *
from APITools import *
from APISubscribe import *
import sys

#from push_msg import *


app = Flask(__name__)
socketio = SocketIO(app)
from flask_socketio import join_room, leave_room


#apiserver = 'http://127.0.0.1:5000'
apiserver = 'http://chatapi:5000'
#apiserver = 'http://139.196.107.14:5000'
header = {'Content-Type': 'application/json'}

def generate_random_str(randomlength=16):
    """
    生成一个指定长度的随机字符串，其中
    string.digits=0123456789
    string.ascii_letters=abcdefghigklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ
    """
    str_list = [random.choice(string.digits + string.ascii_letters) for i in range(randomlength)]
    random_str = ''.join(str_list)
    return random_str

@socketio.on('conn')
def on_connect(msg):
    print('msg is :', msg)
    emit('connstatus', {'data': 'Connected'})

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
        #result = push_msg_to_android(ids, "111111", "xahshxahsxas", "dasdadada", "dsacsacascasca", "dadbjadaj",0)
        #print(result)
        print(ids)
        print(ids)
        print(ids)
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
    if user_role == '1' or user_role == '2' or user_companyrole == '1':
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


@socketio.on('chatbot')
def chatbot_connect(msg):

    print('chatbot msg', msg)
    token = msg['data']['token']
    companyid = msg['data']['companyid']
    if 'msgid' in msg['data']:
        msgid = msg['data']['msgid']
    else:
        msgid = None
    if companyid:
        user_profile_rs = requests.get(apiserver + '/api/v1/user?token=' + token + '&companyid=' + companyid, headers=header)
    else:
        user_profile_rs = requests.get(apiserver + '/api/v1/youke?token=' + token,headers=header)
    print(user_profile_rs.json())
    role = user_profile_rs.json()['role']
    oprole = user_profile_rs.json()['oprole']
    user_companyrole = user_profile_rs.json()['companyrole']
    print(role)
    if role == '1' or role == '2' or user_companyrole == '1':
        room = 'chatbotyouke11111'
    else:
        room = user_profile_rs.json()['companyname']
    join_room(room)
    print('room is:', room)
    chatbottype = msg['data']['type']

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
        msg['data']['role'] = oprole
        msg['data']['oprole'] = oprole
        msg['data']['imageUrl'] = user_profile_rs.json()['imageUrl']
        msg['data']['mobile'] = user_profile_rs.json()['mobile']
        msg['data']['username'] = user_profile_rs.json()['opuser_name']
        msg['data']['userid'] = user_profile_rs.json()['userid']
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
        msg['data']['role'] = oprole
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


#增加消息推送功能
def push_msg_to_android(userid,usertoken, send_packagename, send_title, send_msg, send_msg_desc, send_pass_through):
    APP_SecKey = r"lsoNVMUZH69YvcsLR6SHNQ=="
    result_code = 0
    try:

        #设置app的包名packageName
        #package_name = "com.domain.operationrobot"
        package_name = send_packagename
        #设置在通知栏展示的通知的标题
        title = send_title.replace("'", '')
        #设置要发送的消息内容, 不允许全是空白字符
        msg = send_msg.replace("'", '')
        #设置在通知栏展示的通知描述
        msg_desc = send_msg_desc.replace("'", '')
        #1表示透传, 0表示通知栏, 默认通知栏
        pass_through = int(send_pass_through)

        # build android message
        message = PushMessage() \
            .restricted_package_name(package_name) \
            .title(title).description(msg_desc) \
            .pass_through(pass_through).payload(msg) \
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
        recv = sender.send(message.message_dict(), userid)
        print(recv)
        tools = APITools(APP_SecKey)
        # 查询消息状态
        print(tools.query_message_status('msg_id').data)
        # 验证reg_id是否无效
        print(tools.validate_reg_ids(['reg_id1', 'reg_id2']))
        # 获取无效reg_id
        print(tools.query_invalid_reg_ids())
        # 获取无效alias
        print(tools.query_invalid_aliases())
        # 获取设备订阅topic
        print(tools.query_device_topics('package_name', 'reg_id'))
        print(tools.query_device_presence('package_name', ['reg_id1', 'reg_id2']))
        # 获取设备设置alias
        print(tools.query_device_aliases('package_name', 'reg_id'))
        # 检查定时任务是否存在
        print(tools.check_schedule_job_exist('msg_id'))
    except:
        print("send msg was failed ! ", sys.exc_info()[0])
        result_code = 1
        msg = "send msg was failed "
    finally:
        result = {
            "msg": msg,
            "status": result_code
        }
        return result


def push_msg_to_ios(userid,usertoken, send_packagename, send_title, send_key, send_value, send_msg_desc):
    APP_SecKey = r"XWd6+oOcSmliC4jJJsdrcw=="
    result_code = 0
    try:

        #设置app的包名packageName
        #package_name = "com.domain.operationrobot"
        package_name = send_packagename
        #设置在通知栏展示的通知的标题
        title = send_title.replace("'", '')
        #自定义键值对, 控制客户端行为
        send_key = send_key.replace("'", '')

        #设置在通知栏展示的通知描述
        msg_desc = send_msg_desc.replace("'", '')
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
        message_ios = PushMessage() \
            .description(msg_desc) \
            .sound_url("default") \
            .badge(1) \
            .extra({send_key: send_value})
        recv_ios = sender.send(message_ios.message_dict_ios(), userid)
        print(recv_ios)


        tools = APITools(APP_SecKey)
        # 查询消息状态
        print(tools.query_message_status('msg_id').data)
        # 验证reg_id是否无效
        print(tools.validate_reg_ids(['reg_id1', 'reg_id2']))
        # 获取无效reg_id
        print(tools.query_invalid_reg_ids())
        # 获取无效alias
        print(tools.query_invalid_aliases())
        # 获取设备订阅topic
        print(tools.query_device_topics('package_name', 'reg_id'))
        print(tools.query_device_presence('package_name', ['reg_id1', 'reg_id2']))
        # 获取设备设置alias
        print(tools.query_device_aliases('package_name', 'reg_id'))
        # 检查定时任务是否存在
        print(tools.check_schedule_job_exist('msg_id'))
    except:
        print("send msg was failed ! ", sys.exc_info()[0])
        result_code = 1
        msg = "send msg was failed "
    finally:
        result = {
            "msg": msg,
            "status": result_code
        }
        return result

def push_msg_to_ios10(userid,usertoken, send_packagename, send_title, send_key, send_value, send_msg_desc):
    APP_SecKey = r"XWd6+oOcSmliC4jJJsdrcw=="
    result_code = 0
    message_ios10 = PushMessage() \
        .aps_title("title") \
        .aps_subtitle("subtitle") \
        .aps_body("body") \
        .aps_mutable_content("1") \
        .sound_url("default") \
        .badge(1) \
        .category("action") \
        .extra({"key": "value"})
    try:

        #设置app的包名packageName
        #package_name = "com.domain.operationrobot"
        package_name = send_packagename
        #设置在通知栏展示的通知的标题
        title = send_title.replace("'", '')
        #自定义键值对, 控制客户端行为
        send_key = send_key.replace("'", '')

        #设置在通知栏展示的通知描述
        msg_desc = send_msg_desc.replace("'", '')
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
        message_ios = PushMessage() \
            .description(msg_desc) \
            .sound_url("default") \
            .badge(1) \
            .extra({send_key: send_value})
        recv_ios = sender.send(message_ios.message_dict_ios(), userid)
        print(recv_ios)


        tools = APITools(APP_SecKey)
        # 查询消息状态
        print(tools.query_message_status('msg_id').data)
        # 验证reg_id是否无效
        print(tools.validate_reg_ids(['reg_id1', 'reg_id2']))
        # 获取无效reg_id
        print(tools.query_invalid_reg_ids())
        # 获取无效alias
        print(tools.query_invalid_aliases())
        # 获取设备订阅topic
        print(tools.query_device_topics('package_name', 'reg_id'))
        print(tools.query_device_presence('package_name', ['reg_id1', 'reg_id2']))
        # 获取设备设置alias
        print(tools.query_device_aliases('package_name', 'reg_id'))
        # 检查定时任务是否存在
        print(tools.check_schedule_job_exist('msg_id'))
    except:
        print("send msg was failed ! ", sys.exc_info()[0])
        result_code = 1
        msg = "send msg was failed "
    finally:
        result = {
            "msg": msg,
            "status": result_code
        }
        return result



if __name__ == '__main__':
    socketio.run(app, host='0.0.0.0',port=5002)
