from types import NoneType
from flask import Flask, render_template, flash, request, make_response, redirect, url_for
from db_forms import *
from markupsafe import Markup
from flask_wtf.csrf import CSRFProtect
import os
from sqlalchemy import  create_engine, or_, and_
from sqlalchemy.orm import sessionmaker
from models import *

app = Flask(__name__)
app.config['SECRET_KEY'] = os.urandom(12).hex()
csrf = CSRFProtect(app)

engine = create_engine("mysql+pymysql://root:35678@127.0.0.1/pc_parts")
Session = sessionmaker(bind=engine)

def get_user():
    user_id = request.cookies.get('user_id')
    if user_id:
        with Session() as db:
            user = db.query(Users).filter_by(id=user_id).first()
        if user:
            name = user.first_name
            return name
    else:
        return False

@app.route('/')
def index():
    username = get_user()
    return render_template('index.html', username=username)

@app.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    username = get_user()
    if request.method == 'POST' and form.validate():
        login_str = form.login.data
        password_str = form.password.data
        with Session() as db:
            user = db.query(Users).filter(or_(Users.login == login_str, Users.password_ == password_str)).first()
        if user:
            if user.login == login_str or user.password_ == password_str:
                flash(Markup('<h3>Вы успешно зашли в аккаунт</h3>'))
                flash(Markup(f'<p>Тип аккаунта: {user.account_type}</p>'))
                response = make_response(render_template('login_msg.html', form=form, username=username))
                response.set_cookie('user_id', str(user.id), max_age=60 * 60 * 24)
                return response
        else:
            flash(Markup('<h3>Неверное имя пользователя или пароль</h3>'))

    return render_template('login.html', form=form, username=username)

@app.route('/register', methods=['GET', 'POST'])
def register():
    form = RegisterForm()
    username = get_user()
    if request.method == 'POST' and form.validate():
        login_str = form.login.data
        e_mail_str = form.e_mail.data
        f_name_str = form.first_name.data
        l_name_str = form.last_name.data
        phone_str = form.phone.data
        password_str = form.password.data
        with Session() as db:
            user = db.query(Users).filter(or_(Users.login == login_str, Users.e_mail == e_mail_str)).first()
        if user:
            if user.login == login_str or user.e_mail == e_mail_str:
                flash(Markup('<h3>Такой пользователь уже существует</h3>'))
        else:
            with Session() as db:
                new_user = Users(login=login_str, first_name=f_name_str, last_name=l_name_str, e_mail=e_mail_str, phone_number=phone_str, password_=password_str)
                db.add(new_user)
                db.commit()
            flash(Markup('<h3>Пользователь успешно создан</h3>'))

    return render_template('register.html', form=form, username=username)

@app.route('/parts', methods=['GET', 'POST'])
def parts():
    form = ComponentsForm()
    username = get_user()
    if request.method == 'POST' and form.validate():
        vendor_str = form.vendor.data
        model_str = form.model.data
        type_str = form.type.data
        price_str = form.price.data
        user_id = request.cookies.get('user_id')
        with Session() as db:
            part = db.query(Components).filter(and_(Components.vendor == vendor_str, Components.model == model_str)).first()
        if part:
            if part.model == model_str:
                flash(Markup('<h3>Такая запчасть уже есть</h3>'))
        else:
            with Session() as db:
                new_part = Components(vendor=vendor_str, model=model_str, type=type_str, price=price_str, created_by=user_id)
                db.add(new_part)
                db.commit()
            flash(Markup('<h3>Запчасть успешно добавлена</h3>'))
    with Session() as db:
        query = db.query(Components.id, Components.vendor, Components.model, Components.type, Components.price, Components.creation_date, Users.first_name).join(Users)
        rows = [list(row) for row in query.all()]
    return render_template('catalog.html', type='parts', form=form, page_name='Запчасти', rows=rows, username=username)

@app.route('/suppliers', methods=['GET', 'POST'])
def suppliers():
    form = SuppliersForm()
    username = get_user()
    if request.method == 'POST' and form.validate():
        name_str = form.name.data
        e_mail_str = form.e_mail.data
        phone_str = form.phone.data
        address_str = form.address.data
        with Session() as db:
            supplier = db.query(Suppliers).filter(Suppliers.name == name_str).first()
        if supplier:
            if supplier.name == name_str or supplier.address == address_str:
                flash(Markup('<h3>Такой поставщик уже есть</h3>'))
        else:
            with Session() as db:
                new_supplier = Suppliers(name=name_str, e_mail=e_mail_str, phone_number=phone_str, address=address_str)
                db.add(new_supplier)
                db.commit()
            flash(Markup('<h3>Поставщик успешно добавлен</h3>'))
    with Session() as db:
        query = db.query(Suppliers.id, Suppliers.name, Suppliers.e_mail, Suppliers.phone_number, Suppliers.address)
        rows = [list(row) for row in query.all()]
    return render_template('catalog.html', type='suppliers', form=form, page_name='Поставщики', rows=rows, username=username)

@app.route('/warehouses', methods=['GET', 'POST'])
def warehouses():
    form = WarehousesForm()
    username = get_user()
    if request.method == 'POST' and form.validate():
        name_str = form.name.data
        address_str = form.address.data
        capacity_str = form.capacity.data
        with Session() as db:
            warehouse = db.query(Warehouses).filter(Warehouses.name == name_str).first()
        if warehouse:
            if warehouse.name == name_str or warehouse.address == address_str:
                flash(Markup('<h3>Такой склад уже есть</h3>'))
        else:
            with Session() as db:
                new_warehouse = Warehouses(name=name_str, address=address_str, capacity=capacity_str)
                db.add(new_warehouse)
                db.commit()
            flash(Markup('<h3>Склад успешно добавлен</h3>'))
    with Session() as db:
        query = db.query(Warehouses.id, Warehouses.name, Warehouses.address, Warehouses.capacity)
        rows = [list(row) for row in query.all()]
    return render_template('catalog.html', type='warehouses', form=form, page_name='Склады', rows=rows, username=username)

@app.route('/logout')
def logout():
    response = make_response(redirect(url_for('index')))
    response.set_cookie('user_id', '', expires=0)
    return response


if __name__ == '__main__':
    app.run(debug=True)
