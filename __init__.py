from flask import Flask
from .views.login import login_page
from .views.bussiness import buss_page
from .views.customer import cus_page
from .views.logistics import logics_page
from .views.warehouse import  ware_page
from .views.admin import admin_page
from .extension import db
app = Flask('python-test')
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://root:Py1438222@localhost:3306/python_sql'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.secret_key = "lalskskskskksksjsj"
db.init_app(app)

app.register_blueprint(login_page)
app.register_blueprint(buss_page)
app.register_blueprint(cus_page)
app.register_blueprint(logics_page)
app.register_blueprint(ware_page)
app.register_blueprint(admin_page)


