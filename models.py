from typing import List, Optional

from sqlalchemy import Column, DECIMAL, Enum, ForeignKeyConstraint, Index, Integer, String, TIMESTAMP, Text, text
from sqlalchemy.orm import Mapped, declarative_base, mapped_column, relationship
from sqlalchemy.orm.base import Mapped

Base = declarative_base()


class Components(Base):
    __tablename__ = 'Components'

    id = mapped_column(Integer, primary_key=True)
    vendor = mapped_column(String(40), nullable=False)
    model = mapped_column(String(90), nullable=False)
    type = mapped_column(String(50), nullable=False)
    price = mapped_column(DECIMAL(10, 0), nullable=False)
    creation_date = mapped_column(TIMESTAMP, server_default=text('CURRENT_TIMESTAMP'))
    update_date = mapped_column(TIMESTAMP, server_default=text('CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP'))
    comp_image = mapped_column(String(20))

    Supplier_components: Mapped[List['SupplierComponents']] = relationship('SupplierComponents', uselist=True, back_populates='component')
    Warehouse_stock: Mapped[List['WarehouseStock']] = relationship('WarehouseStock', uselist=True, back_populates='component')
    Order_details: Mapped[List['OrderDetails']] = relationship('OrderDetails', uselist=True, back_populates='component')


class Suppliers(Base):
    __tablename__ = 'Suppliers'

    id = mapped_column(Integer, primary_key=True)
    name = mapped_column(String(60), nullable=False)
    e_mail = mapped_column(String(30))
    phone_number = mapped_column(String(15))
    address = mapped_column(Text)

    Supplier_components: Mapped[List['SupplierComponents']] = relationship('SupplierComponents', uselist=True, back_populates='supplier')


class Users(Base):
    __tablename__ = 'Users'
    __table_args__ = (
        Index('e_mail', 'e_mail', unique=True),
        Index('login', 'login', unique=True)
    )

    id = mapped_column(Integer, primary_key=True)
    login = mapped_column(String(20), nullable=False)
    first_name = mapped_column(String(20), nullable=False)
    last_name = mapped_column(String(20), nullable=False)
    e_mail = mapped_column(String(30), nullable=False)
    phone_number = mapped_column(String(15), nullable=False)
    password_ = mapped_column(String(20), nullable=False)
    account_type = mapped_column(Enum('User', 'Admin'), server_default=text("'User'"))
    profile_image = mapped_column(String(20))

    Orders: Mapped[List['Orders']] = relationship('Orders', uselist=True, back_populates='user')
    Sessions: Mapped[List['Sessions']] = relationship('Sessions', uselist=True, back_populates='user')


class Warehouses(Base):
    __tablename__ = 'Warehouses'

    id = mapped_column(Integer, primary_key=True)
    name = mapped_column(String(60), nullable=False)
    address = mapped_column(Text, nullable=False)
    capacity = mapped_column(Integer, nullable=False)
    creation_date = mapped_column(TIMESTAMP, server_default=text('CURRENT_TIMESTAMP'))

    Warehouse_stock: Mapped[List['WarehouseStock']] = relationship('WarehouseStock', uselist=True, back_populates='warehouse')


class Orders(Base):
    __tablename__ = 'Orders'
    __table_args__ = (
        ForeignKeyConstraint(['user_id'], ['Users.id'], ondelete='CASCADE', name='Orders_ibfk_1'),
        Index('user_id', 'user_id', unique=True)
    )

    id = mapped_column(Integer, primary_key=True)
    user_id = mapped_column(Integer)
    order_date = mapped_column(TIMESTAMP, server_default=text('CURRENT_TIMESTAMP'))
    status = mapped_column(String(50), server_default=text("'В обработке'"))
    total_price = mapped_column(DECIMAL(10, 2), server_default=text("'0.00'"))

    user: Mapped[Optional['Users']] = relationship('Users', back_populates='Orders')
    Order_details: Mapped[List['OrderDetails']] = relationship('OrderDetails', uselist=True, back_populates='order')


class Sessions(Base):
    __tablename__ = 'Sessions'
    __table_args__ = (
        ForeignKeyConstraint(['user_id'], ['Users.id'], ondelete='CASCADE', name='Sessions_ibfk_1'),
        Index('token', 'token', unique=True),
        Index('user_id', 'user_id', unique=True)
    )

    id = mapped_column(Integer, primary_key=True)
    user_id = mapped_column(Integer)
    token = mapped_column(String(40))
    ip_address = mapped_column(String(12))
    start_time = mapped_column(TIMESTAMP, server_default=text('CURRENT_TIMESTAMP'))
    expiration_date = mapped_column(TIMESTAMP)

    user: Mapped[Optional['Users']] = relationship('Users', back_populates='Sessions')


class SupplierComponents(Base):
    __tablename__ = 'Supplier_components'
    __table_args__ = (
        ForeignKeyConstraint(['component_id'], ['Components.id'], name='Supplier_components_ibfk_1'),
        ForeignKeyConstraint(['supplier_id'], ['Suppliers.id'], ondelete='CASCADE', name='Supplier_components_ibfk_2'),
        Index('component_id', 'component_id', unique=True),
        Index('supplier_id', 'supplier_id', unique=True)
    )

    id = mapped_column(Integer, primary_key=True)
    supply_price = mapped_column(DECIMAL(10, 2), nullable=False)
    supplier_id = mapped_column(Integer)
    component_id = mapped_column(Integer)
    supply_date = mapped_column(TIMESTAMP, server_default=text('CURRENT_TIMESTAMP'))

    component: Mapped[Optional['Components']] = relationship('Components', back_populates='Supplier_components')
    supplier: Mapped[Optional['Suppliers']] = relationship('Suppliers', back_populates='Supplier_components')


class WarehouseStock(Base):
    __tablename__ = 'Warehouse_stock'
    __table_args__ = (
        ForeignKeyConstraint(['component_id'], ['Components.id'], ondelete='CASCADE', name='Warehouse_stock_ibfk_2'),
        ForeignKeyConstraint(['warehouse_id'], ['Warehouses.id'], ondelete='CASCADE', name='Warehouse_stock_ibfk_1'),
        Index('component_id', 'component_id', unique=True),
        Index('warehouse_id', 'warehouse_id', unique=True)
    )

    id = mapped_column(Integer, primary_key=True)
    quantity = mapped_column(Integer, nullable=False)
    warehouse_id = mapped_column(Integer)
    component_id = mapped_column(Integer)
    last_updated = mapped_column(TIMESTAMP, server_default=text('CURRENT_TIMESTAMP'))

    component: Mapped[Optional['Components']] = relationship('Components', back_populates='Warehouse_stock')
    warehouse: Mapped[Optional['Warehouses']] = relationship('Warehouses', back_populates='Warehouse_stock')


class OrderDetails(Base):
    __tablename__ = 'Order_details'
    __table_args__ = (
        ForeignKeyConstraint(['component_id'], ['Components.id'], name='Order_details_ibfk_1'),
        ForeignKeyConstraint(['order_id'], ['Orders.id'], ondelete='CASCADE', name='Order_details_ibfk_2'),
        Index('component_id', 'component_id', unique=True),
        Index('order_id', 'order_id', unique=True)
    )

    id = mapped_column(Integer, primary_key=True)
    order_id = mapped_column(Integer)
    component_id = mapped_column(Integer)
    quantity = mapped_column(Integer)
    unit_price = mapped_column(DECIMAL(10, 2))

    component: Mapped[Optional['Components']] = relationship('Components', back_populates='Order_details')
    order: Mapped[Optional['Orders']] = relationship('Orders', back_populates='Order_details')
