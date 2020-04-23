from flask import Blueprint, render_template, session, redirect, request, url_for, flash
from sqlalchemy import or_
from ..models import Orders, User
from ..extension import db
from flask_paginate import Pagination, get_page_parameter
from ..blockchain import add_new_block

import time

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
    return render_template("orderslist.html", orders=ret, pagination=pagination, user=user, type="商家", ops="收货", hre='customer_page.receive')

    #return render_template("customer/orderslist.html", orders=ret, pagination=pagination, user=user)

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
            return render_template('error_page.html', message=message)

        else:
            ord.o_time = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
            ord.status = "已签收"
            db.session.add(ord)
            db.session.commit()
            add_new_block("商家收货", ord.id)

            return redirect(url_for('login_page.users'))






