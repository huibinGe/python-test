from .extension import  db
class User(db.Model):
    __tablename__ = 'user'
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True)
    password = db.Column(db.String(120))
    types = db.Column(db.String(120))
    def __init__(self, username, email, password, types):
        self.username = username
        self.email = email
        self.password = password
        self.types = types

    def __repr__(self):
        return '<User1 %r>' % self.username

class Commodity(db.Model):
    #商品
    __tablename__ = 'commodity'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80), unique=True, nullable=False)
    price =  db.Column(db.Integer, unique=False, nullable=False)
    def __init__(self, name, price):
        self.name = name
        self.price = price

    def __repr__(self):
        return '<Commodity %r>' % self.name

class Logistics(db.Model):
    __tablename__ = 'Logistics'
    #物流
    id = db.Column(db.Integer, primary_key=True)
    order_id = db.Column(db.Integer, db.ForeignKey('order.id')) ##使用order的id
    froms = db.Column(db.String(80), unique=False, nullable=False) #始发地
    tos = db.Column(db.String(80), unique=False, nullable=False) #目的地
    tel = db.Column(db.String(80), nullable=False)
    eve_time = db.Column(db.DateTime, nullable=True)
    def __init__(self, order_id, froms, tos, tel, eve_time):
        self.order_id = order_id
        self.froms = froms
        self.tos = tos
        self.tel = tel
        self.eve_time = eve_time

class Order(db.Model):
    #订单
    __tablename__ = 'order'
    id = db.Column(db.Integer, primary_key=True)
    b_name =  db.Column(db.String(80), unique=False, nullable=False)#客户名字
    c_name = db.Column(db.String(80), unique=False, nullable=False)#商品名
    def __init__(self, b_name, c_name):
        self.b_name = b_name
        self.c_name = c_name


def create_data():
    db.drop_all()
    db.create_all()
    user1 = User("张三", "111@qq.com", "111111", "商家")
    user2 = User("李四", "222@qq.com", "222222", "用户")
    user3 = User("王五", "333@qq.com", "333333", "物流公司")
    c1 = Commodity("王老吉", 5)
    c2 = Commodity("可口可乐", 3)
    c3 = Commodity("旺旺雪饼", 4)
    db.session.add(user1)
    db.session.add(user2)
    db.session.add(user3)
    db.session.add(c1)
    db.session.add(c2)
    db.session.add(c3)
    db.session.commit()



