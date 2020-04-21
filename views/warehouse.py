from flask import Blueprint, render_template, session, redirect, request, url_for, flash
from ..models import Orders, User
from ..extension import db
from sqlalchemy import or_
import time
from flask_paginate import Pagination

ware_page = Blueprint('warehouse_page', __name__)


@ware_page.route('/warehouselist')
def list_all_commodities(limit=10):
    id = session.get('user_id')
    user = User.query.get(id)
    data = Orders.query.filter(or_(Orders.status=="已出厂", Orders.status=="已入仓")).all()
    page = int(request.args.get("page", 1))
    start = (page - 1) * limit
    end = page * limit if len(data) > page * limit else len(data)
    pagination = Pagination(css_framework='bootstrap4', page=page, total=len(data), outer_window=0, inner_window=1)
    ret = Orders.query.filter(or_(Orders.status=="已出厂", Orders.status=="已入仓")).slice(start, end)
    return render_template("warehouse/warehouselist.html", orders=ret, pagination=pagination, user=user)

@ware_page.route('/warehouselist/delete/<int:id>')
def delete_commodities(id):
    result = Orders.query.filter(Orders.id==id).first()
    db.session.delete(result)
    db.session.commit()
    warehouse = Orders.query.all()
    return render_template("warehouse/warehouselist.html", orders=warehouse)





@ware_page.route('/warehouselist/query',methods=['GET', 'POST'])
def query():
    o_id = request.form.get('o_id')
    warehouse = Orders.query.filter(Orders.id==o_id).first()
    return render_template('warehouse/warehouse_query.html', orders=warehouse)

@ware_page.route('/out/<id>', methods=['GET', 'POSt'])
def out(id):
    order = Orders.query.get(id)
    if request.method == 'GET':
        if order.status=="已入仓":
            message = "商品已经入仓，无法入仓"
            return render_template('warehouse/error_page.html', message=message)
        else:
            return render_template("warehouse/out.html", order=order)
    else:
        id = request.form.get("id")
        desc =request.form.get("desc")
        order = Orders.query.get(id)
        order.desc = desc
        order.status = "已入仓"
        order.o_time = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
        db.session.add(order)
        db.session.commit()
        return render_template("warehouse/error_page.html", message="入仓成功")





