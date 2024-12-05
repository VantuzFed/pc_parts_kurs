from typing import List, Optional

from sqlalchemy import Column, DECIMAL, Enum, ForeignKeyConstraint, Index, Integer, String, TIMESTAMP, Text, text
from sqlalchemy.orm import Mapped, declarative_base, mapped_column, relationship
from sqlalchemy.orm.base import Mapped

Base = declarative_base()


class Suppliers(Base):
    __tablename__ = 'Suppliers'

    id = mapped_column(Integer, primary_key=True)
    name = mapped_column(String(60), nullable=False)
    e_mail = mapped_column(String(30))
    phone_number = mapped_column(String(15))
    image = mapped_column(String(20))
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

    Components: Mapped[List['Components']] = relationship('Components', uselist=True, back_populates='Users_')


class Warehouses(Base):
    __tablename__ = 'Warehouses'

    id = mapped_column(Integer, primary_key=True)
    name = mapped_column(String(60), nullable=False)
    address = mapped_column(Text, nullable=False)
    capacity = mapped_column(Integer, nullable=False)
    image = mapped_column(String(20))
    creation_date = mapped_column(TIMESTAMP, server_default=text('CURRENT_TIMESTAMP'))

    Warehouse_stock: Mapped[List['WarehouseStock']] = relationship('WarehouseStock', uselist=True, back_populates='warehouse')


class Components(Base):
    __tablename__ = 'Components'
    __table_args__ = (
        ForeignKeyConstraint(['created_by'], ['Users.id'], ondelete='SET NULL', name='Components_ibfk_1'),
        Index('created_by', 'created_by')
    )

    id = mapped_column(Integer, primary_key=True)
    vendor = mapped_column(String(40), nullable=False)
    model = mapped_column(String(90), nullable=False)
    type = mapped_column(String(50), nullable=False)
    creation_date = mapped_column(TIMESTAMP, server_default=text('CURRENT_TIMESTAMP'))
    update_date = mapped_column(TIMESTAMP, server_default=text('CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP'))
    created_by = mapped_column(Integer)
    image = mapped_column(String(20))

    Users_: Mapped[Optional['Users']] = relationship('Users', back_populates='Components')
    Supplier_components: Mapped[List['SupplierComponents']] = relationship('SupplierComponents', uselist=True, back_populates='component')
    Warehouse_stock: Mapped[List['WarehouseStock']] = relationship('WarehouseStock', uselist=True, back_populates='component')


class SupplierComponents(Base):
    __tablename__ = 'Supplier_components'
    __table_args__ = (
        ForeignKeyConstraint(['component_id'], ['Components.id'], name='Supplier_components_ibfk_2'),
        ForeignKeyConstraint(['supplier_id'], ['Suppliers.id'], ondelete='CASCADE', name='Supplier_components_ibfk_1'),
        Index('component_id', 'component_id'),
        Index('supplier_id', 'supplier_id')
    )

    id = mapped_column(Integer, primary_key=True)
    supplier_id = mapped_column(Integer, nullable=False)
    component_id = mapped_column(Integer, nullable=False)
    price = mapped_column(DECIMAL(10, 2), nullable=False)
    supply_date = mapped_column(TIMESTAMP, server_default=text('CURRENT_TIMESTAMP'))

    component: Mapped['Components'] = relationship('Components', back_populates='Supplier_components')
    supplier: Mapped['Suppliers'] = relationship('Suppliers', back_populates='Supplier_components')


class WarehouseStock(Base):
    __tablename__ = 'Warehouse_stock'
    __table_args__ = (
        ForeignKeyConstraint(['component_id'], ['Components.id'], ondelete='CASCADE', name='Warehouse_stock_ibfk_2'),
        ForeignKeyConstraint(['warehouse_id'], ['Warehouses.id'], ondelete='CASCADE', name='Warehouse_stock_ibfk_1'),
        Index('component_id', 'component_id'),
        Index('warehouse_id', 'warehouse_id')
    )

    id = mapped_column(Integer, primary_key=True)
    warehouse_id = mapped_column(Integer, nullable=False)
    component_id = mapped_column(Integer, nullable=False)
    quantity = mapped_column(Integer, nullable=False)
    last_updated = mapped_column(TIMESTAMP, server_default=text('CURRENT_TIMESTAMP'))

    component: Mapped['Components'] = relationship('Components', back_populates='Warehouse_stock')
    warehouse: Mapped['Warehouses'] = relationship('Warehouses', back_populates='Warehouse_stock')
