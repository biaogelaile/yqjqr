#coding=utf-8
from flask import jsonify, request
from user import *
import zabbix_quey
import houtai
import usermessage
from concurrent.futures import ThreadPoolExecutor
import push_msg
import salt_exec
import search_oper_log
import demjson
from model import *
#获取短信通知
@app.route('/api/v1/sms', methods=['POST'])
def SmsVC():
    request_data = request.get_json()
    mobile = request_data['mobile']
    smsinfo = smsvc(mobile)
    return jsonify(smsinfo)
#忘记密码短信验证接口
@app.route('/api/v1/forgetsms', methods=['POST'])
def ForgetSmsVC():
    request_data = request.get_json()
    mobile = request_data['mobile']
    smsinfo = forget_smsvc(mobile)
    return jsonify(smsinfo)


#查询用户信息
@app.route('/api/v1/user', methods=['GET'])
def UserInfoGet():
    token = request.args.get('token')
    companyid = request.args.get('companyid')
    usertoken = token.split('-')[1]
    userid = token.split('-')[0]
    userinfo = user_info(userid, usertoken, companyid)
    return jsonify(userinfo)

#获取游客信息
@app.route('/api/v1/youke', methods=['GET'])
def YoukeInfoGet():
    token = request.args.get('token')
    print(token)
    #token = "youkechatbot-11111"
    usertoken = token.split('-')[1]
    userid = token.split('-')[0]
    userinfo = user_info(userid, usertoken, None)
    return jsonify(userinfo)

#注册用户
@app.route('/api/v1/user', methods=['POST'])
def UserRegistry():
    request_data = request.get_json()
    mobile = request_data['mobile']
    password = request_data['password']
    smsvc = request_data['smsvc']
    registryrs = mobile_insert(smsvc, password, mobile)
    return jsonify(registryrs)

#校验密码
@app.route('/api/v1/password', methods=['POST'])
def Password():
    request_data = request.get_json()
    password = request_data['password']
    token = request_data['token']
    usertoken = token.split('-')[1]
    userid = token.split('-')[0]

    registryrs = password_jiaoyan(usertoken, userid, password)
    return jsonify(registryrs)

#修改密码
@app.route('/api/v1/password', methods=['PATCH', 'PUT'])
def ChangePassword():
    request_data = request.get_json()
    oldpassword = request_data['oldpassword']
    newpassword = request_data['newpassword']
    token = request_data['token']
    usertoken = token.split('-')[1]
    userid = token.split('-')[0]
    registryrs = change_password(usertoken, userid, newpassword, oldpassword)
    return jsonify(registryrs)


#修改用户信息
@app.route('/api/v1/user', methods=['PATCH', 'PUT'])
def ForgetPassword():
    request_data = request.get_json()
    #action = ['password', 'username', 'mobile']
    action = request_data['action']
    if action == 'password':
        mobile = request_data['mobile']
        newpassword = request_data['newpassword']
        smsvc = request_data['smsvc']
        registryrs = user_forget_password(smsvc, newpassword, mobile)
        return jsonify(registryrs)

    elif action ==  'username':
        token = request_data['token']
        usertoken = token.split('-')[1]
        userid = token.split('-')[0]
        newusername = request_data['newusername']
        registryrs = user_update_username(usertoken,userid, newusername)
        return jsonify(registryrs)

    elif action ==  'mobile':
        token = request_data['token']
        usertoken = token.split('-')[1]
        userid = token.split('-')[0]
        newmobile = request_data['newmobile']
        smsvc = request_data['smsvc']
        registryrs = user_update_mobile(smsvc, usertoken, userid, newmobile)
        return jsonify(registryrs)
    else:
        return jsonify({'status': '999', 'msg': 'Oooops, cant not do this'})


#查询用户是否存在默认公司
@app.route('/api/v1/default', methods=['GET'])
def UserDefaultCompany():
    token = request.args.get('token')
    userid = token.split('-')[0]
    usertoken = token.split('-')[1]
    queryrs = user_default_company(usertoken, userid)
    return jsonify(queryrs)


#登录接口
@app.route('/api/v1/login', methods=['POST'])
def UserLogin():
    request_data = request.get_json()
    print(request_data)
    mobile = request_data['mobile']
    password = request_data['password']
    loginrs = user_login(mobile, password)
    return jsonify(loginrs)

#查询所有公司信息
@app.route('/api/v1/companys', methods=['GET'])
def CompanysGet():
    token = request.args.get('token')
    usertoken = token.split('-')[1]
    companyrs = company_query(None, usertoken)
    return jsonify(companyrs)

#查询某个公司信息
@app.route('/api/v1/company/<string:companyname>', methods=['GET'])
def CompanyGet(companyname):
    token = request.args.get('token')
    usertoken = token.split('-')[1]
    companyrs = company_query(companyname, usertoken)
    return jsonify(companyrs)

#创建公司
@app.route('/api/v1/company', methods=['POST'])
def CompanyAdd():
    request_data = request.get_json()
    email = request_data['email']
    username = request_data['username']
    companyname = request_data['companyname']
    token = request_data['token']
    userid = token.split('-')[0]
    usertoken = token.split('-')[1]
    companyrs = company_insert(email, username, companyname, userid, usertoken)
    return jsonify(companyrs)

#修改公司信息
@app.route('/api/v1/company', methods=['PATCH', 'PUT'])
def UpdateOpUserDefaultCompany():
    request_data = request.get_json()
    token = request_data['token']
    userid = token.split('-')[0]
    usertoken = token.split('-')[1]
    companyid = request_data['companyid']
    joininfors = updateopuserdefaultcompany(usertoken, userid, companyid)
    return jsonify(joininfors)

#创建公司成员
@app.route('/api/v1/member', methods=['POST'])
def MemberAdd():
    request_data = request.get_json()
    token = request_data['token']
    companyname = request_data['companyid']
    username = request_data['username']
    userid = token.split('-')[0]
    usertoken = token.split('-')[1]

    memberrs = join_company(userid, companyname, username, usertoken)
    return jsonify(memberrs)

#删除公司成员
@app.route('/api/v1/member', methods=['DELETE'])
def MemberDel():
    token = request.args.get('token')
    userid = token.split('-')[0]
    usertoken = token.split('-')[1]
    companyid = request.args.get('companyid')
    memberrs = leave_company(usertoken, userid, companyid)
    return jsonify(memberrs)

#获取某个公司的申请信息
@app.route('/api/v1/joininfo', methods=['GET'])
def JoinInfo():
    token = request.args.get('token')
    userid = token.split('-')[0]
    usertoken = token.split('-')[1]
    companyid = request.args.get('companyid')
    joininfors = join_info(userid, usertoken, companyid)
    return jsonify(joininfors)

#获取app侧边栏信息
@app.route('/api/v1/sidebar', methods=['GET'])
def SidebarInfo():
    token = request.args.get('token')
    userid = token.split('-')[0]
    usertoken = token.split('-')[1]
    joininfors = sidebar_get(userid, usertoken)
    return jsonify(joininfors)

#申请加入某个公司
@app.route('/api/v1/joininfo', methods=['POST'])
def JoinUpdate():
    request_data = request.get_json()
    print(request_data)
    token = request_data['token']
    admin_action = request_data['admin_action']
    request_userid = request_data['request_userid']
    request_id = request_data['request_id']
    request_companyid = request_data['request_companyid']
    userid = token.split('-')[0]
    usertoken = token.split('-')[1]
    joininfors = join_update(request_id,userid, usertoken,request_userid, admin_action, request_companyid)
    return jsonify(joininfors)

#获取某个公司的成员信息
@app.route('/api/v1/opusers', methods=['GET'])
def OpUsers():
    token = request.args.get('token')
    userid = token.split('-')[0]
    usertoken = token.split('-')[1]
    companyid = request.args.get('companyid')
    joininfors = opusers(userid, usertoken, companyid)
    return jsonify(joininfors)

#查询公司某个成员的信息
@app.route('/api/v1/opuser/<string:username>', methods=['GET'])
def OpUser(username):
    token = request.args.get('token')
    userid = token.split('-')[0]
    usertoken = token.split('-')[1]
    companyid = request.args.get('companyid')
    joininfors = opuser(userid, usertoken, username, companyid)
    return jsonify(joininfors)

#获取某个公司命令审核情况
@app.route('/api/v1/commandstatus', methods=['GET'])
def CommandStatus():
    token = request.args.get('token')
    userid = token.split('-')[0]
    usertoken = token.split('-')[1]
    companyid = request.args.get('companyid')
    joininfors = commandstatus(userid, usertoken, companyid)
    return jsonify(joininfors)

#修改某个公司的命令审核状态
@app.route('/api/v1/commandstatus', methods=['PATCH', 'PUT'])
def UpdateCommandStatus():
    request_data = request.get_json()
    token = request_data['token']
    adminuserid = token.split('-')[0]
    usertoken = token.split('-')[1]
    companyid = request_data['companyid']
    commandstatus_list = request_data['commandstatus_list']
    joininfors = updatecommandstatus(adminuserid, usertoken, companyid,commandstatus_list)
    return jsonify(joininfors)

#添加运维用户
@app.route('/api/v1/opuser', methods=['POST'])
def AddOpUser():
    request_data = request.get_json()
    token = request_data['token']
    username = request_data['opusername']
    mobile = request_data['opmobile']
    companyid = request_data['companyid']
    adminuserid = token.split('-')[0]
    usertoken = token.split('-')[1]
    joininfors = addopuser(adminuserid, usertoken, username, mobile, companyid)
    return jsonify(joininfors)

#编辑运维用户
@app.route('/api/v1/opuser', methods=['PATCH', 'PUT'])
def UpdateOpUser():
    request_data = request.get_json()
    token = request_data['token']
    adminuserid = token.split('-')[0]
    usertoken = token.split('-')[1]
    print(request_data)
    if 'oprole' in request_data:
        opuserid = request_data['opuserid']
        oprole = request_data['oprole']
        opcompanyid = request_data['opcompanyid']
        joininfors = updateopuserrole(usertoken, adminuserid, opuserid, oprole, opcompanyid)
        return jsonify(joininfors)
    else:
        opuserid = request_data['opuserid']
        opusername = request_data['opusername']
        opmobile = request_data['opmobile']
        opcompanyid = request_data['opcompanyid']
        joininfors = updateopuser(adminuserid, usertoken, opusername, opmobile, opuserid, opcompanyid)
        return jsonify(joininfors)


#删除运维用户
@app.route('/api/v1/opuser', methods=['DELETE'])
def DeleteOpUser():
    token = request.args.get('token')
    opuserid = request.args.get('opmobile')
    companyid = request.args.get('companyid')
    adminuserid = token.split('-')[0]
    usertoken = token.split('-')[1]
    joininfors = deleteopuser(adminuserid, usertoken, opuserid, companyid)
    return jsonify(joininfors)

#删除后台公司
@app.route('/backstage/companydelete', methods=['DELETE'])
def CompanyDelete():
    token = request.args.get('token')
    userid = token.split('-')[0]
    usertoken = token.split('-')[1]
    companyid = request.args.get('companyid')
    joininfors = houtai.backstagecmdelete(usertoken, companyid)
    return jsonify(joininfors)

#获取客服电话
@app.route('/api/v1/custommobile', methods=['GET'])
def CustomMobile():
    token = request.args.get('token')
    userid = token.split('-')[0]
    usertoken = token.split('-')[1]
    rs = houtai.coustomMobile(userid, usertoken)
    return jsonify(rs)

#添加zabbix服务器
@app.route('/api/v1/zabbixserver', methods=['POST'])
def AddZabbixServer():
    request_data = request.get_json()
    token = request_data['token']
    zabbixserver = request_data['zabbixserver']
    zabbixusername = request_data['zabbixusername']
    zabbixpassword = request_data['zabbixpassword']

    adminuserid = token.split('-')[0]
    usertoken = token.split('-')[1]
    joininfors = zabbix_quey.zabbixserver_add(adminuserid, usertoken, zabbixserver, zabbixusername,zabbixpassword)
    return jsonify(joininfors)

#查询zabbix所有主机信息
@app.route('/api/v1/hosts', methods=['GET'])
def ZabbixHosts():
    token = request.args.get('token')
    userid = token.split('-')[0]
    usertoken = token.split('-')[1]
    companyid = request.args.get('companyid')
    joininfors = zabbix_quey.query_hosts(userid, usertoken, companyid)
    return jsonify(joininfors)

#搜索某台主机的信息
@app.route('/api/v1/host/<string:searchname>', methods=['GET'])
def ZabbixHost(searchname):
    token = request.args.get('token')
    #zabbixhostid = request.args.get('hostid')
    userid = token.split('-')[0]
    usertoken = token.split('-')[1]
    companyid = request.args.get('companyid')
    joininfors = zabbix_quey.query_zabbixhost(userid, usertoken, searchname, companyid)
    return jsonify(joininfors)


#添加zabbix服务器监控项到机器人
@app.route('/api/v1/zabbixmonitor', methods=['POST'])
def AddZabbixMonitor():
    request_data = request.get_json()
    token = request_data['token']
    hostinfo_list = request_data['hostinfo']
    print(hostinfo_list)
    companyid = request_data['companyid']
    userid = token.split('-')[0]
    usertoken = token.split('-')[1]
    joininfors = zabbix_quey.zabbixmonitor_add(userid, usertoken, hostinfo_list, companyid)
    return jsonify(joininfors)


#添加所有zabbix服务器
@app.route('/api/v1/zabbixallmonitor', methods=['POST'])
def AddZabbixAllMonitor():
    request_data = request.get_json()
    token = request_data['token']
    hostinfo_list = request_data['hostinfo']
    companyid = request_data['companyid']
    userid = token.split('-')[0]
    usertoken = token.split('-')[1]
    joininfors = zabbix_quey.zabbixallmonitor_add(userid, usertoken, hostinfo_list, companyid)
    return jsonify(joininfors)



#查询zabbix所有主机信息
@app.route('/api/v1/zabbixmonitors', methods=['GET'])
def ZabbixMonitors():
    token = request.args.get('token')
    companyid = request.args.get('companyid')
    userid = token.split('-')[0]
    usertoken = token.split('-')[1]
    joininfors = zabbix_quey.zabbixitem_query(userid, usertoken, companyid)
    return jsonify(joininfors)


#查询zabbix所有主机信息
@app.route('/api/v1/zabbixmonitor/<string:host>', methods=['GET'])
def ZabbixMonitor(host):
    token = request.args.get('token')
    userid = token.split('-')[0]
    usertoken = token.split('-')[1]
    companyid = request.args.get('companyid')
    joininfors = zabbix_quey.zabbixitem_value_query(userid, usertoken, host, companyid)
    return jsonify(joininfors)

#后台功能
@app.route('/backstage/index', methods=['GET'])
def BackstageIndex():
    token = request.args.get('token')
    userid = token.split('-')[0]
    usertoken = token.split('-')[1]
    joininfors = houtai.backstage(userid, usertoken)
    return jsonify(joininfors)

#在web前端页面显示所有公司信息
@app.route('/backstage/companymanages', methods=['GET'])
def BackstageCm():
    token = request.args.get('token')
    userid = token.split('-')[0]
    usertoken = token.split('-')[1]
    joininfors = houtai.backstagecms(userid, usertoken)
    return jsonify(joininfors)


#在web前端页面搜索某个公司的信息
@app.route('/backstage/companymanage/<string:companyname>', methods=['GET'])
def BackstageSearch(companyname):
    token = request.args.get('token')
    userid = token.split('-')[0]
    usertoken = token.split('-')[1]
    joininfors = houtai.backstagecm(userid, usertoken, companyname)
    return jsonify(joininfors)


#在web前端页面显示某个公司的信息
@app.route('/backstage/companymanage/companyinfo', methods=['GET'])
def BackstageSearch1():
    companyid = request.args.get("companyid")
    token = request.args.get('token')
    userid = token.split('-')[0]
    usertoken = token.split('-')[1]
    joininfors = backstagecm1(userid, usertoken, companyid)
    return jsonify(joininfors)


#在前端页面展示某个公司的成员情况
@app.route('/backstage/companymanage/opusersinfo', methods=['GET'])
def Opusersinfo():
    companyid = request.args.get("companyid")
    token = request.args.get('token')
    userid = token.split('-')[0]
    usertoken = token.split('-')[1]
    joininfors = opusersinfo(userid, usertoken, companyid)
    return jsonify(joininfors)


#获取某台主机的信息
@app.route('/api/v1/hostinfo', methods=['GET'])
def Hostinfo():
    hostip = request.args.get("hostip")
    token = request.args.get('token')
    userid = token.split('-')[0]
    usertoken = token.split('-')[1]
    joininfors = hostinfo(userid, usertoken, hostip)
    return jsonify(joininfors)


#获取host/hostid/hostname是否存在
@app.route('/api/v1/hostmessage', methods=['GET'])
def HostmessageGet():

    host = request.args.get("host")
    companyid = request.args.get('companyid')
    joininfors = zabbix_quey.hostmessageget(host, companyid)
    return jsonify(joininfors)


#获取处于试用期中的公司
@app.route('/backstage/tryouts', methods=['GET'])
def BackstageTryOut():
    token = request.args.get('token')
    userid = token.split('-')[0]
    usertoken = token.split('-')[1]
    joininfors = houtai.backstagetryouts(userid, usertoken)
    return jsonify(joininfors)


#获取即将过期的公司
@app.route('/backstage/expiringcompanys', methods=['GET'])
def BackstageExpireC():
    token = request.args.get('token')
    userid = token.split('-')[0]
    usertoken = token.split('-')[1]
    joininfors = houtai.backstageexpiring(userid, usertoken)
    return jsonify(joininfors)


#获取已经过期的公司
@app.route('/backstage/expiredcompanys', methods=['GET'])
def BackstageExpired():
    token = request.args.get('token')
    userid = token.split('-')[0]
    usertoken = token.split('-')[1]
    joininfors = houtai.backstageexpired(userid, usertoken)
    return jsonify(joininfors)

#获取所有用户信息
@app.route('/backstage/users', methods=['GET'])
def BackstageUsers():
    token = request.args.get('token')
    userid = token.split('-')[0]
    usertoken = token.split('-')[1]
    joininfors = houtai.backstageusers(userid, usertoken)
    return jsonify(joininfors)


#禁用某个用户
@app.route('/backstage/disableduser', methods=['POST'])
def DisabledUser():
    
    request_data = request.get_json()
    token = request_data['token']
    userid = token.split('-')[0]
    usertoken = token.split('-')[1]
    if 'disabled' in request_data:
        disabled = request_data['disabled']
    else:
        disabled = None
    joininfors = houtai.disabledUser(userid, usertoken, disabled)
    return jsonify(joininfors)

#禁用某家公司
@app.route('/backstage/disabledcompany', methods=['POST'])
def DisabledCompany():

    request_data = request.get_json()
    token = request_data['token']
    companyid = request_data["companyid"]
    usertoken = token.split('-')[1]
    if 'disabled' in request_data:
        disabled = request_data['disabled']
    else:
        disabled = None
    joininfors = houtai.disabledCompany(companyid, usertoken, disabled)
    return jsonify(joininfors)


#获取后台配置信息
@app.route('/backstage/configs', methods=['GET'])
def BackstageConfigsGet():
    token = request.args.get('token')
    userid = token.split('-')[0]
    usertoken = token.split('-')[1]
    joininfors = houtai.configsGet(userid, usertoken)
    return jsonify(joininfors)

#更改后台配置信息
@app.route('/backstage/configs', methods=['POST'])
def BackstageConfigsChange():
    request_data = request.get_json()
    token = request_data['token']
    userid = token.split('-')[0]
    usertoken = token.split('-')[1]
    if 'customerservice' in request_data:
        customerservice = request_data['customerservice']
    else:
        customerservice = None
    if 'expire' in request_data:
        expire = request_data['expire']
    else:
        expire = None
    if 'trydate' in request_data:
        trydate = request_data['trydate']
    else:
        trydate = None
    joininfors = houtai.configsChange(userid, usertoken, customerservice, expire, trydate)
    return jsonify(joininfors)

#以分页的形式展示所有用户
@app.route('/backstage/pageusers', methods=['GET'])
def PageUsers():
    token = request.args.get('token')
    userid = token.split('-')[0]
    usertoken = token.split('-')[1]
    page = request.args.get('page')
    joininfors = houtai.pageUsers(usertoken, page)
    return jsonify(joininfors)

#以分页的形式展示所有公司
@app.route('/backstage/pagecompanys', methods=['GET'])
def PageCompanys():
    token = request.args.get('token')
    userid = token.split('-')[0]
    usertoken = token.split('-')[1]
    page = request.args.get('page')
    joininfors = houtai.pageCompanys(usertoken, page)
    return jsonify(joininfors)

#修改后台账户和密码
@app.route('/backstage/admin', methods=['POST'])
def AdminInfo():

    request_data = request.get_json()
    username = request_data['username']
    password = request_data['password']
    joininfors = houtai.AdminInfo(username, password)
    return jsonify(joininfors)

#创建消息
@app.route('/api/v1/message', methods=['POST'])
def MessageAdd():
    request_data = request.get_json()
    token = request_data['token']
    userid = token.split('-')[0]
    usertoken = token.split('-')[1]
    companyid = request_data['companyid']
    usernewmessage = request_data['message']
    usermsgid = request_data['msgid']
    joininfors = usermessage.usermessage_insert(usertoken, userid, companyid, usernewmessage, usermsgid)
    return jsonify(joininfors)

#获取消息
@app.route('/api/v1/message', methods=['GET'])
def MessageGet():
    token = request.args.get('token')
    userid = token.split('-')[0]
    usertoken = token.split('-')[1]
    companyid = request.args.get('companyid')
    if request.args.get('msgid'):
        msgid = request.args.get('msgid')
    else:
        msgid = None
    joininfors = usermessage.usermessage_query(usertoken, userid, companyid, msgid)
    return jsonify(joininfors)



# 查询zabbix所有主机信息

@app.route('/api/v1/zabbixmonitor/getcompanyallhostvalue', methods=['POST'])
def getcomplanyallhostvalue():
    try:
        result = dict()
        request_data = request.get_json()
        print(request_data)
        usertoken = request_data['usertoken']
        companyid = request_data['companyid']
        role = request_data['role']


    except:
        print("我错了，dbnszbdnydkysxzjdmx")
        result = {
            "result": [],
            "msg": "parameter error",
            "status": -1
        }
        return jsonify(result)
    company_status = Company.query.filter_by(companyid=companyid).first()
    if company_status:
        company_role = company_status.companyrole
    else:
        #游客，设置和试用中公司项目的角色
        company_role = "2"
  
    #if role == "0" and companyid != "" and company_role != "1":
    if role == "0" and companyid != "":
        #合法用户
        #with ThreadPoolExecutor(2) as executor:
           #all_host_values = executor.submit(zabbix_quey.zabbix_get_complay_hosts, usertoken, companyid)
           # result = all_host_values.result()
            #result = zabbix_quey.zabbix_get_complay_hosts(usertoken, companyid)
        result = zabbix_quey.zabbix_get_complay_hosts(usertoken,companyid)
    else:
        #游客/待审核用户
        result = {"msg": "successful", "result":
            [{"host": "192.168.1.100", "item": [{"available": 89.1668, "key": "cpu", "total": 100.0},
                                                {"free": 12.7165, "key": "disk", "partition": "/", "total": 100.0},
                                                {"free": 31.4891, "key": "disk", "partition": "/boot", "total": 100.0},
                                                {"available": 20.8195, "key": "memory", "total": 31.4851},
                                                {"available": 95.9, "key": "network", "total": 100.0}]}], "status": 0}
        print(result)  
    #result = zabbix_quey.zabbix_get_complay_hosts(usertoken,companyid)
    return jsonify(result)


#推送消息给安卓手机
@app.route('/api/v1/msg_push/android', methods=['POST'])
def push_msg_to_android():
    try:

        request_data = request.get_json()
        usertoken = request_data['usertoken']
        userid = request_data["userid"]
        send_packagename = request_data['send_packagename']
        send_title = request_data['send_title']
        send_msg = request_data['send_msg']
        send_msg_desc = request_data['send_msg_desc']
        send_pass_through = request_data['send_pass_through']
    except:
        print("parameter error")
        result = {
            "result": [],
            "msg": "parameter error",
            "status": -1
        }
        return jsonify(result)

    result = push_msg.push_msg_to_android(usertoken=usertoken, userid=userid, send_packagename=send_packagename,
                                          send_msg=send_msg, send_title=send_title, send_msg_desc=send_msg_desc,
                                          send_pass_through=send_pass_through)
    return jsonify(result)

#推送消息给ios手机
@app.route('/api/v1/msg_push/ios', methods=['POST'])
def push_msg_to_ios():
    try:

        request_data = request.get_json()
        usertoken = request_data['usertoken']
        userid = request_data['userid']
        send_packagename = request_data['send_packagename']
        send_title = request_data['send_title']
        send_msg_desc = request_data['send_msg_desc']
        send_key = request_data['send_key']
        send_value = request_data['send_value']
    except:
        result = {
            "result": [],
            "msg": "parameter error",
            "status": -1
        }
        return jsonify(result)

    result = push_msg.push_msg_to_ios(userid=userid, usertoken=usertoken, send_packagename=send_packagename,
                                      send_title=send_title, send_msg_desc=send_msg_desc, send_key=send_key,
                                      send_value=send_value)
    return result

#执行salt命令
@app.route('/api/v1/salt/command', methods=['POST'])
def exec_command():
    try:
        request_data = request.get_json()
        print(request_data)
        usertoken = request_data['usertoken']
        userid = request_data['userid']
        clientip = request_data['clientip']
        command = request_data['command']
        companyid = request_data['companyid']
        hostinfo = Monitor.query.filter_by(zabbixhostname=clientip).first()
        clientip = hostinfo.zabbixhostip
        hostname = hostinfo.zabbixhostname
    except:
        result = {
            "result": "parameter error",
            "status": -1
        }
        return jsonify(result)
    username = User.query.filter_by(userid=userid).first()
    result = salt_exec.main(usertoken=usertoken, username=username.username, clientip=clientip, command=command,
                            companyid=companyid, hostname=hostname)

    return jsonify(result)

#搜索操作日志
@app.route('/api/v1/operation/operation_log', methods=['POST'])
def search_operation_log():
    try:
        request_data = request.get_json()
        usertoken = request_data['usertoken']
        companyid = request_data['companyid']
        role = request_data['role']
        oprole = request_data['oprole']
    except:
        result = {
            "result": "parameter error",
            "status": -1
        }
        return jsonify(result)
    company_status = Company.query.filter_by(companyid=companyid).first()
    if company_status:
        company_role = company_status.companyrole
    else:
        # 游客，设置和试用中公司项目的角色
        company_role = "2"
    if role == "0" and companyid != "" and oprole != "" and company_role == "2":
        result = search_oper_log.search_oper_log(usertoken=usertoken, companyid=companyid)
    else:
        result = {
    "result": [
        {
            "username":"tom",
            "user_image": "http://139.196.107.14:6001/upload/2018-11-12/qMWML0jLCnhs2o1Nv6a5ajpr-defaultUser@3x.png",
            "exec_time":"2018-12-12 09:28:53",
            "operating_command": "重启服务器 ",
            "msg":" ( ip :10.0.60.187)"
        },
        {
            "username":"tom",
            "user_image": "http://139.196.107.14:6001/upload/2018-11-12/qMWML0jLCnhs2o1Nv6a5ajpr-defaultUser@3x.png",
            "exec_time":"2018-12-10 11:28:53",
            "operating_command": "重启服务器 ",
            "msg":" ( ip :10.0.60.187)"
        },
        {
            "username":"jerry",
            "user_image": "http://139.196.107.14:6001/upload/2018-11-12/qMWML0jLCnhs2o1Nv6a5ajpr-defaultUser@3x.png",
            "exec_time":"2018-12-10 06:28:53",
            "operating_command": "重启服务器 ",
            "msg":" ( ip :10.0.60.187)"
        }
    ],
    "status": 0
}
    return demjson.encode(result)

#创建操作日志
@app.route('/api/v1/operation/operation_log_save', methods=['POST'])
def operation_log_save():
    try:
        request_data = request.get_json()
        companyid = request_data['companyid']
        username = request_data['username']
        exec_com = request_data['exec_com']
        ip = request_data['ip']
        hostname = request_data['hostname']
        exec_time = request_data['exec_time']
        print("有人吗，有人吗，有人吗，有人吗，有人吗，有人吗")
    except:
        result = {
            "result": "parameter error",
            "status": -1
        }
        return jsonify(result)

    result = houtai.save_oper_log(username=username,companyid=companyid,exec_com=exec_com,ip=ip,hostname=hostname,exec_time=exec_time)
    return demjson.encode(result)

#取消某个公司的申请
@app.route('/api/v1/companyapplication_cancel', methods=['POST'])
def cancel_company_application():
    try:
        request_data = request.get_json()
        token = request_data["token"]
        userid = token.split('-')[0]
        usertoken = token.split('-')[1]
        companyid = request_data["companyid"]

    except:
        result = {
            "result": "parameter error",
            "status": -1
        }
        return jsonify(result)

    result = cancel_companyapplication(companyid=companyid,usertoken=usertoken,userid=userid)
    return jsonify(result)

#获取用户禁用/启用状态
@app.route('/api/v1/userstatus',methods=['GET'])
def  search_userstaus():
    try:
        token = request.args.get('token')
        userid = token.split('-')[0]
        usertoken = token.split('-')[1]

    except:
        result = {
            "result": "parameter error",
            "status": -1
        }
        return jsonify(result)

    result = userstatus_search(usertoken=usertoken,userid=userid)
    return jsonify(result)


#不带条件查询所有的机器人操作日志
#@app.route('/api/v1/operation/search_operation_log', methods=['POST'])
def search_operation_log_condition(token, companyid, role, oprole):
    # try:
    #     request_data = request.get_json()
    #     usertoken = request_data['usertoken']
    #     companyid = request_data['companyid']
    #     role = request_data['role']
    #     oprole = request_data['oprole']
    # except:
    #     result = {
    #         "result": "parameter error",
    #         "status": -1
    #     }
    #     return jsonify(result)
    company_status = Company.query.filter_by(companyid=companyid).first()
    if company_status:
        company_role = company_status.companyrole
    else:
        # 游客，设置和试用中公司项目的角色
        company_role = "2"
    if role == "0" and companyid != "" and oprole != "" and company_role == "2":
        result = search_oper_log.search_oper_log(usertoken=token, companyid=companyid)
    else:
        result = {
    "result": [
        {
            "username":"tom",
            "user_image": "http://139.196.107.14:6001/upload/2018-11-12/qMWML0jLCnhs2o1Nv6a5ajpr-defaultUser@3x.png",
            "exec_time":"2018-12-12 09:28:53",
            "operating_command": "重启服务器 ",
            "msg":" ( ip :10.0.60.187)"
        },
        {
            "username":"tom",
            "user_image": "http://139.196.107.14:6001/upload/2018-11-12/qMWML0jLCnhs2o1Nv6a5ajpr-defaultUser@3x.png",
            "exec_time":"2018-12-10 11:28:53",
            "operating_command": "重启服务器 ",
            "msg":" ( ip :10.0.60.187)"
        },
        {
            "username":"jerry",
            "user_image": "http://139.196.107.14:6001/upload/2018-11-12/qMWML0jLCnhs2o1Nv6a5ajpr-defaultUser@3x.png",
            "exec_time":"2018-12-10 06:28:53",
            "operating_command": "重启服务器 ",
            "msg":" ( ip :10.0.60.187)"
        }
    ],
    "status": 0
}
    return result


"""
#提供过滤日志的条件
@app.route('/api/v1/operation/search_condition', methods=['POST'])
def search_operation_search_condition():
    try:
        request_data = request.get_json()
        usertoken = request_data['usertoken']
        companyid = request_data['companyid']
        role = request_data['role']
        oprole = request_data['oprole']
        search_command = request_data['search_command']
        search_user = request_data['search_user']
    except:
        result = {
            "result": "parameter error",
            "status": -1
        }
        return jsonify(result)
    company_status = Company.query.filter_by(companyid=companyid).first()
    if company_status:
        company_role = company_status.companyrole
    else:
        # 游客，设置和试用中公司项目的角色
        company_role = "2"
    if role == "0" and companyid != "" and oprole != "" and company_role == "2":
        result = search_oper_log.operation_search_condition(usertoken=usertoken, companyid=companyid,
                                                            search_user=search_user, search_command=search_command)
    else:
        if search_command == "0":
            result = {
                "result": [
                    {
                        "groupName": "监控项目",
                        "orders":[
                                {
                        "name":"查看主机CPU",
                        "orderId":"10",
                        "type":"3"
                    },
                    {
                        "name":"查看主机内存",
                        "orderId":"11",
                        "type":"4"
                    },
                    {
                        "name":"查看网络流量",
                        "orderId":"12",
                        "type":"8"
                    },
                    {
                        "name":"查看磁盘空间",
                        "orderId":"13",
                        "type":"6"
                    },
                    {
                        "name":"查看磁盘读写",
                        "orderId":"4",
                        "type":"12"
                    },
                    {
                        "name":"查看端口连接数",
                        "orderId":"4"
                    }
                    ]},
                    {
                        "groupName": "重启项目",
                        "orders":[
                                {
                        "name":"服务器重启",
                        "orderId":"20",
                        "type":"10"
                    },
                    {
                        "name":"重启tomcat应用",
                        "orderId":"21"
                    },
                    {
                        "name":"重启mysql数据库服务",
                        "orderId":"22"
                    }]
                    },
                    #{
                    #    "groupName": "数据库查询",
                    #    "orders":[
                    #            {
                    #    "name":"查询数据库表空间",
                    #    "orderId":"30"
                    # },
                    # {
                    #    "name":"查询单表空间",
                    #    "orderId":"31"
                    # },
                    # {
                    #    "name":"查询数据库锁",
                    #    "orderId":"32"
                    # },
                    # {
                    #    "name":"查询数据库会话数",
                    #    "orderId":"32"
                    # }]
                    # },
					{
                        "groupName": "命令操作日志",
                        "orders":[
                                {
                        "name":"查看命令操作日志",
                        "orderId":"40"
                    }]

					}],
                    "msg": "successful",
                    "status": 0
                }
        else:
            result = {
                "result": [{"operationId":"u2LPwkUyAGfOUIovJrCC1",
                        "operationImage":"http://139.196.107.14:6001/upload/2018-11-12/qMWML0jLCnhs2o1Nv6a5ajpr-defaultUser@3x.png",
                        "operationName":"tom"},
                       {"operationId":"u2LPwkUyAGfOUIovJrCC1",
                        "operationImage":"http://139.196.107.14:6001/upload/2018-11-12/qMWML0jLCnhs2o1Nv6a5ajpr-defaultUser@3x.png",
                        "operationName":"jerry"},
                       {"operationId":"u2LPwkUyAGfOUIovJrCC1",
                        "operationImage":"http://139.196.107.14:6001/upload/2018-11-12/qMWML0jLCnhs2o1Nv6a5ajpr-defaultUser@3x.png",
                        "operationName":"\u5f20\u4e09"}],
                "msg": "successful",
                "status": 0
            }

    return demjson.encode(result)
"""

#提供过滤日志的条件
@app.route('/api/v1/operation/search_condition', methods=['POST'])
def search_operation_search_condition():
    try:
        request_data = request.get_json()
        print(request_data)
        usertoken = request_data['usertoken']
        companyid = request_data['companyid']
        role = request_data['role']
        oprole = request_data['oprole']
        search_command = request_data['search_command']
        search_user = request_data['search_user']
    except:
        result = {
            "result": "parameter error",
            "status": -1
        }
        return jsonify(result)
    company_status = Company.query.filter_by(companyid=companyid).first()
    if company_status:
        company_role = company_status.companyrole
    else:
        # 游客，设置和试用中公司项目的角色
        company_role = "2"
    if role == "0" and companyid != "" and oprole != "" and company_role == "2":
        result = search_oper_log.operation_search_condition(usertoken=usertoken, companyid=companyid,
                                                            search_user=search_user, search_command=search_command)
    else:
        if search_command == "0":
            result = {
                "result": [
                    {
                        "groupName": "监控项目",
                        "orders":[
                                {
                        "name":"查看主机CPU",
                        "orderId":"10",
                        "type":"3"
                    },
                    {
                        "name":"查看主机内存",
                        "orderId":"11",
                        "type":"4"
                    },
                    {
                        "name":"查看网络流量",
                        "orderId":"12",
                        "type":'8'

                    },
                    {
                        "name":"查看磁盘状态",
                        "orderId":"13",
                        "type":'6'
                    }
                    ]},
                    {
                        "groupName": "重启项目",
                        "orders":[
                                {
                        "name":"服务器重启",
                        "orderId":"20",
                        "type":"10"
                    }]
                    },
                    #{
                    #    "groupName": "数据库查询",
                    #    "orders":[
                    #      
                    #]
                    #},
		    {
                        "groupName": "命令操作日志",
                        "orders":[
                                {
                        "name":"查看命令操作日志",
                        "orderId":"5"
                    }]

					}],
                    "msg": "successful",
                    "status": 0
                }
        else:
            result = {
                "result": [{"operationId":"u2LPwkUyAGfOUIovJrCC1",
                        "operationImage":"http://139.196.107.14:6001/upload/2018-11-12/qMWML0jLCnhs2o1Nv6a5ajpr-defaultUser@3x.png",
                        "operationName":"tom"},
                       {"operationId":"u2LPwkUyAGfOUIovJrCC1",
                        "operationImage":"http://139.196.107.14:6001/upload/2018-11-12/qMWML0jLCnhs2o1Nv6a5ajpr-defaultUser@3x.png",
                        "operationName":"jerry"},
                       {"operationId":"u2LPwkUyAGfOUIovJrCC1",
                        "operationImage":"http://139.196.107.14:6001/upload/2018-11-12/qMWML0jLCnhs2o1Nv6a5ajpr-defaultUser@3x.png",
                        "operationName":"\u5f20\u4e09"}],
                "msg": "successful",
                "status": 0
            }

    return demjson.encode(result)

#带条件搜索机器人操作日志
@app.route('/api/v1/operation/search_operation_log_condition', methods=['POST'])
def search_operation_with_condition():
    try:
        request_data = request.get_json()
        print(request_data)
        usertoken = request_data['usertoken']
        companyid = request_data['companyid']
        role = request_data['role']
        oprole = request_data['oprole']
        search_command_id = request_data["orderid"]
        search_userid = request_data["operatorid"]
        starttime = request_data['starttime']
        endtime = request_data['endtime']
    except:
        result = {
            "result": "parameter error",
            "status": -1
        }
        return jsonify(result)
    company_status = Company.query.filter_by(companyid=companyid).first()
    if company_status:
        company_role = company_status.companyrole
    else:
        # 游客，设置和试用中公司项目的角色
        company_role = "2"
    if role == "0" and companyid != "" and oprole != "" and company_role == "2":
        #执行不需要在服务器上执行的命令
        if search_command_id == "5":
            result = search_operation_log_condition(token=usertoken, companyid=companyid, role=role, oprole=oprole)
        else:
            result = search_oper_log.operation_search_with_condition(usertoken=usertoken, companyid=companyid,
                                                                     search_command_id=search_command_id,
                                                                     search_user_id=search_userid,
                                                                     starttime=starttime, endtime=endtime)
    else:
        result = {
            "result": [
                {
                    "username": "tom",
                    "user_image": "http://139.196.107.14:6001/upload/2018-11-12/qMWML0jLCnhs2o1Nv6a5ajpr-defaultUser@3x.png",
                    "exec_time": "2018-12-12 09:28:53",
                    "operating_command": "重启服务器 ",
                    "msg": " ( ip :10.0.60.187)"
                },
                {
                    "username": "tom",
                    "user_image": "http://139.196.107.14:6001/upload/2018-11-12/qMWML0jLCnhs2o1Nv6a5ajpr-defaultUser@3x.png",
                    "exec_time": "2018-12-10 11:28:53",
                    "operating_command": "重启服务器 ",
                    "msg": " ( ip :10.0.60.187)"
                },
                {
                    "username": "jerry",
                    "user_image": "http://139.196.107.14:6001/upload/2018-11-12/qMWML0jLCnhs2o1Nv6a5ajpr-defaultUser@3x.png",
                    "exec_time": "2018-12-10 06:28:53",
                    "operating_command": "重启服务器 ",
                    "msg": " ( ip :10.0.60.187)"
                }
            ],
            "status": 0
        }

    return demjson.encode(result)

"""
#获取公司状态
@app.route('/api/v1/companyStatus', methods=['GET'])
def CompanyStatus():
    companyid = request.args.get('companyid')
    companyStatus = getCompanyStatus(companyid)
    return jsonify(companyStatus)
"""

# 获取用户公司状态
@app.route('/api/v1/userCompanyStatus', methods=['GET'])
def UserCompanyStatus():
    
    token = request.args.get('token')
    companyid = request.args.get('companyid')
    userid = token.split('-')[0]
    userCompanyStatus = getUserCompanyStatus(userid, companyid)
    return jsonify(userCompanyStatus)


#获取目标主机磁盘性能
@app.route('/api/v1/salt/diskperformance', methods=['POST'])
def user_exec_command():
    try:
        request_data = request.get_json()
        token = request_data['token']
        userid = token.split('-')[0]
        usertoken = token.split('-')[1]
        clientip = request_data['clientip']
        commandid = int(request_data['commandid'])
        companyid = request_data['companyid']
        oprole = request_data['oprole']
        role = request_data['role']
    except:
        result = {
            "result": "parameter error",
            "status": -1
        }
        return demjson.encode(result)
    company_status = Company.query.filter_by(companyid=companyid).first()
    if company_status:
        company_role = company_status.companyrole
    else:
        # 游客，设置和试用中公司项目的角色
        company_role = "2"
    if role == "0" and companyid != "" and oprole != "" and company_role == "2":
        username = User.query.filter_by(userid=userid).first()
        with ThreadPoolExecutor(2) as executor:
            cmd_result = executor.submit(salt_exec.exec_passport, username.username, usertoken, clientip,
                                              commandid, companyid)
            result = cmd_result.result()
        # result = salt_exec.exec_passport(usertoken=usertoken, username=username.username, clientip=clientip,
        #                                  commandid=commandid, companyid=companyid)
    else:
        result = {"msg":"successful",
                  "result":{"command_result":[{"Blk_read":"7.26","Blk_wrtn":"534.83","Device":"sda"}],
                            "server":"192.168.1.1"},"status":0}

    return demjson.encode(result)

@app.route('/api/v1/md5', methods=['POST'])
def UserRegistr111y():

    registryrs = md5_password()
    return jsonify(registryrs)


if __name__ == '__main__':
    app.run(debugTrue, host='0.0.0.0', port=5000)
