from flask import Blueprint, render_template, session, redirect, request, url_for, flash
from sqlalchemy import or_
from ..models import Commodity, Orders
from ..extension import db
import time
buss_page = Blueprint('bussiness_page', __name__)

@buss_page.route('/corderslist')
def list_all_orders():
    orders = Orders.query.filter(or_(Orders.status=="已出厂", Orders.status=="已生产")).all()
    return render_template("bussiness/orderslist.html", orders=orders)

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
            return render_template('bussiness/error_page.html', message=message)
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
        orders = Orders.query.filter(or_(Orders.status == "已出厂", Orders.status == "已生产")).all()
        return render_template("bussiness/error_page.html", message="出仓成功")

@buss_page.route('/add', methods=['GET', 'POSt'])
def add():
    if request.method == 'GET':
        return render_template('bussiness/add.html')
    else:
        o_name = request.form.get("o_name")
        location = request.form.get("location")
        o_time  = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
        status = "已生产"
        person = ""
        tel = ""
        desc = ""
        comp = ""
        order = Orders(o_name, o_time, location, person, tel, desc, comp, status )
        db.session.add(order)
        db.session.commit()
        return render_template("bussiness/error_page.html", message="新增成功")


