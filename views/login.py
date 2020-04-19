from flask import Blueprint, render_template, session, redirect, request, url_for, flash
from ..models import User, create_data
from ..extension import db

login_page = Blueprint('login_page', __name__)


@login_page.route('/login_page')
def users():
    id = session.get('user_id')
    if id:
        user = User.query.get(int(id))
        if user.types== "管理员":
            return render_template('admin/index.html')
        else:
            return render_template('login/index.html', user=user)
    else:
        return redirect('/')


@login_page.route('/')
@login_page.route('/login', methods=['GET', 'PoSt'])
def login():
    if request.method == 'GET':
        return render_template('login/login.html')
    else:
        name = request.form.get('name')
        pwd = request.form.get('password')

        user = User.query.filter(User.username == name).first()

        if user and user.password == pwd:
            session['user_id'] = user.id
            return redirect(url_for('login_page.users'))
        else:
            flash('登陆失败')
            return render_template('login/login.html')

@login_page.route('/addinitdata', methods=['GET', 'POST'])
def addinitdata():
    if request.method == 'POST':
        create_data()
        return render_template('login/login.html')



@login_page.route('/user_index/<id>', methods=['GET', 'POST'])
def edit(id):
    user = User.query.get(id)

    if request.method == 'GET':
        return render_template('login/edit.html',user=user)
    else:
        username = request.form.get('username')
        password = request.form.get('password')
        gender = request.form.get('gender')
        email = request.form.get('email')

        user.username = username
        user.password = password
        user.gender = gender
        user.email = email
        db.session.commit()
        session['user_id'] = user.id
        return redirect(url_for('login_page.users'))

@login_page.route('/go_page/<id>')
def go_page(id):
    user = User.query.get(id)
    if user.types == "厂商":
        return render_template('bussiness/index.html')
    elif user.types == "商家":
        return render_template('customer/index.html')
    elif user.types == "物流公司":
        return render_template('logistics/index.html')
    elif user.types == "仓库":
        return render_template('warehouse/index.html')

