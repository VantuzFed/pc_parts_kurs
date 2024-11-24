from types import NoneType
from flask import Flask, render_template, flash, request
from db_forms import *
from markupsafe import Markup
from flask_wtf.csrf import CSRFProtect
import os
from sqlalchemy import  create_engine, or_
from sqlalchemy.orm import sessionmaker
from models import *

app = Flask(__name__)
app.config['SECRET_KEY'] = os.urandom(12).hex()
csrf = CSRFProtect(app)

engine = create_engine("mysql+pymysql://root:35678@127.0.0.1/pc_parts")
Session = sessionmaker(bind=engine)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if request.method == 'POST' and form.validate():
        login_str = form.login.data
        password_str = form.password.data
        with Session() as db:
            user = db.query(Users).filter(or_(Users.login == login_str, Users.password_ == password_str)).first()
        if user:
            if user.login == login_str or user.password_ == password_str:
                flash(Markup('<h3>Вы успешно зашли в аккаунт</h3>'))
                flash(Markup(f'<p>Тип аккаунта: {user.account_type}</p>'))
        else:
            flash(Markup('<h3>Неверное имя пользователя или пароль</h3>'))

    return render_template('login.html', form=form)

@app.route('/register', methods=['GET', 'POST'])
def register():
    form = RegisterForm()
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

    return render_template('register.html', form=form)

@app.route('/catalog')
def catalog():
    return render_template('catalog.html')


if __name__ == '__main__':
    app.run(debug=True)
