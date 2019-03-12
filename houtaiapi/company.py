from model import *
from datetime import datetime, timedelta
import time
import requests, json
from urllib.parse import unquote
import math
import string
import re
import random
import sqlalchemy
url = apiserverurl + "/api/v1/hosts?token=xxx-11111"



headers = {'Content-Type': 'application/json-rpc'}

def auth(zabbixusername, zabbixpassword, zabbixurl):

    data = json.dumps(
    {
        "jsonrpc": "2.0",
        "method": "user.login",
        "params": {
            "user": zabbixusername,
            "password": zabbixpassword
        },
        "id": 0
    })

    authrs = requests.post(zabbixurl + '/zabbix/api_jsonrpc.php', data=data, headers=headers)
    token = authrs.json()['result']
    return token


def hostgroups(zabbixtoken, zabbixurl):
    data = json.dumps(
    {
        "jsonrpc":"2.0",
        "method":"hostgroup.get",
        "params":{
            "output":["groupid","name"],
        },
        "auth":zabbixtoken, # theauth id is what auth script returns, remeber it is string
        "id":1,
    })
    hostgroups = requests.post(zabbixurl + '/zabbix/api_jsonrpc.php', data=data, headers=headers)
    group_list = hostgroups.json()['result']
    return group_list

def zabbix_hosts_query(companyid):
        zabbixinfo_query = Zabbix.query.filter_by(companyid=companyid).first()
        if zabbixinfo_query is None:
            db.session.close()
            return {'status': 2, 'msg': '使用监控功能之前，需要先添加zabbix服务器'}
        zabbixusername = zabbixinfo_query.zabbixuser
        zabbixpassword = zabbixinfo_query.zabbixpassword
        zabbixurl = zabbixinfo_query.zabbixserver
        zabbixtoken = auth(zabbixusername, zabbixpassword, zabbixurl)

        group_list = hostgroups(zabbixtoken, zabbixurl)
        print(group_list)
        hostinfo_list = []
        for group in group_list:
            #hostinfo_dict = {}
            hostinfo_list.append(group['groupid'])
            #groupid = group['groupid']
            #groupname = group['name']
        print(hostinfo_list)
        data = json.dumps(
            {
                    "jsonrpc": "2.0",
                    "method": "host.get",
                    "params": {
                        "output": ["hostid", "name", "host"],
                        "groupids": hostinfo_list,
                    },
                    "auth": zabbixtoken,  # theauth id is what auth script returns, remeber it is string
                    "id": 1,
            })
        hosts = requests.post(zabbixurl + '/zabbix/api_jsonrpc.php', data=data, headers=headers)
        
        
        hosts_list =  hosts.json()['result']
        checkhosts_list = []
        for checkhost_dict in hosts_list:

            checkhostid = checkhost_dict['hostid']
            checkhost_query = Monitor.query.filter_by(zabbixhostid=checkhostid).first()
            if checkhost_query:
                checkhost_dict['hoststatus'] = 'in'
            else:
                checkhost_dict['hoststatus'] = 'out'
            checkhosts_list.append(checkhost_dict)

        allhostsnumber = len(checkhosts_list)
        inhostsnumber_query = Monitor.query.all()
        inhostsnumber = len(inhostsnumber_query)
        inhostinfo_list = []
        for inhost in inhostsnumber_query:
            inhostinfo_dict = {'hostid':inhost.zabbixhostid, 'host':inhost.zabbixhostip, 'name':inhost.zabbixhostname, 'hoststatus':'in'}
            inhostinfo_list.append(inhostinfo_dict)

        hosts_queryrs = {'status': 0, 'totalamount': allhostsnumber,
                         'inamount':inhostsnumber, 'totalhosts': checkhosts_list,
                         'inhosts':inhostinfo_list,
                         }
        db.session.close()
        return hosts_queryrs

def backstagecms(userid, token, page):
    if token != '11111':
        return {'status':1, 'msg':'token不可用'}

    #公司总数量
    rs_query_list = []
    page = int(page)

    companys_total_query = Company.query.all()
    companys_total =  len(companys_total_query) / 15
    page_total = math.ceil(companys_total)

    todays_datetime = datetime(datetime.today().year, datetime.today().month, datetime.today().day)
    backstage_expiredate_query = Backstage.query.first()
    backstage_expiredate = backstage_expiredate_query.companyexpire
    expire_date = todays_datetime + timedelta(days=int(backstage_expiredate))
    companys_query_page = Company.query.order_by(Company.createtime.desc()).paginate(page, per_page=15, error_out=False)
    companys_query = companys_query_page.items
    for company_query in companys_query:
        companyid = company_query.companyid
        zabbixhostinfo = zabbix_hosts_query(companyid)
        if zabbixhostinfo['status'] != 2:
            totalhost = len(zabbixhostinfo['totalhosts'])
        else:
            totalhost = None
        companyname = company_query.companyname
        disable = company_query.disable
        companyexpire = company_query.companyexpiredate
        companyrole = company_query.companyrole
        user_query = Opuser.query.filter(Opuser.opcompanyid==companyid, Opuser.oprole!=2).all()
        totalcompanyusers = int(len(user_query)) - 1
        adminuser_query = Opuser.query.filter_by(opcompanyid=companyid, oprole='4').first()
        zabbix_query = Zabbix.query.filter_by(companyid=companyid).first()
        zabbix_exist = "false"
        if zabbix_query:
            zabbixid = zabbix_query.zabbixid
            zabbixserver = zabbix_query.zabbixserver
            zabbixuser = zabbix_query.zabbixuser
            zabbixpassword = zabbix_query.zabbixpassword
            zabbix_exist = "true"
        else:
            zabbixid = None
            zabbixserver = None
            zabbixuser = None
            zabbixpassword = None
            zabbix_exist = "true"
        adminusername = adminuser_query.opusername
        defaultcompany = adminuser_query.default
        adminmobile = adminuser_query.opmobile
        companyemail = company_query.companyemail
        companymark = company_query.companymark
        expirestring = ""
        if companyexpire:
            if companyexpire <= expire_date and companyexpire >= todays_datetime and disable == False:
                expirestring = "即将到期"
            elif companyexpire <= expire_date and companyexpire >= todays_datetime and disable == False:
                expirestring = "即将到期"
            elif companyexpire <= todays_datetime and disable== False:
                expirestring = "试用中"
            elif disable == True:
                expirestring = "停用中"
            elif companyexpire > expire_date and disable == False:
                expirestring = "正常使用中"
            companyexpire = int(round(time.mktime(companyexpire.timetuple()) * 1000))
        elif disable == 0 and companyexpire is None:
            expirestring = "试用中"
        elif disable == 1 and companyexpire is None:
            expirestring = "停用中"
        rs_query_dict = {'companyid':companyid, 'companyname': companyname, 'adminusername': adminusername,
          'adminmobile': adminmobile,'adminemail':companyemail,"zabbixid":zabbixid,"zabbixserver":zabbixserver,"zabbixuser":zabbixuser,"zabbixpassword":zabbixpassword,
          'companyexpire': companyexpire,'totalhost':totalhost,"zabbix_exist":zabbix_exist,"disable":disable,
            'companyrole':companyrole, 'members':totalcompanyusers,
                         'companymark':companymark,'defaultcompany':defaultcompany,"expirestring":expirestring
          }
        rs_query_list.append(rs_query_dict)
    db.session.close()
    return {"status":0,"msg":"查询成功",'pagetotal':page_total,"companyinfo": rs_query_list}


def backstagecm(userid, token, urlsearchcompanyname, page):
    if token != '11111':
        return {'status':1, 'msg':'token不可用'}

    searchcompanyname = unquote(urlsearchcompanyname, 'utf-8')
    #公司总数量
    rs_query_list = []
    #companys_query = Company.query.all()
    page = int(page)

    companys_query = Company.query.filter(Company.companyname.like('%' + urlsearchcompanyname + '%')).order_by(Company.createtime.desc()).paginate(page, per_page=15, error_out=False)

    companys_page_query = companys_query.items
    companys_total =  len(companys_page_query) / 15
    page_total = math.ceil(companys_total)

    for company_query in companys_page_query:
        companyid = company_query.companyid
        zabbixhostinfo = zabbix_hosts_query(companyid)
        if zabbixhostinfo['status'] != 2:
            totalhost = len(zabbixhostinfo['totalhosts'])
        else:
            totalhost = None
        companyname = company_query.companyname
        disable = company_query.disable
        companyexpire = company_query.companyexpiredate
        companyrole = company_query.companyrole
        user_query = Opuser.query.filter_by(opcompanyid=companyid).all()
        totalcompanyusers = len(user_query)
        adminuser_query = Opuser.query.filter_by(opcompanyid=companyid, oprole='4').first()
        zabbix_query = Zabbix.query.filter_by(companyid=companyid).first()
        zabbix_exist = "false"
        if zabbix_query:
            zabbixid = zabbix_query.zabbixid
            zabbixserver = zabbix_query.zabbixserver
            zabbixuser = zabbix_query.zabbixuser
            zabbixpassword = zabbix_query.zabbixpassword
            zabbix_exist = "true"
        else:
            zabbixid = None
            zabbixserver = None
            zabbixuser = None
            zabbixpassword = None
            zabbix_exist = "false"
        adminusername = adminuser_query.opusername
        adminmobile = adminuser_query.opmobile
        defaultcompany = adminuser_query.default
        admimemail = company_query.companyemail
        companymark = company_query.companymark

        if companyexpire:
            companyexpire = int(round(time.mktime(companyexpire.timetuple()) * 1000))
        rs_query_dict = {'companyid':companyid, 'companyname': companyname, 'adminusername': adminusername,
                'adminmobile': adminmobile,'adminemail':admimemail,"zabbixid":zabbixid,"zabbixserver":zabbixserver,"zabbixuser":zabbixuser,"zabbixpassword":zabbixpassword,
                'companyexpire': companyexpire,'totalhost':totalhost,"zabbix_exist":zabbix_exist,"disable":disable,
                'companyrole':companyrole, 'members':totalcompanyusers,
                         'companymark': companymark,'defaultcompany':defaultcompany
                }
        rs_query_list.append(rs_query_dict)
    db.session.close()
    return {"status": 0, "msg":"查询成功", 'pagetotal':page_total,"companyinfo": rs_query_list}


#这个接口是我新添的，没有暴露出来
def backstagecm1(userid, token, searchcompanyid, page):
    if token != '11111':
        return {'status':1, 'msg':'token不可用'}

    #公司总数量
    rs_query_list = []
    #companys_query = Company.query.all()
    page = int(page)

    companys_query = Company.query.filter(companyid=searchcompanyid).order_by(Company.createtime.desc()).paginate(page, per_page=15, error_out=False)

    companys_page_query = companys_query.items


    companys_total =  len(companys_page_query) / 15
    page_total = math.ceil(companys_total)

    for company_query in companys_page_query:
        companyid = company_query.companyid
        zabbixhostinfo = zabbix_hosts_query(companyid)
        if zabbixhostinfo['status'] != 2:
            totalhost = len(zabbixhostinfo['totalhosts'])
        else:
            totalhost = None
        companyname = company_query.companyname
        disable = company_query.disable
        companyexpire = company_query.companyexpiredate
        companyrole = company_query.companyrole
        user_query = Opuser.query.filter_by(opcompanyid=companyid).all()
        totalcompanyusers = len(user_query)
        adminuser_query = Opuser.query.filter_by(opcompanyid=companyid, oprole='4').first()
        zabbix_query = Zabbix.query.filter_by(companyid=companyid).first()
        zabbix_exist = "false"
        if zabbix_query:
            zabbixid = zabbix_query.zabbixid
            zabbixserver = zabbix_query.zabbixserver
            zabbixuser = zabbix_query.zabbixuser
            zabbixpassword = zabbix_query.zabbixpassword
            zabbix_exist = "true"
        else:
            zabbixid = None
            zabbixserver = None
            zabbixuser = None
            zabbixpassword = None
            zabbix_exist = "false"
        adminusername = adminuser_query.opusername
        adminuserid = adminuser_query.opuserid
        adminmobile = adminuser_query.opmobile
        defaultcompany = adminuser_query.default
        admimemail = company_query.companyemail
        companymark = company_query.companymark

        if companyexpire:
            companyexpire = int(round(time.mktime(companyexpire.timetuple()) * 1000))
        rs_query_dict = {'companyid':companyid, 'companyname': companyname, 'adminusername': adminusername,'adminuserid':adminuserid,
                'adminmobile': adminmobile,'adminemail':admimemail,"zabbixid":zabbixid,"zabbixserver":zabbixserver,"zabbixuser":zabbixuser,"zabbixpassword":zabbixpassword,
                'companyexpire': companyexpire,'totalhost':totalhost,"zabbix_exist":zabbix_exist,"disable":disable,
                'companyrole':companyrole, 'members':totalcompanyusers,
                         'companymark': companymark,'defaultcompany':defaultcompany
                }
        rs_query_list.append(rs_query_dict)
    db.session.close()
    return {"status": 0, "msg":"查询成功", 'pagetotal':page_total,"companyinfo": rs_query_list}


def backstagetryouts(userid, token, page):
    if token != '11111':
        return {'status':1, 'msg':'token不可用'}
    todays_datetime = datetime(datetime.today().year, datetime.today().month, datetime.today().day)
    #试用公司
    rs_query_list = []
    page = int(page)
    companys_query = Company.query.filter_by(companyexpiredate=None).order_by(Company.createtime.desc()).paginate(page, per_page=15, error_out=False)
    companys_page_query = companys_query.items

    companys_total =  len(companys_page_query) / 15
    page_total = math.ceil(companys_total)

    print(companys_page_query)

    #companys_query = Company.query.filter_by(companyrole='1').all()
    for company_query in companys_page_query:
        companyid = company_query.companyid
        zabbixhostinfo = zabbix_hosts_query(companyid)
        if zabbixhostinfo['status'] != 2:
            totalhost = len(zabbixhostinfo['totalhosts'])
        else:
            totalhost = None
        companyname = company_query.companyname
        disable = company_query.disable
        companyexpire = company_query.companyexpiredate
        companyrole = company_query.companyrole
        # user_query = Opuser.query.filter_by(opcompanyid=companyid).all()
        # totalcompanyusers = len(user_query)
        user_query = Opuser.query.filter(Opuser.opcompanyid==companyid, Opuser.oprole!=2).all()
        totalcompanyusers = int(len(user_query)) - 1
        zabbix_query = Zabbix.query.filter_by(companyid=companyid).first()
        zabbix_exist = "false"
        if zabbix_query:
            zabbixid = zabbix_query.zabbixid
            zabbixserver = zabbix_query.zabbixserver
            zabbixuser = zabbix_query.zabbixuser
            zabbixpassword = zabbix_query.zabbixpassword
            zabbix_exist = "true"
        else:
            zabbixid = None
            zabbixserver = None
            zabbixuser = None
            zabbixpassword = None
            zabbix_exist = "false"

        adminuser_query = Opuser.query.filter_by(opcompanyid=companyid, oprole='4').first()
        adminusername = adminuser_query.opusername
        adminmobile = adminuser_query.opmobile
        admimemail = company_query.companyemail
        defaultcompany = adminuser_query.default
        companymark = company_query.companymark
     
        if companyexpire:
            if companyexpire <= todays_datetime:
                expirestring = "试用公司"
            companyexpire = int(round(time.mktime(companyexpire.timetuple()) * 1000))
        else:
            expirestring = "试用中"
            if disable == True:
                expirestring = "停用中"
        rs_query_dict = {'companyid':companyid, 'companyname': companyname, 'adminusername': adminusername,
          'adminmobile': adminmobile,'adminemail':admimemail,"zabbixid":zabbixid,"zabbixserver":zabbixserver,"zabbixuser":zabbixuser,"zabbixpassword":zabbixpassword,
          'companyexpire': companyexpire,'totalhost':totalhost,"zabbix_exist":zabbix_exist,"disable":disable,
            'companyrole':companyrole, 'members':totalcompanyusers,"expirestring":expirestring,
                         'companymark': companymark,'defaultcompany':defaultcompany
          }
        rs_query_list.append(rs_query_dict)
    db.session.close()
    return {"status": 0, "msg":"查询成功", 'pagetotal':page_total,"companyinfo": rs_query_list}

def backstageexpiring(userid, token, page):
    if token != '11111':
        return {'status':1, 'msg':'token不可用'}

    #即将过期
    todays_datetime = datetime(datetime.today().year, datetime.today().month, datetime.today().day)
    backstage_expiredate_query = Backstage.query.first()
    backstage_expiredate = backstage_expiredate_query.companyexpire
    expire_date = todays_datetime + timedelta(days=int(backstage_expiredate))
    page = int(page)

    try_expire_companys_query_page = Company.query.filter(Company.companyexpiredate <= expire_date, Company.companyexpiredate >= todays_datetime, Company.companyrole == '2').order_by(Company.createtime.desc()).paginate(page, per_page=15, error_out=False)
    try_expire_companys_query = try_expire_companys_query_page.items
    companys_total =  len(try_expire_companys_query) / 15
    page_total = math.ceil(companys_total)


    if try_expire_companys_query is None:
        db.session.close()
        return {"status": 0, "msg":"查询成功", "companyinfo": []}
    rs_query_list = []
    for company_query in try_expire_companys_query:
        companyid = company_query.companyid
        zabbixhostinfo = zabbix_hosts_query(companyid)
        if zabbixhostinfo['status'] != 2:
            totalhost = len(zabbixhostinfo['totalhosts'])
        else:
            totalhost = None
        companyname = company_query.companyname
        disable = company_query.disable
        companyexpire = company_query.companyexpiredate
        companyrole = company_query.companyrole
        #user_query = Opuser.query.filter_by(opcompanyid=companyid).all()
        #totalcompanyusers = len(user_query)
        user_query = Opuser.query.filter(Opuser.opcompanyid==companyid, Opuser.oprole!=2).all()
        totalcompanyusers = int(len(user_query)) - 1
        adminuser_query = Opuser.query.filter_by(opcompanyid=companyid, oprole='4').first()
        adminusername = adminuser_query.opusername
        adminmobile = adminuser_query.opmobile
        admimemail = company_query.companyemail
        defaultcompany = adminuser_query.default
        companymark = company_query.companymark

        if companyexpire:
            companyexpire = int(round(time.mktime(companyexpire.timetuple()) * 1000))
        rs_query_dict = {'companyid':companyid, 'companyname': companyname, 'adminusername': adminusername,
          'adminmobile': adminmobile,'adminemail':admimemail,"disable":disable,
          'companyexpire': companyexpire,'totalhost':totalhost,
            'companyrole':companyrole, 'members':totalcompanyusers,
                         'companymark': companymark,'defaultcompany':defaultcompany
          }
        rs_query_list.append(rs_query_dict)
    db.session.close()
    return {"status": 0, "msg":"查询成功",'pagetotal':page_total, "companyinfo": rs_query_list}


def backstageexpired(userid, token, page):
    if token != '11111':
        return {'status':1, 'msg':'token不可用'}
    #已过期
    page = int(page)
    todays_datetime = datetime(datetime.today().year, datetime.today().month, datetime.today().day)
    try_expire_companys_query_page = Company.query.filter(Company.companyexpiredate <= todays_datetime, Company.companyrole == '2').order_by(Company.createtime.desc()).paginate(page, per_page=15, error_out=False)
    try_expire_companys_query = try_expire_companys_query_page.items
    companys_total =  len(try_expire_companys_query) / 15
    page_total = math.ceil(companys_total)

    if try_expire_companys_query is None:
        db.session.close()
        return {"status": 0, "msg": "查询成功", "companyinfo": []}
    rs_query_list = []
    for company_query in try_expire_companys_query:
        companyid = company_query.companyid
        zabbixhostinfo = zabbix_hosts_query(companyid)
        if zabbixhostinfo['status'] != 2:
            totalhost = len(zabbixhostinfo['totalhosts'])
        else:
            totalhost = None
        companyname = company_query.companyname
        disable = company_query.disable
        companyexpire = company_query.companyexpiredate
        companyrole = company_query.companyrole
        #user_query = Opuser.query.filter_by(opcompanyid=companyid).all()
        #totalcompanyusers = len(user_quer
        user_query = Opuser.query.filter(Opuser.opcompanyid==companyid, Opuser.oprole!=2).all()
        totalcompanyusers = int(len(user_query)) - 1
        adminuser_query = Opuser.query.filter_by(opcompanyid=companyid, oprole='4').first()
        adminusername = adminuser_query.opusername
        adminmobile = adminuser_query.opmobile
        defaultcompany = adminuser_query.default
        admimemail = company_query.companyemail
        companymark = company_query.companymark

        if companyexpire:
            companyexpire = int(round(time.mktime(companyexpire.timetuple()) * 1000))
        rs_query_dict = {'companyid':companyid, 'companyname': companyname, 'adminusername': adminusername,
          'adminmobile': adminmobile,'adminemail':admimemail,"disable":disable,
          'companyexpire': companyexpire,'totalhost':totalhost,
            'companyrole':companyrole, 'members':totalcompanyusers,
                         'companymark': companymark,'defaultcompany':defaultcompany
          }
        rs_query_list.append(rs_query_dict)
        db.session.close()
        return {"status": 0, "msg": "查询成功",'pagetotal':page_total, "companyinfo": rs_query_list}

def backstagenewcompanytoday(userid, token, page):
    if token != '11111':
        return {'status':1, 'msg':'token不可用'}

    #即将过期
    todays_datetime = datetime(datetime.today().year, datetime.today().month, datetime.today().day)
    print(todays_datetime)
    page = int(page)

    try_expire_companys_query_page = Company.query.filter(Company.createtime >= todays_datetime).order_by(Company.createtime.desc()).paginate(page, per_page=15, error_out=False)
    try_expire_companys_query = try_expire_companys_query_page.items
    companys_total =  len(try_expire_companys_query) / 15
    page_total = math.ceil(companys_total)

    if try_expire_companys_query is None:
        db.session.close()
        return {"status": 0, "msg":"查询成功", "companyinfo": []}
    rs_query_list = []
    for company_query in try_expire_companys_query:
        companyid = company_query.companyid
        zabbixhostinfo = zabbix_hosts_query(companyid)
        if zabbixhostinfo['status'] != 2:
            totalhost = len(zabbixhostinfo['totalhosts'])
        else:
            totalhost = None
        companyname = company_query.companyname
        disable = company_query.disable
        companyexpire = company_query.companyexpiredate
        companyrole = company_query.companyrole
        companyemail = company_query.companyemail
        user_query = Opuser.query.filter_by(opcompanyid=companyid).all()
        totalcompanyusers = len(user_query)
        adminuser_query = Opuser.query.filter_by(opcompanyid=companyid, oprole='4').first()
        adminusername = adminuser_query.opusername
        adminmobile = adminuser_query.opmobile
        admimemail = company_query.companyemail
        defaultcompany = adminuser_query.default
        companymark = company_query.companymark
        expirestring = ""
        if companyexpire:
            if companyexpire <= expire_date and companyexpire >= todays_datetime and disable == False:
                expirestring = "即将到期"
            elif companyexpire <= expire_date and companyexpire >= todays_datetime and disable == False:
                expirestring = "即将到期"
            elif companyexpire <= todays_datetime and disable== False:
                expirestring = "试用中"
            elif disable == True:
                expirestring = "停用中"
            elif companyexpire > expire_date and disable == False:
                expirestring = "正常使用中"
            companyexpire = int(round(time.mktime(companyexpire.timetuple()) * 1000))
        elif disable == 0 and companyexpire is None:
            expirestring = "试用中"
        elif disable == 1 and companyexpire is None:
            expirestring = "停用中"
        rs_query_dict = {'companyid':companyid, 'companyname': companyname, 'adminusername': adminusername,
          'adminmobile': adminmobile,'adminemail':admimemail,"companyemail":companyemail,
          'companyexpire': companyexpire,'totalhost':totalhost,"expirestring":expirestring,"disable":disable,
            'companyrole':companyrole, 'members':totalcompanyusers,
                         'companymark': companymark,'defaultcompany':defaultcompany
          }
        rs_query_list.append(rs_query_dict)
    db.session.close()
    return {"status": 0, "msg":"查询成功", 'pagetotal':page_total,"companyinfo": rs_query_list}

def companymemberinfo(adminuserid, token, page, searchcompanyname):
    if token != '11111':
        return {'status':1, 'msg':'token不可用'}
    #所有用户信息
    page = int(page)
    search_companyid_list = []
    companys_query_page = Company.query.filter(Company.companyname.like('%' + searchcompanyname + '%')).order_by(
        Company.createtime.desc()).paginate(page, per_page=20, error_out=False)
    companys_query = companys_query_page.items
    companys_total =  len(companys_query) / 15
    page_total = math.ceil(companys_total)

    for company_query in companys_query:
        search_company_dict = {}
        search_company_dict['companyid'] = company_query.companyid
        search_company_dict['companyname'] = company_query.companyname

        search_companyid_list.append(search_company_dict)

    search_opuserid_list = []
    for searchcompanyidinfo in search_companyid_list:

        opusers_query = Opuser.query.filter_by(opcompanyid=searchcompanyidinfo['companyid']).all()
        for opuser_query in opusers_query:
            searchopuserid = opuser_query.opuserid
            searchopuserrole = opuser_query.oprole
            userstatus = opuser_query.userstatus
            if searchopuserrole != '5' and searchopuserrole != '2' and searchopuserid:
                searchopuser_dict = {
                            "companyname": searchcompanyidinfo['companyname'],
                            "userallinfo": {
                                "userid": searchopuserid,
                                "oprole": searchopuserrole,
                                "userstatus": userstatus,
                                    }
                                }
                search_opuserid_list.append(searchopuser_dict)
    lastuserinfo_list = []
    print(search_opuserid_list)
    for useridinfo in search_opuserid_list:

        queryuserid = useridinfo['userallinfo']['userid']
        userinfo_query = User.query.filter_by(userid=queryuserid).first()
        if userinfo_query:
            username = userinfo_query.username
            usermobile = userinfo_query.mobile
            userlogintime = userinfo_query.logintime
            if userlogintime:
                userlogintime = int(round(time.mktime(userlogintime.timetuple()) * 1000))
            userrole = userinfo_query.role
        useridinfo['userallinfo']['username'] = username
        useridinfo['userallinfo']['mobile'] = usermobile
        useridinfo['userallinfo']['logintime'] = userlogintime
        useridinfo['userallinfo']['role'] = userrole

        lastuserinfo_list.append(useridinfo)
    db.session.close()
    return {"status":0, "msg": "查询成功", 'pagetotal':page_total,"userinfo": lastuserinfo_list}

def companyhostsinfo(adminuserid, token, page, companyname):
    if token != '11111':
        return {'status': 1, 'msg': 'token不可用'}
    else:
        companyid_query = Company.query.filter_by(companyname=companyname).first()

        if companyid_query is None:
            db.session.close()
            return {'status': 2, 'msg': '未找到相关公司'}
        companyid = companyid_query.companyid
        zabbixinfo_query = Zabbix.query.filter_by(companyid=companyid).first()
        if zabbixinfo_query is None:
            db.session.close()
            return {'status': 3, 'msg': '使用监控功能之前，需要先添加zabbix服务器'}
        zabbixusername = zabbixinfo_query.zabbixuser
        zabbixpassword = zabbixinfo_query.zabbixpassword
        zabbixurl = zabbixinfo_query.zabbixserver
        zabbixtoken = auth(zabbixusername, zabbixpassword, zabbixurl)

        group_list = hostgroups(zabbixtoken, zabbixurl)
        print(group_list)
        hostinfo_list = []
        for group in group_list:
            # hostinfo_dict = {}
            hostinfo_list.append(group['groupid'])
            # groupid = group['groupid']
            # groupname = group['name']
        print(hostinfo_list)
        data = json.dumps(
            {
                "jsonrpc": "2.0",
                "method": "host.get",
                "params": {
                    "output": ["hostid", "name", "host"],
                    "groupids": hostinfo_list,
                },
                "auth": zabbixtoken,  # theauth id is what auth script returns, remeber it is string
                "id": 1,
            })
        hosts = requests.post(zabbixurl + '/zabbix/api_jsonrpc.php', data=data, headers=headers)
        hosts_list = hosts.json()['result']
        checkhosts_list = []
        for checkhost_dict in hosts_list:

            checkhostid = checkhost_dict['hostid']
            checkhost_query = Monitor.query.filter_by(zabbixhostid=checkhostid).first()
            if checkhost_query:
                checkhost_dict['hoststatus'] = 'in'
            else:
                checkhost_dict['hoststatus'] = 'out'
            checkhosts_list.append(checkhost_dict)

        allhostsnumber = len(checkhosts_list)
        pagetotal = len(checkhosts_list)/5
        if pagetotal == 0:
            pagetotal = 1
        inhostsnumber_query = Monitor.query.all()
        inhostsnumber = len(inhostsnumber_query)
        inhostinfo_list = []
        for inhost in inhostsnumber_query:
            inhostinfo_dict = {'hostid': inhost.zabbixhostid, 'host': inhost.zabbixhostip,
                               'name': inhost.zabbixhostname, 'hoststatus': 'in'}
            inhostinfo_list.append(inhostinfo_dict)

        hosts_queryrs = {'status': 0, 'totalamount': allhostsnumber,
                         'inamount': inhostsnumber, 'totalhosts': checkhosts_list,"pagetotal":pagetotal,
                         }
        db.session.close()
        return hosts_queryrs


def companyexpire(adminuserid, token, companyname, time_chuo):
    if token != '11111':
        return {'status': 1, 'msg': 'token不可用'}
    else:
        companyid_query = Company.query.filter_by(companyname=companyname).first()

        if companyid_query is None:
            db.session.close()
            return {'status': 2, 'msg': '未找到相关公司'}
        else:
            time_chuo_zhuan = int(time_chuo) / 1000
            userinfologintime = time.localtime(time_chuo_zhuan)
            userinfologintime_dt = time.strftime("%Y-%m-%d %H:%M:%S", userinfologintime)
            companyid_query.companyexpiredate = userinfologintime_dt
            companyid_query.companyrole = 2
            db.session.commit()
            db.session.close()
            return {'status': 0, 'msg': '修改成功'}

def companypatch(userid, usertoken,oldcompanyname, newcompanyname,companyemail, mark, disable):
    if usertoken != '11111':
        return {'status': 1, 'msg': 'token不可用'}
    else:
        companyid_query = Company.query.filter_by(companyname=oldcompanyname).first()

        if companyid_query is None:
            db.session.close()
            return {'status': 2, 'msg': '未找到相关公司'}
        else:
            companyid_query.companyname = newcompanyname
            companyid_query.companyemail = companyemail
            #if len(companyemail) == 0:
            if companyemail is None:
                return {'status': 4, 'msg': '邮箱输入为空，请重新输入！！！'}
            elif re.match(r'^[0-9a-zA-Z_]{0,19}@[0-9a-zA-Z]{1,13}\.[com,cn,net]{1,3}$', companyemail) is None:
                return {'status': 3, 'msg': '您输入的邮箱地址无效，请重新输入！！！'}
            companyid_query.companymark = mark
            #companyid_query.companyrole = 2
            companyid_query.disable = disable
            #这个地方注意一下
            """
            opusers_query = Opuser.query.filter_by(opcompanyid=companyid_query.companyid).all()
            for opuser in opusers_query:
               user_query = User.query.filter_by(userid=opuser.opuserid)
               if disable == 0:
                   user_query.role = '0'
               elif disable == 1:
                   user_query.role = '1'
            """
            opusers_query = Opuser.query.filter_by(opcompanyid=companyid_query.companyid).all()
            for opuser in opusers_query:
               opuserid = opuser.opuserid
               companys = Opuser.query.filter(opuserid==opuserid,disable==0,Opuser.opcompanyid!=companyid_query.companyid).all()               

               if companys:
                   user_query = User.query.filter_by(userid=opuser.opuserid)
                   if disable == 0:
                       user_query.role = '0'
                   elif disable == 1:
                       user_query.role = '0'
               else:
                   user_query = User.query.filter_by(userid=opuser.opuserid)
                   if disable == 0:
                       user_query.role = '0'
                   elif disable == 1:
                       user_query.role = '1'
            if disable == 0:
                opusers_query = Opuser.query.filter_by(opcompanyid=companyid_query.companyid).all()
                for opuser in opusers_query:
                    user_query = User.query.filter_by(userid=opuser.opuserid).first()
                    user_query.role = '0'
            db.session.commit()
            db.session.close()
            expirestring = ""

            if newcompanyname != None and newcompanyname !="":
                todays_datetime = datetime(datetime.today().year, datetime.today().month, datetime.today().day)
                backstage_expiredate_query = Backstage.query.first()
                backstage_expiredate = backstage_expiredate_query.companyexpire
                expire_date = todays_datetime + timedelta(days=int(backstage_expiredate))
                company_query = Company.query.filter_by(companyname=newcompanyname).first()
                companyname = company_query.companyname
                disable = company_query.disable
                companyexpire = company_query.companyexpiredate
                companyrole = company_query.companyrole
                companyemail = company_query.companyemail
                companyid = company_query.companyid
                adminuser_query = Opuser.query.filter_by(opcompanyid=companyid, oprole='4').first()
                adminusername = adminuser_query.opusername
                adminmobile = adminuser_query.opmobile
                admimemail = company_query.companyemail
                defaultcompany = adminuser_query.default
                companymark = company_query.companymark
                expirestring = ""
                if companyexpire:
                    if companyexpire <= expire_date and companyexpire >= todays_datetime and disable == False:
                        expirestring = "即将到期"
                    elif companyexpire <= expire_date and companyexpire >= todays_datetime and disable == False:
                        expirestring = "即将到期"
                    elif companyexpire <= todays_datetime and disable== False:
                        expirestring = "试用中"
                    elif disable == True:
                        expirestring = "停用中"
                    elif companyexpire > expire_date and disable == False:
                        expirestring = "正常使用中"
                    companyexpire = int(round(time.mktime(companyexpire.timetuple()) * 1000))
                elif disable == 0 and companyexpire is None:
                    expirestring = "试用中"
                elif disable == 1 and companyexpire is None:
                    expirestring = "停用中"

                rs_query_dict = {'companyid':companyid, 'companyname': companyname, 'adminusername': adminusername,
                                'adminmobile': adminmobile,'adminemail':admimemail,"companyemail":companyemail,
                                'companyexpire': companyexpire,"disable":disable,
                                'companyrole':companyrole,"expirestring":expirestring,
                                'companymark': companymark,'defaultcompany':defaultcompany }
            else:
                todays_datetime = datetime(datetime.today().year, datetime.today().month, datetime.today().day)
                backstage_expiredate_query = Backstage.query.first()
                backstage_expiredate = backstage_expiredate_query.companyexpire
                expire_date = todays_datetime + timedelta(days=int(backstage_expiredate))
                company_query = Company.query.filter_by(companyname=oldcompanyname).first()
                companyname = company_query.companyname
                disable = company_query.disable
                companyexpire = company_query.companyexpiredate
                companyrole = company_query.companyrole
                companyemail = company_query.companyemail
                companyid = company_query.companyid
                adminuser_query = Opuser.query.filter_by(opcompanyid=companyid, oprole='4').first()
                adminusername = adminuser_query.opusername
                adminmobile = adminuser_query.opmobile
                admimemail = company_query.companyemail
                defaultcompany = adminuser_query.default
                companymark = company_query.companymark
                expirestring = ""
                if companyexpire:
                    if companyexpire <= expire_date and companyexpire >= todays_datetime and disable == False:
                        expirestring = "即将到期"
                    elif companyexpire <= expire_date and companyexpire >= todays_datetime and disable == False:
                        expirestring = "即将到期"
                    elif companyexpire <= todays_datetime and disable== False:
                        expirestring = "试用中"
                    elif disable == True:
                        expirestring = "停用中"
                    elif companyexpire > expire_date and disable == False:
                        expirestring = "正常使用中"
                    companyexpire = int(round(time.mktime(companyexpire.timetuple()) * 1000))
                elif disable == 0 and companyexpire is None:
                    expirestring = "试用中"
                elif disable == 1 and companyexpire is None:
                    expirestring = "停用中"

                rs_query_dict = {'companyid':companyid, 'companyname': companyname, 'adminusername': adminusername,
                                'adminmobile': adminmobile,'adminemail':admimemail,"companyemail":companyemail,
                                'companyexpire': companyexpire,"disable":disable,
                                'companyrole':companyrole,"expirestring":expirestring,
                                'companymark': companymark,'defaultcompany':defaultcompany }
            return {'status': 0, 'msg': '修改成功',"companyinfo":rs_query_dict}

def companydelete(userid, usertoken,companyname):
    if usertoken != '11111':
        return {'status': 1, 'msg': 'token不可用'}
    company_query = Company.query.filter_by(companyname=companyname).first()
    opusers_query = Opuser.query.filter_by(opcompanyid=company_query.companyid).all()
    topic_query = Topic.query.filter_by(companyid=company_query.companyid).all()
    for opuser in opusers_query:
        companys_query = Opuser.query.filter_by(opuserid=opuser.opuserid).all()
        if len(companys_query) == 1:
            user_query = User.query.filter_by(userid=opuser.opuserid).first()
            user_query.role = 1
        db.session.delete(opuser)
    db.session.delete(company_query)
    for tmp in topic_query:
        db.session.delete(tmp)
        db.session.commit()
    db.session.commit()
    db.session.close()
    return {'status': 0, 'msg': '删除成功'}

def generate_random_str(randomlength=16):
    """
    生成一个指定长度的随机字符串，其中
    string.digits=0123456789
    string.ascii_letters=abcdefghigklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ
    """
    str_list = [random.choice(string.digits + string.ascii_letters) for i in range(randomlength)]
    random_str = ''.join(str_list)
    return random_str

"""
def zabbixserver_update(userid, usertoken, companyid, zabbixid, zabbixserver, zabbixusername, zabbixpassword):
    try:
        if usertoken != '11111':
            return {'status':1, 'msg': 'token不可用'}

        #adminuserinfo_query =Opuser.query.filter_by(opuserid=userid).first()
        #adminuserrole = adminuserinfo_query.oprole
        #if adminuserrole != '4':
            #return {'status': 2, 'msg': '没有权限'}

        zabbixinfo_query = Zabbix.query.filter_by(companyid=companyid).first()
        if zabbixinfo_query:
            zabbixinfo_query.zabbixid = zabbixid
            zabbixinfo_query.zabbixserver = zabbixserver
            zabbixinfo_query.zabbixusername = zabbixusername
            zabbixinfo_query.zabbixpassword = zabbixpassword
            db.session.commit()
            return {'status':0, 'msg': '修改成功'}
        else:
            zabbixserverid = 'z' + generate_random_str()
            insert_zabbixserver = Zabbix(companyid=companyid, zabbixid=zabbixserverid,
                                         zabbixserver=zabbixserver, zabbixuser=zabbixusername,
                                         zabbixpassword=zabbixpassword)
            db.session.add(insert_zabbixserver)
            db.session.commit()
            return {'status': 0, 'msg': '添加成功'}
    except sqlalchemy.exc.OperationalError:
        return {'status': 3, 'Oooops': '数据库连接出现错误'}
"""

def zabbixserver_update(userid, usertoken, companyid, zabbixid, zabbixserver, zabbixusername, zabbixpassword):
    try:
        if usertoken != '11111':
            return {'status':1, 'msg': 'token不可用'}

        #adminuserinfo_query =Opuser.query.filter_by(opuserid=userid).first()
        #adminuserrole = adminuserinfo_query.oprole
        #if adminuserrole != '4':
            #return {'status': 2, 'msg': '没有权限'}

        zabbixinfo_query = Zabbix.query.filter_by(companyid=companyid).first()
        if zabbixinfo_query:
            zabbixinfo_query.zabbixid = zabbixid
            zabbixinfo_query.zabbixserver = zabbixserver
            zabbixinfo_query.zabbixusername = zabbixusername
            zabbixinfo_query.zabbixpassword = zabbixpassword

            data = json.dumps(
                {
                    "jsonrpc": "2.0",
                    "method": "user.login",
                    "params": {
                        "user": zabbixusername,
                        "password": zabbixpassword
                    },
                    "id": 0
                })
            try: 
                authrs = requests.post(zabbixserver + '/zabbix/api_jsonrpc.php', data=data, headers=headers)
            except Exception as e:
                db.session.close()
                return {'status':4, 'msg':"zabbix服务器地址配置不正确"}
            if authrs.status_code == 200:
                db.session.commit()
                return {'status': 0, 'msg': '修改成功'}
            else:
                db.session.close()
                return {'status':4, 'msg':"zabbix服务器地址配置不正确"}



        else:
            data = json.dumps(
                {
                    "jsonrpc": "2.0",
                    "method": "user.login",
                    "params": {
                        "user": zabbixusername,
                        "password": zabbixpassword
                    },
                    "id": 0
                })

            authrs = requests.post(zabbixserver + '/zabbix/api_jsonrpc.php', data=data, headers=headers)
            if authrs.status_code == 200:
                zabbixserverid = 'z' + generate_random_str()
                insert_zabbixserver = Zabbix(companyid=companyid, zabbixid=zabbixserverid,
                                             zabbixserver=zabbixserver, zabbixuser=zabbixusername,
                                             zabbixpassword=zabbixpassword)
                db.session.add(insert_zabbixserver)
                db.session.commit()
                return {'status': 0, 'msg': '添加成功'}
            else:
                db.session.close()
                return {'status': 4, 'msg': "zabbix服务器地址配置不正确"}


    except sqlalchemy.exc.OperationalError:
        return {'status': 3, 'Oooops': '数据库连接出现错误'}
