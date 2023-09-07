from functools import wraps
from itertools import groupby
import requests
from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
import jwt
from sqlalchemy import func, or_
from sqlalchemy.orm import aliased
from flask_cors import CORS

import pymysql
from werkzeug.security import generate_password_hash, check_password_hash
import datetime

import config

pymysql.install_as_MySQLdb()
app = Flask(__name__)
app.config.from_object(config)

cors = CORS(app)
db = SQLAlchemy(app)

def create_db_if_not_exists(no,password,name="超级管理员"):
    try:
        User.query.filter_by(roleId=0).first()
    except Exception:
        from sqlalchemy_utils import database_exists, create_database
        if not database_exists(db.engine.url):
            create_database(db.engine.url)
        db.create_all()
        menus = [
    Menu(id=1, menucode='001', menuname='管理员', menulevel='1', menuclick='Admin' ,menuright=0 ,menucomponent='admin/AdminManage.vue', menuicon='Avatar'),
    Menu(id=2, menucode='002', menuname='用户管理', menulevel='1', menuclick='User' ,menuright=1 ,menucomponent='user/UserManage.vue', menuicon='User'),
    Menu(id=3, menucode='003', menuname='仓库管理', menulevel='1', menuclick='Storage' ,menuright=1 ,menucomponent='storage/StorageManage.vue', menuicon='HomeFilled'),
    Menu(id=4, menucode='004', menuname='分类管理', menulevel='1', menuclick='Goodstype' ,menuright=1 ,menucomponent='goodstype/GoodstypeManage.vue', menuicon='ChatLineSquare'),
    Menu(id=5, menucode='005', menuname='物品管理', menulevel='1', menuclick='Goods' ,menuright=2 ,menucomponent='goods/GoodsManage.vue', menuicon='Box'),
    Menu(id=6, menucode='006', menuname='记录管理', menulevel='1', menuclick='Record' ,menuright=2 ,menucomponent='record/RecordManage.vue', menuicon='List'),
    Menu(id=7, menucode='007', menuname='数据地图', menulevel='1', menuclick='Map' ,menuright=2 ,menucomponent='map/Map.vue', menuicon='PictureFilled')
]

# 添加多条记录
        db.session.add_all(menus)
        db.session.add(User(no=no,name=name,password=generate_password_hash(password),roleId=0))
        db.session.commit()
        
def token_required(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        token = request.headers.get('Authorization')

        if not token:
            return Result(400, "失败").get_value(), 401
        try:
            data = jwt.decode(
                token, app.config['SECRET_KEY'], algorithms=['HS256'])
            roleId = data['roleId']
        except:
            return Result(400, "失败").get_value(), 401

        return f(roleId, *args, **kwargs)

    return decorated


class Result():
    def __init__(self, code=400, msg="", total=0, data=None):
        self.code = code
        self.msg = msg
        self.total = total
        self.data = data

    def get_value(self):
        return jsonify({
            "msg": self.msg,
            "code": self.code,
            "total": self.total,
            "data": self.data
        })


class Base:
    def to_dict(self):
        col_keys = self.__table__.columns.keys()
        col_dict = {i: self.__getattribute__(i)
                    for i in col_keys if i != "password"}
        return col_dict


class User(Base, db.Model):
    __tablename__ = 'user'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    no = db.Column(db.String(20), unique=True, nullable=False)
    name = db.Column(db.String(100), nullable=False)
    password = db.Column(db.String(256), nullable=False)
    age = db.Column(db.Integer)
    sex = db.Column(db.String(1))
    phone = db.Column(db.String(20))
    roleId = db.Column(db.Integer)
    isValid = db.Column(db.String(4))


class Menu(Base, db.Model):
    __tablename__ = 'menu'
    id = db.Column(db.Integer, primary_key=True)
    menucode = db.Column(db.String(8))
    menuname = db.Column(db.String(30))
    menulevel = db.Column(db.String(2))
    menuparentcode = db.Column(db.String(8))
    menuclick = db.Column(db.String(16))
    menuright = db.Column(db.Integer)
    menucomponent = db.Column(db.String(200))
    menuicon = db.Column(db.String(100))


class Goods(Base, db.Model):
    __tablename__ = 'goods'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String(100), nullable=False)
    storage = db.Column(db.Integer, db.ForeignKey(
        'storage.id', ondelete='RESTRICT'), nullable=False)
    goodstype = db.Column(db.Integer, db.ForeignKey(
        'goodstype.id', ondelete='RESTRICT'), nullable=False)
    count = db.Column(db.Integer)
    remark = db.Column(db.String(1000))

    st = db.relationship('Storage', backref=db.backref('goods'))
    gt = db.relationship('Goodstype', backref=db.backref('goods'))


class Goodstype(Base, db.Model):
    __tablename__ = 'goodstype'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String(100), nullable=False)
    remark = db.Column(db.String(1000))


class Storage(Base, db.Model):
    __tablename__ = 'storage'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String(100), nullable=False)
    address = db.Column(db.String(100), nullable=False)
    location = db.Column(db.JSON, nullable=False)
    remark = db.Column(db.String(1000))


class Record(Base, db.Model):
    __tablename__ = 'record'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    action = db.Column(db.String(2))
    goods = db.Column(db.Integer, db.ForeignKey('goods.id'), nullable=False)
    userId = db.Column(db.Integer, db.ForeignKey('user.id'))
    adminId = db.Column(db.Integer, db.ForeignKey('user.id'))
    count = db.Column(db.Integer)
    createtime = db.Column(db.DateTime, default=datetime.datetime.now)
    remark = db.Column(db.String(1000))


def str_int(s):
    if s is None or s == '':
        return None
    return int(s)


@app.route('/user/login', methods=['POST'])
def login():
    no = request.json.get('no')
    password = request.json.get('password')
    user = User.query.filter_by(no=no).first()
    data = None
    if not user or not (check_password_hash(user.password, password)):
        return Result(400, "失败", 0, data).get_value(), 200
    token = jwt.encode({'no':user.no,'roleId': user.roleId, 'exp': datetime.datetime.utcnow(
    ) + datetime.timedelta(hours=4)}, config.SECRET_KEY)
    data = {
        "menu": [i.to_dict() for i in Menu.query.filter(Menu.menuright >= user.roleId)],
        "user": user.to_dict(),
        "token": token.encode("UTF-8").decode('UTF-8')
    }
    return Result(200, "成功", 0, data).get_value(), 200


@app.route('/user/findByNo', methods=['POST', 'GET'])
@token_required
def findbyno(roleId):
    fno = request.args.get('no')
    data = [i.to_dict() for i in User.query.filter_by(no=fno)]
    if len(data) == 0:
        return Result(400, "失败", 0, data).get_value(), 200
    return Result(200, "成功", 0, data).get_value(), 200


@app.route('/<table>/list')
@token_required
def tablelist(roleId, table):
    try:
        match table:
            case "goodstype":
                tb = Goodstype
            case "goods":
                tb = Goods
            case "storage":
                tb = Storage
            case "user":
                tb = User
        results = tb.query.all()
        data = [i.to_dict() for i in results]
        return Result(200, "成功", len(data), data).get_value(), 200
    except:
        return Result(400, "失败").get_value(), 200


@app.route('/<table>/listPage', methods=['POST', 'GET'])
@token_required
def listPage(roleId, table):
    try:
        pageSize = request.json.get('pageSize')
        pageNum = request.json.get('pageNum')
        param = request.json.get('param')
        name = param.get('name')
        match table:
            case "goodstype":
                tb = Goodstype
                result = tb.query.filter(tb.name.contains(name))
            case "goods":
                tb = Goods
                storage = str_int(param.get('storage'))
                goodstype = str_int(param.get('goodstype'))
                result = Goods.query.filter(
                    Goods.name.contains(name) &
                    or_(storage is None, Goods.storage == storage) &
                    or_(goodstype is None, Goods.goodstype == goodstype)
                )
            case "storage":
                tb = Storage
                result = tb.query.filter(tb.name.contains(name))
            case "user":
                tb = User
                roleId = int(param.get('roleId'))
                sex = param.get('sex')
                result = tb.query.filter(tb.name.contains(
                    name) & tb.sex.contains(sex)).filter_by(roleId=roleId)
        results = result.paginate(page=pageNum, per_page=pageSize)
        data = [i.to_dict() for i in results]
        return Result(200, "成功", results.total, data).get_value(), 200
    except:
        return Result(400, "失败").get_value(), 200


@app.route('/<table>/save', methods=['POST', 'GET'])
@token_required
def save(roleId, table):
    try:
        param = request.json
        match table:
            case "goodstype":
                tb = Goodstype
            case "goods":
                tb = Goods
            case "storage":
                param['location'] = location(param['address'])
                tb = Storage 
            case "user":
                param['password'] = generate_password_hash(param['password'])
                tb = User
            case "record":
                tb = Record
                param.pop('username')
                param.pop('goodsname')
                if param['action'] == "入库":
                    count = param['count']
                elif param['action'] == "出库":
                    count = - param['count']
                db.session.query(Goods).filter_by(id=param['goods']).update(
                    {Goods.count: Goods.count + count})
        subquery = db.session.query(tb.id, func.row_number().over(
            order_by=tb.id).label('row_number')).subquery()
        max_id = db.session.query(func.max(subquery.c.id)).\
            filter(subquery.c.id == subquery.c.row_number).\
            scalar()
        if max_id:
            pass
        else:
            max_id = 0
        param['id'] = max_id+1
        db.session.add(tb(**param))
        db.session.commit()
        return Result(200, "成功").get_value(), 200
    except:
        return Result(400, "失败").get_value(), 200


@app.route('/<table>/update', methods=['POST'])
@token_required
def update(roleId, table):
    try:
        param = request.json
        match table:
            case "goodstype":
                tb = Goodstype(**param)
            case "goods":
                tb = Goods(**param)
            case "storage":
                param['location'] = location(param['address'])
                tb = Storage(**param)
            case "user":
                param['password'] = generate_password_hash(param['password'])
                tb = User(**param)
        db.session.merge(tb)
        db.session.commit()
        return Result(200, "成功").get_value(), 200
    except:
        return Result(400, "失败").get_value(), 400


@app.route('/<table>/del', methods=['GET'])
@token_required
def nodel(roleId, table):
    try:
        id = str_int(request.args.get("id"))
        match table:
            case "goodstype":
                tb = Goodstype
            case "goods":
                tb = Goods
            case "storage":
                tb = Storage
            case "user":
                tb = User
        re = tb.query.filter_by(id=id).first()
        db.session.delete(re)
        db.session.commit()
        return Result(200, "成功").get_value(), 200
    except Exception:
        db.session.rollback()
        return Result(400, "失败").get_value(), 200


"""
    select a.*,b.name goodsname,c.name storagename,d.name goodstypename,
        (select u.name from user u where u.id=a.userid)username,
        (select u.name from user u where u.id=a.admin_id)adminname
        from record a ,goods b,storage c,goodstype d
"""


@app.route('/record/listPage', methods=['POST', 'GET'])
@token_required
def recordlistPage(roleId):
    pageSize = request.json.get('pageSize')
    pageNum = request.json.get('pageNum')
    param = request.json.get('param')
    goods = param.get('name')
    storage = str_int(param.get('storage'))
    goodstype = str_int(param.get('goodstype'))
    roleId = int(param.get('roleId'))
    userId = int(param.get('userId'))
    User1 = aliased(User)
    User2 = aliased(User)
    results = db.session.query(Record, Goods.name.label('goodsname'), Storage.name.label('storagename'),
                              Goodstype.name.label(
                                  'goodstypename'), User1.name.label('username'),
                              User2.name.label('adminname'),)\
        .outerjoin(Goods, Record.goods == Goods.id)\
        .outerjoin(Storage, Goods.storage == Storage.id)\
        .outerjoin(Goodstype, Goods.goodstype == Goodstype.id)\
        .outerjoin(User1, Record.userId == User1.id)\
        .outerjoin(User2, Record.adminId == User2.id)\
        .filter(
        Goods.name.contains(goods) &
        or_(storage is None, Goods.storage == storage) &
        or_(goodstype is None, Goods.goodstype == goodstype)
    ).order_by(Record.id.desc()).paginate(page=pageNum, per_page=pageSize)
    data = []
    for record, goodsname, storagename, goodstypename, username, adminname in results:
        result = {
            'id': record.id,
            'goodsname': goodsname,
            'storagename': storagename,
            'action': record.action,
            'goodstypename': goodstypename,
            'username': username,
            'adminname': adminname,
            'count': record.count,
            'createtime': record.createtime,
            'remark': record.remark
        }
        data.append(result)
    return Result(200, "成功", results.total, data).get_value(), 200

@app.route('/storage/map')
@token_required
def query_goods_quantity(roleId):
    goods_quantities = db.session.query(Goodstype.name, Storage.name,Storage.location, db.func.sum(Goods.count).label('total_quantity'),Storage.address).\
        join(Goods, Goodstype.id == Goods.goodstype).join(Storage, Goods.storage == Storage.id).\
        group_by(Goodstype.id, Storage.id).all()
    groups = groupby(goods_quantities, key=lambda x: x[1])
    results={}
    for key, group in groups:
        if not results.get(key):
            results[key]=[]
        for i in group:
            groupi = list(i)
            results[key].append(groupi) 
    return Result(200, "成功", 0, results).get_value(), 200

def location(address):
    """{'status': '1', 'info': 'OK', 'infocode': '10000', 'count': '1', 'geocodes': [{'formatted_address': '北京市朝阳区阜通东大街6号', 'country': '中国', 'province': '北京市', 'citycode': '010', 'city': '北京市', 'district': '朝阳区', 'township': [], 'neighborhood': {'name': [], 'type': []}, 'building': {'name': [], 'type': []}, 'adcode': '110105', 'street': '阜通东大街', 'number': '6号', 'location': '116.482086,39.990496', 'level': '门牌号'}]}
    """
    geo=requests.get(f"https://restapi.amap.com/v3/geocode/geo?address={address}&output=JSON&key={config.KEY}")
    data=geo.json()
    if data["status"]=='1':
        return list(map(float,data["geocodes"][0]["location"].split(',')))
    else:
        return


default_no=config.default_no
default_password=config.default_password
with app.app_context():
    create_db_if_not_exists(default_no,default_password)
if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
                                                      
