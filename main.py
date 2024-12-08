from types import NoneType

from blueman.bluez.obex.Session import Session
from flask import Flask, render_template, flash, request, make_response, redirect, url_for, send_from_directory, abort, jsonify
from werkzeug.utils import secure_filename
from db_forms import *
from markupsafe import Markup
from flask_wtf.csrf import CSRFProtect
import os, uuid
from sqlalchemy import  create_engine, or_, and_, func
from sqlalchemy.orm import sessionmaker
from models import *

app = Flask(__name__)
app.config['SECRET_KEY'] = os.urandom(12).hex()
csrf = CSRFProtect(app)
UPLOAD_FOLDER = 'uploads'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif'}
def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

engine = create_engine("mysql+pymysql://root:35678@127.0.0.1/pc_parts")
Session = sessionmaker(bind=engine)


def get_user():
    user_id = request.cookies.get('user_id')
    if user_id:
        with Session() as db:
            user = db.query(Users).filter_by(id=user_id).first()
            print(user.id)
        if user:
            name = user.first_name
            return name
        else:
            return False
    else:
        return False

def file_upload(file):
    if file and allowed_file(file.filename):
        secure_name = secure_filename(file.filename)
        name, ext = os.path.splitext(secure_name)
        truncated_name = name[:5]
        unique_id = uuid.uuid4().hex[:8]
        filename = f"{truncated_name}_{unique_id}{ext}"
        file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
        return filename
    else:
        return None

@app.route('/delete_record/<type_page>/<int:record_id>', methods=['POST'])
def delete_record(type_page, record_id):
    model_mapping = {
        'parts': Components,
        'suppliers': Suppliers,
        'warehouses': Warehouses,
        'comp_to_sup': SupplierComponents,
        'ware_to_comp': WarehouseStock,
    }
    model = model_mapping.get(type_page)
    if not model:
        return jsonify({"success": False, "message": "Invalid type_page specified."}), 400
    with Session() as db:
        record = db.query(model).filter_by(id=record_id).first()
        if record:
            db.delete(record)
            db.commit()
            return jsonify({"success": True, "message": f"Record {record_id} deleted."})
        else:
            return jsonify({"success": False, "message": "Record not found."}), 404


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
            user = db.query(Users).filter(and_(Users.login == login_str, Users.password_ == password_str)).first()
        if user:
            if user.login == login_str or user.password_ == password_str:
                flash(Markup('<h3>Вы успешно зашли в аккаунт</h3>'))
                flash(Markup(f'<p>Имя: {user.first_name}</p><p>Тип аккаунта: {user.account_type}</p>'))
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
        user_id = request.cookies.get('user_id')
        file = form.image.data
        with Session() as db:
            part = db.query(Components).filter(and_(Components.vendor == vendor_str, Components.model == model_str)).first()
        if part:
            if part.model == model_str:
                flash(Markup('<h3>Такая запчасть уже есть</h3>'))
        else:
            with Session() as db:
                new_part = Components(vendor=vendor_str, model=model_str, type=type_str, created_by=user_id, image=file_upload(file))
                db.add(new_part)
                db.commit()
            flash(Markup('<h3>Запчасть успешно добавлена</h3>'))
    with Session() as db:
        query = db.query(Components.id, Components.vendor, Components.model, Components.type, Components.creation_date, Users.first_name, Components.image).join(Users)
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
        file = form.image.data
        with Session() as db:
            supplier = db.query(Suppliers).filter(Suppliers.name == name_str).first()
        if supplier:
            if supplier.name == name_str or supplier.address == address_str:
                flash(Markup('<h3>Такой поставщик уже есть</h3>'))
        else:
            with Session() as db:
                new_supplier = Suppliers(name=name_str, e_mail=e_mail_str, phone_number=phone_str, address=address_str, image=file_upload(file))
                db.add(new_supplier)
                db.commit()
            flash(Markup('<h3>Поставщик успешно добавлен</h3>'))
    with Session() as db:
        query = db.query(Suppliers.id, Suppliers.name, Suppliers.e_mail, Suppliers.phone_number, Suppliers.address, Suppliers.image)
        rows = [list(row) for row in query.all()]
    return render_template('catalog.html', type='suppliers', form=form, page_name='Поставщики', rows=rows, username=username)

@app.route('/warehouses', methods=['GET', 'POST'])
def warehouses():
    form = WarehousesForm()
    username = get_user()
    file = form.image.data
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
                new_warehouse = Warehouses(name=name_str, address=address_str, capacity=capacity_str, image=file_upload(file))
                db.add(new_warehouse)
                db.commit()
            flash(Markup('<h3>Склад успешно добавлен</h3>'))
    with Session() as db:
        query = db.query(Warehouses.id, Warehouses.name, Warehouses.address, Warehouses.capacity, Warehouses.image)
        rows = [list(row) for row in query.all()]
    return render_template('catalog.html', type='warehouses', form=form, page_name='Склады', rows=rows, username=username)

@app.route('/logout')
def logout():
    response = make_response(redirect(url_for('index')))
    response.set_cookie('user_id', '', expires=0)
    return response

@app.route('/comp_to_sup', methods=['GET', 'POST'])
def comp_to_sup():
    form = SupplierComponentsForm()
    username = get_user()
    file = form.image.data
    with Session() as db:
        sup_items = db.query(Suppliers).all()
        form.sup_id.choices = [(item.id, item.name) for item in sup_items]
        comp_items = db.query(Components).all()
        form.comp_id.choices = [(item.id, f'{item.vendor} {item.model}') for item in comp_items]
    if request.method == 'POST' and form.validate():
        sup_str = form.sup_id.data
        comp_str = form.comp_id.data
        price_str = form.price.data
        with Session() as db:
            sup_comp = db.query(SupplierComponents).filter(and_((SupplierComponents.supplier_id == sup_str),(SupplierComponents.component_id == comp_str))).first()
        if sup_comp:
            if sup_comp == sup_str and sup_comp == comp_str:
                flash(Markup('<h3>Такая связь уже есть</h3>'))
        else:
            with Session() as db:
                new_sup_comp = SupplierComponents(supplier_id=sup_str, component_id=comp_str, price=price_str, image=file_upload(file))
                db.add(new_sup_comp)
                db.commit()
            flash(Markup('<h3>Связь успешно добавлена</h3>'))
    with Session() as db:
        query = db.query(SupplierComponents.id, Suppliers.name, Components.model, SupplierComponents.price, SupplierComponents.image).join(Components).join(Suppliers)
        rows = [list(row) for row in query.all()]
    return render_template('catalog.html', type='comp_to_sup', form=form, page_name='Поставщики и комплектующие', rows=rows, username=username)

@app.route('/ware_to_comp', methods=['GET', 'POST'])
def ware_to_comp():
    form = WarehouseStockForm()
    username = get_user()
    file = form.image.data
    with Session() as db:
        ware_items = db.query(Warehouses).all()
        form.ware_id.choices = [(item.id, item.name) for item in ware_items]
        comp_items = db.query(Components).all()
        form.comp_id.choices = [(item.id, f'{item.vendor} {item.model}') for item in comp_items]
    if request.method == 'POST' and form.validate():
        ware_str = form.ware_id.data
        comp_str = form.comp_id.data
        quan_str = form.quantity.data
        with Session() as db:
            ware_comp = db.query(WarehouseStock).filter(and_((WarehouseStock.warehouse_id == ware_str),(WarehouseStock.component_id == comp_str))).first()
            ware_capacity = db.query(Warehouses.capacity).filter(Warehouses.id == ware_str).first()
            ware_taken1 = db.query(func.sum(WarehouseStock.quantity)).filter(WarehouseStock.warehouse_id == ware_str).all()
            if ware_taken1[0][0]:
                ware_taken = ware_taken1[0][0]
            else:
                ware_taken = 0
            print(ware_capacity[0], ware_taken)
        if ware_comp:
            if ware_comp == ware_str and ware_comp == comp_str:
                flash(Markup('<h3>Такая связь уже есть</h3>'))
        elif ware_taken + quan_str > ware_capacity[0]:
            flash(Markup('<h3>На складе не достаточно места</h3>'))
        else:
            with Session() as db:
                new_ware_comp = WarehouseStock(warehouse_id=ware_str, component_id=comp_str, quantity=quan_str, image=file_upload(file))
                db.add(new_ware_comp)
                db.commit()
            flash(Markup('<h3>Связь успешно добавлена</h3>'))
    with Session() as db:
        query = db.query(WarehouseStock.id, Warehouses.name, Components.model, WarehouseStock.quantity, WarehouseStock.image).join(Components).join(Warehouses)
        rows = [list(row) for row in query.all()]
    return render_template('catalog.html', type='ware_to_comp', form=form, page_name='Учет комплектующих на складе', rows=rows, username=username)

@app.route('/uploads/<path:filename>')
def uploaded_file(filename):
    try:
        return send_from_directory(UPLOAD_FOLDER, filename)
    except FileNotFoundError:
        abort(404)

if __name__ == '__main__':
    app.run(debug=True)
