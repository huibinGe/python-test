from flask import Blueprint, render_template, session, redirect, request, url_for, flash
from sqlalchemy import or_
from ..models import Orders
from ..extension import db
import time

logics_page = Blueprint('logistics_page', __name__)


@logics_page.route('/logisticslist')
def list_all_orders():
    orders = Orders.query.filter(or_(Orders.status == "已入仓", Orders.status == "已发货")).all()
    return render_template("logistics/logisticslist.html", orders=orders)


@logics_page.route('/logistics/delete/<int:id>')
def delete_orders(id):
    result = Orders.query.filter(Orders.id == id).first()
    db.session.delete(result)
    db.session.commit()
    orders = Orders.query.filter(or_(Orders.status == "已发货", Orders.status == "已入仓")).all()
    return render_template("logistics/logisticslist.html", orders=orders)


# @logics_page.route('/logistics/ship', methods=['GET', 'PoSt'])
# def ship():
#     id = request.form.get('id')
#     o_name = request.form.get('o_name')
#     o_time = request.form.get('o_time')
#     location = request.form.get('location')
#     person = request.form.get('person')
#     tel = request.form.get('tel')
#     desc = request.form.get('desc')
#     status = request.form.get('status')
#     ord = Orders.query.filter(Orders.id == int(id)).first()
#     ord.o_name = o_name
#     ord.o_time = o_time
#     ord.location = location
#     ord.person = person
#     ord.tel = tel
#     ord.desc = desc
#     ord.status = "已发货"
#     db.session.add(ord)
#     db.session.commit()
#     return render_template('logistics/ship_success.html')

# 发货英文翻译：ship
@logics_page.route('/logistics/outc/<int:id>', methods=['GET', 'PoSt'])
def outc(id):
    order = Orders.query.get(id)
    if request.method == 'GET':
        if order.status == "已发货":
            message = "商品已经发货，无法发货"
            return render_template('logistics/error_page.html', message=message)
        else:
            return render_template('logistics/outc.html', order=order)
    else:
        id = request.form.get("id")
        desc = request.form.get("desc")
        tel = request.form.get("tel")
        person = request.form.get("person")
        order = Orders.query.get(id)
        order.desc = desc
        order.tel = tel
        order.person = person
        order.status = "已发货"
        order.o_time = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
        db.session.add(order)
        db.session.commit()
        orders = Orders.query.filter(or_(Orders.status == "已入仓", Orders.status == "已发货")).all()
        return render_template("logistics/error_page.html", message="发货成功")


@logics_page.route('/logistics/add', methods=['GET', 'POST'])
def add():
    # id = request.form.get('id')
    o_name = request.form.get('o_name')
    o_time = request.form.get('o_time')
    location = request.form.get('location')
    person = request.form.get('person')
    tel = request.form.get('tel')
    desc = request.form.get('desc')
    comp = request.form.get('comp')
    status = request.form.get('status')
    ord = Orders(o_name, o_time, location, person, tel, desc, comp, status)
    db.session.add(ord)
    db.session.commit()
    # orders = Orders.query.all()
    orders = Orders.query.filter(or_(Orders.status == "已入仓", Orders.status == "已发货")).all()
    return render_template('logistics/logisticslist.html', orders=orders)


@logics_page.route('/logistics/query', methods=['GET', 'POST'])
def query():
    # o_name = request.form.get('o_name')
    # orders = Orders.query.filter(or_(Orders.status == "已发货", Orders.status == "已入仓")).all()
    # orders = Orders.query.filter(Orders.o_name == o_name, or_(Orders.status == "已发货", Orders.status == "已入仓")).all()
    id = request.form.get('o_id')
    order = Orders.query.get(id)
    return render_template('logistics/logistics_query.html', order=order)