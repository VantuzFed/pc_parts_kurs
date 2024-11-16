from flask import Flask, render_template, flash, request
from db_forms import *
from markupsafe import Markup
from flask_wtf.csrf import CSRFProtect
from mysql.connector import connect
import os

mydb = connect(
    host='127.0.0.1',
    user='root',
    password='35678'
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
        # self.log = self.ui.ent_login.text()
        # self.passwd = self.ui.ent_passwd.text()
        # cur = self.obj.cursor()
        # cur.execute('select * from users where login = \'{}\' and passwd = \'{}\''.format(self.log, self.passwd))
        # res = cur.fetchone()
        # try:
        #     if res[2] == self.log and res[3] == self.passwd:
        #         QMessageBox.information(self,'Сообщение', 'Авторизация прошла успешно')
        # except:
        #     QMessageBox.warning(self,'Предупреждение', 'Неверное имя пользователя или пароль')
        # cur.close()
        flash(f'login: {form.login.data} | password: {form.password.data}')
    return render_template('login.html', form=form)

@app.route('/register')
def register():

    # def registration(self):
    #     self.username = self.ui.ent_username.text()
    #     self.log = self.ui.ent_login.text()
    #     self.passwd = self.ui.ent_passwd.text()
    #     cur = self.obj.cursor()
    #     cur.execute('select * from users where login = \'{}\' and passwd = \'{}\' and username = \'{}\''.format(self.log, self.passwd, self.username))
    #     res = cur.fetchone()
    #     print(res)
    #     try:
    #         if res[2] == self.log and res[3] == self.passwd and res[1] == self.username:
    #             QMessageBox.warning(self,'Сообщение', 'Такой пользователь уже существует')
    #     except:
    #         val = (self.username, self.log, self.passwd)
    #         sql = 'INSERT INTO users (username, login, passwd) VALUES(%s,%s,%s)'
    #         cur.execute(sql, val)
    #         self.obj.commit()
    #         QMessageBox.information(self, 'Сообщение', 'Пользователь успешно создан')
    #     finally:
    #         cur.close()
    return '<h1 style=\"text-align: center;\">WIP</h1>'

@app.route('/catalog')
def catalog():
    return '<h1 style=\"text-align: center;\">WIP</h1>'


if __name__ == '__main__':
    app.run(debug=True)
