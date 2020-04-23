from flask import Blueprint, render_template, session, redirect, request, url_for, flash
from ..models import User, Orders
from ..extension import db
from flask_paginate import Pagination, get_page_parameter
from ..blockchain import add_new_block
from werkzeug.security import check_password_hash, generate_password_hash

import time

admin_page = Blueprint('admin_page', __name__)

@admin_page.route('/userlist')
def index():
    return render_template('admin/index.html')

@admin_page.route('/admin_page/users')
def users(limit=10):
    id = session.get('user_id')
    user = User.query.get(id)
    data = User.query.all()
    page = int(request.args.get("page", 1))
    start = (page - 1) * limit
    end = page * limit if len(data) > page * limit else len(data)
    pagination = Pagination(css_framework='bootstrap4', page=page, total=len(data), outer_window=0, inner_window=1)
    ret = User.query.slice(start, end)
    return render_template("admin/user_manage.html", users=ret, pagination=pagination, user=user)

@admin_page.route('/admin_page/orders')
def orders(limit=10):
    id = session.get('user_id')
    user = User.query.get(id)
    data = Orders.query.all()
    page = int(request.args.get("page", 1))
    start = (page - 1) * limit
    end = page * limit if len(data) > page * limit else len(data)
    pagination = Pagination(css_framework='bootstrap4', page=page, total=len(data), outer_window=0, inner_window=1)
    ret = Orders.query.slice(start, end)
    return render_template("admin/order_manage.html", orders=ret, pagination=pagination, user=user)

@admin_page.route('/admin_page/user/edit/<id>', methods=['GET', 'POST'])
def user_edit(id):
    user = User.query.get(id)

    if request.method == 'GET':
        return render_template('admin/edit.html',user=user)
    else:
        username = request.form.get('username')
        password = request.form.get('password')
        gender = request.form.get('gender')
        email = request.form.get('email')
        if username == "" or password == "":
            flash('账号或者密码不能为空')
            return render_template('admin/edit.html', user=user)
        else:
            user.username = username
            user.password = generate_password_hash(password)
            user.gender = gender
            user.email = email
            db.session.commit()
            return redirect(url_for('admin_page.users'))

@admin_page.route('/admin_page/order/edit/<id>', methods=['GET', 'POST'])
def order_edit(id):
    order = Orders.query.get(id)

    if request.method == 'GET':
        return render_template('admin/order_edit.html',order=order)
    else:
        order.o_name = request.form.get('o_name')
        order.o_time = request.form.get('o_time')
        order.location = request.form.get('location')
        order.person = request.form.get('person')
        order.tel = request.form.get('tel')
        order.desc = request.form.get('desc')
        order.comp = request.form.get('comp')
        order.comp_id = request.form.get('com_id')
        order.status = request.form.get('status')


        db.session.commit()
        add_new_block("管理员修改", order.id)

        return redirect(url_for('admin_page.orders'))

@admin_page.route('/admin_page/user/delete/<id>')
def user_delete(id):
    user = User.query.get(id)
    db.session.delete(user)
    db.session.commit()
    return redirect(url_for('admin_page.users'))

@admin_page.route('/admin_page/order/delete/<id>')
def order_delete(id):
    order = Orders.query.get(id)
    #add_new_block("管理员删除", order.id)
    db.session.delete(order)
    db.session.commit()

    return redirect(url_for('admin_page.orders'))

@admin_page.route('/admin_page/user/add', methods=['GET', 'POST'])
def user_add():

    if request.method == 'GET':
        return render_template('admin/add.html')
    else:
        username = request.form.get('username')
        password = request.form.get('password')
        gender = request.form.get('gender')
        email = request.form.get('email')
        types = request.form.get('types')
        user = User(username, email, password,types, gender)
        if username == "" or password == "":
            flash('账号或者密码不能为空')
            return render_template('admin/add.html')
        else:
            db.session.add(user)
            db.session.commit()
            return redirect(url_for('admin_page.users'))

@admin_page.route('/admin_page/order/add', methods=['GET', 'POST'])
def order_add():

    if request.method == 'GET':
        return render_template('admin/order_add.html')
    else:
        o_name = request.form.get('o_name')
        o_time  = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
        location = request.form.get('location')
        person = request.form.get('person')
        tel = request.form.get('tel')
        desc = request.form.get('desc')
        comp = request.form.get('comp')
        status = request.form.get('status')
        comp_id = request.form.get('com_id')
        order = Orders(o_name, o_time, location, person, tel, desc, comp, status, comp_id=comp_id )
        if o_name == "" or location == "":
            flash('商品名或者初始地不能为空')
            return render_template('admin/order_add.html')
        else:
            db.session.add(order)
            db.session.commit()
            add_new_block("管理员新增", order.id)

            return redirect(url_for('admin_page.orders'))

@admin_page.route('/orderslist/query', methods=[ 'POST'])
def query():
    id = request.form.get('o_id')
    order = Orders.query.get(id)
    if(order):
        return render_template("admin/orders_query.html", order=order)
    else:
        return render_template('error_page.html', message="查询结果不存在")


@admin_page.route('/orderslist/query_user', methods=[ 'POST'])
def query_user():
    id = request.form.get('u_id')
    user = User.query.get(id)
    if(user):
        return render_template("admin/user_query.html", user=user)
    else:
        return render_template('error_page.html', message="查询结果不存在")
