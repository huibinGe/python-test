from flask import Blueprint, render_template, session, redirect, request, url_for, flash
from ..models import Commodity
from ..extension import db
buss_page = Blueprint('bussiness_page', __name__)


@buss_page.route('/commoditylist')
def list_all_commodities():
    commodity = Commodity.query.all()
    return render_template("bussiness/commoditylist.html", commodity=commodity)


@buss_page.route('/commoditylist/delete/<int:id>')
def delete_commodities(id):
    result = Commodity.query.filter(Commodity.id==id).first()
    db.session.delete(result)
    db.session.commit()
    commodity = Commodity.query.all()
    return render_template("bussiness/commoditylist.html", commodity=commodity)



@buss_page.route('/commoditylist/edit', methods=['GET', 'PoSt'])
def edit():
        id = request.form.get('id')
        name = request.form.get('name')
        price = request.form.get('price')
        co = Commodity.query.filter(Commodity.id == int(id)).first()
        co.name = name
        co.price = price
        db.session.add(co)
        db.session.commit()
        commodity = Commodity.query.all()
        return render_template('bussiness/editcommo_success.html')
@buss_page.route('/commoditylist/add', methods=['GET', 'POST'])
def add():
        name = request.form.get('name')
        price = request.form.get('price')
        co = Commodity("name", price)
        db.session.add(co)
        db.session.commit()
        commodity = Commodity.query.all()
        return render_template('bussiness/commoditylist.html', commodity=commodity)

@buss_page.route('/commoditylist/query',methods=['GET', 'POST'])
def query():
    name = request.form.get('name')
    commodity = Commodity.query.filter(Commodity.name==name).first()
    print(111111)
    return render_template('bussiness/commodity_query.html', commodity=commodity)





