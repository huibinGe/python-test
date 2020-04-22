from flask import Blueprint, render_template, session, redirect, request, url_for, flash
from ..models import User, create_data, Orders
from ..extension import db
from .blockchain import get_all_blocks
from werkzeug.security import check_password_hash, generate_password_hash

login_page = Blueprint('login_page', __name__)


@login_page.route('/login_page')
def users():
    id = session.get('user_id')
    if id:
        user = User.query.get(int(id))
        if user.types== "管理员":
            return redirect(url_for('admin_page.orders'))
        elif user.types == "厂商":
            return redirect(url_for('bussiness_page.list_all_orders'))
        elif user.types == "商家":
            return redirect(url_for('customer_page.list_all_orders'))
        elif user.types == "物流公司":
            return redirect(url_for('logistics_page.list_all_commodities'))
        elif user.types == "仓库":
            return redirect(url_for('warehouse_page.list_all_commodities'))
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

        if user and check_password_hash(user.password, pwd):
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
        old_password = request.form.get('old_password')
        password = request.form.get('new_password')
        gender = request.form.get('gender')
        email = request.form.get('email')

        if not check_password_hash(user.password, old_password):
            flash("原密码输入错误")
            return render_template('login/edit.html', user=user)

        user.username = username
        user.password = generate_password_hash(password)
        user.gender = gender
        user.email = email
        db.session.commit()
        message = "修改成功"
        return render_template('login/error_page.html', message=message)

@login_page.route('/exit', methods=['GET', 'POST'])
def exit():
    return render_template('login/login.html')

@login_page.route('/show_detail/<order_id>')
def show_detail(order_id):
    order = Orders.query.get(order_id)
    block_in_chain = get_all_blocks(order_id)
    if len(block_in_chain) != 0:
        block = block_in_chain[-1]
        message = block.history
        messages = message.split('\n')
        if messages[-1] == "":
            messages = messages[:-1]
    else:
        messages = ""
    return render_template('showdetail.html', order=order, messages=messages)