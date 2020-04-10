from flask import Flask, render_template, url_for, request, redirect, session, flash
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://root:11111111@localhost:3306/user2'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.secret_key = "lalskskskskksksjsj"

db = SQLAlchemy(app)
class User(db.Model):
    __tablename__ = 'user'
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True)
    password = db.Column(db.String(120))
    def __init__(self, username, email, password):
        self.username = username
        self.email = email
        self.password = password

    def __repr__(self):
        return '<User1 %r>' % self.username

@app.route('/users')
def users():
    if session.get('user_id'):
        users = User.query.all()
        return render_template('index.html', users=users)
    else:
        return redirect('/')
def index(name):
    return render_template('index.html', name=name)
@app.route('/')
@app.route('/login', methods=['GET', 'PoSt'])
def login():
    if request.method == 'GET':
        return render_template('login.html')
    else:
        name = request.form.get('name')
        pwd = request.form.get('password')

        user = User.query.filter(User.username==name).first()

        if user and user.password == pwd:
            session['user_id'] = user.id
            return redirect(url_for('users'))
        else:
            flash("登陆失败")
            return render_template('login.html')
'''
class Role(db.Model):
    __tablename__ = 'roles'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(64), unique=True)
    users = db.relationship('User', backref='role')

    def __repr__(self):
        return "<Role %r>"%self.name


class User(db.Model):
    __tablename__ = 'users'

    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(64), unique=True)
    role_id = db.Column(db.Integer, db.ForeignKey('roles.id'))

    def __repe__(self):
        return "<User %r>"%self.username
'''
def add_data():
    db.drop_all()
    db.create_all()
    #admin_role = Role(name='Admin')
    #mod_role = Role(name='Moderator')
    #user_role = Role(name='User')
    user_john = User(username='john', email='john@126.com', password='111111')
    user_susan = User(username='susan', email='susan@126.com', password='222222')
    user_david = User(username='david',  email='david@126.com', password='333333')

    #db.session.add(admin_role)
    #db.session.add(mod_role)
    #db.session.add(user_role)
    db.session.add(user_john)
    db.session.add(user_susan)
    db.session.add(user_david)

    db.session.commit()
