from mysql.connector import connect
from flask import Flask, render_template, flash, request
from flask_wtf import FlaskForm
from markupsafe import Markup
from wtforms import StringField
from wtforms.validators import DataRequired
from flask_wtf.csrf import CSRFProtect



class LoginForm(FlaskForm):
    name = StringField('name', validators=[DataRequired()])

mydb = connect(
    host='127.0.0.1',
    user='root',
    password='35678'
)

app = Flask(__name__)
app.config['SECRET_KEY'] = '57f347f0c3f3d5970a7d5548'
csrf = CSRFProtect(app)
@app.route('/')
def index():
    return render_template('index.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if request.method == 'POST' and form.validate():
        return form.name.data
    return render_template('login.html', form=form)

if __name__ == '__main__':
    app.run(debug=True)