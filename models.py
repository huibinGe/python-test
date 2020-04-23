from .extension import  db
from werkzeug.security import generate_password_hash

class User(db.Model):
    __tablename__ = 'user'
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True)
    password = db.Column(db.String(120))
    types = db.Column(db.String(120))
    gender = db.Column(db.Integer, default=0)
    def __init__(self, username, email, password, types, gender):
        self.username = username
        self.email = email
        self.password = generate_password_hash(password)
        self.types = types
        self.gender = gender

    def __repr__(self):
        return '<User1 %r>' % self.username

class BlockChain(db.Model):
    #商品
    __tablename__ = 'blockchain'
    id = db.Column(db.Integer, primary_key=True)
    order_id = db.Column(db.Integer, unique=False, nullable=True)
    chain_index = db.Column(db.Integer, unique= False, default=0)
    current_hash = db.Column(db.String(200), unique=False, nullable=True)
    pre_hash = db.Column(db.String(200), unique=False, nullable=True)
    history = db.Column(db.String(1000), unique=False, nullable=True)
    little_h = db.Column(db.String(600), unique=False, nullable=True)
    random_num = db.Column(db.Integer, unique=False, nullable=True)


    def __repr__(self):
        return '<Commodity %r>' % self.name

class Orders(db.Model):
    __tablename__ = 'Orders'
    #物流
    id = db.Column(db.Integer, primary_key=True)
    o_name = db.Column(db.String(80), unique=False, nullable=True, default='')#商品名
    o_time = db.Column(db.DateTime, nullable=True)
    location = db.Column(db.String(80), unique=False, nullable=True, default='')#初始地
    person = db.Column(db.String(20), unique=False, nullable=True, default='')
    tel = db.Column(db.String(80), unique=False, nullable=True)
    desc = db.Column(db.String(200), unique=False, nullable=True)#目的地
    comp = db.Column(db.String(100), unique=False, nullable=True, default='')
    status = db.Column(db.String(5), unique=False, nullable=True)
    qrcode = db.Column(db.Text(200), unique = False,nullable=True)
    comp_id = db.Column(db.String(100), unique=False, nullable=True, default='')

    def __init__(self, o_name, o_time, location, person, tel, desc,comp, status, qrcode="", comp_id=""):
        self.o_name = o_name
        self.o_time = o_time
        self.location = location
        self.person = person
        self.tel = tel
        self.desc = desc
        self.comp = comp
        self.status = status
        self.qrcode = qrcode
        self.comp_id = comp_id


def create_data():
    db.drop_all()
    db.create_all()
    user1 = User("张三", "111@qq.com", "111111", "厂商", 0)
    user2 = User("李四", "222@qq.com", "222222", "商家", 0)
    user3 = User("王五", "333@qq.com", "333333", "物流公司", 0)
    user4 = User("王六", "444@qq.com", "444444", "仓库", 0)
    user5 = User("admin", "666@qq.com", "111111", "管理员", 0)

    o1 = Orders("王老吉",'2019-03-13 11:35:52.13',"杭州","李四","13843558644","西安","","已生产")
    o2 = Orders("可口可乐",'2019-04-05 06:33:35.33',"上海","李四","13843558644","贵阳","","已入仓")
    o3 = Orders("旺旺雪饼",'2019-03-05 01:53:55.63',"福州","李四","13843558644","西安","申通","已发货",comp_id="123455678")
    o4 = Orders("旺旺雪饼",'2019-04-05 01:53:55.63',"福州","李四","13843558644","西安","顺丰","已签收",comp_id="123455678")
    o5 = Orders("旺旺雪饼",'2019-04-06 01:53:55.63',"福州","霍六","1384355865","福州","","已出厂")
    o6 = Orders("旺旺雪饼",'2019-04-05 01:53:55.63',"福州","李四","13843558644","西安","顺丰","已发货",comp_id="123455678")
    o7 = Orders("旺旺雪饼",'2019-04-05 01:53:55.63',"福州","张三","13843558645","","","已生产")


    db.session.add(user1)
    db.session.add(user2)
    db.session.add(user3)
    db.session.add(user4)
    db.session.add(user5)
    db.session.add(o1)
    db.session.add(o2)
    db.session.add(o3)
    db.session.add(o4)
    db.session.add(o5)
    db.session.add(o6)
    db.session.add(o7)
    db.session.commit()



