from flask_wtf import FlaskForm
from wtforms import StringField
from wtforms.validators import DataRequired, Length, Email

class LoginForm(FlaskForm):
    login = StringField('login', validators=[DataRequired(), Length(min=4, max=20)])
    password = StringField('password', validators=[DataRequired(), Length(min=4, max=20)])

class RegisterForm(FlaskForm):
    login = StringField('login', validators=[DataRequired(), Length(min=4, max=20)])
    e_mail = StringField('e-mail', validators=[DataRequired(), Email()])
    first_name = StringField('f_name', validators=[DataRequired(), Length(min=4, max=20)])
    last_name = StringField('l_name', validators=[DataRequired(), Length(min=4, max=20)])
    phone = StringField('phone', validators=[DataRequired(), Length(min=15, max=15)])
    password = StringField('password', validators=[DataRequired(), Length(min=4, max=20)])