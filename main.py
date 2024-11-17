from flask import Flask, render_template, flash, request
from db_forms import *
from markupsafe import Markup
from flask_wtf.csrf import CSRFProtect
from mysql.connector import connect
import os

mydb = connect(
    host='127.0.0.1',
    user='root',
    password='35678',
    db='pc_parts'
)

app = Flask(__name__)
app.config['SECRET_KEY'] = os.urandom(12).hex()
csrf = CSRFProtect(app)
@app.route('/')
def index():
    return render_template('index.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if request.method == 'POST' and form.validate():
        login_str = form.login.data
        password_str = form.password.data
        cur = mydb.cursor()
        cur.execute('select * from users where login = \'{}\' and password_ = \'{}\''.format(login_str, password_str))
        res = cur.fetchone()
        print(res)
        try:
            if res[1] == login_str or res[6] == password_str:
                flash('Вы успешно зашли в аккаунт')
        except:
            flash('Неверное имя пользователя или пароль')
        cur.close()
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
        cur = mydb.cursor()
        cur.execute('select * from users where login = \'{}\' and e_mail = \'{}\''.format(login_str, e_mail_str))
        res = cur.fetchone()
        print(res)
        try:
            if res[1] == login_str or res[4] == e_mail_str:
                flash('Такой пользователь уже существует')
        except:
            val = (login_str, f_name_str, l_name_str, e_mail_str, phone_str, password_str)
            sql = 'INSERT INTO users (login, first_name, last_name, e_mail, phone_number, password_) VALUES(%s,%s,%s,%s,%s,%s)'
            print(sql)
            cur.execute(sql, val)
            mydb.commit()
            flash('Пользователь успешно создан')
        finally:
            cur.close()
    return render_template('register.html', form=form)

@app.route('/catalog')
def catalog():
    return '<h1 style=\"text-align: center;\">WIP</h1>'


if __name__ == '__main__':
    app.run(debug=True)
