from model import *
from datetime import datetime
import time
import math



"""
def backstageusers(adminuserid, token, page):
    if token != '11111':
        return {'status':1, 'msg':'token不可用'}

    #所有用户信息
    page = int(page)
    rs_query_list = []

    users_query_page = User.query.filter(User.mobile.like('1%')).order_by(User.createtime.desc()).paginate(page, per_page=20, error_out=False)
    users_query = users_query_page.items
    #users_total =  len(users_query) / 15
    users_query_total = User.query.filter(User.mobile.like('1%')).order_by(User.createtime.desc()).all()
    users_total =  len(users_query_total) / 15
    page_total = math.ceil(users_total)
    for user_query in users_query:
        userid = user_query.userid
        username = user_query.username
        usermobile = user_query.mobile
        userrole = user_query.role
        mark = user_query.mark
        userlogintime = user_query.logintime
        if userlogintime:
            userlogintime = int(round(time.mktime(userlogintime.timetuple()) * 1000))

        if username != 'chatbot' or usermobile.find('c') == -1:
            rs_query_dict = {'username': username, 'mobile': usermobile,
                'role': userrole,'logintime':userlogintime,'userid':userid,
                'mark':mark
                }
            rs_query_list.append(rs_query_dict)
    userinfo_list = []


    for userallinfo in rs_query_list:
        userinfo_dict = {}
        queryuserid = userallinfo['userid']
        companyinfos_query = Opuser.query.filter_by(opuserid=queryuserid).all()
        companyid_list = []
        for companyinfo_query in companyinfos_query:
            companyid = companyinfo_query.opcompanyid
            companyid_list.append(companyid)
        companyname_list = []
        for companyid in companyid_list:
            companyinfos_query = Company.query.filter_by(companyid=companyid).first()
            if companyinfos_query:
                companyname = companyinfos_query.companyname
                companyname_list.append(companyname)
        userinfo_dict['companynamelist'] = companyname_list
        userinfo_dict['userinfo'] = userallinfo
        userinfo_list.append(userinfo_dict)
    print(userinfo_list)


    userallinfo_list = []
    for userinfo in userinfo_list:
        userallinfo_dict = {}
        companyname_list = userinfo['companynamelist']
        userallinfo = userinfo['userinfo']
        if companyname_list:
            pass
        else:
            companyname_list = ['未关联公司']

        for companyname in companyname_list:
            userallinfo_dict['companyname'] = companyname
            userallinfo_dict['userallinfo'] = userallinfo

        userallinfo_list.append(userallinfo_dict)


    print(len(userallinfo_list))
    print(userallinfo_list)
    db.session.close()
    return {"status":0, "msg": "查询成功",'pagetotal':page_total, "userinfo": userallinfo_list}


def backstageusers(adminuserid, token, page):
    if token != '11111':
        return {'status':1, 'msg':'token不可用'}

    #所有用户信息
    page = int(page)
    rs_query_list = []

    users_query_page = User.query.filter(User.mobile.like('1%')).order_by(User.createtime.desc()).paginate(page, per_page=20, error_out=False)
    users_query = users_query_page.items
    #users_total =  len(users_query) / 15
    users_query_total = User.query.filter(User.mobile.like('1%')).order_by(User.createtime.desc()).all()
    users_total =  len(users_query_total) / 15
    page_total = math.ceil(users_total)
    for user_query in users_query:
        userid = user_query.userid
        username = user_query.username
        usermobile = user_query.mobile
        userrole = user_query.role
        mark = user_query.mark
        userlogintime = user_query.logintime
        if userlogintime:
            userlogintime = int(round(time.mktime(userlogintime.timetuple()) * 1000))

        if username != 'chatbot' or usermobile.find('c') == -1:
            rs_query_dict = {'username': username, 'mobile': usermobile,
                'role': userrole,'logintime':userlogintime,'userid':userid,
                'mark':mark
                }
            rs_query_list.append(rs_query_dict)
            
    userallinfo_list = []

    for userallinfo in rs_query_list:
        #userinfo_dict = {}
        queryuserid = userallinfo['userid']
        opuserinfos_query = Opuser.query.filter_by(opuserid=queryuserid).all()

        if opuserinfos_query:
            for opuserinfo in opuserinfos_query:
                userinfo_dict = {}
                companyid = opuserinfo.opcompanyid
                companyinfo = Company.query.filter_by(companyid=companyid).first()
               # 运维用户状态
                company_user_status = opuserinfo.company_user_status
                
                # 修改用户的 mark 字段、设置成运维用户的状态、前端取的是mark 这样前端就不用修改了。
                # begin
                if company_user_status:
                    if company_user_status == '3':
                        userallinfo['mark'] = 'userenabled'
                    elif company_user_status == '4':
                         userallinfo['mark'] = 'userdisabled'
                # end

                if companyinfo:
                    companyname = companyinfo.companyname
                    companyid = companyinfo.companyid
                    if companyid:
                        userinfo_dict["companyid"] = companyid
                    else:
                        userinfo_dict["companyid"] = ''
                    userinfo_dict["companyname"] = companyname
                    userinfo_dict["userallinfo"] = userallinfo
                    userallinfo_list.append(userinfo_dict)

        else:
            userinfo_dict = {}
            companyname = "未关联公司"
            userinfo_dict["companyid"] = ''
            userinfo_dict["companyname"] = companyname
            userinfo_dict["userallinfo"] = userallinfo
            userallinfo_list.append(userinfo_dict)


    print(userallinfo_list)


    print(len(userallinfo_list))
    db.session.close()
    return {"status":0, "msg": "查询成功",'pagetotal':page_total, "userinfo": userallinfo_list}
"""

def backstageusers(adminuserid, token, page):
    if token != '11111':
        return {'status':1, 'msg':'token不可用'}

    #所有用户信息
    page = int(page)
    rs_query_list = []

    users_query_page = User.query.filter(User.mobile.like('1%')).order_by(User.createtime.desc()).paginate(page, per_page=20, error_out=False)
    users_query = users_query_page.items
    #users_total =  len(users_query) / 15
    users_query_total = User.query.filter(User.mobile.like('1%')).order_by(User.createtime.desc()).all()
    users_total =  len(users_query_total) / 15
    page_total = math.ceil(users_total)
    for user_query in users_query:
        userid = user_query.userid
        username = user_query.username
        usermobile = user_query.mobile
        userrole = user_query.role
        mark = user_query.mark
        userlogintime = user_query.logintime
        if userlogintime:
            userlogintime = int(round(time.mktime(userlogintime.timetuple()) * 1000))

        if username != 'chatbot' or usermobile.find('c') == -1:
            rs_query_dict = {'username': username, 'mobile': usermobile,
                'role': userrole,'logintime':userlogintime,'userid':userid,
                'mark':mark
                }
            rs_query_list.append(rs_query_dict)
    userinfo_list = []

    for userallinfo in rs_query_list:
        userinfo_dict = {}
        queryuserid = userallinfo['userid']
        companyinfos_query = Opuser.query.filter_by(opuserid=queryuserid).all()
        companyid_list = []
        for companyinfo_query in companyinfos_query:
            companyid = companyinfo_query.opcompanyid
            companyid_list.append(companyid)
        companyname_list = []
        companyid_list = []
        for companyid in companyid_list:
            companyinfos_query = Company.query.filter_by(companyid=companyid).first()
            if companyinfos_query:
                companyname = companyinfos_query.companyname
                companyname_list.append(companyname)
                companyid_list.append(companyinfos_query.companyid)
                
                opuserinfo = Opuser.query.filter_by(opuserid=queryuserid,opcompanyid=companyinfos_query.companyid).first()
                # 运维用户状态
                company_user_status = opuserinfo.company_user_status
                # 修改用户的 mark 字段、设置成运维用户的状态、前端取的是mark 这样前端就不用修改了。
                # begin
                if company_user_status:
                    if company_user_status == '3':
                        userallinfo['mark'] = 'userenabled'
                    elif company_user_status == '4':
                        userallinfo['mark'] = 'userdisabled'
                # end
                
        userinfo_dict['companyidlist'] = companyid_list
        userinfo_dict['companynamelist'] = companyname_list
        userinfo_dict['userinfo'] = userallinfo
        userinfo_list.append(userinfo_dict)

    userallinfo_list = []
    for userinfo in userinfo_list:
        userallinfo_dict = {}
        companyname_list = userinfo['companynamelist']
        companyid_list = userinfo['companyidlist']
        userallinfo = userinfo['userinfo']
        if companyname_list:
            pass
        else:
            companyname_list = ['未关联公司']
        
        for companyname in companyname_list:
            userallinfo_dict['companyname'] = companyname
            userallinfo_dict['userallinfo'] = userallinfo
        
        for companyid in companyid_list:
            userallinfo_dict['companyid'] = companyid
        userallinfo_list.append(userallinfo_dict)


    print(len(userallinfo_list))
    db.session.close()
    return {"status":0, "msg": "查询成功",'pagetotal':page_total, "userinfo": userallinfo_list}

def backstagenewusers(adminuserid, token, page):
    if token != '11111':
        return {'status':1, 'msg':'token不可用'}

    #所有用户信息
    todays_datetime = datetime(datetime.today().year, datetime.today().month, datetime.today().day)
    print(todays_datetime)
    page = int(page)
    rs_query_list = []

    users_query_page = User.query.filter(User.mobile.like('1%'), User.createtime >= todays_datetime).order_by(User.createtime.desc()).paginate(page, per_page=20, error_out=False)
    users_query = users_query_page.items
    #users_total =  len(users_query) / 15
    users_query_total = User.query.filter(User.mobile.like('1%'), User.createtime >= todays_datetime).order_by(User.createtime.desc()).all()
    users_total =  len(users_query_total) / 15
    page_total = math.ceil(users_total)
    for user_query in users_query:
        userid = user_query.userid
        username = user_query.username
        usermobile = user_query.mobile
        userrole = user_query.role
        mark = user_query.mark
        userlogintime = user_query.logintime
        if userlogintime:
            userlogintime = int(round(time.mktime(userlogintime.timetuple()) * 1000))
        if username != 'chatbot' or usermobile.find('c') == -1:
            rs_query_dict = {'username': username, 'mobile': usermobile,
                'role': userrole,'logintime':userlogintime,'userid':userid,
                'mark':mark
                }
            rs_query_list.append(rs_query_dict)
    """
    userinfo_list = []
    for userallinfo in rs_query_list:
        userinfo_dict = {}
        queryuserid = userallinfo['userid']
        companyinfos_query = Opuser.query.filter_by(opuserid=queryuserid).all()
        companyid_list = []
        for companyinfo_query in companyinfos_query:
            companyid = companyinfo_query.opcompanyid
            companyid_list.append(companyid)
        companyname_list = []
        for companyid in companyid_list:
            companyinfos_query = Company.query.filter_by(companyid=companyid).first()
            companyname = companyinfos_query.companyname
            companyname_list.append(companyname)
        userinfo_dict['companynamelist'] = companyname_list
        userinfo_dict['userinfo'] = userallinfo
        userinfo_list.append(userinfo_dict)
   
    userallinfo_list = []
    for userinfo in userinfo_list:

        userallinfo_dict = {}
        companyname_list = userinfo['companynamelist']
        userallinfo = userinfo['userinfo']
        if companyname_list:
            pass
        else:
            companyname_list = ['未关联公司']

        for companyname in companyname_list:
            userallinfo_dict['companyname'] = companyname
            userallinfo_dict['userallinfo'] = userallinfo

        userallinfo_list.append(userallinfo_dict)
    """
    userallinfo_list = []

    for userallinfo in rs_query_list:
        #userinfo_dict = {}
        queryuserid = userallinfo['userid']
        opuserinfos_query = Opuser.query.filter_by(opuserid=queryuserid).all()

        if opuserinfos_query:
            for opuserinfo in opuserinfos_query:
                userinfo_dict = {}
                companyid = opuserinfo.opcompanyid
                companyinfo = Company.query.filter_by(companyid=companyid).first()
                if companyinfo:
                    companyname = companyinfo.companyname
                    userinfo_dict["companyname"] = companyname
                    userinfo_dict["userallinfo"] = userallinfo
                    userallinfo_list.append(userinfo_dict)

        else:
            userinfo_dict = {}
            companyname = "未关联公司"
            userinfo_dict["companyname"] = companyname
            userinfo_dict["userallinfo"] = userallinfo
            userallinfo_list.append(userinfo_dict)

    print(len(userallinfo_list))
    db.session.close()
    return {"status":0, "msg": "查询成功",'pagetotal':page_total, "userinfo": userallinfo_list}

"""
def backstagesearchusersmobile(adminuserid, token, page, mobile):
    if token != '11111':
        return {'status':1, 'msg':'token不可用'}

    #所有用户信息
    page = int(page)
    rs_query_list = []
    users_query_page = User.query.filter(User.mobile.like('%' + mobile + '%')).order_by(
        User.createtime.desc()).paginate(page, per_page=20, error_out=False)
    users_query = users_query_page.items
    users_query1 = User.query.filter(User.mobile.like('%' + mobile + '%')).order_by(User.createtime.desc()).all()
    users_total =  len(users_query1) / 15
    page_total = math.ceil(users_total)
    for user_query in users_query:
        userid = user_query.userid
        username = user_query.username
        usermobile = user_query.mobile
        userrole = user_query.role
        mark = user_query.mark
        userlogintime = user_query.logintime
        if userlogintime:
            userlogintime = int(round(time.mktime(userlogintime.timetuple()) * 1000))
        if username != 'chatbot' or usermobile.find('c') == -1:
            rs_query_dict = {'username': username, 'mobile': usermobile,
                             'role': userrole, 'logintime': userlogintime, 'userid': userid,
                             'mark':mark
                             }
            rs_query_list.append(rs_query_dict)
    
    userinfo_list = []
    for userallinfo in rs_query_list:
        userinfo_dict = {}
        queryuserid = userallinfo['userid']
        companyinfos_query = Opuser.query.filter_by(opuserid=queryuserid).all()
        companyid_list = []
        for companyinfo_query in companyinfos_query:
            companyid = companyinfo_query.opcompanyid
            companyid_list.append(companyid)
        companyname_list = []
        for companyid in companyid_list:
            companyinfos_query = Company.query.filter_by(companyid=companyid).first()
            companyname = companyinfos_query.companyname
            companyname_list.append(companyname)
        userinfo_dict['companynamelist'] = companyname_list
        userinfo_dict['userinfo'] = userallinfo
        userinfo_list.append(userinfo_dict)

    userallinfo_list = []
    for userinfo in userinfo_list:

        userallinfo_dict = {}
        companyname_list = userinfo['companynamelist']
        userallinfo = userinfo['userinfo']
        if companyname_list:
            pass
        else:
            companyname_list = ['未关联公司']

        for companyname in companyname_list:
            userallinfo_dict['companyname'] = companyname
            userallinfo_dict['userallinfo'] = userallinfo

        userallinfo_list.append(userallinfo_dict)
    
    userallinfo_list = []

    for userallinfo in rs_query_list:
        #userinfo_dict = {}
        queryuserid = userallinfo['userid']
        opuserinfos_query = Opuser.query.filter_by(opuserid=queryuserid).all()

        if opuserinfos_query:
            for opuserinfo in opuserinfos_query:
                userinfo_dict = {}
                companyid = opuserinfo.opcompanyid
                companyinfo = Company.query.filter_by(companyid=companyid).first()
                if companyinfo:
                    companyname = companyinfo.companyname
                    userinfo_dict["companyname"] = companyname
                    userinfo_dict["userallinfo"] = userallinfo
                    userallinfo_list.append(userinfo_dict)

        else:
            userinfo_dict = {}
            companyname = "未关联公司"
            userinfo_dict["companyname"] = companyname
            userinfo_dict["userallinfo"] = userallinfo
            userallinfo_list.append(userinfo_dict)

    print(len(userallinfo_list))
    print(userallinfo_list)

    db.session.close()
    return {"status":0, "msg": "查询成功",'pagetotal':page_total, "userinfo": userallinfo_list}
"""


def backstagesearchusersmobile(adminuserid, token, page, mobile):
    if token != '11111':
        return {'status':1, 'msg':'token不可用'}

    #所有用户信息
    page = int(page)
    rs_query_list = []
    users_query_page = User.query.filter(User.mobile.like('%' + mobile + '%')).order_by(
        User.createtime.desc()).paginate(page, per_page=20, error_out=False)
    #users_query = users_query_page.items
    users_query = User.query.filter(User.mobile.like('%' + mobile + '%')).order_by(User.createtime.desc()).all()
    users_total =  len(users_query) / 15
    page_total = math.ceil(users_total)
    for user_query in users_query:
        userid = user_query.userid
        username = user_query.username
        usermobile = user_query.mobile
        userrole = user_query.role
        mark = user_query.mark
        userlogintime = user_query.logintime
        if userlogintime:
            userlogintime = int(round(time.mktime(userlogintime.timetuple()) * 1000))
        if username != 'chatbot' or usermobile.find('c') == -1:
            rs_query_dict = {'username': username, 'mobile': usermobile,
                             'role': userrole, 'logintime': userlogintime, 'userid': userid,
                             'mark':mark
                             }
            rs_query_list.append(rs_query_dict)

    userallinfo_list = []

    for userallinfo in rs_query_list:
        #userinfo_dict = {}
        queryuserid = userallinfo['userid']
        opuserinfos_query = Opuser.query.filter_by(opuserid=queryuserid).all()

        if opuserinfos_query:
            for opuserinfo in opuserinfos_query:
                userinfo_dict = {}
                companyid = opuserinfo.opcompanyid
                companyinfo = Company.query.filter_by(companyid=companyid).first()
                

                userallinfocopy = {'username': userallinfo['username'],
                                    'mobile': userallinfo['mobile'],
                                    'role': userallinfo['role'],
                                    'logintime': userallinfo['logintime'],
                                    'userid': userallinfo['userid'],
                                    'mark':userallinfo['mark'] }

                if opuserinfo.company_user_status == '3':
                    userallinfocopy['mark'] = 'userenabled'
                elif opuserinfo.company_user_status == '4':
                    userallinfocopy['mark'] = 'userdisabled'
                userinfo_dict["userallinfo"] = userallinfocopy
                if companyinfo:
                    companyname = companyinfo.companyname
                    userinfo_dict["companyid"] = companyinfo.companyid
                    userinfo_dict["companyname"] = companyname
                    userallinfo_list.append(userinfo_dict)
        else:
            userinfo_dict = {}
            companyname = "未关联公司"
            userinfo_dict["companyid"] = ''
            userinfo_dict["companyname"] = companyname
            userinfo_dict["userallinfo"] = userallinfo
            userallinfo_list.append(userinfo_dict)
  
    db.session.close()
    return {"status":0, "msg": "查询成功",'pagetotal':page_total, "userinfo": userallinfo_list}






"""
def backstagesearchuserscompany(adminuserid, token, page, searchcompanyname):
    if token != '11111':
        return {'status':1, 'msg':'token不可用'}
    #所有用户信息
    page = int(page)
    rs_query_list = []
    search_companyid_list = []
    companys_query_page = Company.query.filter(Company.companyname.like('%' + searchcompanyname + '%')).order_by(
        Company.createtime.desc()).paginate(page, per_page=20, error_out=False)
    companys_query = companys_query_page.items
    users_total =  len(companys_query) / 15
    page_total = math.ceil(users_total)
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
            if searchopuserrole != '5' and searchopuserid:
                searchopuser_dict = {
                            "companyname": searchcompanyidinfo['companyname'],
                            "userallinfo": {
                                "userid": searchopuserid,
                                    }
                                }
                search_opuserid_list.append(searchopuser_dict)
    lastuserinfo_list = []
    print(search_opuserid_list)
    for useridinfo in search_opuserid_list:

        queryuserid = useridinfo['userallinfo']['userid']
        userinfo_query = User.query.filter_by(userid=queryuserid).first()
        username = userinfo_query.username
        usermobile = userinfo_query.mobile
        userlogintime = userinfo_query.logintime
        if userlogintime:
            userlogintime = int(round(time.mktime(userlogintime.timetuple()) * 1000))
        userrole = userinfo_query.role
        mark = userinfo_query.mark
        useridinfo['userallinfo']['username'] = username
        useridinfo['userallinfo']['mobile'] = usermobile
        useridinfo['userallinfo']['logintime'] = userlogintime
        useridinfo['userallinfo']['role'] = userrole
        useridinfo['userallinfo']['mark'] = mark
        lastuserinfo_list.append(useridinfo)
    db.session.close()
    return {"status":0, "msg": "查询成功", 'pagetotal':page_total,"userinfo": lastuserinfo_list}
"""

def backstagesearchuserscompany(adminuserid, token, page, searchcompanyname):
    if token != '11111':
        return {'status':1, 'msg':'token不可用'}
    #所有用户信息
    page = int(page)
    rs_query_list = []
    search_companyid_list = []
    companys_query_page = Company.query.filter(Company.companyname.like('%' + searchcompanyname + '%')).order_by(
        Company.createtime.desc()).paginate(page, per_page=20, error_out=False)
    companys_query = companys_query_page.items
    users_total =  len(companys_query) / 15
    page_total = math.ceil(users_total)
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
            if searchopuserrole != '5' and searchopuserid:
                searchopuser_dict = {
                            "companyid": searchcompanyidinfo['companyid'],
                            "companyname": searchcompanyidinfo['companyname'],
                            "userallinfo": {
                                "userid": searchopuserid,
                                    }
                                }
                search_opuserid_list.append(searchopuser_dict)
    lastuserinfo_list = []
    print(search_opuserid_list)
    for useridinfo in search_opuserid_list:

        queryuserid = useridinfo['userallinfo']['userid']
        userinfo_query = User.query.filter_by(userid=queryuserid).first()
        username = userinfo_query.username
        usermobile = userinfo_query.mobile
        userlogintime = userinfo_query.logintime
        if userlogintime:
            userlogintime = int(round(time.mktime(userlogintime.timetuple()) * 1000))
        userrole = userinfo_query.role
        mark = userinfo_query.mark
        useridinfo['userallinfo']['username'] = username
        useridinfo['userallinfo']['mobile'] = usermobile
        useridinfo['userallinfo']['logintime'] = userlogintime
        useridinfo['userallinfo']['role'] = userrole

        # 查询运维用户的状态 begin
        cpmpanyid = useridinfo['companyid']
        opuser = Opuser.query.filter_by(opuserid=queryuserid,opcompanyid=cpmpanyid).first()
        if opuser:
            if opuser.company_user_status == '3':
                useridinfo['userallinfo']['mark'] = 'userenabled'
            elif opuser.company_user_status == '4':
                useridinfo['userallinfo']['mark'] = 'userdisabled'
        # end

        lastuserinfo_list.append(useridinfo)
    db.session.close()
    return {"status":0, "msg": "查询成功", 'pagetotal':page_total,"userinfo": lastuserinfo_list}
"""
def backstagesearchusersall(adminuserid, token, page, mobile, searchcompanyname):
    if token != '11111':
        return {'status':1, 'msg':'token不可用'}
    #所有用户信息
    page = int(page)
    search_userinfo_list = []
    userss_query_page = db.session.query(User, Company).filter(User.mobile.like('%' + mobile + '%')).filter(Company.companyname.like('%' + searchcompanyname + '%')).order_by(
        User.createtime.desc()).paginate(page, per_page=20, error_out=False)

    users_query = userss_query_page.items
    users_total =  len(users_query) / 15
    page_total = math.ceil(users_total)
    for user_query in users_query:
        print(user_query)
        search_user_dict = {}
        userinfo = {}
        userinfo['userid'] = user_query[0].userid
        userinfo['username'] = user_query[0].username
        userinfo['mobile'] = user_query[0].mobile
        userlogintime = user_query[0].logintime
        if userlogintime:
            userlogintime = int(round(time.mktime(userlogintime.timetuple()) * 1000))
        userinfo['logintime'] = userlogintime
        userinfo['role'] = user_query[0].role
        userinfo['mark'] = user_query[0].mark
        search_user_dict['companyname'] = user_query[1].companyname
        search_user_dict['userallinfo'] = userinfo

        search_userinfo_list.append(search_user_dict)
    print(search_userinfo_list)
    db.session.close()
    return {"status": 0, "msg": "查询成功",'pagetotal':page_total, "userinfo": search_userinfo_list}
"""

def backstagesearchusersall(adminuserid, token, page, mobile, searchcompanyname):
    if token != '11111':
        return {'status':1, 'msg':'token不可用'}
    #所有用户信息
    page = int(page)
    search_userinfo_list = []
    userss_query_page = db.session.query(User, Company).filter(User.mobile.like('%' + mobile + '%')).filter(Company.companyname.like('%' + searchcompanyname + '%')).order_by(
        User.createtime.desc()).paginate(page, per_page=20, error_out=False)
    userss_query = db.session.query(User, Company).filter(User.mobile.like('%' + mobile + '%')).filter(Company.companyname.like('%' + searchcompanyname + '%')).order_by(User.createtime.desc()).all()
    users_query = userss_query_page.items
    users_total =  len(userss_query) / 15
    page_total = math.ceil(users_total)
    for user_query in users_query:
        print(user_query)
        search_user_dict = {}
        userinfo = {}
        userinfo['userid'] = user_query[0].userid
        userinfo['username'] = user_query[0].username
        userinfo['mobile'] = user_query[0].mobile
        userlogintime = user_query[0].logintime
        if userlogintime:
            userlogintime = int(round(time.mktime(userlogintime.timetuple()) * 1000))
        userinfo['logintime'] = userlogintime
        userinfo['role'] = user_query[0].role
        userinfo['mark'] = user_query[0].mark
        
        opuserinfo = Opuser.query.filter_by(opuserid=userinfo['userid'],opcompanyid=user_query[1].companyid).first()
        if opuserinfo:
            if opuserinfo.company_user_status == '3':
                userinfo['mark'] = 'userenabled'
            elif opuserinfo.company_user_status == '4':
                userinfo['mark'] = 'userdisabled'

        search_user_dict['companyid'] = user_query[1].companyid
        search_user_dict['companyname'] = user_query[1].companyname
        search_user_dict['userallinfo'] = userinfo

        search_userinfo_list.append(search_user_dict)
    print(search_userinfo_list)
    db.session.close()
    return {"status": 0, "msg": "查询成功",'pagetotal':page_total, "userinfo": search_userinfo_list}


def backstagetourist(adminuserid, token, page):
    if token != '11111':
        return {'status':1, 'msg':'token不可用'}
    #所有用户信息
    page = int(page)
    search_userinfo_list = []
    users_query_page = User.query.filter_by(role='1').order_by(
        User.createtime.desc()).paginate(page, per_page=20, error_out=False)
    users_query = users_query_page.items
    users_total =  len(users_query) / 15
    page_total = math.ceil(users_total)
    for user_query in users_query:
        search_user_dict = {}
        userinfo = {}
        userinfo['userid'] = user_query.userid
        userinfo['username'] = user_query.username
        userinfo['mobile'] = user_query.mobile
        userlogintime = user_query.logintime
        if userlogintime:
            userlogintime = int(round(time.mktime(userlogintime.timetuple()) * 1000))
        userinfo['logintime'] = userlogintime
        userinfo['role'] = user_query.role
        userinfo['mark'] = user_query.mark
        search_user_dict['companyname'] = None
        search_user_dict['userallinfo'] = userinfo

        search_userinfo_list.append(search_user_dict)
    print(search_userinfo_list)
    db.session.close()
    return {"status": 0, "msg": "查询成功", 'pagetotal':page_total,"userinfo": search_userinfo_list}


def backstageuserstopped(adminuserid, token, page):
    if token != '11111':
        return {'status':1, 'msg':'token不可用'}
    #所有用户信息
    page = int(page)
    search_userinfo_list = []
    users_query_page = User.query.filter_by(mark="userdisabled").order_by(
        User.createtime.desc()).paginate(page, per_page=20, error_out=False)
    users_query = users_query_page.items
    users_total =  len(users_query) / 15
    page_total = math.ceil(users_total)
    for user_query in users_query:
        opuser = Opuser.query.filter_by(opuserid=user_query.userid).first()
        if opuser:
            company = Company.query.filter_by(companyid=opuser.opcompanyid).first()
            search_user_dict = {}
            userinfo = {}
            userinfo['userid'] = user_query.userid
            userinfo['username'] = user_query.username
            userinfo['mobile'] = user_query.mobile
            userinfo['company'] = company.companyname
            userlogintime = user_query.logintime
            if userlogintime:
                userlogintime = int(round(time.mktime(userlogintime.timetuple()) * 1000))
            userinfo['logintime'] = userlogintime
            userinfo['role'] = user_query.role
            userinfo['mark'] = user_query.mark
            search_user_dict['companyname'] = company.companyname
            search_user_dict['userallinfo'] = userinfo

            search_userinfo_list.append(search_user_dict)
    print(search_userinfo_list)
    db.session.close()
    return {"status": 0, "msg": "查询成功", 'pagetotal':page_total,"userinfo": search_userinfo_list}




"""
def userdisable(adminuserid, token, userdisable, userid):
    if token != '11111':
        return {'status':1, 'msg':'token不可用'}
    #所有用户信息

    return {"status": 0, "msg": "暂未支持"}
"""
"""
def userdelete(adminuserid, token, userid):
    if token != '11111':
        return {'status':1, 'msg':'token不可用'}
    #所有用户信息

    return {"status": 0, "msg": "暂未支持"}
"""
