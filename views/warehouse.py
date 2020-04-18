from flask import Blueprint, render_template, session, redirect, request, url_for, flash
from ..models import Warehouse
from ..extension import db
import time
ware_page = Blueprint('warehouse_page', __name__)


@ware_page.route('/warehouselist')
def list_all_commodities():
    warehouse = Warehouse.query.all()
    return render_template("warehouse/warehouselist.html", warehouse=warehouse)


@ware_page.route('/warehouselist/delete/<int:id>')
def delete_commodities(id):
    result = Warehouse.query.filter(Warehouse.id==id).first()
    db.session.delete(result)
    db.session.commit()
    warehouse = Warehouse.query.all()
    return render_template("warehouse/warehouselist.html", warehouse=warehouse)



@ware_page.route('/warehouselist/edit', methods=['GET', 'PoSt'])
def edit():
        id = request.form.get('id')
        name = request.form.get('name')
        price = request.form.get('price')
        location=request.form.get('location')
        i_time=time.localtime(time.time())
        co = Warehouse.query.filter(Warehouse.id == int(id)).first()
        co.name = name
        co.price = price
        co.location=location
        co.i_time=i_time
        co.status="已入仓"
        db.session.add(co)
        db.session.commit()
        commodity = Commodity.query.all()
        return render_template('warehouse/warehouse_success.html')


@ware_page.route('/warehouselist/query',methods=['GET', 'POST'])
def query():
    name = request.form.get('name')
    warehouse = Warehouse.query.filter(Warehouse.name==name).first()
    print(111111)
    return render_template('warehouse/warehouse_query.html', warehouse=warehouse)





