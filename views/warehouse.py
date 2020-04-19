from flask import Blueprint, render_template, session, redirect, request, url_for, flash
from ..models import Orders
from ..extension import db
from sqlalchemy import or_
import time
ware_page = Blueprint('warehouse_page', __name__)


@ware_page.route('/warehouselist')
def list_all_commodities():
    warehouse = Orders.query.filter(or_(Orders.status=="已出厂", Orders.status=="已入仓")).all()
    return render_template("warehouse/warehouselist.html", orders=warehouse)


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
        orders = Orders.query.filter(or_(Orders.status == "已出厂", Orders.status == "已入仓")).all()
        return render_template("warehouse/warehouselist.html", orders=orders)





