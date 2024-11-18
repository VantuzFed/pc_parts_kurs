from types import NoneType
from flask import Flask, render_template, flash, request
from db_forms import *
from markupsafe import Markup
from flask_wtf.csrf import CSRFProtect
from mysql.connector import connect
import os

try:
        mydb = connect(
        host='127.0.0.1',
        user='root',
        password='35678',
        db='pc_parts'
    )
except:
    print('db connection error, aborted')
    exit(1)

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
        if type(res) is NoneType:
            flash(Markup('<h3>Неверное имя пользователя или пароль</h3>'))
        elif res[1] == login_str or res[6] == password_str:
            flash(Markup('<h3>Вы успешно зашли в аккаунт</h3>'))
            for i in range(1,len(res),1):
                flash(Markup(f'<p>{res[i]}</p>'))
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
        cur.execute('select * from users where login = \'{}\' or e_mail = \'{}\''.format(login_str, e_mail_str))
        res = cur.fetchone()
        if type(res) is NoneType:
            val = (login_str, f_name_str, l_name_str, e_mail_str, phone_str, password_str)
            sql = 'INSERT INTO users (login, first_name, last_name, e_mail, phone_number, password_) VALUES(%s,%s,%s,%s,%s,%s)'
            cur.execute(sql, val)
            mydb.commit()
            flash(Markup('<h3>Пользователь успешно создан</h3>'))
        elif res[1] == login_str or res[4] == e_mail_str:
            flash(Markup('<h3>Такой пользователь уже существует</h3>'))
        cur.close()
    return render_template('register.html', form=form)

@app.route('/catalog')
def catalog():
    return render_template('catalog.html')


if __name__ == '__main__':
    app.run(debug=True)
