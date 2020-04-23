from flask import Blueprint, render_template, session, redirect, request, url_for, flash
from sqlalchemy import or_
from ..models import  Orders, User
from ..extension import db
from flask_paginate import Pagination, get_page_parameter
import time
from ..zmqpublisher import publisher
from ..blockchain import add_new_block
import threading
import os
import json

_basepath = os.path.abspath(os.path.dirname(__file__))
conf = json.load(open(os.path.abspath(os.path.dirname(__file__))+"/../conf.json"))

buss_page = Blueprint('bussiness_page', __name__)

@buss_page.route('/corderslist')
def list_all_orders(limit=10):
    id = session.get('user_id')
    user = User.query.get(id)
    data = Orders.query.filter(or_(Orders.status=="已出厂", Orders.status=="已生产")).all()
    page = int(request.args.get("page", 1))
    start = (page - 1) * limit
    end = page * limit if len(data) > page * limit else len(data)
    pagination = Pagination(css_framework='bootstrap4', page=page, total=len(data), outer_window=0, inner_window=1)
    ret = Orders.query.filter(or_(Orders.status=="已出厂", Orders.status=="已生产")).slice(start, end)
    return render_template("bussiness/orderslist.html", orders=ret, pagination=pagination, user=user)


@buss_page.route('/corderslist/query', methods=[ 'POST'])
def query():
    id = request.form.get('o_id')
    order = Orders.query.get(id)
    return render_template("bussiness/orders_query.html", order=order)

@buss_page.route('/outc/<id>', methods=['GET', 'POSt'])
def outc(id):
    order = Orders.query.get(id)
    if request.method == 'GET':
        if order.status=="已出厂":
            message = "商品已经出厂，无法出厂"
            return render_template('error_page.html', message=message)
        else:
            return render_template('bussiness/outc.html', order=order)
    else:
        id = request.form.get("id")
        desc =request.form.get("desc")
        tel = request.form.get("tel")
        person = request.form.get("person")
        order = Orders.query.get(id)
        order.desc = desc
        order.tel =tel
        order.person = person
        order.status = "已出厂"
        order.o_time = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
        db.session.add(order)
        db.session.commit()
        add_new_block("生产商出厂", order.id)
        return redirect(url_for('login_page.users'))

        #return redirect(url_for('login_page.users'))


@buss_page.route('/add', methods=['GET', 'POSt'])
def add():
    if request.method == 'GET':
        return render_template('bussiness/add.html')
    else:
        o_name = request.form.get("o_name")
        location = request.form.get("location")
        o_time  = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
        status = "已生产"
        person = "无"
        tel = "无"
        desc = "无"
        comp = "无"
        order = Orders(o_name, o_time, location, person, tel, desc, comp, status )
        db.session.add(order)
        db.session.commit()
        add_new_block("生产商出厂", order.id)
        return redirect(url_for('login_page.users'))

        #return render_template("bussiness/error_page.html", message="新增成功")


