from model import *
from socketIO_client import SocketIO, BaseNamespace
from flask_socketio import SocketIO,emit
import sqlalchemy
from datetime import datetime, timedelta
import time
from urllib.parse import unquote
from flask_socketio import join_room, leave_room
app = Flask(__name__)
socketio = SocketIO(app)

def backstage(userid, token):
    if token != '11111':
        return {'status':1, 'msg':'token不可用'}

    #公司总数量
    companys_query = Company.query.all()
    totalcompanys = len(companys_query)

    #当天新增公司数量
    todays_datetime = datetime(datetime.today().year, datetime.today().month, datetime.today().day)
    #todays_datetime = '2018-10-30 00:00:00'
    newcompanys_query = Company.query.filter(Company.createtime >= todays_datetime).all()
    newcompanys = len(newcompanys_query)

    #试用中的公司
    num = 0
    try_companys_query = Company.query.all()
    for company in try_companys_query:
        if not company.companyexpiredate:
            num += 1
    try_companys = num

    #用户总数量
    users_query = User.query.filter(
        User.mobile.like('1%')).all()
    totalusers = len(users_query)

    #当天新增用户
    newusers_query = User.query.filter(User.createtime >= todays_datetime, User.mobile.like('1%')).all()
    newusers = len(newusers_query)

    backstage_expiredate_query = Backstage.query.first()
    backstage_expiredate = backstage_expiredate_query.companyexpire
    expire_date = todays_datetime + timedelta(days=int(backstage_expiredate))
    try_expire_companys_query = Company.query.filter(Company.companyexpiredate <= expire_date, Company.companyexpiredate >= todays_datetime, Company.companyrole == '2').all()
    expire_companys = len(try_expire_companys_query)
    rs = {'total_companys': totalcompanys, 'new_companys': newcompanys,
          'try_companys': try_companys,'total_users':totalusers,
          'new_users': newusers, 'expiring_companys':expire_companys,
          }
    db.session.close()
    return rs

def AdminInfo(username, password):
    #所有用户信息

    admin_query = Backstage.query.filter_by(rootname='root').first()
    adminpassword = admin_query.rootpassword
    if username == 'root' and password == adminpassword:
        db.session.close()
        return {'status':0, 'msg': '登录成功', 'token':'xxx-11111'}
    else:
        db.session.close()
        return {'status':1, 'msg':'用户名或密码错误'}

def adminpatch(adminuserid, admintoken, oldpassword, newpassword):
    #所有用户信息
    if admintoken != '11111':
        return {'status':1, 'msg':'token不可用'}

    admin_query = Backstage.query.filter_by(rootname='root').first()
    adminpassword = admin_query.rootpassword
    if oldpassword == adminpassword:
        admin_query.rootpassword = newpassword
        db.session.commit()
        db.session.close()
        return {'status':0, 'msg': '修改成功'}
    else:
        db.session.close()
        return {'status':2, 'msg':'旧密码错误'}
"""
def userdelete(adminuserid, adminusertoken, userid):
    try:
        if adminusertoken != '11111':
            return {'status':1, 'msg':'token不可用'}
        user_query = User.query.filter_by(userid=userid).first()
        db.session.delete(user_query)
        db.session.commit()
        return {'status':0, 'msg': '修改成功'}
    except sqlalchemy.exc.OperationalError:
        db.session.close()
        return {'Oooops': 'There is a problem with the database'}

def userdisable(adminuserid,adminusertoken,userstatus,userid):
    try:
        if adminusertoken != '11111':
            return {'status':1, 'msg':'token不可用'}
        user_query = User.query.filter_by(userid=userid).first()
        if userstatus:
            user_query.mark = userstatus
        db.session.commit()
        topic = Topic.query.filter_by(admin_userid=adminuserid).first()
        if topic:
            companyid = topic.companyid
            companyname = Company.query.filter_by(companyid=companyid).first()
            room = companyname
            join_room(room)
            socket.emit("talkstatus",{"type":14,"companyid":companyid},room=room)
        return {'status':0, 'msg': '修改成功'}
    except sqlalchemy.exc.OperationalError:
        db.session.close()
        return {'Oooops': 'There is a problem with the database'}
"""

# 删除用户
# 1、如果用户是游客直接删除账户
# 2、如果用户有1家公司直接删除账户
# 3、如果存在2家或者以上的公司，把用户从当前公司下删除(从 Opuser 中删除)
def userdelete(adminuserid, adminusertoken, userid, companyid):
    try:
        # 不存在公司（游客）直接删除账户
        if len(companyid) == 0:
           return deleteTouristAccount(adminusertoken, userid)
        # 用户存在几家公司
        companys = Opuser.query.filter_by(opuserid=userid)
        
        if companys:
            # 存在1家以下的公司直接删除账户
            if len(companys) <= 1:
                return deleteTouristAccount(adminusertoken, userid)
            # 删除当前选中公司中的当前运维用户
            else:
                opUser = Opuser.query.filter_by(opuserid=userid,opcompanyid=companyid).first()
                db.session.delete(opUser)
                db.session.commit()
                return {'status':0, 'msg': '修改成功'}
        # 公司不存在直接删除用户
        else:
            return deleteTouristAccount(adminusertoken, userid)
                
    except sqlalchemy.exc.OperationalError:
        db.session.close()
        return {'Oooops': 'There is a problem with the database'}

# 用户禁用
# 1、用户没有公司、直接禁用用户的账户
# 2、有公司、禁用当前公司下的该用户 Opuser.company_user_status = '4'
def userdisable(adminuserid,adminusertoken,userstatus,userid, companyid):
    try:
        # 不存在公司（游客）账户被禁用
        if len(companyid) == 0:
            if adminusertoken != '11111':
                return {'status':1, 'msg':'token不可用'}
            user_query = User.query.filter_by(userid=userid).first()
            if userstatus:
                user_query.mark = userstatus
            db.session.commit()
            return {'status':0, 'msg': '修改成功'}
                
        # 禁用公司下的运维用户 Opuser company_user_status = '4'
        opUser = Opuser.query.filter_by(opuserid=userid,opcompanyid=companyid).first()
        if opUser:
            
            if userstatus=='userenabled':
                opUser.company_user_status = '3'
            else:
                opUser.company_user_status = '4'

        db.session.commit()
        return {'status':0, 'msg': '修改成功'}
                
    except sqlalchemy.exc.OperationalError:
        db.session.close()
        return {'Oooops': 'There is a problem with the database'}
