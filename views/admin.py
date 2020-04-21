from flask import Blueprint, render_template, session, redirect, request, url_for, flash
from ..models import User, Orders
from ..extension import db
from flask_paginate import Pagination, get_page_parameter

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

        user.username = username
        user.password = password
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
        order.status = request.form.get('status')

        db.session.commit()
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
        order = Orders(o_name, o_time, location, person, tel, desc, comp, status )
        db.session.add(order)

        db.session.commit()
        return redirect(url_for('admin_page.orders'))