from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField
from wtforms.validators import DataRequired, Length, Email

class LoginForm(FlaskForm):
    login = StringField('Логин:', validators=[DataRequired(), Length(min=4, max=20)])
    password = PasswordField('Пароль:', validators=[DataRequired(), Length(min=4, max=20)])

class RegisterForm(FlaskForm):
    login = StringField('Логин:', validators=[DataRequired(), Length(min=4, max=20)])
    e_mail = StringField('E-mail:', validators=[DataRequired(), Email(message="Введите корректный адресс электронной почты")])
    first_name = StringField('Имя:', validators=[DataRequired(), Length(min=4, max=20)])
    last_name = StringField('Фамилия:', validators=[DataRequired(), Length(min=4, max=20)])
    phone = StringField('Номер телефона:', validators=[DataRequired(), Length(min=11, max=15)])
    password = PasswordField('Пароль:', validators=[DataRequired(), Length(min=4, max=20)])