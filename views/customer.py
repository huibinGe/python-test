from flask import Blueprint, render_template, session, redirect, request, url_for, flash
from sqlalchemy import or_
from ..models import Orders, User
from ..extension import db
from flask_paginate import Pagination, get_page_parameter

cus_page = Blueprint('customer_page', __name__)


@cus_page.route('/orderslist')
def list_all_orders(limit=10):
    id = session.get('user_id')
    user = User.query.get(id)
    data = Orders.query.filter(or_(Orders.status=="已发货", Orders.status=="已签收")).all()
    page = int(request.args.get("page", 1))
    start = (page - 1) * limit
    end = page * limit if len(data) > page * limit else len(data)
    pagination = Pagination(css_framework='bootstrap4', page=page, total=len(data), outer_window=0, inner_window=1)
    ret = Orders.query.filter(or_(Orders.status=="已发货", Orders.status=="已签收")).slice(start, end)
    return render_template("customer/orderslist.html", orders=ret, pagination=pagination, user=user)

@cus_page.route('/orderslist/delete/<int:id>')
def delete_orders(id):
    result = Orders.query.filter(Orders.id==id).first()
    db.session.delete(result)
    db.session.commit()
    orders = Orders.query.filter(or_(Orders.status=="已发货", Orders.status=="已签收")).all()
    return render_template("customer/orderslist.html", orders=orders)



@cus_page.route('/orderslist/receive/<int:id>', methods=['GET', 'PoSt'])
def receive(id):
        ord = Orders.query.get(id)
        if ord.status == "已签收":
            message = "商品已被签收，无法签收"
            return render_template('customer/error_page.html', message=message)

        else:
            ord.status = "已签收"
            db.session.add(ord)
            db.session.commit()
            return render_template('customer/error_page.html',message="签收成功")

@cus_page.route('/orderslist/add', methods=['GET', 'POST'])
def add():
        id = request.form.get('id')
        o_name = request.form.get('o_name')
        o_time = request.form.get('o_time')
        location = request.form.get('location')
        person = request.form.get('person')
        tel = request.form.get('tel')
        desc = request.form.get('desc')
        status = request.form.get('status')
        ord = Orders("o_name",person,tel,desc)
        db.session.add(ord)
        db.session.commit()
        orders = Orders.query.all()
        return render_template('customer/orderslist.html', orders=orders)

@cus_page.route('/orderslist/query',methods=['GET', 'POST'])
def query():
    o_id = request.form.get('o_id')
    orders = Orders.query.filter(Orders.id==o_id).first()
    return render_template('customer/orders_query.html', orders=orders)





