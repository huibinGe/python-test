from flask import Blueprint, render_template, session, redirect, request, url_for, flash
from ..models import User, create_data

login_page = Blueprint('login_page', __name__)


@login_page.route('/login_page')
def users():
    if session.get('user_id'):
        users = User.query.all()
        return render_template('login/index.html', users=users)
    else:
        return redirect('/')


@login_page.route('/')
@login_page.route('/login', methods=['GET', 'PoSt'])
def login():
    if request.method == 'GET':
        return render_template('login/login.html')
    else:
        name = request.form.get('name')
        pwd = request.form.get('password')

        user = User.query.filter(User.username == name).first()

        if user and user.password == pwd:
            if user.types == "商家":
                return render_template('bussiness/index.html')
            else:
                session['user_id'] = user.id
                return redirect(url_for('user_page.users'))
        else:
            flash('登陆失败')
            return render_template('login/login.html')

@login_page.route('/addinitdata', methods=['GET', 'POST'])
def addinitdata():
    if request.method == 'POST':
        create_data()
        return render_template('login/login.html')



