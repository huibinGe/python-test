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

class Orders(db.Model):
    __tablename__ = 'Orders'
    #物流
    id = db.Column(db.Integer, primary_key=True)
    o_name = db.Column(db.String(80), unique=True, nullable=True, default='')
    o_time = db.Column(db.DateTime, nullable=True)
    location = db.Column(db.String(80), unique=False, nullable=True, default='')
    person = db.Column(db.String(20), unique=False, nullable=True)
    tel = db.Column(db.String(80), unique=False, nullable=True)
    desc = db.Column(db.String(200), unique=False, nullable=True)
    status = db.Column(db.String(5), unique=False, nullable=True)

    def __init__(self, o_name, o_time, location, person, tel, desc, status):
        self.o_name = o_name
        self.o_time = o_time
        self.location = location
        self.person = person
        self.tel = tel
        self.desc = desc
        self.status = status


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



