from flask_wtf import FlaskForm

from wtforms import StringField, PasswordField, IntegerField, FloatField, SelectField, FileField, HiddenField, SubmitField
from wtforms.validators import DataRequired, Length, Email

class LoginForm(FlaskForm):
    login = StringField('Логин:', validators=[DataRequired(), Length(min=4, max=20)])
    password = PasswordField('Пароль:', validators=[DataRequired(), Length(min=4, max=20)])

class RegisterForm(FlaskForm):
    login = StringField('Логин:', validators=[DataRequired(), Length(min=4, max=20)])
    e_mail = StringField('E-mail:', validators=[DataRequired(), Email(message="Введите корректный адресс электронной почты")])
    first_name = StringField('Имя:', validators=[DataRequired(), Length(min=4, max=20)])
    last_name = StringField('Фамилия:', validators=[DataRequired(), Length(min=3, max=20)])
    phone = StringField('Номер телефона:', validators=[DataRequired(), Length(min=11, max=15)])
    password = PasswordField('Пароль:', validators=[DataRequired(), Length(min=4, max=20)])

class SuppliersForm(FlaskForm):
    name = StringField('Название поставщика:', validators=[DataRequired(), Length(min=3, max=60)])
    e_mail = StringField('E-mail:', validators=[DataRequired(), Email(message="Введите корректный адресс электронной почты")])
    phone = StringField('Номер телефона:', validators=[DataRequired(), Length(min=11, max=15)])
    address = StringField('Адрес поставщика:', validators=[DataRequired(), Length(min=4, max=100)])
    image = FileField('Загрузить изображение')

class WarehousesForm(FlaskForm):
    name = StringField('Название склада:', validators=[DataRequired(), Length(min=5, max=60)])
    address = StringField('Адрес склада:', validators=[DataRequired(), Length(min=4, max=100)])
    capacity = IntegerField('Вместимость склада:', validators=[DataRequired()])
    image = FileField('Загрузить изображение')

class ComponentsForm(FlaskForm):
    vendor = StringField('Производитель запчасти:', validators=[DataRequired(), Length(min=3, max=60)])
    model = StringField('Модель запчасти:', validators=[DataRequired(), Length(min=5, max=60)])
    type = SelectField('Тип комплектующего',
        choices =['Центральный процессор', 'Видеокарта', 'Материнская плата', 'ОЗУ', 'Сетевая карта', 'Жесткий диск', 'Твердотельный накопитель'],
        validators = [DataRequired()])
    image = FileField('Загрузить изображение')

class SupplierComponentsForm(FlaskForm):
    sup_id = SelectField('Поставщик:',
        choices =[],
        validators = [DataRequired()])
    comp_id = SelectField('Комплектующее:',
        choices =[],
        validators = [DataRequired()])
    price = FloatField('Цена комплектующего:')
    image = FileField('Загрузить изображение')

class WarehouseStockForm(FlaskForm):
    ware_id = SelectField('Склад:',
        choices =[],
        validators = [DataRequired()])
    comp_id = SelectField('Комплеткующее:',
        choices =[],
        validators = [DataRequired()])
    quantity = IntegerField('Количество:')
    image = FileField('Загрузить изображение')

