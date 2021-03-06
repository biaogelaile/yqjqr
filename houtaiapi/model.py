#from flask_sqlalchemy import SQLAlchemy
from flask import Flask
from config import *
from flask_cors import CORS

from flask_sqlalchemy import SQLAlchemy as SQLAlchemyBase
from sqlalchemy.pool import NullPool


class SQLAlchemy(SQLAlchemyBase):
  def apply_driver_hacks(self, app, info, options):
    super(SQLAlchemy, self).apply_driver_hacks(app, info, options)
    options['poolclass'] = NullPool
    options.pop('pool_size', None)

'''配置数据库'''
app = Flask(__name__)
app.config['SECRET_KEY'] ='hard to guess'
app.config['SQLALCHEMY_DATABASE_URI'] = localdatabase

#设置这一项是每次请求结束后都会自动提交数据库中的变动
app.config['SQLALCHEMY_COMMIT_ON_TEARDOWN']=True
app.config['SQLALCHEMY_TRACK_MODIFICATIONS']=False
#实例化
db = SQLAlchemy(app)

CORS(app, origins="*", allow_headers=[
    "Content-Type", "Authorization", "Access-Control-Allow-Credentials","Access-Control-Allow-Origin"],
    supports_credentials=True)


class User(db.Model):
    # 定义表名
    __tablename__ = 'tbl_users'
    # 定义列对象
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(128), nullable=True, comment='用户名')
    userid = db.Column(db.String(128), nullable=True,unique=True, comment='用户名')
    role = db.Column(db.String(128), nullable=True, comment='用户状态')
    #password_hash = db.Column(db.String(64))
    password = db.Column(db.String(128), nullable=False, comment='用户密码')
    mobile = db.Column(db.String(128), nullable=False,unique=True, comment='用户手机号码')
    #1为游客，2为申请待同意用户，3为普通公司用户，4为公司管理员
    profile = db.Column(db.String(128), nullable=False, server_default='http://139.196.107.14:6001/upload/2018-11-12/qMWML0jLCnhs2o1Nv6a5ajpr-defaultUser@3x.png', comment='profile picture')
    mark = db.Column(db.String(128), nullable=True, comment='用户备注')
    logintime = db.Column(db.TIMESTAMP(True), nullable=False, comment='登录时间')
    createtime = db.Column(db.TIMESTAMP(True), nullable=False,comment='创建时间')
    updatetime = db.Column(db.TIMESTAMP(True), nullable=False, comment='更新时间')

class Opuser(db.Model):
    # 定义表名
    __tablename__ = 'tbl_opusers'
    # 定义列对象
    id = db.Column(db.Integer, primary_key=True)
    opusername = db.Column(db.String(128), nullable=True, comment='用户名')
    opuserid = db.Column(db.String(128), nullable=True, comment='用户名')
    opmobile = db.Column(db.String(128), nullable=True, comment='用户手机号码')
    opcompanyid = db.Column(db.String(128), nullable=True, comment='公司id')
    default = db.Column(db.String(128), nullable=True, comment='是否是默认公司')
    oprole = db.Column(db.String(128), nullable=True, comment='用户状态')
    userstatus = db.Column(db.String(128), nullable=False,server_default='register', comment='用户渠道')
    company_user_status = db.Column(db.String(128), nullable=False,server_default='3', comment='公司用户状态')
    opemail = db.Column(db.String(128), nullable=True, comment='email')
    createtime = db.Column(db.TIMESTAMP(True), nullable=False,comment='创建时间')
    updatetime = db.Column(db.TIMESTAMP(True), nullable=False, comment='更新时间')

class Company(db.Model):
    # 定义表名
    __tablename__ = 'tbl_company'
    # 定义列对象
    id = db.Column(db.Integer, primary_key=True)
    companyid =  db.Column(db.String(128), nullable=True,unique=True, comment='公司id')
    companyname = db.Column(db.String(128), nullable=True, comment='公司名称')
    companyrole = db.Column(db.String(128), nullable=True, comment='公司角色')
    companyemail = db.Column(db.String(128), nullable=True, comment='公司email')
    companymark = db.Column(db.String(128), nullable=True, comment='公司备注')
    #disable = db.Column(db.String(128), nullable=True, default="true", comment='公司开启禁用')
    disable = db.Column(db.Boolean, nullable=True, default=0, comment='公司开启禁用')
    companyexpiredate = db.Column(db.TIMESTAMP(True),nullable=True,comment='过期时间')
    createtime = db.Column(db.TIMESTAMP(True), nullable=False,comment='创建时间')
    updatetime = db.Column(db.TIMESTAMP(True), nullable=False, comment='更新时间')
   


class Permission(db.Model):
    # 定义表名
    __tablename__ = 'tbl_permission'
    # 定义列对象
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.String(128), nullable=False, comment='管理员')
    user_role = db.Column(db.String(128), nullable=False, comment='申请人用户名')
    createtime = db.Column(db.TIMESTAMP(True), nullable=False,comment='创建时间')
    updatetime = db.Column(db.TIMESTAMP(True), nullable=False, comment='更新时间')


class Topic(db.Model):
    # 定义表名
    __tablename__ = 'tbl_topic'
    # 定义列对象
    id = db.Column(db.Integer, primary_key=True)
    admin_userid = db.Column(db.String(128), nullable=False, comment='管理员')
    companyid = db.Column(db.String(128), nullable=False, comment='公司id')
    request_username = db.Column(db.String(128), nullable=False, comment='申请人用户名')
    request_mobile = db.Column(db.String(128), nullable=False, comment='申请人手机')
    request_userid = db.Column(db.String(128), nullable=False, comment='申请人用户id')
    admin_action = db.Column(db.String(128), nullable=True, comment='管理员动作')
    createtime = db.Column(db.TIMESTAMP(True), nullable=False,comment='创建时间')
    updatetime = db.Column(db.TIMESTAMP(True), nullable=False, comment='更新时间')


class Sms(db.Model):
    # 定义表名
    __tablename__ = 'tbl_sms'
    # 定义列对象
    id = db.Column(db.Integer, primary_key=True)
    user_mobile = db.Column(db.String(128), nullable=False, comment='管理员')
    user_sms = db.Column(db.String(128), nullable=False, comment='申请人用户名')
    createtime = db.Column(db.TIMESTAMP(True), nullable=False,comment='创建时间')
    updatetime = db.Column(db.TIMESTAMP(True), nullable=False, comment='更新时间')


class Zabbix(db.Model):
    # 定义表名
    __tablename__ = 'tbl_zabbix'
    # 定义列对象
    id = db.Column(db.Integer, primary_key=True)
    companyid = db.Column(db.String(128), nullable=False, comment='公司id')
    zabbixid = db.Column(db.String(128), nullable=False, comment='zabbix服务器id')
    zabbixserver = db.Column(db.String(128), nullable=False, comment='zabbix服务器地址')
    zabbixuser = db.Column(db.String(128), nullable=False, comment='zabbix用户')
    zabbixpassword = db.Column(db.String(128), nullable=False, comment='zabbix密码')
    official = db.Column(db.String(20), nullable=True, default='1', comment='zabbix服务器类型')
    createtime = db.Column(db.TIMESTAMP(True), nullable=False,comment='创建时间')
    updatetime = db.Column(db.TIMESTAMP(True), nullable=False, comment='更新时间')

class Monitor(db.Model):
    # 定义表名
    __tablename__ = 'tbl_monitor'
    # 定义列对象
    id = db.Column(db.Integer, primary_key=True)
    companyid = db.Column(db.String(128), nullable=False, comment='公司id')
    zabbixhostid = db.Column(db.String(128), nullable=False, comment='zabbix服务器id')
    #zabbixgroupid = db.Column(db.String(128), nullable=False, comment='zabbix组id')
    zabbixhostip = db.Column(db.String(128), nullable=False, comment='zabbix hostip')
    zabbixhostname = db.Column(db.String(128), nullable=False, comment='zabbix hostname')
    zabbixitemid = db.Column(db.String(1280), nullable=True, comment='zabbix组id')
    zabbixitemname = db.Column(db.String(128), nullable=True, comment='zabbix组id')
    createtime = db.Column(db.TIMESTAMP(True), nullable=False,comment='创建时间')
    updatetime = db.Column(db.TIMESTAMP(True), nullable=False, comment='更新时间')


class Backstage(db.Model):
    # 定义表名
    __tablename__ = 'tbl_backstage'
    # 定义列对象
    id = db.Column(db.Integer, primary_key=True)
    rootname = db.Column(db.String(128), nullable=False, comment='超级管理员名称')
    companyexpire = db.Column(db.String(128), nullable=False, comment='过期时间')
    tryoutdata = db.Column(db.String(128), nullable=False, comment='试用时间')
    customerservicemobile = db.Column(db.String(128), nullable=False, comment='客服电话')
    rootpassword = db.Column(db.String(1280), nullable=True, comment='超级管理员密码')
    createtime = db.Column(db.TIMESTAMP(True), nullable=False,comment='创建时间')
    updatetime = db.Column(db.TIMESTAMP(True), nullable=False, comment='更新时间')


class UserToken(db.Model):
    #定义表名
    __tablename__ = 'tbl_usertoken'
    id = db.Column(db.Integer, primary_key=True)
    token = db.Column(db.String(128), nullable=False, comment='用户token')
    createtime = db.Column(db.TIMESTAMP(True), nullable=False,comment='创建时间')

#db.create_all()
